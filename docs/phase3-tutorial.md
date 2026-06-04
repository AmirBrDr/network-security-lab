# Phase 3 - Observability Stack With Prometheus, Grafana, Loki, And Alloy

Network Security Lab

## Summary

This practical lab extends the existing FRRouting OSPF triangle into an
observable network platform. The goal is to collect system metrics, interface
traffic, service state, FRR logs, OSPF events, and failure evidence from the
routers and lab VMs.

The stack is deliberately simple:

- Prometheus stores metrics.
- Node Exporter exposes Linux host metrics.
- A small textfile collector script exposes FRR-specific state.
- Loki stores logs.
- Grafana Alloy reads the systemd journal and forwards logs to Loki.
- Grafana displays dashboards and alert rules.

At the end of this lab, an OSPF failure such as the VLAN `440` loss tested in
Phase 2 must be visible in metrics, logs, dashboards, and alerts.

## Table Of Contents

1. Objectives
2. Lab Topology
3. Addressing And Service Plan
4. Prepare The Management VM
5. Install Node Exporter On Lab Nodes
6. Add FRR Metrics With The Textfile Collector
7. Install And Configure Prometheus
8. Validate Prometheus Metrics
9. Install Loki On The Management VM
10. Install And Configure Grafana Alloy
11. Validate Centralized Logs
12. Install Grafana
13. Provision Grafana Data Sources
14. Build Dashboards
15. Configure Alerts
16. Replay An OSPF Failure
17. Save Evidence
18. Troubleshooting
19. Conclusion
20. References

## 1. Objectives

After completing this practical lab, you should be able to:

1. Deploy an observability VM on the management network.
2. Install Prometheus and scrape all lab nodes through VLAN `99`.
3. Collect CPU, memory, disk, uptime, and interface traffic from all VMs.
4. Monitor `frr.service` state and simple OSPF neighbor counts.
5. Install Loki as a centralized log store.
6. Use Grafana Alloy to collect systemd journal logs from routers and VMs.
7. Connect Grafana to Prometheus and Loki.
8. Build network, system, and OSPF dashboards.
9. Configure practical alerts for router outage, FRR failure, OSPF neighbor
   loss, interface errors, high resource usage, and critical logs.
10. Replay a controlled OSPF failure and prove that it appears in dashboards,
    logs, and alerts.

## 2. Lab Topology

The observability stack is added after the Phase 1 OSPF foundation and Phase 2
failure testing work.

The routing topology remains the same:

```text
             VLAN 440
        R1 ----------- R2
         \             /
 VLAN 441 \           / VLAN 442
           \         /
              R3
```

The management and observability plane is separate from the OSPF transit links.
All observability traffic uses VLAN `99`.

```text
                 Management VLAN 99

 R1 10.99.0.1  ----+
 R2 10.99.0.2  ----+
 R3 10.99.0.3  ----+---- Management VM 10.99.0.66
 Monitoring VM ----+          Prometheus
 10.99.0.65                  Loki
                              Grafana
                              Alloy
```

The Management VM is not a router. It is a collector and dashboard host.
The Monitoring VM remains reserved for IDS and Phase 4 security work.

## 3. Addressing And Service Plan

### 3.1. Node Inventory

| Node | Role | TAP | Management IPv4 | Management IPv6 |
| --- | --- | --- | --- | --- |
| `R1` | Router and default route origin | `tap62` | `10.99.0.1` | `fd14:ca46:3864:99::1` |
| `R2` | Router | `tap63` | `10.99.0.2` | `fd14:ca46:3864:99::2` |
| `R3` | Router | `tap64` | `10.99.0.3` | `fd14:ca46:3864:99::3` |
| `monitoring` | IDS sensor, Phase 4 | `tap65` | `10.99.0.65` | `fd14:ca46:3864:99::65` |
| `management` | Observability stack | `tap66` | `10.99.0.66` | `fd14:ca46:3864:99::66` |

### 3.2. Service Ports

| Service | Node | Port | Purpose |
| --- | --- | ---: | --- |
| Prometheus | `management` | `9090/tcp` | Metrics database and query UI |
| Node Exporter | All lab VMs | `9100/tcp` | Linux host metrics |
| Loki | `management` | `3100/tcp` | Log ingestion and query API |
| Grafana | `management` | `3000/tcp` | Dashboards and alert UI |
| Alloy | All lab VMs | local service | Reads journal and forwards logs |
| SSH | All lab VMs | `22/tcp` | Administration |

Keep these services reachable only inside the lab management network unless a
reverse proxy and authentication are added later.

## 4. Prepare The Management VM

Q1. How should the management VM be connected?

The management VM uses `tap66` as an access port in VLAN `99`. It uses `R1` as
its default gateway.

Expected Netplan file on the Management VM:

```yaml
network:
  version: 2
  ethernets:
    enp0s1:
      dhcp4: false
      dhcp6: false
      addresses:
        - 10.99.0.66/24
        - fd14:ca46:3864:99::66/64
      routes:
        - to: default
          via: 10.99.0.1
        - to: "::/0"
          via: fd14:ca46:3864:99::1
      nameservers:
        addresses:
          - 172.16.0.2
          - 2001:678:3fc:3::2
```

Apply and verify:

```console
sudo netplan apply
ip addr show enp0s1
ip route
ip -6 route
```

Q2. How do we validate the management plane before installing monitoring?

From the Management VM:

```console
for host in 10.99.0.1 10.99.0.2 10.99.0.3 10.99.0.65; do
    ping -c 2 "$host"
done

for host in fd14:ca46:3864:99::1 fd14:ca46:3864:99::2 fd14:ca46:3864:99::3 fd14:ca46:3864:99::65; do
    ping -c 2 "$host"
done
```

Expected result:

- `0%` packet loss to all management addresses.
- Default route through `10.99.0.1`.
- No OSPF adjacency on VLAN `99`.

Q3. Which base packages are useful on the Management VM?

```console
sudo apt update
sudo apt install -y curl wget gnupg ca-certificates apt-transport-https \
    vim jq moreutils prometheus prometheus-alertmanager
```

The package list keeps the Management VM practical for metric queries, JSON
parsing, and later alert testing.

Access note from the workstation:

If the management VLAN is reachable only through SSH, open a tunnel from the
repository root using the provided `scripts/config` SSH file:

```console
ssh -F scripts/config -N \
    -L 3000:127.0.0.1:3000 \
    -L 9090:127.0.0.1:9090 \
    -L 3100:127.0.0.1:3100 \
    management
```

Then use these local URLs from the workstation browser:

| Service | Local URL |
| --- | --- |
| Grafana | `http://127.0.0.1:3000` |
| Prometheus | `http://127.0.0.1:9090` |
| Loki API | `http://127.0.0.1:3100` |

## 5. Install Node Exporter On Lab Nodes

Q4. Which nodes need Node Exporter?

Install Node Exporter on:

- `R1`
- `R2`
- `R3`
- `monitoring`
- `management`

Q5. How do we install Node Exporter?

Run on each node:

```console
sudo apt update
sudo apt install -y prometheus-node-exporter prometheus-node-exporter-collectors
sudo systemctl enable --now prometheus-node-exporter
sudo systemctl status prometheus-node-exporter --no-pager
```

Q6. How do we validate Node Exporter locally?

Run on each node:

```console
curl -s http://127.0.0.1:9100/metrics | head
curl -s http://127.0.0.1:9100/metrics | grep -E "node_cpu_seconds_total|node_memory_MemAvailable_bytes|node_filesystem_avail_bytes" | head
```

Run from the Management VM:

```console
for host in 10.99.0.1 10.99.0.2 10.99.0.3 10.99.0.65 10.99.0.66; do
    echo "===== $host ====="
    curl -s "http://$host:9100/metrics" | grep -m1 node_exporter_build_info
done
```

Expected result:

- Every node returns `node_exporter_build_info`.
- No firewall or routing issue blocks port `9100/tcp`.

## 6. Add FRR Metrics With The Textfile Collector

Node Exporter already exposes Linux system metrics. FRR-specific OSPF state is
not included by default. For this lab, use a small script that writes
Prometheus-formatted metrics into Node Exporter's textfile collector directory.

This is intentionally simple and transparent. It is enough to create useful
Phase 3 dashboards and alerts without introducing a separate FRR exporter.

Q7. Which custom metrics should routers expose?

| Metric | Meaning |
| --- | --- |
| `frr_service_active` | `1` when `frr.service` is active, else `0` |
| `frr_ospf_neighbor_full_total{protocol="ospfv2"}` | Count of OSPFv2 neighbors in `Full` state |
| `frr_ospf_neighbor_full_total{protocol="ospfv3"}` | Count of OSPFv3 neighbors in `Full` state |
| `frr_textfile_last_success_unixtime` | Last successful script execution time |

Expected full-neighbor count:

| Router | OSPFv2 Full neighbors | OSPFv3 Full neighbors |
| --- | ---: | ---: |
| `R1` | `2` | `2` |
| `R2` | `2` | `2` |
| `R3` | `2` | `2` |

Q8. How do we create the FRR textfile script?

Run this on `R1`, `R2`, and `R3` only:

```console
sudo install -d -m 0755 /usr/local/lib/prometheus
sudo install -d -m 0755 /var/lib/prometheus/node-exporter

sudo tee /usr/local/lib/prometheus/frr_textfile.sh >/dev/null <<'EOF'
#!/bin/sh
set -eu

HOST="$(hostname -s)"
DIR="/var/lib/prometheus/node-exporter"
TMP="$DIR/frr.prom.$$"
OUT="$DIR/frr.prom"

if systemctl is-active --quiet frr.service; then
    FRR_ACTIVE=1
else
    FRR_ACTIVE=0
fi

if command -v vtysh >/dev/null 2>&1; then
    OSPFV2_FULL="$(vtysh -c 'show ip ospf neighbor' 2>/dev/null | awk '/Full/ {c++} END {print c+0}')"
    OSPFV3_FULL="$(vtysh -c 'show ipv6 ospf6 neighbor' 2>/dev/null | awk '/Full/ {c++} END {print c+0}')"
else
    OSPFV2_FULL=0
    OSPFV3_FULL=0
fi

cat > "$TMP" <<METRICS
# HELP frr_service_active 1 if frr.service is active, otherwise 0.
# TYPE frr_service_active gauge
frr_service_active{node="$HOST"} $FRR_ACTIVE
# HELP frr_ospf_neighbor_full_total Number of OSPF neighbors in Full state.
# TYPE frr_ospf_neighbor_full_total gauge
frr_ospf_neighbor_full_total{node="$HOST",protocol="ospfv2"} $OSPFV2_FULL
frr_ospf_neighbor_full_total{node="$HOST",protocol="ospfv3"} $OSPFV3_FULL
# HELP frr_textfile_last_success_unixtime Unix timestamp of the last successful FRR textfile collection.
# TYPE frr_textfile_last_success_unixtime gauge
frr_textfile_last_success_unixtime{node="$HOST"} $(date +%s)
METRICS

chmod 0644 "$TMP"
mv "$TMP" "$OUT"
EOF

sudo chmod 0755 /usr/local/lib/prometheus/frr_textfile.sh
sudo /usr/local/lib/prometheus/frr_textfile.sh
cat /var/lib/prometheus/node-exporter/frr.prom
```

Q9. How do we run this script continuously?

Create a systemd timer on `R1`, `R2`, and `R3`:

```console
sudo tee /etc/systemd/system/frr-textfile.service >/dev/null <<'EOF'
[Unit]
Description=Write FRR metrics for Prometheus Node Exporter

[Service]
Type=oneshot
ExecStart=/usr/local/lib/prometheus/frr_textfile.sh
EOF

sudo tee /etc/systemd/system/frr-textfile.timer >/dev/null <<'EOF'
[Unit]
Description=Refresh FRR textfile metrics

[Timer]
OnBootSec=30s
OnUnitActiveSec=15s
AccuracySec=1s

[Install]
WantedBy=timers.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable --now frr-textfile.timer
systemctl list-timers frr-textfile.timer
```

Q10. How do we confirm Prometheus will see the custom metrics?

On each router:

```console
curl -s http://127.0.0.1:9100/metrics | grep '^frr_'
```

Expected result:

```text
frr_service_active{node="R1"} 1
frr_ospf_neighbor_full_total{node="R1",protocol="ospfv2"} 2
frr_ospf_neighbor_full_total{node="R1",protocol="ospfv3"} 2
```

The router name and values must match the node where the command runs.

## 7. Install And Configure Prometheus

Q11. Where should Prometheus run?

Prometheus runs on the Management VM at `10.99.0.66`.

Q12. How do we configure scrape targets?

Create or replace `/etc/prometheus/prometheus.yml` on the Management VM:

```console
sudo tee /etc/prometheus/prometheus.yml >/dev/null <<'EOF'
global:
  scrape_interval: 15s
  scrape_timeout: 10s
  evaluation_interval: 15s

rule_files:
  - /etc/prometheus/rules/*.yml

scrape_configs:
  - job_name: prometheus
    static_configs:
      - targets: ["127.0.0.1:9090"]
        labels:
          node: management
          role: observability

  - job_name: node
    static_configs:
      - targets: ["10.99.0.1:9100"]
        labels:
          node: R1
          role: router
      - targets: ["10.99.0.2:9100"]
        labels:
          node: R2
          role: router
      - targets: ["10.99.0.3:9100"]
        labels:
          node: R3
          role: router
      - targets: ["10.99.0.65:9100"]
        labels:
          node: monitoring
          role: ids
      - targets: ["10.99.0.66:9100"]
        labels:
          node: management
          role: observability

  - job_name: loki
    static_configs:
      - targets: ["127.0.0.1:3100"]
        labels:
          node: management
          role: logs
EOF
```

Validate and restart:

```console
sudo install -d -m 0755 /etc/prometheus/rules
promtool check config /etc/prometheus/prometheus.yml
sudo systemctl enable --now prometheus
sudo systemctl restart prometheus
sudo systemctl status prometheus --no-pager
```

Q13. How do we verify targets?

From the Management VM:

```console
curl -s http://127.0.0.1:9090/api/v1/targets | jq '.data.activeTargets[] | {job: .labels.job, node: .labels.node, health: .health, scrapeUrl: .scrapeUrl}'
```

Expected result:

- `prometheus` target is `up`.
- All five `node` targets are `up`.
- `loki` target will be `down` until Loki is installed, then `up`.

## 8. Validate Prometheus Metrics

Q14. Which PromQL queries prove that host metrics are available?

Use the Prometheus web UI at:

```text
http://10.99.0.66:9090
```

Useful queries:

```promql
up
```

```promql
node_uname_info
```

```promql
100 * (1 - avg by (node) (rate(node_cpu_seconds_total{mode="idle"}[5m])))
```

```promql
100 * (1 - node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes)
```

```promql
100 * (1 - node_filesystem_avail_bytes{mountpoint="/",fstype!~"tmpfs|overlay"} / node_filesystem_size_bytes{mountpoint="/",fstype!~"tmpfs|overlay"})
```

```promql
rate(node_network_receive_bytes_total{device!~"lo"}[5m])
```

```promql
rate(node_network_transmit_bytes_total{device!~"lo"}[5m])
```

Q15. Which PromQL queries prove FRR metrics are available?

```promql
frr_service_active
```

```promql
frr_ospf_neighbor_full_total
```

```promql
frr_ospf_neighbor_full_total{protocol="ospfv2"} < 2
```

```promql
time() - frr_textfile_last_success_unixtime
```

Expected result:

- `frr_service_active` equals `1` on `R1`, `R2`, and `R3`.
- OSPFv2 and OSPFv3 neighbor counts equal `2` on all three routers in the
  healthy topology.
- The textfile age stays below `60` seconds.

## 9. Install Loki On The Management VM

Loki receives logs from Alloy agents. In this lab, Loki runs as a single binary
on the Management VM and stores data on local disk.

Warning: Loki does not include an authentication layer by itself. Keep it bound
to the lab management network and do not expose it to untrusted networks.

Q16. How do we install Loki from the Grafana APT repository?

Run on the Management VM:

```console
sudo apt-get install -y apt-transport-https wget gnupg
sudo mkdir -p /etc/apt/keyrings
sudo wget -O /etc/apt/keyrings/grafana.asc https://apt.grafana.com/gpg-full.key
sudo chmod 0644 /etc/apt/keyrings/grafana.asc
echo "deb [signed-by=/etc/apt/keyrings/grafana.asc] https://apt.grafana.com stable main" | sudo tee /etc/apt/sources.list.d/grafana.list
sudo apt-get update
sudo apt-get install -y loki
```

Q17. How do we configure Loki for this lab?

If the package starts successfully with its default `/etc/loki/config.yml`, keep
the package file and only verify that Loki listens on the management network.

For a clean single-node lab configuration, use this filesystem-backed config:

```console
sudo install -d -o loki -g loki -m 0750 /var/lib/loki
sudo cp -a /etc/loki/config.yml /etc/loki/config.yml.bak.$(date +%Y%m%d%H%M%S)

sudo tee /etc/loki/config.yml >/dev/null <<'EOF'
auth_enabled: false

server:
  http_listen_address: 10.99.0.66
  http_listen_port: 3100

common:
  ring:
    instance_addr: 10.99.0.66
    kvstore:
      store: inmemory
  replication_factor: 1
  path_prefix: /var/lib/loki

schema_config:
  configs:
    - from: 2024-04-01
      store: tsdb
      object_store: filesystem
      schema: v13
      index:
        prefix: index_
        period: 24h

storage_config:
  filesystem:
    directory: /var/lib/loki/chunks
EOF

sudo chown -R loki:loki /var/lib/loki
sudo systemctl enable --now loki
sudo systemctl restart loki
sudo systemctl status loki --no-pager
```

Q18. How do we verify Loki?

```console
curl -s http://10.99.0.66:3100/ready
curl -s http://10.99.0.66:3100/metrics | head
```

Expected result:

- `/ready` returns `ready`.
- `/metrics` returns Prometheus-formatted Loki metrics.
- The Prometheus `loki` target becomes `up`.

## 10. Install And Configure Grafana Alloy

Alloy is the log collection agent. It reads the systemd journal locally on each
node and forwards log lines to Loki on the Management VM.

Q19. Which nodes need Alloy?

Install Alloy on:

- `R1`
- `R2`
- `R3`
- `monitoring`
- `management`

Q20. How do we install Alloy?

If the Grafana APT repository is already configured, install directly:

```console
sudo apt-get update
sudo apt-get install -y alloy
```

If the node does not yet have the Grafana repository:

```console
sudo apt-get install -y apt-transport-https wget gnupg
sudo mkdir -p /etc/apt/keyrings
sudo wget -O /etc/apt/keyrings/grafana.asc https://apt.grafana.com/gpg-full.key
sudo chmod 0644 /etc/apt/keyrings/grafana.asc
echo "deb [signed-by=/etc/apt/keyrings/grafana.asc] https://apt.grafana.com stable main" | sudo tee /etc/apt/sources.list.d/grafana.list
sudo apt-get update
sudo apt-get install -y alloy
```

Q21. How do we allow Alloy to read the systemd journal?

Run on every Alloy node:

```console
sudo usermod -aG adm alloy
sudo usermod -aG systemd-journal alloy
```

Restart Alloy after writing the configuration.

Q22. How do we configure Alloy to send journal logs to Loki?

Create `/etc/alloy/config.alloy` on every node.

On `R1`, use `node = "R1"`. Change the `node` label on each node:

- `R1`
- `R2`
- `R3`
- `monitoring`
- `management`

```console
sudo cp -a /etc/alloy/config.alloy /etc/alloy/config.alloy.bak.$(date +%Y%m%d%H%M%S) 2>/dev/null || true

sudo tee /etc/alloy/config.alloy >/dev/null <<'EOF'
loki.relabel "journal" {
  forward_to = []

  rule {
    source_labels = ["__journal__hostname"]
    target_label  = "host"
  }

  rule {
    source_labels = ["__journal__systemd_unit"]
    target_label  = "unit"
  }

  rule {
    source_labels = ["__journal_priority_keyword"]
    target_label  = "level"
  }
}

loki.source.journal "system" {
  forward_to    = [loki.write.lab.receiver]
  relabel_rules = loki.relabel.journal.rules
  labels        = {
    job  = "systemd-journal",
    lab  = "network-security-lab",
    node = "R1",
  }
}

loki.write "lab" {
  endpoint {
    url = "http://10.99.0.66:3100/loki/api/v1/push"
  }
}
EOF

sudo systemctl enable --now alloy
sudo systemctl restart alloy
sudo systemctl status alloy --no-pager
```

Q23. How do we validate Alloy locally?

```console
journalctl -u alloy -n 50 --no-pager
```

Expected result:

- No parse error in `/etc/alloy/config.alloy`.
- No permission error when reading the journal.
- No connection error to `10.99.0.66:3100`.

## 11. Validate Centralized Logs

Q24. How do we check that Loki receives logs?

From the Management VM:

```console
curl -G -s "http://10.99.0.66:3100/loki/api/v1/labels" | jq
curl -G -s "http://10.99.0.66:3100/loki/api/v1/label/node/values" | jq
```

Expected result:

```json
{
  "status": "success",
  "data": [
    "R1",
    "R2",
    "R3",
    "management",
    "monitoring"
  ]
}
```

Q25. Which LogQL queries are useful?

In Grafana Explore or through the Loki API:

```logql
{job="systemd-journal"}
```

```logql
{job="systemd-journal", node="R2"}
```

```logql
{job="systemd-journal", unit="frr.service"}
```

```logql
{job="systemd-journal"} |= "AdjChg"
```

```logql
{job="systemd-journal"} |= "Full -> Deleted"
```

```logql
{job="systemd-journal", node="R2"} |= "enp0s1.440"
```

Q26. How do we generate a harmless test log?

Run on `R2`:

```console
logger -t phase3-test "Phase 3 Loki test from R2"
```

Then query:

```logql
{job="systemd-journal", node="R2"} |= "Phase 3 Loki test"
```

Expected result:

- The log line appears in Loki within a few seconds.

## 12. Install Grafana

Q27. Where should Grafana run?

Grafana runs on the Management VM at:

```text
http://10.99.0.66:3000
```

Q28. How do we install Grafana OSS?

The Grafana APT repository was already added for Loki and Alloy. Run on the
Management VM:

```console
sudo apt-get update
sudo apt-get install -y grafana
sudo systemctl enable --now grafana-server
sudo systemctl status grafana-server --no-pager
```

Default local login:

| Field | Value |
| --- | --- |
| URL | `http://10.99.0.66:3000` |
| Username | `admin` |
| Password | `admin` on first login, then change it |

Use a lab-only password and record it in a private password manager, not in the
public repository.

## 13. Provision Grafana Data Sources

Q29. How do we connect Grafana to Prometheus and Loki without clicking through
the UI?

Create a Grafana provisioning file on the Management VM:

```console
sudo tee /etc/grafana/provisioning/datasources/network-security-lab.yml >/dev/null <<'EOF'
apiVersion: 1

datasources:
  - name: Prometheus
    uid: prometheus
    type: prometheus
    access: proxy
    url: http://127.0.0.1:9090
    isDefault: true

  - name: Loki
    uid: loki
    type: loki
    access: proxy
    url: http://127.0.0.1:3100
    jsonData:
      maxLines: 1000
EOF

sudo systemctl restart grafana-server
```

Q30. How do we verify data sources?

In Grafana:

1. Open `Connections`.
2. Open `Data sources`.
3. Select `Prometheus`, then `Save & test`.
4. Select `Loki`, then `Save & test`.

CLI checks:

```console
curl -s http://127.0.0.1:3000/api/health
curl -s http://127.0.0.1:9090/-/ready
curl -s http://127.0.0.1:3100/ready
```

Expected result:

- Grafana is healthy.
- Prometheus is ready.
- Loki is ready.

## 14. Build Dashboards

Create three dashboard folders:

- `Network`
- `System`
- `Routing`

Q31. Which panels should the System dashboard contain?

| Panel | Query |
| --- | --- |
| Target health | `up` |
| CPU usage | `100 * (1 - avg by (node) (rate(node_cpu_seconds_total{mode="idle"}[5m])))` |
| Memory usage | `100 * (1 - node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes)` |
| Root disk usage | `100 * (1 - node_filesystem_avail_bytes{mountpoint="/",fstype!~"tmpfs|overlay"} / node_filesystem_size_bytes{mountpoint="/",fstype!~"tmpfs|overlay"})` |
| Uptime | `time() - node_boot_time_seconds` |
| Load average | `node_load1` |

Q32. Which panels should the Network dashboard contain?

| Panel | Query |
| --- | --- |
| Receive bandwidth | `8 * rate(node_network_receive_bytes_total{device!~"lo"}[5m])` |
| Transmit bandwidth | `8 * rate(node_network_transmit_bytes_total{device!~"lo"}[5m])` |
| Receive packet rate | `rate(node_network_receive_packets_total{device!~"lo"}[5m])` |
| Transmit packet rate | `rate(node_network_transmit_packets_total{device!~"lo"}[5m])` |
| Receive errors | `rate(node_network_receive_errs_total{device!~"lo"}[5m])` |
| Transmit errors | `rate(node_network_transmit_errs_total{device!~"lo"}[5m])` |
| Interface up/down | `node_network_up{device!~"lo"}` |

Recommended interface filters:

- Router transit VLANs: `enp0s1.440`, `enp0s1.441`, `enp0s1.442`
- Management VLAN: `enp0s1.99` on routers, `enp0s1` on management and monitoring
- Hosting SVIs: `vlan10`, `vlan20`, `vlan30`

Q33. Which panels should the Routing dashboard contain?

| Panel | Query |
| --- | --- |
| FRR service state | `frr_service_active` |
| OSPFv2 full neighbors | `frr_ospf_neighbor_full_total{protocol="ospfv2"}` |
| OSPFv3 full neighbors | `frr_ospf_neighbor_full_total{protocol="ospfv3"}` |
| FRR textfile age | `time() - frr_textfile_last_success_unixtime` |
| FRR journal events | Loki query `{job="systemd-journal", unit="frr.service"}` |
| OSPF adjacency changes | Loki query `{job="systemd-journal"} |= "AdjChg"` |

Q34. Which dashboard design choices make evidence easier to read?

Use:

- One row per topic: health, resources, traffic, routing, logs.
- The `node` label as the main legend.
- Separate OSPFv2 and OSPFv3 panels.
- Fixed units: percent, bits/sec, seconds, short.
- Time range: `Last 15 minutes` for live tests, `Last 6 hours` for reports.
- Annotations or screenshots when replaying a failure.

## 15. Configure Alerts

Prometheus alert rules are stored under `/etc/prometheus/rules`.

Q35. Which alerts are required for Phase 3?

Create `/etc/prometheus/rules/network-security-lab.yml` on the Management VM:

```console
sudo tee /etc/prometheus/rules/network-security-lab.yml >/dev/null <<'EOF'
groups:
  - name: network-security-lab
    rules:
      - alert: LabNodeDown
        expr: up{job="node"} == 0
        for: 1m
        labels:
          severity: critical
          phase: phase-3-observability
        annotations:
          summary: "Lab node {{ $labels.node }} is down"
          description: "Prometheus cannot scrape {{ $labels.node }} at {{ $labels.instance }}."

      - alert: FRRServiceDown
        expr: frr_service_active == 0
        for: 30s
        labels:
          severity: critical
          phase: phase-3-observability
        annotations:
          summary: "FRR is down on {{ $labels.node }}"
          description: "frr.service is not active on {{ $labels.node }}."

      - alert: OSPFNeighborLoss
        expr: frr_ospf_neighbor_full_total < 2
        for: 30s
        labels:
          severity: warning
          phase: phase-3-observability
        annotations:
          summary: "{{ $labels.protocol }} neighbor loss on {{ $labels.node }}"
          description: "{{ $labels.node }} has fewer than two Full {{ $labels.protocol }} neighbors."

      - alert: FRRTextfileStale
        expr: time() - frr_textfile_last_success_unixtime > 60
        for: 1m
        labels:
          severity: warning
          phase: phase-3-observability
        annotations:
          summary: "FRR textfile metrics are stale on {{ $labels.node }}"
          description: "The FRR textfile collector has not updated recently."

      - alert: HighCPUUsage
        expr: 100 * (1 - avg by (node) (rate(node_cpu_seconds_total{mode="idle"}[5m]))) > 85
        for: 5m
        labels:
          severity: warning
          phase: phase-3-observability
        annotations:
          summary: "High CPU usage on {{ $labels.node }}"
          description: "CPU usage is above 85 percent for five minutes."

      - alert: HighMemoryUsage
        expr: 100 * (1 - node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes) > 90
        for: 5m
        labels:
          severity: warning
          phase: phase-3-observability
        annotations:
          summary: "High memory usage on {{ $labels.node }}"
          description: "Memory usage is above 90 percent for five minutes."

      - alert: RootDiskAlmostFull
        expr: 100 * (1 - node_filesystem_avail_bytes{mountpoint="/",fstype!~"tmpfs|overlay"} / node_filesystem_size_bytes{mountpoint="/",fstype!~"tmpfs|overlay"}) > 85
        for: 5m
        labels:
          severity: warning
          phase: phase-3-observability
        annotations:
          summary: "Root disk almost full on {{ $labels.node }}"
          description: "Root filesystem usage is above 85 percent."

      - alert: InterfaceReceiveErrors
        expr: rate(node_network_receive_errs_total{device!~"lo"}[5m]) > 0
        for: 2m
        labels:
          severity: warning
          phase: phase-3-observability
        annotations:
          summary: "Receive errors on {{ $labels.node }} {{ $labels.device }}"
          description: "The interface is reporting receive errors."
EOF

promtool check rules /etc/prometheus/rules/network-security-lab.yml
sudo systemctl reload prometheus || sudo systemctl restart prometheus
```

Q36. How do we inspect alerts?

Open:

```text
http://10.99.0.66:9090/alerts
```

Or query:

```console
curl -s http://127.0.0.1:9090/api/v1/alerts | jq
```

Expected baseline:

- No critical alert should fire in a healthy lab.
- The OSPF neighbor alert should be inactive while all three routers have two
  full neighbors.

## 16. Replay An OSPF Failure

The validation scenario should reuse a known Phase 2 failure. The safest choice
is the VLAN `440` loss between `R1` and `R2`, because it has already been
documented.

Q37. What should be visible before the failure?

Before the failure:

```promql
frr_ospf_neighbor_full_total{node="R2"}
```

Expected:

```text
ospfv2 = 2
ospfv3 = 2
```

LogQL:

```logql
{job="systemd-journal", unit="frr.service"} |= "AdjChg"
```

Expected:

- No new adjacency loss event during the healthy baseline window.

Q38. How do we start evidence capture?

Open four browser tabs:

1. Grafana System dashboard.
2. Grafana Network dashboard.
3. Grafana Routing dashboard.
4. Grafana Explore with the LogQL query:

```logql
{job="systemd-journal"} |= "AdjChg"
```

Also start a timestamped data-plane test from a container or router terminal:

```console
date -Ins
ping -D -i 0.2 10.10.0.169
```

Adapt the destination to a known host behind the affected path.

Q39. How do we trigger the OVS-side VLAN `440` failure?

Run on the hypervisor:

```console
date -Ins
sudo ovs-vsctl remove port tap62 trunks 440
date -Ins
sudo ovs-vsctl list port tap62 | grep -E "name|trunks|vlan_mode"
```

Expected OVS state:

```text
trunks : [99, 360, 441]
vlan_mode : trunk
```

Q40. What should change in metrics?

Expected Prometheus behavior:

```promql
frr_ospf_neighbor_full_total{node="R2",protocol="ospfv2"}
```

Expected value after convergence:

```text
1
```

Same for OSPFv3:

```promql
frr_ospf_neighbor_full_total{node="R2",protocol="ospfv3"}
```

Expected value:

```text
1
```

The alert `OSPFNeighborLoss` should become pending, then firing if the failure
lasts longer than the configured `for` duration.

Q41. What should change in logs?

LogQL queries:

```logql
{job="systemd-journal", node="R2"} |= "Full -> Deleted"
```

```logql
{job="systemd-journal", node="R2"} |= "enp0s1.440"
```

Expected log content:

- OSPFv2 adjacency to `1.0.0.4` is deleted on `enp0s1.440`.
- OSPFv3 adjacency to `1.0.0.6` is deleted on `enp0s1.440`.

Q42. How do we restore the link?

Run on the hypervisor:

```console
date -Ins
sudo ovs-vsctl add port tap62 trunks 440
date -Ins
sudo ovs-vsctl list port tap62 | grep -E "name|trunks|vlan_mode"
```

Expected OVS state:

```text
trunks : [99, 360, 440, 441]
vlan_mode : trunk
```

Q43. What should be visible after recovery?

PromQL:

```promql
frr_ospf_neighbor_full_total{node="R2"}
```

Expected:

```text
ospfv2 = 2
ospfv3 = 2
```

LogQL:

```logql
{job="systemd-journal", node="R2"} |= "Exchange -> Full"
```

Expected:

- OSPF adjacency returns to `Full`.
- Grafana dashboard returns to the healthy baseline.
- Alert resolves after the rule expression is false.

## 17. Save Evidence

Q44. What screenshots should be saved?

Save screenshots under `screenshots/phase3/`:

| Evidence | Suggested filename |
| --- | --- |
| Prometheus targets all up | `phase3-prometheus-targets.png` |
| System dashboard baseline | `phase3-system-baseline.png` |
| Network dashboard baseline | `phase3-network-baseline.png` |
| Routing dashboard baseline | `phase3-routing-baseline.png` |
| Loki FRR logs baseline | `phase3-loki-frr-baseline.png` |
| OSPF neighbor loss alert | `phase3-ospf-neighbor-loss-alert.png` |
| OSPF adjacency loss logs | `phase3-ospf-adjch-failure.png` |
| Dashboard during VLAN `440` failure | `phase3-routing-vlan440-failure.png` |
| Dashboard after recovery | `phase3-routing-recovery.png` |

Q45. Which command outputs should be copied into the proof report?

Use a future `docs/proofs-phase3.md` file and include:

```console
curl -s http://127.0.0.1:9090/api/v1/targets | jq '.data.activeTargets[] | {job: .labels.job, node: .labels.node, health: .health}'
```

```console
curl -s http://127.0.0.1:9090/api/v1/query --data-urlencode 'query=frr_ospf_neighbor_full_total' | jq
```

```console
curl -G -s "http://127.0.0.1:3100/loki/api/v1/query_range" \
    --data-urlencode 'query={job="systemd-journal"} |= "AdjChg"' \
    --data-urlencode 'limit=20' | jq
```

```console
sudo systemctl status prometheus loki grafana-server alloy --no-pager
```

On routers:

```console
systemctl status prometheus-node-exporter frr-textfile.timer frr --no-pager
curl -s http://127.0.0.1:9100/metrics | grep '^frr_'
```

Q46. Which configuration files should be backed up?

Back up these files into private notes or a controlled evidence folder:

| Node | Files |
| --- | --- |
| `management` | `/etc/prometheus/prometheus.yml` |
| `management` | `/etc/prometheus/rules/network-security-lab.yml` |
| `management` | `/etc/loki/config.yml` |
| `management` | `/etc/grafana/provisioning/datasources/network-security-lab.yml` |
| All nodes | `/etc/alloy/config.alloy` |
| Routers | `/usr/local/lib/prometheus/frr_textfile.sh` |
| Routers | `/etc/systemd/system/frr-textfile.service` |
| Routers | `/etc/systemd/system/frr-textfile.timer` |

Do not commit passwords, Grafana session tokens, cookies, or private SSH keys.

## 18. Troubleshooting

### Prometheus Target Down

Q47. What should be checked first?

From the Management VM:

```console
ping -c 2 10.99.0.2
nc -vz 10.99.0.2 9100
curl -s http://10.99.0.2:9100/metrics | head
```

On the target:

```console
sudo systemctl status prometheus-node-exporter --no-pager
sudo ss -ltnp | grep 9100
journalctl -u prometheus-node-exporter -n 50 --no-pager
```

### FRR Metrics Missing

Q48. What should be checked?

On the router:

```console
sudo systemctl status frr-textfile.timer --no-pager
sudo systemctl status frr-textfile.service --no-pager
sudo /usr/local/lib/prometheus/frr_textfile.sh
cat /var/lib/prometheus/node-exporter/frr.prom
curl -s http://127.0.0.1:9100/metrics | grep '^frr_'
```

If `vtysh` fails, verify:

```console
sudo systemctl status frr --no-pager
sudo vtysh -c 'show ip ospf neighbor'
sudo vtysh -c 'show ipv6 ospf6 neighbor'
```

### Loki Receives No Logs

Q49. What should be checked?

On the source node:

```console
groups alloy
sudo systemctl restart alloy
journalctl -u alloy -n 100 --no-pager
logger -t phase3-test "manual Loki test from $(hostname -s)"
```

On the Management VM:

```console
curl -s http://10.99.0.66:3100/ready
curl -G -s "http://10.99.0.66:3100/loki/api/v1/label/node/values" | jq
```

Common causes:

- Alloy is not in the `systemd-journal` group.
- The `node` label was not changed after copying the config.
- Loki is listening only on `127.0.0.1`.
- A firewall blocks `3100/tcp`.
- The Alloy config contains a syntax error.

### Grafana Data Source Fails

Q50. What should be checked?

On the Management VM:

```console
sudo systemctl status grafana-server prometheus loki --no-pager
curl -s http://127.0.0.1:9090/-/ready
curl -s http://127.0.0.1:3100/ready
sudo journalctl -u grafana-server -n 100 --no-pager
```

Check the provisioned file:

```console
sudo cat /etc/grafana/provisioning/datasources/network-security-lab.yml
```

Then restart Grafana:

```console
sudo systemctl restart grafana-server
```

## 19. Conclusion

This Phase 3 lab turns the OSPF network into an observable system. The routing
foundation from Phase 1 and the failure scenarios from Phase 2 now produce
live operational evidence:

- Prometheus confirms whether nodes, interfaces, and FRR are healthy.
- Custom FRR textfile metrics expose OSPF neighbor state.
- Loki and Alloy centralize systemd and FRR journal events.
- Grafana makes the lab understandable through dashboards and alerts.
- A replayed VLAN `440` failure is visible across metrics, logs, and alerts.

The exit criteria for Phase 3 are satisfied when the dashboards show useful
live data, logs are centralized, and an important failure such as OSPF neighbor
loss is visible without manually logging into every router.

## 20. References

- InetDoc OSPF practical lab style and structure: <https://inetdoc.net/travaux_pratiques/interco_05.ospf/>
- Prometheus installation and configuration documentation: <https://prometheus.io/docs/prometheus/latest/installation/>
- Prometheus Node Exporter guide: <https://prometheus.io/docs/guides/node-exporter/>
- Prometheus alerting rules: <https://prometheus.io/docs/prometheus/latest/configuration/alerting_rules/>
- Grafana Debian/Ubuntu installation: <https://grafana.com/docs/grafana/latest/setup-grafana/installation/debian/>
- Grafana provisioning documentation: <https://grafana.com/docs/grafana/latest/administration/provisioning/>
- Loki local installation: <https://grafana.com/docs/loki/latest/setup/install/local/>
- Loki local filesystem configuration example: <https://grafana.com/docs/loki/latest/configure/examples/configuration-examples/>
- Grafana Alloy Linux installation: <https://grafana.com/docs/alloy/latest/set-up/install/linux/>
- Grafana Alloy journal source component: <https://grafana.com/docs/alloy/latest/reference/components/loki/loki.source.journal/>
