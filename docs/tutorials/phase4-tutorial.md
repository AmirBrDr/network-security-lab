# Phase 4 - Security Layer With Suricata And Incident Evidence

Network Security Lab

## Summary

This practical lab turns the routed and observable OSPF platform into a
security monitoring lab. It deploys Suricata on the Monitoring VM, connects IDS
events to the existing Loki and Grafana stack, exposes simple Prometheus metrics
for IDS health, and runs controlled lab-only attack simulations.

The security layer is deliberately modest and reproducible:

- Suricata inspects copied traffic from the lab networks.
- EVE JSON stores alerts, flows, HTTP records, DNS records, TLS records, and
  SSH records.
- Grafana Alloy forwards Suricata EVE JSON to Loki.
- Node Exporter's textfile collector exposes Suricata service and alert
  counters to Prometheus.
- Grafana displays IDS logs and metrics next to the existing network,
  routing, and system dashboards.
- The test scenarios stay inside the lab: Nmap scan, SSH connection burst,
  suspicious HTTP marker, and ICMP sweep.

At the end of this lab, at least two security incidents must be documented with
alerts, logs, screenshots, timestamps, and packet or command evidence.

## Table Of Contents

1. Objectives
2. Lab Topology
3. Safety Boundary
4. Security Addressing And Roles
5. Prepare The Monitoring VM
6. Confirm What The IDS Can Observe
7. Configure OVS Traffic Mirroring
8. Install Suricata
9. Configure Suricata For The Lab
10. Add Local Detection Rules
11. Validate Live Capture
12. Forward Suricata Logs To Loki
13. Add Suricata Metrics With The Textfile Collector
14. Add Prometheus Alert Rules
15. Build The Grafana Security Dashboard
16. Prepare Attacker And Victim Endpoints
17. Scenario 1 - Nmap Reconnaissance Scan
18. Scenario 2 - SSH Connection Burst
19. Scenario 3 - Suspicious HTTP Marker
20. Scenario 4 - ICMP Sweep
21. Save Evidence
22. Write Incident Reports
23. Tune Rules And Reduce Noise
24. Troubleshooting
25. Conclusion
26. References

## 1. Objectives

After completing this practical lab, you should be able to:

1. Deploy a Suricata IDS sensor on the Monitoring VM.
2. Explain which lab traffic the IDS can and cannot observe.
3. Configure an Open vSwitch mirror for selected OSPF, hosting, and management
   VLANs.
4. Run Suricata in IDS mode on the mirror interface.
5. Enable EVE JSON output and validate alert, flow, HTTP, DNS, TLS, and SSH
   records.
6. Add deterministic local Suricata rules for Phase 4 validation.
7. Forward `/var/log/suricata/eve.json` to Loki through Grafana Alloy.
8. Query Suricata alerts in Grafana Explore with LogQL.
9. Expose basic Suricata service and alert counters to Prometheus.
10. Create a Grafana security dashboard.
11. Run controlled internal attack simulations only inside the lab.
12. Save evidence and write incident reports with honest limitations.

## 2. Lab Topology

Phase 4 starts from the end of Phase 3:

- OSPFv2 and OSPFv3 are stable between `R1`, `R2`, and `R3`.
- Hosting networks behind the routers are reachable through OSPF.
- The Management VM runs Prometheus, Loki, Grafana, and dashboard
  provisioning.
- Grafana Alloy already forwards systemd journal logs from the routers and VMs.
- Node Exporter already runs on the routers, Monitoring VM, and Management VM.

The routed topology remains unchanged:

```text
             VLAN 440
        R1 ----------- R2
         \             /
 VLAN 441 \           / VLAN 442
           \         /
              R3
```

The management and security plane uses the existing management network:

```text
                 Management VLAN 99

 R1 10.99.0.1  ----+
 R2 10.99.0.2  ----+
 R3 10.99.0.3  ----+---- Management VM 10.99.0.66
 Monitoring VM ----+          Prometheus
 10.99.0.65                  Loki
                              Grafana
```

Suricata should inspect mirrored traffic, not act as a router. The Monitoring
VM remains an observation node.

Recommended Phase 4 capture design:

```text
                  OVS bridge dsw-host

 tap62 R1 trunk ----+
 tap63 R2 trunk ----+---- mirror selected VLANs ---- tap67 IDS sensor NIC
 tap64 R3 trunk ----+                              Monitoring VM

 tap65 management access VLAN 99 ----------------- Monitoring VM
```

If only `tap65` is available, keep in mind that it is currently an access port
for VLAN `99`. Without a mirror or a second capture interface, Suricata will
see only traffic addressed to the Monitoring VM plus broadcasts. That is not
enough to validate inter-container attacks.

## 3. Safety Boundary

Q1. What is the security boundary for this phase?

All tests in this tutorial are limited to lab-owned VMs and containers:

- Routers: `R1`, `R2`, `R3`
- Monitoring VM: `10.99.0.65`
- Management VM: `10.99.0.66`
- Existing Incus containers behind VLANs `10`, `20`, and `30`

Do not scan, brute-force, fuzz, or send suspicious traffic toward:

- University infrastructure outside this lab
- Public internet targets
- Other students' systems
- Unknown private networks
- Any system that is not explicitly part of this project

Q2. Which commands must be treated carefully?

Commands such as `nmap`, repeated SSH attempts, packet generators, and custom
traffic loops are allowed only when the destination is an internal lab address.

Before every scenario, print the variables that define the attacker and victim:

```console
echo "ATTACKER_IP=$ATTACKER_IP"
echo "VICTIM_IP=$VICTIM_IP"
```

Expected result:

- Both addresses are inside `10.10.0.0/24`, `10.20.0.0/24`,
  `10.30.0.0/24`, or another documented lab prefix.
- No command uses a public IP address or external DNS name as a target.

## 4. Security Addressing And Roles

### 4.1. Node Inventory

| Node | Role | TAP | Management IPv4 | Management IPv6 |
| --- | --- | --- | --- | --- |
| `R1` | Router and default route origin | `tap62` | `10.99.0.1` | `fd14:ca46:3864:99::1` |
| `R2` | Router | `tap63` | `10.99.0.2` | `fd14:ca46:3864:99::2` |
| `R3` | Router | `tap64` | `10.99.0.3` | `fd14:ca46:3864:99::3` |
| `monitoring` | IDS sensor | `tap65` | `10.99.0.65` | `fd14:ca46:3864:99::65` |
| `management` | Observability stack | `tap66` | `10.99.0.66` | `fd14:ca46:3864:99::66` |

Optional but recommended:

| TAP | Purpose |
| --- | --- |
| `tap67` | Dedicated IDS mirror interface for the Monitoring VM |

### 4.2. Observed Networks

| VLAN | Prefix | Purpose | IDS expectation |
| ---: | --- | --- | --- |
| `10` | `10.10.0.0/24` | R1 hosting network | Observe attacker or victim traffic |
| `20` | `10.20.0.0/24` | R2 hosting network | Observe attacker or victim traffic |
| `30` | `10.30.0.0/24` | R3 hosting network | Observe attacker or victim traffic |
| `440` | `10.44.0.0/29` | R1 to R2 transit | Observe routed copies |
| `441` | `10.44.1.0/29` | R1 to R3 transit | Observe routed copies |
| `442` | `10.44.2.0/29` | R2 to R3 transit | Observe routed copies |
| `99` | `10.99.0.0/24` | Management | Observe only if intentionally mirrored |

### 4.3. Suggested Scenario Roles

Use the existing Incus containers when possible.

| Role | Suggested location | Example IPv4 from Phase 1 evidence |
| --- | --- | --- |
| Attacker | `R2` hosting network, VLAN `20` | `10.20.0.156` |
| Victim web/SSH server | `R1` hosting network, VLAN `10` | `10.10.0.169` |
| Additional victim or sweep target | `R3` hosting network, VLAN `30` | `10.30.0.101` |
| IDS | Monitoring VM | `10.99.0.65` |
| Dashboard and log storage | Management VM | `10.99.0.66` |

The exact container addresses may change. Always rediscover them before running
tests.

## 5. Prepare The Monitoring VM

Q3. How should the Monitoring VM be connected?

The Monitoring VM already uses `tap65` as an access port in VLAN `99` and uses
`R1` as its default gateway.

Expected Netplan file for the management interface:

```yaml
network:
  version: 2
  ethernets:
    enp0s1:
      dhcp4: false
      dhcp6: false
      addresses:
        - 10.99.0.65/24
        - fd14:ca46:3864:99::65/64
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
ip -br addr
ip route
ip -6 route
```

Expected result:

- `enp0s1` has `10.99.0.65/24`.
- The default IPv4 route points to `10.99.0.1`.
- The default IPv6 route points to `fd14:ca46:3864:99::1`.

Q4. Which base packages are useful on the Monitoring VM?

```console
sudo apt update
sudo apt install -y curl wget gnupg ca-certificates software-properties-common \
    jq tcpdump tshark ethtool net-tools iproute2 nmap openssh-client \
    prometheus-node-exporter prometheus-node-exporter-collectors
```

Q5. How do we confirm management reachability?

Run from the Monitoring VM:

```console
for host in 10.99.0.1 10.99.0.2 10.99.0.3 10.99.0.66; do
    ping -c 2 "$host"
done

curl -s http://10.99.0.66:3100/ready
curl -s http://10.99.0.66:9090/-/ready
```

Expected result:

- Pings to routers and the Management VM return `0%` packet loss.
- Loki returns `ready`.
- Prometheus returns ready output.

## 6. Confirm What The IDS Can Observe

Q6. Why is this step important?

An IDS can only alert on packets it receives. A reachable Monitoring VM is not
automatically a useful IDS. In the current topology, `tap65` is a management
access port, so it does not automatically receive routed container traffic.

Q7. What should be visible before mirroring?

On the Monitoring VM:

```console
sudo timeout 20 tcpdump -ni enp0s1 -c 20
```

Expected result:

- You see management traffic, ARP, IPv6 neighbor discovery, or packets to and
  from `10.99.0.65`.
- You should not expect to see full flows between `10.10.0.0/24` and
  `10.20.0.0/24` before mirroring.

Q8. How do we identify interfaces on the Monitoring VM?

```console
ip -br link
ip -br addr
```

Typical result with one NIC:

```text
enp0s1 UP 10.99.0.65/24 fd14:ca46:3864:99::65/64
```

Typical result with a second mirror NIC:

```text
enp0s1 UP 10.99.0.65/24 fd14:ca46:3864:99::65/64
enp0s2 UP
```

In the rest of this tutorial, the dedicated IDS capture interface is named
`enp0s2`. Adjust it if your VM uses another name.

## 7. Configure OVS Traffic Mirroring

Q9. Which capture design is recommended?

Use two interfaces on the Monitoring VM:

| Interface | TAP | Purpose |
| --- | --- | --- |
| `enp0s1` | `tap65` | Management VLAN `99` |
| `enp0s2` | `tap67` | Dedicated mirror receiver |

This keeps SSH, Alloy, Node Exporter, and package updates separate from the
IDS capture path.

Q10. How do we add `tap67` as the dedicated mirror port?

On the hypervisor, attach an additional NIC for the Monitoring VM to `tap67`.
Then add the TAP to the OVS bridge if it is not already present:

```console
sudo ovs-vsctl --may-exist add-port dsw-host tap67
sudo ovs-vsctl list port tap67
```

Set the sensor port up:

```console
sudo ip link set tap67 up
sudo ovs-vsctl set port tap67 vlan_mode=trunk trunks=10,20,30,440,441,442,99
```

The mirror output port should be dedicated to observation. Do not use it as the
Monitoring VM's management path.

Persistence note:

- Keep `tap65` as the documented management interface.
- Treat the mirror as runtime lab configuration unless you also update the
  hypervisor switch configuration and VM definition.
- Recheck the mirror after a VM restart or hypervisor reboot, because TAP
  interfaces can disappear and be recreated.

Q11. How do we mirror selected router VLANs to the IDS port?

On the hypervisor:

```console
sudo ovs-vsctl clear Bridge dsw-host mirrors

sudo ovs-vsctl \
  -- --id=@ids get Port tap67 \
  -- --id=@r1 get Port tap62 \
  -- --id=@r2 get Port tap63 \
  -- --id=@r3 get Port tap64 \
  -- --id=@m create Mirror name=ids-phase4 \
       select-src-port=@r1,@r2,@r3 \
       select-dst-port=@r1,@r2,@r3 \
       select-vlan=10,20,30,440,441,442 \
       output-port=@ids \
  -- set Bridge dsw-host mirrors=@m
```

Inspect the mirror:

```console
sudo ovs-vsctl list Bridge dsw-host
sudo ovs-vsctl list Mirror ids-phase4 || sudo ovs-vsctl list Mirror
```

Expected result:

- The bridge has one mirror named `ids-phase4`.
- `tap67` is the output port.
- `tap62`, `tap63`, and `tap64` are selected source and destination ports.
- VLANs `10`, `20`, `30`, `440`, `441`, and `442` are selected.

Q12. How do we disable the mirror after testing?

On the hypervisor:

```console
sudo ovs-vsctl clear Bridge dsw-host mirrors
```

Q13. How do we validate mirrored traffic?

On the Monitoring VM:

```console
IDS_IF=enp0s2

sudo ip link set "$IDS_IF" up
sudo ip link set "$IDS_IF" promisc on
sudo ethtool -K "$IDS_IF" gro off lro off tso off gso off 2>/dev/null || true

sudo timeout 30 tcpdump -eni "$IDS_IF" -c 50
```

Generate a harmless ping between two lab containers while `tcpdump` runs.

Expected result:

- `tcpdump` sees traffic that is not addressed to `10.99.0.65`.
- You see packets involving hosting or transit prefixes, for example
  `10.10.0.0/24`, `10.20.0.0/24`, `10.30.0.0/24`, or `10.44.0.0/29`.
- VLAN tags may or may not be visible depending on the OVS mirror behavior and
  guest NIC offload settings. Record what you observe.

## 8. Install Suricata

Q14. Which IDS should Phase 4 use?

Use Suricata first. It is enough for this phase because it provides packet
inspection, alerting, protocol metadata, EVE JSON logs, and practical rule
management. Zeek can be added later after Suricata is stable.

Q15. How do we install Suricata from Ubuntu packages?

On the Monitoring VM:

```console
sudo apt update
sudo apt install -y suricata suricata-update jq
suricata -V
suricata --build-info | head -n 40
```

Q16. How do we use the OISF stable PPA if the Ubuntu package is too old?

Use this option only if you need a newer stable Suricata package:

```console
sudo add-apt-repository -y ppa:oisf/suricata-stable
sudo apt update
sudo apt install -y suricata suricata-update jq
suricata -V
```

Q17. How do we confirm the service exists?

```console
systemctl status suricata --no-pager
systemctl cat suricata
```

Do not worry if the service is not fully configured yet. The next sections
define the capture interface, rule files, and local variables.

## 9. Configure Suricata For The Lab

Q18. Which interface should Suricata monitor?

Use the dedicated mirror interface:

```console
IDS_IF=enp0s2
ip -br link show "$IDS_IF"
```

Expected result:

- The interface exists.
- It is not the management interface used for SSH.

Q19. How do we set lab network variables?

Back up the Suricata configuration:

```console
sudo cp -a /etc/suricata/suricata.yaml /etc/suricata/suricata.yaml.bak.$(date +%Y%m%d%H%M%S)
```

Edit `/etc/suricata/suricata.yaml` and set the address variables:

```yaml
vars:
  address-groups:
    HOME_NET: "[10.10.0.0/24,10.20.0.0/24,10.30.0.0/24,10.44.0.0/29,10.44.1.0/29,10.44.2.0/29,10.99.0.0/24]"
    EXTERNAL_NET: "any"
```

For this lab, `EXTERNAL_NET` is `any` because the attacker and victim are both
inside the controlled lab. This makes local validation rules deterministic.

Q20. Which Suricata output should be enabled?

Keep EVE JSON enabled. In `/etc/suricata/suricata.yaml`, verify the EVE output
contains useful event types:

```yaml
outputs:
  - eve-log:
      enabled: yes
      filetype: regular
      filename: eve.json
      types:
        - alert
        - anomaly
        - flow
        - http
        - dns
        - tls
        - ssh
```

The exact YAML around this block may differ by package version. Keep the
package defaults where possible and only add missing event types.

Q21. How do we configure AF_PACKET capture?

In `/etc/suricata/suricata.yaml`, verify or add an `af-packet` block for the
mirror interface:

```yaml
af-packet:
  - interface: enp0s2
    cluster-id: 99
    cluster-type: cluster_flow
    defrag: yes
    use-mmap: yes
    tpacket-v3: yes
```

If your IDS interface is not `enp0s2`, replace the interface name.

Q22. How do we make the service use the IDS interface?

On Debian and Ubuntu packages, `/etc/default/suricata` is commonly used to
select live capture mode. Verify the file first:

```console
sudo cp -a /etc/default/suricata /etc/default/suricata.bak.$(date +%Y%m%d%H%M%S) 2>/dev/null || true
sudo sed -n '1,160p' /etc/default/suricata 2>/dev/null || true
```

If the file exists, set these values:

```console
IDS_IF=enp0s2

sudo sed -i 's/^RUN=.*/RUN=yes/' /etc/default/suricata 2>/dev/null || true
sudo sed -i 's/^LISTENMODE=.*/LISTENMODE=af-packet/' /etc/default/suricata 2>/dev/null || true
sudo sed -i "s/^IFACE=.*/IFACE=$IDS_IF/" /etc/default/suricata 2>/dev/null || true
```

If your package does not use `/etc/default/suricata`, inspect the unit:

```console
systemctl cat suricata
```

Then adapt the service according to the installed package. The required final
state is simple: Suricata must run with `/etc/suricata/suricata.yaml` and must
capture on the dedicated IDS interface.

Q23. How do we test the configuration?

```console
sudo suricata -T -c /etc/suricata/suricata.yaml -v
```

Expected result:

- The configuration test completes successfully.
- No fatal YAML, rule, or interface error is reported.

## 10. Add Local Detection Rules

Q24. Why add local rules if Suricata has community rules?

Community rules are useful, but a portfolio lab needs deterministic validation.
The local rules below are intentionally simple and trigger on lab-only
scenarios. They prove the pipeline without depending on external threat intel
or internet traffic.

Q25. How do we update the community rules?

```console
sudo suricata-update
sudo ls -lh /var/lib/suricata/rules/
```

Expected result:

- A generated rule file such as `/var/lib/suricata/rules/suricata.rules`
  exists.

Q26. How do we create Phase 4 local rules?

Create a local rule file:

```console
sudo install -d -m 0755 /var/lib/suricata/rules

sudo tee /var/lib/suricata/rules/local-phase4.rules >/dev/null <<'EOF'
alert tcp $EXTERNAL_NET any -> $HOME_NET any (msg:"LOCAL Phase4 TCP SYN scan candidate"; flags:S; detection_filter: track by_src, count 25, seconds 60; classtype:attempted-recon; sid:1000401; rev:1;)
alert tcp $EXTERNAL_NET any -> $HOME_NET 22 (msg:"LOCAL Phase4 SSH connection burst"; flags:S; detection_filter: track by_src, count 5, seconds 60; classtype:attempted-recon; sid:1000402; rev:1;)
alert http $EXTERNAL_NET any -> $HOME_NET any (msg:"LOCAL Phase4 suspicious HTTP user agent"; flow:to_server,established; http.user_agent; content:"phase4-suspicious-curl"; nocase; classtype:policy-violation; sid:1000403; rev:1;)
alert icmp $EXTERNAL_NET any -> $HOME_NET any (msg:"LOCAL Phase4 ICMP sweep candidate"; itype:8; detection_filter: track by_src, count 10, seconds 60; classtype:attempted-recon; sid:1000404; rev:1;)
EOF
```

Q27. How do we load the local rule file?

In `/etc/suricata/suricata.yaml`, verify the rule path and rule files:

```yaml
default-rule-path: /var/lib/suricata/rules

rule-files:
  - suricata.rules
  - local-phase4.rules
```

If your package uses `/etc/suricata/rules` instead, either keep the package
path and put `local-phase4.rules` there, or change `default-rule-path`
consistently. Do not split rule files across two paths without documenting it.

Validate:

```console
sudo suricata -T -c /etc/suricata/suricata.yaml -v
```

Expected result:

- The four local rules load without syntax errors.
- The configuration test reports no fatal error.

Q28. How do we restart Suricata?

```console
IDS_IF=enp0s2

sudo ip link set "$IDS_IF" up
sudo ip link set "$IDS_IF" promisc on
sudo ethtool -K "$IDS_IF" gro off lro off tso off gso off 2>/dev/null || true

sudo systemctl enable --now suricata
sudo systemctl restart suricata
sudo systemctl status suricata --no-pager
```

Expected result:

- `suricata.service` is active.
- `/var/log/suricata/eve.json` is created.
- `/var/log/suricata/fast.log` may be created when alerts fire.

## 11. Validate Live Capture

Q29. How do we check Suricata logs locally?

```console
sudo tail -n 80 /var/log/suricata/suricata.log
sudo ls -lh /var/log/suricata/
sudo jq -c 'select(.event_type=="stats")' /var/log/suricata/eve.json | tail -n 3
```

Expected result:

- Suricata starts without fatal errors.
- `eve.json` receives records.
- Stats or flow records appear after traffic crosses the mirror.

Q30. How do we generate harmless test traffic?

From a lab container or router, ping a known lab endpoint:

```console
ping -c 5 10.10.0.169
```

On the Monitoring VM:

```console
sudo jq -c 'select(.event_type=="flow") | {timestamp,src_ip,dest_ip,proto,event_type}' /var/log/suricata/eve.json | tail -n 10
```

Expected result:

- Flow records include lab addresses.
- If no flow record appears, troubleshoot mirroring before continuing.

Q31. How do we confirm local rules are loaded?

```console
sudo suricata --dump-config | grep -E "default-rule-path|local-phase4"
sudo grep -R "LOCAL Phase4" /var/lib/suricata/rules /etc/suricata/rules 2>/dev/null
```

Expected result:

- `local-phase4.rules` is present in the active rule path.
- The four local rules are visible.

## 12. Forward Suricata Logs To Loki

Q32. How should EVE JSON reach Loki?

Use the existing Grafana Alloy agent on the Monitoring VM. Keep the journal
pipeline from Phase 3 and add a file pipeline for `/var/log/suricata/eve.json`.

Q33. How do we allow Alloy to read EVE JSON?

On the Monitoring VM:

```console
sudo apt install -y acl
sudo usermod -aG adm alloy
sudo setfacl -m u:alloy:rx /var/log/suricata
sudo setfacl -m u:alloy:r /var/log/suricata/eve.json
sudo setfacl -d -m u:alloy:rx /var/log/suricata
sudo -u alloy test -r /var/log/suricata/eve.json && echo "Alloy can read eve.json"
```

If `eve.json` does not exist yet, restart Suricata and generate a small amount
of lab traffic.

Q34. How do we configure Alloy for Suricata EVE JSON?

Back up the existing config:

```console
sudo cp -a /etc/alloy/config.alloy /etc/alloy/config.alloy.bak.$(date +%Y%m%d%H%M%S)
```

Append the following blocks to `/etc/alloy/config.alloy` on the Monitoring VM.
Keep the existing `loki.write "lab"` block from Phase 3.

```alloy
local.file_match "suricata_eve" {
  path_targets = [
    {
      __path__ = "/var/log/suricata/eve.json",
      job      = "suricata-eve",
      lab      = "network-security-lab",
      node     = "monitoring",
    },
  ]
}

loki.source.file "suricata_eve" {
  targets    = local.file_match.suricata_eve.targets
  forward_to = [loki.process.suricata_eve.receiver]
}

loki.process "suricata_eve" {
  stage.json {
    expressions = {
      event_type = "event_type",
    }
  }

  stage.labels {
    values = {
      event_type = "",
    }
  }

  forward_to = [loki.write.lab.receiver]
}
```

Restart Alloy:

```console
sudo systemctl restart alloy
sudo systemctl status alloy --no-pager
journalctl -u alloy -n 80 --no-pager
```

Expected result:

- Alloy starts without syntax errors.
- No permission error appears for `/var/log/suricata/eve.json`.
- No connection error appears for `10.99.0.66:3100`.

Q35. How do we verify Suricata logs in Loki?

From the Management VM:

```console
curl -G -s "http://10.99.0.66:3100/loki/api/v1/label/job/values" | jq
curl -G -s "http://10.99.0.66:3100/loki/api/v1/label/event_type/values" | jq
```

Expected result:

- `suricata-eve` appears as a Loki job.
- Event types such as `flow`, `stats`, or `alert` appear after traffic.

Useful LogQL queries:

```logql
{job="suricata-eve", node="monitoring"}
```

```logql
{job="suricata-eve", node="monitoring", event_type="alert"}
```

```logql
{job="suricata-eve", node="monitoring"} | json | event_type="alert"
```

```logql
{job="suricata-eve", node="monitoring"} | json | alert_signature =~ "LOCAL Phase4.*"
```

## 13. Add Suricata Metrics With The Textfile Collector

Loki stores security event details. Prometheus is useful for simple health and
counting checks: Is Suricata running? Is EVE JSON updating? Did an alert appear
recently?

Q36. Which custom metrics should the Monitoring VM expose?

| Metric | Meaning |
| --- | --- |
| `suricata_service_active` | `1` when `suricata.service` is active, else `0` |
| `suricata_eve_alert_events_total` | Count of alert records in the current EVE file |
| `suricata_eve_last_alert_unixtime` | Unix timestamp of the last alert, or `0` |
| `suricata_eve_last_success_unixtime` | Last successful textfile collector run |

Q37. How do we create the Suricata textfile script?

Run on the Monitoring VM:

```console
sudo install -d -m 0755 /usr/local/lib/prometheus
sudo install -d -m 0755 /var/lib/prometheus/node-exporter

sudo tee /usr/local/lib/prometheus/suricata_textfile.sh >/dev/null <<'EOF'
#!/bin/sh
set -eu

HOST="$(hostname -s)"
DIR="/var/lib/prometheus/node-exporter"
EVE="/var/log/suricata/eve.json"
TMP="$DIR/suricata.prom.$$"
OUT="$DIR/suricata.prom"

if systemctl is-active --quiet suricata.service; then
    SURICATA_ACTIVE=1
else
    SURICATA_ACTIVE=0
fi

if [ -r "$EVE" ]; then
    ALERTS_TOTAL="$(jq -c 'select(.event_type=="alert")' "$EVE" 2>/dev/null | wc -l | awk '{print $1}')"
    LAST_ALERT_TS="$(jq -r 'select(.event_type=="alert") | .timestamp' "$EVE" 2>/dev/null | tail -n 1)"
else
    ALERTS_TOTAL=0
    LAST_ALERT_TS=""
fi

if [ -n "${LAST_ALERT_TS:-}" ] && [ "$LAST_ALERT_TS" != "null" ]; then
    LAST_ALERT_UNIX="$(date -d "$LAST_ALERT_TS" +%s 2>/dev/null || echo 0)"
else
    LAST_ALERT_UNIX=0
fi

cat > "$TMP" <<METRICS
# HELP suricata_service_active 1 if suricata.service is active, otherwise 0.
# TYPE suricata_service_active gauge
suricata_service_active{node="$HOST"} $SURICATA_ACTIVE
# HELP suricata_eve_alert_events_total Number of alert records in the current Suricata EVE file.
# TYPE suricata_eve_alert_events_total counter
suricata_eve_alert_events_total{node="$HOST"} $ALERTS_TOTAL
# HELP suricata_eve_last_alert_unixtime Unix timestamp of the last Suricata alert.
# TYPE suricata_eve_last_alert_unixtime gauge
suricata_eve_last_alert_unixtime{node="$HOST"} $LAST_ALERT_UNIX
# HELP suricata_eve_last_success_unixtime Unix timestamp of the last successful Suricata textfile collection.
# TYPE suricata_eve_last_success_unixtime gauge
suricata_eve_last_success_unixtime{node="$HOST"} $(date +%s)
METRICS

chmod 0644 "$TMP"
mv "$TMP" "$OUT"
EOF

sudo chmod 0755 /usr/local/lib/prometheus/suricata_textfile.sh
sudo /usr/local/lib/prometheus/suricata_textfile.sh
cat /var/lib/prometheus/node-exporter/suricata.prom
```

Q38. How do we run this script continuously?

Create a systemd timer on the Monitoring VM:

```console
sudo tee /etc/systemd/system/suricata-textfile.service >/dev/null <<'EOF'
[Unit]
Description=Write Suricata metrics for Prometheus Node Exporter

[Service]
Type=oneshot
ExecStart=/usr/local/lib/prometheus/suricata_textfile.sh
EOF

sudo tee /etc/systemd/system/suricata-textfile.timer >/dev/null <<'EOF'
[Unit]
Description=Refresh Suricata textfile metrics

[Timer]
OnBootSec=30s
OnUnitActiveSec=15s
AccuracySec=1s

[Install]
WantedBy=timers.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable --now suricata-textfile.timer
systemctl list-timers suricata-textfile.timer
```

Q39. How do we confirm Prometheus can see the custom metrics?

On the Monitoring VM:

```console
curl -s http://127.0.0.1:9100/metrics | grep '^suricata_'
```

From the Management VM:

```console
curl -s "http://10.99.0.65:9100/metrics" | grep '^suricata_'
```

PromQL:

```promql
suricata_service_active
```

```promql
suricata_eve_alert_events_total
```

```promql
time() - suricata_eve_last_success_unixtime
```

Expected result:

- `suricata_service_active` equals `1`.
- The textfile collector age stays below `60` seconds.
- The alert counter increases after Phase 4 scenarios.

## 14. Add Prometheus Alert Rules

Q40. Which Phase 4 alerts should Prometheus know?

Add these rules to `/etc/prometheus/rules/network-security-lab.yml` on the
Management VM, inside the existing `network-security-lab` group.

```yaml
      - alert: SuricataServiceDown
        expr: suricata_service_active == 0
        for: 30s
        labels:
          severity: critical
          phase: phase-4-security
          dashboard: security
        annotations:
          summary: "Suricata is down on {{ $labels.node }}"
          description: "suricata.service is not active on the IDS sensor."

      - alert: SuricataTextfileStale
        expr: time() - suricata_eve_last_success_unixtime > 60
        for: 1m
        labels:
          severity: warning
          phase: phase-4-security
          dashboard: security
        annotations:
          summary: "Suricata textfile metrics are stale on {{ $labels.node }}"
          description: "The Suricata textfile collector has not updated recently."

      - alert: SuricataAlertObserved
        expr: increase(suricata_eve_alert_events_total[5m]) > 0
        for: 0m
        labels:
          severity: info
          phase: phase-4-security
          dashboard: security
        annotations:
          summary: "Suricata alert observed on {{ $labels.node }}"
          description: "Suricata recorded at least one alert in the last five minutes."
```

Validate and reload:

```console
promtool check rules /etc/prometheus/rules/network-security-lab.yml
sudo systemctl reload prometheus || sudo systemctl restart prometheus
curl -s http://127.0.0.1:9090/api/v1/rules | jq '.data.groups[].rules[] | select(.name|test("Suricata")) | {name,health,type}'
```

Expected result:

- Prometheus accepts the rule file.
- The three Suricata rules appear in the Prometheus API.

## 15. Build The Grafana Security Dashboard

Create a Grafana folder named `Security`.

Q41. Which panels should the Security dashboard contain?

| Panel | Data source | Query |
| --- | --- | --- |
| Suricata service state | Prometheus | `suricata_service_active` |
| Suricata alert counter | Prometheus | `suricata_eve_alert_events_total` |
| Recent alert activity | Prometheus | `increase(suricata_eve_alert_events_total[5m])` |
| Textfile collector age | Prometheus | `time() - suricata_eve_last_success_unixtime` |
| All Suricata EVE logs | Loki | `{job="suricata-eve", node="monitoring"}` |
| Suricata alerts | Loki | `{job="suricata-eve", node="monitoring", event_type="alert"}` |
| Phase 4 local rules | Loki | `{job="suricata-eve", node="monitoring"} | json | alert_signature =~ "LOCAL Phase4.*"` |
| Top source IPs | Loki | `{job="suricata-eve", event_type="alert"} | json` with Grafana transformations |
| Nmap incident | Loki | `{job="suricata-eve"} | json | alert_signature =~ ".*SYN scan.*|.*Nmap.*"` |
| SSH burst incident | Loki | `{job="suricata-eve"} | json | alert_signature =~ ".*SSH connection burst.*"` |

Q42. Which dashboard design choices make evidence easier to read?

Use:

- Time range `Last 15 minutes` during live scenarios.
- Time range `Last 6 hours` when preparing the proof report.
- One row for IDS health.
- One row for alerts.
- One row for raw EVE JSON logs.
- A visible panel title for each scenario.
- The same timestamp window in Grafana, terminal logs, and incident reports.

Q43. Which Grafana Explore queries should be bookmarked?

```logql
{job="suricata-eve", event_type="alert"}
```

```logql
{job="suricata-eve"} | json | src_ip="10.20.0.156"
```

```logql
{job="suricata-eve"} | json | dest_ip="10.10.0.169"
```

```logql
{job="suricata-eve"} | json | alert_signature =~ "LOCAL Phase4.*"
```

```logql
{job="systemd-journal", node="monitoring", unit="suricata.service"}
```

## 16. Prepare Attacker And Victim Endpoints

Q44. How do we rediscover container addresses?

Run on each router:

```console
incus list
```

Or query only names and addresses:

```console
incus list --format csv -c n4s
```

Record the addresses:

| Router | Container | Role | IPv4 |
| --- | --- | --- | --- |
| `R2` | `c0` | Attacker | `10.20.0.x` |
| `R1` | `c0` | Victim web/SSH | `10.10.0.x` |
| `R3` | `c0` | Optional extra target | `10.30.0.x` |

Q45. How do we set variables before each scenario?

On the attacker router or in your notes:

```console
ATTACKER_ROUTER=R2
ATTACKER_CONTAINER=c0
ATTACKER_IP=10.20.0.156
VICTIM_ROUTER=R1
VICTIM_CONTAINER=c0
VICTIM_IP=10.10.0.169

echo "ATTACKER_IP=$ATTACKER_IP"
echo "VICTIM_IP=$VICTIM_IP"
```

Replace the example IPs with the current addresses from `incus list`.
Set the same `ATTACKER_IP` and `VICTIM_IP` variables in the Monitoring VM
terminal before running `tcpdump` or local evidence commands.

Q46. How do we install attacker tools?

On the attacker container:

```console
incus exec "$ATTACKER_CONTAINER" -- bash -lc 'apt update && apt install -y nmap curl openssh-client iputils-ping netcat-openbsd'
```

Q47. How do we prepare the victim service?

On the victim container:

```console
incus exec "$VICTIM_CONTAINER" -- bash -lc 'apt update && apt install -y python3 openssh-server iproute2 procps'
incus exec "$VICTIM_CONTAINER" -- bash -lc 'systemctl enable --now ssh 2>/dev/null || service ssh start'
incus exec "$VICTIM_CONTAINER" -- bash -lc 'mkdir -p /tmp/phase4-web && printf "phase4 victim service\n" >/tmp/phase4-web/index.html'
incus exec "$VICTIM_CONTAINER" -- bash -lc 'cd /tmp/phase4-web && nohup python3 -m http.server 80 >/tmp/phase4-http.log 2>&1 &'
incus exec "$VICTIM_CONTAINER" -- bash -lc 'ss -ltnp'
```

Expected result:

- Port `22/tcp` is listening for SSH.
- Port `80/tcp` is listening for the Python HTTP server.

Q48. How do we validate normal connectivity before attacks?

From the attacker container:

```console
incus exec "$ATTACKER_CONTAINER" -- ping -c 3 "$VICTIM_IP"
incus exec "$ATTACKER_CONTAINER" -- curl -s "http://$VICTIM_IP/"
```

Expected result:

- Ping succeeds.
- HTTP returns `phase4 victim service`.
- Suricata records flow and HTTP metadata.

## 17. Scenario 1 - Nmap Reconnaissance Scan

Q49. What is the purpose of this scenario?

This scenario detects reconnaissance from one lab container toward another. It
should trigger the local TCP SYN scan rule and may also trigger community Nmap
rules depending on the installed ruleset.

Q50. How do we start evidence capture?

On the Monitoring VM:

```console
IDS_IF=enp0s2
EVIDENCE_DIR="$HOME/phase4-evidence"
ATTACKER_IP=10.20.0.156
VICTIM_IP=10.10.0.169
mkdir -p "$EVIDENCE_DIR"

echo "ATTACKER_IP=$ATTACKER_IP"
echo "VICTIM_IP=$VICTIM_IP"
date -Ins | tee "$EVIDENCE_DIR/nmap-start.txt"
sudo timeout 120 tcpdump -i "$IDS_IF" -nn -s 0 \
    -w "$EVIDENCE_DIR/phase4-nmap-$(date +%Y%m%d%H%M%S).pcap" \
    host "$ATTACKER_IP" or host "$VICTIM_IP"
```

Keep this running while the scan is executed.

Q51. How do we run the scan?

From the attacker router:

```console
date -Ins
incus exec "$ATTACKER_CONTAINER" -- nmap -Pn -sS -sV -p 1-1000 --reason "$VICTIM_IP"
date -Ins
```

If SYN scan is not allowed in the container, use a TCP connect scan:

```console
incus exec "$ATTACKER_CONTAINER" -- nmap -Pn -sT -sV -p 1-1000 --reason "$VICTIM_IP"
```

Q52. How do we validate the alert locally?

On the Monitoring VM:

```console
sudo jq -c 'select(.event_type=="alert") | {timestamp,src_ip,dest_ip,signature:.alert.signature,severity:.alert.severity}' /var/log/suricata/eve.json | tail -n 20
```

Expected alert:

```text
LOCAL Phase4 TCP SYN scan candidate
```

Q53. How do we validate the alert in Loki?

In Grafana Explore:

```logql
{job="suricata-eve", event_type="alert"} | json | alert_signature =~ ".*SYN scan.*|.*Nmap.*"
```

Expected result:

- The alert appears with the attacker IP as `src_ip`.
- The victim IP appears as `dest_ip`.
- The timestamp matches the terminal test window.

Q54. What evidence should be saved?

| Evidence | Suggested filename |
| --- | --- |
| Nmap command output | `phase4-nmap-command.txt` |
| Suricata alert in Grafana | `phase4-suricata-nmap-alert.png` |
| Loki alert query | `phase4-loki-nmap-alert.png` |
| PCAP | `phase4-nmap-YYYYmmddHHMMSS.pcap` |
| Prometheus alert counter | `phase4-prometheus-suricata-alert-counter.png` |

## 18. Scenario 2 - SSH Connection Burst

Q55. What is the purpose of this scenario?

This scenario simulates repeated SSH connection attempts against a lab service.
It does not need valid credentials. The goal is to produce a detectable burst
of SSH connection attempts from one lab source.

Q56. How do we run the scenario?

From the attacker router:

```console
date -Ins
incus exec "$ATTACKER_CONTAINER" -- env VICTIM_IP="$VICTIM_IP" bash -lc '
for i in $(seq 1 12); do
  ssh -o BatchMode=yes -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null \
      -o ConnectTimeout=2 "invalid${i}@${VICTIM_IP}" true </dev/null 2>/dev/null || true
done
'
date -Ins
```

Q57. How do we validate the alert locally?

On the Monitoring VM:

```console
sudo jq -c 'select(.event_type=="alert") | select(.alert.signature|test("SSH connection burst")) | {timestamp,src_ip,dest_ip,signature:.alert.signature}' /var/log/suricata/eve.json | tail -n 10
```

Expected alert:

```text
LOCAL Phase4 SSH connection burst
```

Q58. Which Loki query should show the incident?

```logql
{job="suricata-eve", event_type="alert"} | json | alert_signature =~ ".*SSH connection burst.*"
```

Useful supporting query:

```logql
{job="suricata-eve"} | json | event_type="ssh"
```

Q59. What evidence should be saved?

| Evidence | Suggested filename |
| --- | --- |
| SSH burst terminal output | `phase4-ssh-burst-command.txt` |
| Suricata SSH alert in Grafana | `phase4-suricata-ssh-burst-alert.png` |
| Loki SSH records | `phase4-loki-ssh-events.png` |
| Victim SSH logs if useful | `phase4-victim-ssh-logs.txt` |

On the victim container, SSH service logs can be useful if systemd or syslog is
available:

```console
incus exec "$VICTIM_CONTAINER" -- bash -lc 'journalctl -u ssh -n 80 --no-pager 2>/dev/null || tail -n 80 /var/log/auth.log 2>/dev/null || true'
```

## 19. Scenario 3 - Suspicious HTTP Marker

Q60. What is the purpose of this scenario?

This scenario proves that Suricata can parse HTTP and alert on a controlled
marker. The marker is harmless and intentionally specific:
`phase4-suspicious-curl`.

Q61. How do we run the scenario?

From the attacker router:

```console
date -Ins
incus exec "$ATTACKER_CONTAINER" -- curl -A "phase4-suspicious-curl" -s "http://$VICTIM_IP/phase4-test" || true
date -Ins
```

Q62. How do we validate the alert locally?

On the Monitoring VM:

```console
sudo jq -c 'select(.event_type=="alert") | select(.alert.signature|test("suspicious HTTP user agent")) | {timestamp,src_ip,dest_ip,signature:.alert.signature}' /var/log/suricata/eve.json | tail -n 10
```

Expected alert:

```text
LOCAL Phase4 suspicious HTTP user agent
```

Q63. Which Loki queries should show the incident?

```logql
{job="suricata-eve", event_type="alert"} | json | alert_signature =~ ".*suspicious HTTP user agent.*"
```

```logql
{job="suricata-eve"} |= "phase4-suspicious-curl"
```

If Grafana extracts nested Suricata HTTP fields in your Loki version, this
format is also useful:

```logql
{job="suricata-eve"} | json | event_type="http" | line_format "{{.timestamp}} {{.src_ip}} -> {{.dest_ip}} {{.http_http_user_agent}} {{.http_url}}"
```

Q64. What evidence should be saved?

| Evidence | Suggested filename |
| --- | --- |
| HTTP marker command | `phase4-http-marker-command.txt` |
| Suricata HTTP alert | `phase4-suricata-http-marker-alert.png` |
| Loki HTTP metadata | `phase4-loki-http-event.png` |
| Victim HTTP service log | `phase4-victim-http-log.txt` |

## 20. Scenario 4 - ICMP Sweep

Q65. What is the purpose of this scenario?

This scenario simulates a simple host discovery sweep inside one lab subnet.
It should trigger the local ICMP sweep rule if enough echo requests cross the
mirror during the threshold window.

Q66. How do we run the scenario?

From the attacker router:

```console
date -Ins
incus exec "$ATTACKER_CONTAINER" -- bash -lc '
for ip in $(seq 1 30); do
  ping -c 1 -W 1 10.10.0.$ip >/dev/null 2>&1 || true
done
'
date -Ins
```

Q67. How do we validate the alert?

On the Monitoring VM:

```console
sudo jq -c 'select(.event_type=="alert") | select(.alert.signature|test("ICMP sweep")) | {timestamp,src_ip,dest_ip,signature:.alert.signature}' /var/log/suricata/eve.json | tail -n 10
```

Grafana Explore:

```logql
{job="suricata-eve", event_type="alert"} | json | alert_signature =~ ".*ICMP sweep.*"
```

Expected alert:

```text
LOCAL Phase4 ICMP sweep candidate
```

Q68. What evidence should be saved?

| Evidence | Suggested filename |
| --- | --- |
| ICMP sweep command output | `phase4-icmp-sweep-command.txt` |
| Suricata ICMP alert | `phase4-suricata-icmp-sweep-alert.png` |
| Loki ICMP alert query | `phase4-loki-icmp-sweep-alert.png` |

## 21. Save Evidence

Q69. What screenshots should be saved?

Save screenshots under `screenshots/phase4/`:

| Evidence | Suggested filename |
| --- | --- |
| Suricata service healthy | `phase4-suricata-service-healthy.png` |
| Loki Suricata job visible | `phase4-loki-suricata-job.png` |
| Security dashboard baseline | `phase4-security-dashboard-baseline.png` |
| Nmap alert | `phase4-suricata-nmap-alert.png` |
| SSH burst alert | `phase4-suricata-ssh-burst-alert.png` |
| HTTP marker alert | `phase4-suricata-http-marker-alert.png` |
| ICMP sweep alert | `phase4-suricata-icmp-sweep-alert.png` |
| Prometheus Suricata alert counter | `phase4-prometheus-suricata-alert-counter.png` |
| Prometheus Suricata alerts | `phase4-prometheus-suricata-alerts.png` |

Q70. Which command outputs should be copied into the proof report?

Use `docs/proofs-phase4.md` and include:

```console
systemctl status suricata alloy prometheus-node-exporter suricata-textfile.timer --no-pager
```

```console
suricata -V
sudo suricata -T -c /etc/suricata/suricata.yaml -v
```

```console
sudo jq -c 'select(.event_type=="alert") | {timestamp,src_ip,dest_ip,signature:.alert.signature,severity:.alert.severity}' /var/log/suricata/eve.json | tail -n 30
```

```console
curl -G -s "http://10.99.0.66:3100/loki/api/v1/query_range" \
    --data-urlencode 'query={job="suricata-eve", event_type="alert"}' \
    --data-urlencode 'limit=20' | jq
```

```console
curl -s "http://10.99.0.66:9090/api/v1/query" \
    --data-urlencode 'query=suricata_service_active' | jq
```

```console
curl -s "http://10.99.0.66:9090/api/v1/query" \
    --data-urlencode 'query=suricata_eve_alert_events_total' | jq
```

On the hypervisor:

```console
sudo ovs-vsctl list Mirror ids-phase4 || sudo ovs-vsctl list Mirror
```

Q71. Which configuration files should be backed up?

Back up these files into a controlled evidence folder:

| Node | Files |
| --- | --- |
| `monitoring` | `/etc/suricata/suricata.yaml` |
| `monitoring` | `/var/lib/suricata/rules/local-phase4.rules` |
| `monitoring` | `/etc/default/suricata` if used |
| `monitoring` | `/etc/alloy/config.alloy` |
| `monitoring` | `/usr/local/lib/prometheus/suricata_textfile.sh` |
| `monitoring` | `/etc/systemd/system/suricata-textfile.service` |
| `monitoring` | `/etc/systemd/system/suricata-textfile.timer` |
| `management` | `/etc/prometheus/rules/network-security-lab.yml` |

Do not commit passwords, SSH private keys, Grafana session cookies, or large
PCAP files unless you intentionally sanitize and document them.

## 22. Write Incident Reports

Q72. What incidents are required for Phase 4?

At minimum, document two incidents:

1. Nmap reconnaissance scan.
2. SSH connection burst or suspicious HTTP marker.

Q73. What incident report structure should be used?

Create `docs/proofs-phase4.md` or a separate incident file under
`security/phase4/incidents/`.

Template:

```markdown
## Incident: Nmap Reconnaissance Scan

Status: validated

Time window:

- Start: 2026-mm-ddThh:mm:ss+offset
- End: 2026-mm-ddThh:mm:ss+offset

Scope:

- Attacker: R2 container c0, 10.20.0.x
- Victim: R1 container c0, 10.10.0.x
- IDS: monitoring, 10.99.0.65

Scenario:

Short description of the command and why it is safe inside the lab.

Detection:

- Suricata signature:
- Suricata event type:
- Loki query:
- Prometheus metric:

Evidence:

- Screenshot:
- Command output:
- PCAP:
- Relevant log excerpt:

Impact:

What the activity means in a real network.

Response:

What an operator should check next.

Limitations:

What this test does not prove.

Conclusion:

One or two sentences summarizing the result.
```

Q74. What should the conclusion say?

Keep it factual:

- The IDS observed the controlled flow.
- Suricata generated the expected alert.
- Loki stored the event with useful fields.
- Grafana displayed the event in the selected time window.
- Prometheus exposed health and alert-count metrics.
- The test stayed inside documented lab networks.

## 23. Tune Rules And Reduce Noise

Q75. When should rules be tuned?

Tune only after the baseline works. First prove that Suricata sees traffic,
loads rules, writes EVE JSON, forwards logs, and displays alerts. Then reduce
noise.

Q76. How can local rules be disabled temporarily?

Comment a rule in `/var/lib/suricata/rules/local-phase4.rules`, then test and
restart:

```console
sudo suricata -T -c /etc/suricata/suricata.yaml -v
sudo systemctl restart suricata
```

Q77. How can noisy community rules be disabled?

Use Suricata Update filter files instead of editing generated rules directly.
For example:

```console
sudo tee -a /etc/suricata/disable.conf >/dev/null <<'EOF'
# Example only. Replace SID with a confirmed noisy rule.
1:2000000
EOF

sudo suricata-update
sudo suricata -T -c /etc/suricata/suricata.yaml -v
sudo systemctl restart suricata
```

Record every disabled rule and the reason in the proof report.

Q78. What should not be tuned away?

Do not suppress the Phase 4 local validation rules until the proof report is
complete. They are the deterministic evidence path for this lab.

## 24. Troubleshooting

### Suricata Sees No Packets

Q79. What should be checked first?

On the Monitoring VM:

```console
IDS_IF=enp0s2
ip -br link show "$IDS_IF"
sudo ip link set "$IDS_IF" promisc on
sudo timeout 30 tcpdump -eni "$IDS_IF" -c 30
```

On the hypervisor:

```console
sudo ovs-vsctl list Bridge dsw-host
sudo ovs-vsctl list Mirror ids-phase4 || sudo ovs-vsctl list Mirror
sudo ovs-vsctl list port tap67
```

Common causes:

- The Monitoring VM has only the management NIC.
- The OVS mirror was not configured.
- The mirror output port is wrong.
- The wrong guest interface was given to Suricata.
- No test traffic crossed the selected VLANs.
- NIC offloads hide details from packet capture.

### Suricata Fails To Start

Q80. What should be checked?

```console
sudo suricata -T -c /etc/suricata/suricata.yaml -v
journalctl -u suricata -n 100 --no-pager
sudo tail -n 100 /var/log/suricata/suricata.log
```

Common causes:

- YAML indentation error.
- Rule syntax error.
- Wrong rule path.
- Wrong interface name.
- Interface is down.
- Another Suricata process is already running.

### No Alerts Appear

Q81. What should be checked?

```console
sudo grep -R "LOCAL Phase4" /var/lib/suricata/rules /etc/suricata/rules 2>/dev/null
sudo suricata -T -c /etc/suricata/suricata.yaml -v
sudo jq -c 'select(.event_type=="flow") | {src_ip,dest_ip,proto}' /var/log/suricata/eve.json | tail
sudo jq -c 'select(.event_type=="alert")' /var/log/suricata/eve.json | tail
```

Common causes:

- Suricata sees flows but not the test traffic direction.
- `HOME_NET` does not include the victim subnet.
- `local-phase4.rules` is not listed in `rule-files`.
- The scan threshold was not reached.
- The traffic did not cross the mirrored OVS ports.

### Loki Does Not Receive Suricata Logs

Q82. What should be checked?

On the Monitoring VM:

```console
sudo -u alloy test -r /var/log/suricata/eve.json && echo readable
sudo systemctl status alloy --no-pager
journalctl -u alloy -n 100 --no-pager
```

On the Management VM:

```console
curl -s http://10.99.0.66:3100/ready
curl -G -s "http://10.99.0.66:3100/loki/api/v1/label/job/values" | jq
```

Common causes:

- Alloy lacks file permissions.
- The `local.file_match` path is wrong.
- The Alloy config has a syntax error.
- Loki is not reachable from the Monitoring VM.
- The event time range in Grafana is too narrow.

### Prometheus Metrics Are Missing

Q83. What should be checked?

On the Monitoring VM:

```console
sudo systemctl status prometheus-node-exporter suricata-textfile.timer --no-pager
sudo /usr/local/lib/prometheus/suricata_textfile.sh
cat /var/lib/prometheus/node-exporter/suricata.prom
curl -s http://127.0.0.1:9100/metrics | grep '^suricata_'
```

On the Management VM:

```console
curl -s "http://10.99.0.65:9100/metrics" | grep '^suricata_'
curl -s http://127.0.0.1:9090/api/v1/targets | jq '.data.activeTargets[] | select(.labels.node=="monitoring") | {health:.health,lastError:.lastError}'
```

Common causes:

- Node Exporter is down.
- The textfile directory is wrong.
- The script cannot read `eve.json`.
- Prometheus is scraping an old target address.

### Grafana Shows No Data

Q84. What should be checked?

```console
curl -s http://127.0.0.1:3000/api/health
curl -s http://127.0.0.1:9090/-/ready
curl -s http://127.0.0.1:3100/ready
```

In Grafana:

- Confirm the dashboard time window includes the test.
- Confirm the Prometheus and Loki data sources still pass `Save & test`.
- Query raw Loki logs before adding filters.
- Query raw Prometheus metrics before building panels.

## 25. Conclusion

This Phase 4 lab adds a reproducible security monitoring layer to the existing
OSPF and observability platform.

The exit criteria are satisfied when:

- The Monitoring VM runs Suricata on a real capture interface.
- The IDS can observe documented lab traffic through an OVS mirror.
- Suricata writes EVE JSON events and local validation alerts.
- Alloy forwards Suricata logs to Loki.
- Prometheus shows Suricata service and alert metrics.
- Grafana displays IDS health, alert activity, and raw EVE events.
- At least two controlled incidents are documented with evidence.
- All simulations stay inside the network security lab.

The most important limitation to document is visibility. If the mirror does not
copy the right VLANs or ports, the IDS cannot detect the scenario. Phase 4 is
therefore not only a Suricata exercise; it is also a validation of the capture
path.

## 26. References

- InetDoc OSPF practical lab style and structure: <https://inetdoc.net/travaux_pratiques/interco_05.ospf/>
- Suricata quickstart: <https://docs.suricata.io/en/latest/quickstart.html>
- Suricata EVE JSON output: <https://docs.suricata.io/en/latest/output/eve/eve-json-output.html>
- Suricata EVE JSON format: <https://docs.suricata.io/en/latest/output/eve/eve-json-format.html>
- Suricata rule management with `suricata-update`: <https://docs.suricata.io/en/latest/rule-management/suricata-update.html>
- Suricata rules format: <https://docs.suricata.io/en/latest/rules/intro.html>
- Open vSwitch mirroring FAQ: <https://docs.openvswitch.org/en/latest/faq/configuration/>
- Grafana Alloy `loki.source.file`: <https://grafana.com/docs/alloy/latest/reference/components/loki/loki.source.file/>
- Grafana Alloy `loki.process`: <https://grafana.com/docs/alloy/latest/reference/components/loki/loki.process/>
- Grafana Alloy log collection tutorial: <https://grafana.com/docs/alloy/latest/tutorials/send-logs-to-loki/>
