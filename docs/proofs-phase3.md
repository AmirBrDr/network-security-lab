# Phase 3 Observability Proof Report

Status: complete

Evidence window: June 5, 2026 through June 10, 2026

Phase 3 adds a working observability layer on top of the OSPF lab. The
management VM on `tap66` now hosts Prometheus, Loki, and Grafana. Alloy forwards
systemd journal logs into Loki, node exporter exposes host metrics, and custom
FRR textfile metrics expose routing health for the OSPF routers.

## Executive Summary

The captured evidence proves that the lab has useful live monitoring, central
logs, routing-aware metrics, dashboards, and alert rules:

- Prometheus scrapes `R1`, `R2`, `R3`, the monitoring VM, the management VM,
  itself, and Loki.
- Node exporter exposes CPU, memory, disk, uptime, and interface metrics from
  all lab nodes.
- A custom FRR textfile collector reports `frr.service` status and full
  OSPFv2/OSPFv3 neighbor counts on each router.
- Loki is reachable and stores journal labels for `R1`, `R2`, `R3`,
  `management`, and `monitoring`.
- Grafana is provisioned with Prometheus and Loki data sources.
- Grafana dashboards cover network traffic, routing health, and system health.
- Prometheus rules detect node loss, FRR service loss, OSPF neighbor loss,
  stale FRR metrics, high CPU, high memory, disk pressure, and interface errors.
- A controlled VLAN `440` failure triggered OSPF neighbor-loss visibility in
  dashboards, Loki logs, and Prometheus alerts, then cleared after recovery.

## Evidence Index

| Area | Result | Primary evidence |
| --- | --- | --- |
| Prometheus service | Ready and scraping lab targets | [up query](../screenshots/phase3/phase3-prometheus-up-query.png), [query console](../screenshots/phase3/phase3-prometheus-query-console.png) |
| Host metrics | Node exporter data visible for all lab nodes | [node inventory](../screenshots/phase3/phase3-prometheus-node-inventory.png), [memory query](../screenshots/phase3/phase3-prometheus-memory-usage.png) |
| Interface metrics | Network traffic is graphed from Prometheus data | [traffic graph](../screenshots/phase3/phase3-prometheus-network-traffic-graph.png), [network dashboard](../screenshots/phase3/phase3-network-baseline.png) |
| FRR metrics | FRR service state and OSPF neighbor counts are exposed | [FRR textfile age query](../screenshots/phase3/phase3-prometheus-frr-textfile-age.png), [routing dashboard](../screenshots/phase3/phase3-routing-baseline.png) |
| Loki logs | Journal labels and FRR adjacency events are searchable | [adjacency loss logs](../screenshots/phase3/phase3-loki-ospf-adjacency-loss.png), [adjacency recovery logs](../screenshots/phase3/phase3-loki-ospf-adjacency-recovery.png) |
| Grafana | Data sources and dashboards are provisioned | [data sources](../screenshots/phase3/phase3-grafana-datasources.png), [Grafana home](../screenshots/phase3/phase3-grafana-home.png) |
| Alert rules | Rules load in Prometheus and reflect healthy/failure states | [baseline alerts](../screenshots/phase3/phase3-prometheus-alerts-baseline.png), [OSPF alert firing](../screenshots/phase3/phase3-prometheus-ospf-neighbor-loss-alert.png), [alerts recovered](../screenshots/phase3/phase3-prometheus-alerts-recovered.png) |

## Configuration Snapshots

| Component | Repository snapshot |
| --- | --- |
| Prometheus scrape configuration | [configs/prometheus.yml](../configs/prometheus.yml) |
| Prometheus alert rules | [configs/prometheus-rules.yml](../configs/prometheus-rules.yml) |
| Grafana data sources | [configs/grafana-datasources.yml](../configs/grafana-datasources.yml) |
| Loki configuration | [configs/loki-config.yml](../configs/loki-config.yml) |
| Alloy journal forwarding, management VM | [configs/management-config.alloy](../configs/management-config.alloy) |
| Alloy journal forwarding, monitoring VM | [configs/monitoring-config.alloy](../configs/monitoring-config.alloy) |
| Alloy journal forwarding, routers | [configs/r1-config.alloy](../configs/r1-config.alloy), [configs/r2-config.alloy](../configs/r2-config.alloy), [configs/r3-config.alloy](../configs/r3-config.alloy) |
| FRR textfile collector | [configs/routers-frr_textfile.sh](../configs/routers-frr_textfile.sh) |
| FRR textfile timer | [configs/routers-frr-textfile.service](../configs/routers-frr-textfile.service), [configs/routers-frr-textfile.timer](../configs/routers-frr-textfile.timer) |
| Grafana dashboards | [network](../monitoring/grafana/dashboards/network/network.json), [routing](../monitoring/grafana/dashboards/routing/routing.json), [system](../monitoring/grafana/dashboards/system/system.json) |

## Observability Scope

| Node | Role | Management address | Metrics | Logs |
| --- | --- | --- | --- | --- |
| `R1` | Router | `10.99.0.1` | node exporter, FRR textfile | Alloy journal forwarder |
| `R2` | Router | `10.99.0.2` | node exporter, FRR textfile | Alloy journal forwarder |
| `R3` | Router | `10.99.0.3` | node exporter, FRR textfile | Alloy journal forwarder |
| `monitoring` | IDS-ready VM | `10.99.0.65` | node exporter | Alloy journal forwarder |
| `management` | Observability VM | `10.99.0.66` | node exporter, Prometheus, Loki | Alloy journal forwarder |

## Result Summary

| Check | Result |
| --- | --- |
| Management VM network | `10.99.0.66/24` and `fd14:ca46:3864:99::66/64` configured with working default routes. |
| Management reachability | IPv4 and IPv6 pings to `R1`, `R2`, `R3`, and `monitoring` returned `0%` packet loss. |
| Node exporter reachability | All five lab nodes returned `node_exporter_build_info` from port `9100`. |
| FRR textfile collector | `R1`, `R2`, and `R3` reported active FRR and two full OSPF neighbors for both OSPFv2 and OSPFv3 at baseline. |
| Prometheus | Configuration validated and service started successfully. Loki initially appeared down until Loki was configured, then reported up. |
| Loki | Service returned `ready` and exposed labels for all expected nodes. |
| Alloy | Journal pipelines started on routers and VMs and pushed logs to Loki. |
| Grafana | Health endpoint returned `database: ok`, and both Prometheus and Loki data sources were present. |
| Alerts | Eight Prometheus alert rules were visible. The VLAN `440` replay fired `OSPFNeighborLoss` and recovered cleanly. |

## Screenshot Evidence

### Prometheus Validation

**Prometheus query console**

<img src="../screenshots/phase3/phase3-prometheus-query-console.png" alt="Prometheus query console" width="900">

**Prometheus `up` query across lab targets**

<img src="../screenshots/phase3/phase3-prometheus-up-query.png" alt="Prometheus up query across lab targets" width="900">

**Prometheus node inventory**

<img src="../screenshots/phase3/phase3-prometheus-node-inventory.png" alt="Prometheus node inventory query" width="900">

**Prometheus memory usage query**

<img src="../screenshots/phase3/phase3-prometheus-memory-usage.png" alt="Prometheus memory usage query" width="900">

**Prometheus network traffic graph**

<img src="../screenshots/phase3/phase3-prometheus-network-traffic-graph.png" alt="Prometheus network traffic graph" width="900">

**Prometheus FRR textfile freshness**

<img src="../screenshots/phase3/phase3-prometheus-frr-textfile-age.png" alt="Prometheus FRR textfile age query" width="900">

**Prometheus alert rules at baseline**

<img src="../screenshots/phase3/phase3-prometheus-alerts-baseline.png" alt="Prometheus alert rules at healthy baseline" width="900">

### Grafana Setup

**Grafana login screen**

<img src="../screenshots/phase3/phase3-grafana-login.png" alt="Grafana login screen" width="900">

**Grafana home screen**

<img src="../screenshots/phase3/phase3-grafana-home.png" alt="Grafana home screen" width="900">

**Grafana Prometheus and Loki data sources**

<img src="../screenshots/phase3/phase3-grafana-datasources.png" alt="Grafana Prometheus and Loki data sources" width="900">

### Grafana Dashboards

**Network dashboard baseline**

<img src="../screenshots/phase3/phase3-network-baseline.png" alt="Grafana network dashboard baseline" width="900">

**Routing dashboard baseline**

<img src="../screenshots/phase3/phase3-routing-baseline.png" alt="Grafana routing dashboard baseline" width="900">

**System dashboard baseline**

<img src="../screenshots/phase3/phase3-system-baseline.png" alt="Grafana system dashboard baseline" width="900">

### Failure Replay And Recovery

**Routing dashboard during VLAN `440` failure**

<img src="../screenshots/phase3/phase3-routing-vlan440-failure.png" alt="Grafana routing dashboard during VLAN 440 failure" width="900">

**Loki FRR adjacency-loss logs**

<img src="../screenshots/phase3/phase3-loki-ospf-adjacency-loss.png" alt="Loki FRR adjacency-loss logs" width="900">

**Prometheus `OSPFNeighborLoss` alert firing**

<img src="../screenshots/phase3/phase3-prometheus-ospf-neighbor-loss-alert.png" alt="Prometheus OSPF neighbor loss alert firing" width="900">

**Routing dashboard after VLAN `440` recovery**

<img src="../screenshots/phase3/phase3-routing-vlan440-recovery.png" alt="Grafana routing dashboard after VLAN 440 recovery" width="900">

**Loki FRR adjacency-recovery logs**

<img src="../screenshots/phase3/phase3-loki-ospf-adjacency-recovery.png" alt="Loki FRR adjacency-recovery logs" width="900">

**Prometheus alerts after recovery**

<img src="../screenshots/phase3/phase3-prometheus-alerts-recovered.png" alt="Prometheus alerts cleared after VLAN 440 recovery" width="900">

## Command Evidence

### Management VM Network

The management VM is statically addressed on the management VLAN and has IPv4
and IPv6 default routes through `R1`.

```console
etu@management:~$ sudo cat /etc/netplan/enp0s1.yaml
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

```console
etu@management:~$ ip addr show enp0s1
2: enp0s1: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc mq state UP group default qlen 1000
    link/ether b8:ad:ca:fe:00:42 brd ff:ff:ff:ff:ff:ff
    inet 10.99.0.66/24 brd 10.99.0.255 scope global enp0s1
    inet6 fd14:ca46:3864:99::66/64 scope global
    inet6 fe80::baad:caff:fefe:42/64 scope link proto kernel_ll

etu@management:~$ ip route
default via 10.99.0.1 dev enp0s1 proto static
10.99.0.0/24 dev enp0s1 proto kernel scope link src 10.99.0.66

etu@management:~$ ip -6 route
fd14:ca46:3864:99::/64 dev enp0s1 proto kernel metric 256 pref medium
default via fd14:ca46:3864:99::1 dev enp0s1 proto static metric 1024 pref medium
```

### Management Reachability

The management VM reached all router and monitoring management addresses over
IPv4 and IPv6 with no packet loss.

| Target | IPv4 result | IPv6 result |
| --- | --- | --- |
| `R1` | `10.99.0.1`, `0%` packet loss | `fd14:ca46:3864:99::1`, `0%` packet loss |
| `R2` | `10.99.0.2`, `0%` packet loss | `fd14:ca46:3864:99::2`, `0%` packet loss |
| `R3` | `10.99.0.3`, `0%` packet loss | `fd14:ca46:3864:99::3`, `0%` packet loss |
| `monitoring` | `10.99.0.65`, `0%` packet loss | `fd14:ca46:3864:99::65`, `0%` packet loss |

### SSH Forwarding

Local forwards provide browser access to Grafana, Prometheus, and Loki through
the management VM.

```sshconfig
Host management
    HostName 10.99.0.66
    User etu
    Port 22
    ProxyJump r1

    LocalForward 3000 127.0.0.1:3000
    LocalForward 9090 127.0.0.1:9090
    LocalForward 3100 127.0.0.1:3100
    ExitOnForwardFailure yes
```

### Node Exporter

Every Phase 3 node answered on port `9100` with node exporter metrics.

```console
etu@management:~$ for host in 10.99.0.1 10.99.0.2 10.99.0.3 10.99.0.65 10.99.0.66; do
>   echo "===== $host ====="
>   curl -s "http://$host:9100/metrics" | grep -m1 node_exporter_build_info
> done
===== 10.99.0.1 =====
# HELP node_exporter_build_info A metric with a constant '1' value labeled by version, revision, branch, goversion from which node_exporter was built, and the goos and goarch for the build.
===== 10.99.0.2 =====
# HELP node_exporter_build_info A metric with a constant '1' value labeled by version, revision, branch, goversion from which node_exporter was built, and the goos and goarch for the build.
===== 10.99.0.3 =====
# HELP node_exporter_build_info A metric with a constant '1' value labeled by version, revision, branch, goversion from which node_exporter was built, and the goos and goarch for the build.
===== 10.99.0.65 =====
# HELP node_exporter_build_info A metric with a constant '1' value labeled by version, revision, branch, goversion from which node_exporter was built, and the goos and goarch for the build.
===== 10.99.0.66 =====
# HELP node_exporter_build_info A metric with a constant '1' value labeled by version, revision, branch, goversion from which node_exporter was built, and the goos and goarch for the build.
```

### FRR Textfile Metrics

The FRR textfile collector publishes routing-health metrics for each router.
At baseline, all three routers reported active FRR and two full neighbors for
both OSPFv2 and OSPFv3.

```console
etu@R1:~$ curl -s http://127.0.0.1:9100/metrics | grep '^frr_'
frr_ospf_neighbor_full_total{node="R1",protocol="ospfv2"} 2
frr_ospf_neighbor_full_total{node="R1",protocol="ospfv3"} 2
frr_service_active{node="R1"} 1
frr_textfile_last_success_unixtime{node="R1"} 1.780664327e+09

etu@R2:~$ curl -s http://127.0.0.1:9100/metrics | grep '^frr_'
frr_ospf_neighbor_full_total{node="R2",protocol="ospfv2"} 2
frr_ospf_neighbor_full_total{node="R2",protocol="ospfv3"} 2
frr_service_active{node="R2"} 1
frr_textfile_last_success_unixtime{node="R2"} 1.780664332e+09

etu@R3:~$ curl -s http://127.0.0.1:9100/metrics | grep '^frr_'
frr_ospf_neighbor_full_total{node="R3",protocol="ospfv2"} 2
frr_ospf_neighbor_full_total{node="R3",protocol="ospfv3"} 2
frr_service_active{node="R3"} 1
frr_textfile_last_success_unixtime{node="R3"} 1.780664336e+09
```

The collector is refreshed by a systemd timer.

```console
etu@R1:~$ systemctl list-timers frr-textfile.timer
NEXT LEFT LAST                           PASSED UNIT               ACTIVATES
-       - Fri 2026-06-05 14:57:44 CEST 27ms ago frr-textfile.timer frr-textfile.service

1 timers listed.
```

### Prometheus Targets

Prometheus configuration validation succeeded and the service started.

```console
etu@management:~$ promtool check config /etc/prometheus/prometheus.yml
Checking /etc/prometheus/prometheus.yml
 SUCCESS: /etc/prometheus/prometheus.yml is valid prometheus config file syntax

etu@management:~$ sudo systemctl status prometheus --no-pager
prometheus.service - Monitoring system and time series database
   Active: active (running) since Fri 2026-06-05 15:02:18 CEST
```

The first target check correctly showed Loki as down before Loki was configured.
After Loki was remediated, the Loki scrape target reported healthy.

```console
etu@management:~$ curl -s http://127.0.0.1:9090/api/v1/targets \
>   | jq '.data.activeTargets[] | {job: .labels.job, node: .labels.node, health: .health, scrapeUrl: .scrapeUrl}'
{
  "job": "loki",
  "node": "management",
  "health": "down",
  "scrapeUrl": "http://127.0.0.1:3100/metrics"
}
{
  "job": "node",
  "node": "monitoring",
  "health": "up",
  "scrapeUrl": "http://10.99.0.65:9100/metrics"
}
{
  "job": "node",
  "node": "management",
  "health": "up",
  "scrapeUrl": "http://10.99.0.66:9100/metrics"
}
{
  "job": "node",
  "node": "R1",
  "health": "up",
  "scrapeUrl": "http://10.99.0.1:9100/metrics"
}
{
  "job": "node",
  "node": "R2",
  "health": "up",
  "scrapeUrl": "http://10.99.0.2:9100/metrics"
}
{
  "job": "node",
  "node": "R3",
  "health": "up",
  "scrapeUrl": "http://10.99.0.3:9100/metrics"
}
{
  "job": "prometheus",
  "node": "management",
  "health": "up",
  "scrapeUrl": "http://127.0.0.1:9090/metrics"
}
```

```console
etu@management:~$ curl -s http://127.0.0.1:9090/api/v1/targets \
>   | jq '.data.activeTargets[] | select(.labels.job=="loki") | {job: .labels.job, node: .labels.node, health: .health, scrapeUrl: .scrapeUrl}'
{
  "job": "loki",
  "node": "management",
  "health": "up",
  "scrapeUrl": "http://127.0.0.1:3100/metrics"
}
```

### Loki And Alloy

Loki became ready after the ingester warm-up period and exposed Prometheus
metrics.

```console
etu@management:~$ curl -s http://10.99.0.66:3100/ready
ready

etu@management:~$ curl -s http://10.99.0.66:3100/metrics | head
# HELP deprecated_flags_inuse_total The number of deprecated flags currently set.
# TYPE deprecated_flags_inuse_total counter
deprecated_flags_inuse_total 0
```

Loki labels confirm that journal logs are present for the expected Phase 3
nodes.

```console
etu@management:~$ curl -G -s "http://10.99.0.66:3100/loki/api/v1/labels" | jq
{
  "status": "success",
  "data": [
    "host",
    "job",
    "lab",
    "level",
    "node",
    "service_name",
    "unit"
  ]
}

etu@management:~$ curl -G -s "http://10.99.0.66:3100/loki/api/v1/label/node/values" | jq
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

Alloy loaded the journal pipeline and began serving its local HTTP endpoint.

```console
etu@R3:~$ journalctl -u alloy -n 50 --no-pager
Jun 05 18:23:18 R3 systemd[1]: Started alloy.service - Vendor-agnostic OpenTelemetry Collector distribution with programmable pipelines.
Jun 05 18:23:18 R3 alloy[16469]: ts=2026-06-05T16:23:18.892488725Z level=info msg="finished node evaluation" node_id=loki.relabel.journal
Jun 05 18:23:18 R3 alloy[16469]: ts=2026-06-05T16:23:18.892656216Z level=info msg="finished node evaluation" node_id=loki.source.journal.system
Jun 05 18:23:18 R3 alloy[16469]: ts=2026-06-05T16:23:18.892291337Z level=info msg="finished node evaluation" node_id=loki.write.lab
Jun 05 18:23:18 R3 alloy[16469]: ts=2026-06-05T16:23:18.894389756Z level=info msg="now listening for http traffic" service=http addr=127.0.0.1:12345
```

### Grafana

Grafana, Prometheus, and Loki health checks all returned ready responses.

```console
etu@management:~$ curl -s http://127.0.0.1:3000/api/health
{
  "database": "ok",
  "version": "13.0.2",
  "commit": "3fcdbc5a"
}

etu@management:~$ curl -s http://127.0.0.1:9090/-/ready
Prometheus Server is Ready.

etu@management:~$ curl -s http://127.0.0.1:3100/ready
ready
```

Grafana is provisioned with Prometheus as the default metrics source and Loki
as the log source.

```yaml
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
```

### Alert Rules

The Phase 3 rule group is stored in
[configs/prometheus-rules.yml](../configs/prometheus-rules.yml). The rules
cover:

| Alert | Purpose |
| --- | --- |
| `LabNodeDown` | Detects failed node exporter scrapes. |
| `FRRServiceDown` | Detects an inactive `frr.service`. |
| `OSPFNeighborLoss` | Detects fewer than two full OSPF neighbors on a router. |
| `FRRTextfileStale` | Detects stale FRR textfile metrics. |
| `HighCPUUsage` | Detects sustained CPU pressure. |
| `HighMemoryUsage` | Detects sustained memory pressure. |
| `RootDiskAlmostFull` | Detects root filesystem pressure. |
| `InterfaceReceiveErrors` | Detects interface receive errors. |

The baseline screenshot shows all eight rules inactive. The VLAN `440` failure
replay shows `OSPFNeighborLoss` firing for the affected routers and protocols.
The recovery screenshot shows the alert state cleared again.

### VLAN `440` Failure Replay

The controlled replay removed VLAN `440` from `tap62`, which breaks the direct
`R1` to `R2` transit link. It was then restored. The timestamps line up with
the Grafana routing panels, Loki FRR adjacency logs, and Prometheus alert
screenshots.

```console
amirmahdighasemi@bob:~$ date -Ins
2026-06-10T11:36:13,580185553+02:00

amirmahdighasemi@bob:~$ sudo ovs-vsctl remove port tap62 trunks 440

amirmahdighasemi@bob:~$ date -Ins
2026-06-10T11:36:13,784447523+02:00

amirmahdighasemi@bob:~$ sudo ovs-vsctl list port tap62 | grep -E "name|trunks|vlan_mode"
name                : tap62
trunks              : [99, 360, 441]
vlan_mode           : trunk
```

```console
amirmahdighasemi@bob:~$ date -Ins
2026-06-10T11:47:42,257627922+02:00

amirmahdighasemi@bob:~$ sudo ovs-vsctl add port tap62 trunks 440

amirmahdighasemi@bob:~$ date -Ins
2026-06-10T11:47:42,455935615+02:00

amirmahdighasemi@bob:~$ sudo ovs-vsctl list port tap62 | grep -E "name|trunks|vlan_mode"
name                : tap62
trunks              : [99, 360, 440, 441]
vlan_mode           : trunk
```

## Completion Checklist

- [x] Management / observability VM deployed on `tap66`.
- [x] Prometheus installed and running.
- [x] Node exporters installed and reachable.
- [x] Router and VM scrape targets configured.
- [x] CPU, RAM, disk, uptime, and interface metrics collected.
- [x] FRR service state and OSPF neighbor counts collected.
- [x] Loki installed and running.
- [x] System logs centralized through Alloy.
- [x] Grafana installed.
- [x] Prometheus and Loki data sources connected.
- [x] Network, system, and routing dashboards created.
- [x] Router, OSPF, CPU, memory, disk, and interface alert rules configured.
- [x] Controlled VLAN `440` failure replayed and visible in metrics, logs, and alerts.
- [x] Dashboard and alert screenshots saved.
- [x] Observability setup documented.

## Notes

- Phase 3 proves local observability and Prometheus-native alerting. It does
  not claim an external Alertmanager notification path.
- The IDS VM is monitored in Phase 3, but Suricata deployment belongs to
  Phase 4.
- The captured failure replay validates visibility for the existing Phase 2
  VLAN `440` failure scenario and gives Phase 4 a reliable monitoring base.
