 etu@management  ~  sudo cat /etc/netplan/enp0s1.yaml
[sudo] password for etu: 
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
 etu@management  ~  


 etu@management  ~  ip addr show enp0s1
2: enp0s1: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc mq state UP group default qlen 1000
    link/ether b8:ad:ca:fe:00:42 brd ff:ff:ff:ff:ff:ff
    altname enxb8adcafe0042
    inet 10.99.0.66/24 brd 10.99.0.255 scope global enp0s1
       valid_lft forever preferred_lft forever
    inet6 fd14:ca46:3864:99::66/64 scope global 
       valid_lft forever preferred_lft forever
    inet6 fe80::baad:caff:fefe:42/64 scope link proto kernel_ll 
       valid_lft forever preferred_lft forever
 etu@management  ~  ip route
default via 10.99.0.1 dev enp0s1 proto static 
10.99.0.0/24 dev enp0s1 proto kernel scope link src 10.99.0.66 
 etu@management  ~  ip -6 route
fd14:ca46:3864:99::/64 dev enp0s1 proto kernel metric 256 pref medium
fe80::/64 dev enp0s1 proto kernel metric 256 pref medium
default via fd14:ca46:3864:99::1 dev enp0s1 proto static metric 1024 pref medium
 etu@management  ~  



 etu@management  ~  for host in 10.99.0.1 10.99.0.2 10.99.0.3 10.99.0.65; do
    ping -c 2 "$host"
done
PING 10.99.0.1 (10.99.0.1) 56(84) bytes of data.
64 bytes from 10.99.0.1: icmp_seq=1 ttl=64 time=0.856 ms
64 bytes from 10.99.0.1: icmp_seq=2 ttl=64 time=0.876 ms

--- 10.99.0.1 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1003ms
rtt min/avg/max/mdev = 0.856/0.866/0.876/0.010 ms
PING 10.99.0.2 (10.99.0.2) 56(84) bytes of data.
64 bytes from 10.99.0.2: icmp_seq=1 ttl=64 time=2.49 ms
64 bytes from 10.99.0.2: icmp_seq=2 ttl=64 time=0.897 ms

--- 10.99.0.2 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1002ms
rtt min/avg/max/mdev = 0.897/1.692/2.488/0.795 ms
PING 10.99.0.3 (10.99.0.3) 56(84) bytes of data.
64 bytes from 10.99.0.3: icmp_seq=1 ttl=64 time=2.08 ms
64 bytes from 10.99.0.3: icmp_seq=2 ttl=64 time=0.877 ms

--- 10.99.0.3 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1001ms
rtt min/avg/max/mdev = 0.877/1.478/2.079/0.601 ms
PING 10.99.0.65 (10.99.0.65) 56(84) bytes of data.
64 bytes from 10.99.0.65: icmp_seq=1 ttl=64 time=2.66 ms
64 bytes from 10.99.0.65: icmp_seq=2 ttl=64 time=0.854 ms

--- 10.99.0.65 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1002ms
rtt min/avg/max/mdev = 0.854/1.758/2.663/0.904 ms
 etu@management  ~  


  etu@management  ~  for host in fd14:ca46:3864:99::1 fd14:ca46:3864:99::2 fd14:ca46:3864:99::3 fd14:ca46:3864:99::65; do
    ping -c 2 "$host"
done
PING fd14:ca46:3864:99::1 (fd14:ca46:3864:99::1) 56 data bytes
64 bytes from fd14:ca46:3864:99::1: icmp_seq=1 ttl=64 time=3.27 ms
64 bytes from fd14:ca46:3864:99::1: icmp_seq=2 ttl=64 time=0.872 ms

--- fd14:ca46:3864:99::1 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1002ms
rtt min/avg/max/mdev = 0.872/2.071/3.270/1.199 ms
PING fd14:ca46:3864:99::2 (fd14:ca46:3864:99::2) 56 data bytes
64 bytes from fd14:ca46:3864:99::2: icmp_seq=1 ttl=64 time=3.70 ms
64 bytes from fd14:ca46:3864:99::2: icmp_seq=2 ttl=64 time=0.903 ms

--- fd14:ca46:3864:99::2 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1002ms
rtt min/avg/max/mdev = 0.903/2.301/3.699/1.398 ms
PING fd14:ca46:3864:99::3 (fd14:ca46:3864:99::3) 56 data bytes
64 bytes from fd14:ca46:3864:99::3: icmp_seq=1 ttl=64 time=3.44 ms
64 bytes from fd14:ca46:3864:99::3: icmp_seq=2 ttl=64 time=0.902 ms

--- fd14:ca46:3864:99::3 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1002ms
rtt min/avg/max/mdev = 0.902/2.169/3.436/1.267 ms
PING fd14:ca46:3864:99::65 (fd14:ca46:3864:99::65) 56 data bytes
64 bytes from fd14:ca46:3864:99::65: icmp_seq=1 ttl=64 time=3.29 ms
64 bytes from fd14:ca46:3864:99::65: icmp_seq=2 ttl=64 time=0.939 ms

--- fd14:ca46:3864:99::65 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1002ms
rtt min/avg/max/mdev = 0.939/2.115/3.291/1.176 ms
 etu@management  ~  




 Host management
    HostName 10.99.0.66
    User etu
    Port 22
    ProxyJump r1

    LocalForward 3000 127.0.0.1:3000
    LocalForward 9090 127.0.0.1:9090
    LocalForward 3100 127.0.0.1:3100
    ExitOnForwardFailure yes


     etu@management  ~  for host in 10.99.0.1 10.99.0.2 10.99.0.3 10.99.0.65 10.99.0.66; do
    echo "===== $host ====="
    curl -s "http://$host:9100/metrics" | grep -m1 node_exporter_build_info
done
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
 etu@management  ~  



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


sudo /usr/local/lib/prometheus/frr_textfile.sh
cat /var/lib/prometheus/node-exporter/frr.prom
# HELP frr_service_active 1 if frr.service is active, otherwise 0.
# TYPE frr_service_active gauge
frr_service_active{node="R1"} 1
# HELP frr_ospf_neighbor_full_total Number of OSPF neighbors in Full state.
# TYPE frr_ospf_neighbor_full_total gauge
frr_ospf_neighbor_full_total{node="R1",protocol="ospfv2"} 2
frr_ospf_neighbor_full_total{node="R1",protocol="ospfv3"} 2
# HELP frr_textfile_last_success_unixtime Unix timestamp of the last successful FRR textfile collection.
# TYPE frr_textfile_last_success_unixtime gauge
frr_textfile_last_success_unixtime{node="R1"} 1780664052
 etu@R1  ~  



sudo /usr/local/lib/prometheus/frr_textfile.sh
cat /var/lib/prometheus/node-exporter/frr.prom
# HELP frr_service_active 1 if frr.service is active, otherwise 0.
# TYPE frr_service_active gauge
frr_service_active{node="R2"} 1
# HELP frr_ospf_neighbor_full_total Number of OSPF neighbors in Full state.
# TYPE frr_ospf_neighbor_full_total gauge
frr_ospf_neighbor_full_total{node="R2",protocol="ospfv2"} 2
frr_ospf_neighbor_full_total{node="R2",protocol="ospfv3"} 2
# HELP frr_textfile_last_success_unixtime Unix timestamp of the last successful FRR textfile collection.
# TYPE frr_textfile_last_success_unixtime gauge
frr_textfile_last_success_unixtime{node="R2"} 1780664135
 etu@R2  ~  


sudo /usr/local/lib/prometheus/frr_textfile.sh
cat /var/lib/prometheus/node-exporter/frr.prom
# HELP frr_service_active 1 if frr.service is active, otherwise 0.
# TYPE frr_service_active gauge
frr_service_active{node="R3"} 1
# HELP frr_ospf_neighbor_full_total Number of OSPF neighbors in Full state.
# TYPE frr_ospf_neighbor_full_total gauge
frr_ospf_neighbor_full_total{node="R3",protocol="ospfv2"} 2
frr_ospf_neighbor_full_total{node="R3",protocol="ospfv3"} 2
# HELP frr_textfile_last_success_unixtime Unix timestamp of the last successful FRR textfile collection.
# TYPE frr_textfile_last_success_unixtime gauge
frr_textfile_last_success_unixtime{node="R3"} 1780664163
 etu@R3  ~  


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

Created symlink '/etc/systemd/system/timers.target.wants/frr-textfile.timer' → '/etc/systemd/system/frr-textfile.timer'.
NEXT LEFT LAST                           PASSED UNIT               ACTIVATES           
-       - Fri 2026-06-05 14:57:44 CEST 27ms ago frr-textfile.timer frr-textfile.service

1 timers listed.
Pass --all to see loaded but inactive timers, too.
 etu@R1  ~  


 etu@R1  ~  curl -s http://127.0.0.1:9100/metrics | grep '^frr_'
frr_ospf_neighbor_full_total{node="R1",protocol="ospfv2"} 2
frr_ospf_neighbor_full_total{node="R1",protocol="ospfv3"} 2
frr_service_active{node="R1"} 1
frr_textfile_last_success_unixtime{node="R1"} 1.780664327e+09
 etu@R1  ~  


  etu@R2  ~  curl -s http://127.0.0.1:9100/metrics | grep '^frr_'
frr_ospf_neighbor_full_total{node="R2",protocol="ospfv2"} 2
frr_ospf_neighbor_full_total{node="R2",protocol="ospfv3"} 2
frr_service_active{node="R2"} 1
frr_textfile_last_success_unixtime{node="R2"} 1.780664332e+09
 etu@R2  ~  


 etu@R3  ~  curl -s http://127.0.0.1:9100/metrics | grep '^frr_'
frr_ospf_neighbor_full_total{node="R3",protocol="ospfv2"} 2
frr_ospf_neighbor_full_total{node="R3",protocol="ospfv3"} 2
frr_service_active{node="R3"} 1
frr_textfile_last_success_unixtime{node="R3"} 1.780664336e+09
 etu@R3  ~  


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


 etu@management  ~  sudo install -d -m 0755 /etc/prometheus/rules
promtool check config /etc/prometheus/prometheus.yml
sudo systemctl enable --now prometheus
sudo systemctl restart prometheus
sudo systemctl status prometheus --no-pager
Checking /etc/prometheus/prometheus.yml
 SUCCESS: /etc/prometheus/prometheus.yml is valid prometheus config file syntax

● prometheus.service - Monitoring system and time series database
     Loaded: loaded (/usr/lib/systemd/system/prometheus.service; enabled; preset: enabled)
     Active: active (running) since Fri 2026-06-05 15:02:18 CEST; 58ms ago
 Invocation: 592a8a233f4d4bf99096375576fb1102
       Docs: https://prometheus.io/docs/introduction/overview/
             man:prometheus(1)
   Main PID: 3464 ((prometheus))
      Tasks: 1 (limit: 14253)
     Memory: 2.2M (peak: 2.2M)
        CPU: 32ms
     CGroup: /system.slice/prometheus.service
             └─3464 "(prometheus)"

Jun 05 15:02:18 management systemd[1]: Started prometheus.service - Monitoring system and time s…abase.
Hint: Some lines were ellipsized, use -l to show in full.
 etu@management  ~  


 etu@management  ~  curl -s http://127.0.0.1:9090/api/v1/targets | jq '.data.activeTargets[] | {job: .labels.job, node: .labels.node, health: .health, scrapeUrl: .scrapeUrl}'
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
 etu@management  ~  

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


 ✘ etu@management  ~  sudo groupadd --system loki
sudo usermod -g loki loki
sudo install -d -o loki -g loki -m 0750 /var/lib/loki
sudo chown -R loki:loki /var/lib/loki
sudo systemctl restart loki
sudo systemctl status loki --no-pager
● loki.service - Loki service
     Loaded: loaded (/etc/systemd/system/loki.service; enabled; preset: enabled)
     Active: active (running) since Fri 2026-06-05 15:23:56 CEST; 54ms ago
 Invocation: 82125a7a208949029f6bd861312b28b7
   Main PID: 5322 (loki)
      Tasks: 10 (limit: 14253)
     Memory: 11.6M (peak: 11.6M)
        CPU: 37ms
     CGroup: /system.slice/loki.service
             └─5322 /usr/bin/loki -config.file /etc/loki/config.yml

Jun 05 15:23:56 management systemd[1]: Started loki.service - Loki service.
 etu@management  ~  curl -s http://10.99.0.66:3100/ready
Ingester not ready: waiting for 15s after being ready
 etu@management  ~  curl -s http://10.99.0.66:3100/ready
Ingester not ready: waiting for 15s after being ready
 etu@management  ~  curl -s http://10.99.0.66:3100/ready
ready


 etu@management  ~  curl -s http://10.99.0.66:3100/metrics | head
# HELP deprecated_flags_inuse_total The number of deprecated flags currently set.
# TYPE deprecated_flags_inuse_total counter
deprecated_flags_inuse_total 0
# HELP go_cgo_go_to_c_calls_calls_total Count of calls made from Go to C by the current process. Sourced from /cgo/go-to-c-calls:calls.
# TYPE go_cgo_go_to_c_calls_calls_total counter
go_cgo_go_to_c_calls_calls_total 0
# HELP go_cpu_classes_gc_mark_assist_cpu_seconds_total Estimated total CPU time goroutines spent performing GC tasks to assist the GC and prevent it from falling behind the application. This metric is an overestimate, and not directly comparable to system CPU time measurements. Compare only with other /cpu/classes metrics. Sourced from /cpu/classes/gc/mark/assist:cpu-seconds.
# TYPE go_cpu_classes_gc_mark_assist_cpu_seconds_total counter
go_cpu_classes_gc_mark_assist_cpu_seconds_total 0.003985566
# HELP go_cpu_classes_gc_mark_dedicated_cpu_seconds_total Estimated total CPU time spent performing GC tasks on processors (as defined by GOMAXPROCS) dedicated to those tasks. This metric is an overestimate, and not directly comparable to system CPU time measurements. Compare only with other /cpu/classes metrics. Sourced from /cpu/classes/gc/mark/dedicated:cpu-seconds.
 etu@management  ~  


 etu@management  ~  curl -s http://127.0.0.1:9090/api/v1/targets | jq '.data.activeTargets[] | select(.labels.job=="loki") | {job: .labels.job, node: .labels.node, health: .health, scrapeUrl: .scrapeUrl}'
{
  "job": "loki",
  "node": "management",
  "health": "up",
  "scrapeUrl": "http://127.0.0.1:3100/metrics"
}
 etu@management  ~  


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


etu@R3  ~  journalctl -u alloy -n 50 --no-pager
Jun 05 18:23:18 R3 systemd[1]: Started alloy.service - Vendor-agnostic OpenTelemetry Collector distribution with programmable pipelines.
Jun 05 18:23:18 R3 systemd[1]: Stopping alloy.service - Vendor-agnostic OpenTelemetry Collector distribution with programmable pipelines...
Jun 05 18:23:18 R3 systemd[1]: alloy.service: Deactivated successfully.
Jun 05 18:23:18 R3 systemd[1]: Stopped alloy.service - Vendor-agnostic OpenTelemetry Collector distribution with programmable pipelines.
Jun 05 18:23:18 R3 systemd[1]: Started alloy.service - Vendor-agnostic OpenTelemetry Collector distribution with programmable pipelines.
Jun 05 18:23:18 R3 alloy[16469]: ts=2026-06-05T16:23:18.892667001Z level=info boringcrypto_enabled=false
Jun 05 18:23:18 R3 alloy[16469]: ts=2026-06-05T16:23:18.890884652Z level=info source=/go/pkg/mod/github.com/!kim!machine!gun/automemlimit@v0.7.5/memlimit/memlimit.go:175 msg="memory is not limited, skipping" package=github.com/KimMachineGun/automemlimit/memlimit
Jun 05 18:23:18 R3 alloy[16469]: ts=2026-06-05T16:23:18.892740186Z level=info msg="no peer discovery configured: both join and discover peers are empty" service=cluster
Jun 05 18:23:18 R3 alloy[16469]: ts=2026-06-05T16:23:18.891897438Z level=info source=/__w/alloy/alloy/internal/runtime/internal/controller/loader.go:201 msg="starting complete graph evaluation" controller_path=/ controller_id="" trace_id=1fc2a046b11f5f74c3f8d3c20e0955a6
Jun 05 18:23:18 R3 alloy[16469]: ts=2026-06-05T16:23:18.89276298Z level=info msg="running usage stats reporter"
Jun 05 18:23:18 R3 alloy[16469]: ts=2026-06-05T16:23:18.892291337Z level=info source=/__w/alloy/alloy/internal/runtime/internal/controller/loader.go:218 msg="finished node evaluation" controller_path=/ controller_id="" trace_id=1fc2a046b11f5f74c3f8d3c20e0955a6 node_id=loki.write.lab duration=383.699µs
Jun 05 18:23:18 R3 alloy[16469]: ts=2026-06-05T16:23:18.8923038Z level=info source=/__w/alloy/alloy/internal/runtime/internal/controller/loader.go:218 msg="finished node evaluation" controller_path=/ controller_id="" trace_id=1fc2a046b11f5f74c3f8d3c20e0955a6 node_id=tracing duration=5.71µs
Jun 05 18:23:18 R3 alloy[16469]: ts=2026-06-05T16:23:18.892313277Z level=info source=/__w/alloy/alloy/internal/runtime/internal/controller/loader.go:218 msg="finished node evaluation" controller_path=/ controller_id="" trace_id=1fc2a046b11f5f74c3f8d3c20e0955a6 node_id=livedebugging duration=6.776µs
Jun 05 18:23:18 R3 alloy[16469]: ts=2026-06-05T16:23:18.892488725Z level=info source=/__w/alloy/alloy/internal/runtime/internal/controller/loader.go:218 msg="finished node evaluation" controller_path=/ controller_id="" trace_id=1fc2a046b11f5f74c3f8d3c20e0955a6 node_id=loki.relabel.journal duration=172.631µs
Jun 05 18:23:18 R3 alloy[16469]: ts=2026-06-05T16:23:18.892656216Z level=info source=/__w/alloy/alloy/internal/runtime/internal/controller/loader.go:218 msg="finished node evaluation" controller_path=/ controller_id="" trace_id=1fc2a046b11f5f74c3f8d3c20e0955a6 node_id=loki.source.journal.system duration=164.297µs
Jun 05 18:23:18 R3 alloy[16469]: ts=2026-06-05T16:23:18.892806061Z level=info source=/__w/alloy/alloy/internal/runtime/internal/controller/loader.go:218 msg="finished node evaluation" controller_path=/ controller_id="" trace_id=1fc2a046b11f5f74c3f8d3c20e0955a6 node_id=logging duration=146.666µs
Jun 05 18:23:18 R3 alloy[16469]: ts=2026-06-05T16:23:18.892876094Z level=info source=/__w/alloy/alloy/internal/runtime/internal/controller/loader.go:218 msg="finished node evaluation" controller_path=/ controller_id="" trace_id=1fc2a046b11f5f74c3f8d3c20e0955a6 node_id=remotecfg duration=60.037µs
Jun 05 18:23:18 R3 alloy[16469]: ts=2026-06-05T16:23:18.89289761Z level=info msg="applying non-TLS config to HTTP server" service=http
Jun 05 18:23:18 R3 alloy[16469]: ts=2026-06-05T16:23:18.892905516Z level=info source=/__w/alloy/alloy/internal/runtime/internal/controller/loader.go:218 msg="finished node evaluation" controller_path=/ controller_id="" trace_id=1fc2a046b11f5f74c3f8d3c20e0955a6 node_id=http duration=18.116µs
Jun 05 18:23:18 R3 alloy[16469]: ts=2026-06-05T16:23:18.892919752Z level=info source=/__w/alloy/alloy/internal/runtime/internal/controller/loader.go:218 msg="finished node evaluation" controller_path=/ controller_id="" trace_id=1fc2a046b11f5f74c3f8d3c20e0955a6 node_id=ui duration=3.613µs
Jun 05 18:23:18 R3 alloy[16469]: ts=2026-06-05T16:23:18.892932012Z level=info source=/__w/alloy/alloy/internal/runtime/internal/controller/loader.go:218 msg="finished node evaluation" controller_path=/ controller_id="" trace_id=1fc2a046b11f5f74c3f8d3c20e0955a6 node_id=cluster duration=3.326µs
Jun 05 18:23:18 R3 alloy[16469]: ts=2026-06-05T16:23:18.892944026Z level=info source=/__w/alloy/alloy/internal/runtime/internal/controller/loader.go:218 msg="finished node evaluation" controller_path=/ controller_id="" trace_id=1fc2a046b11f5f74c3f8d3c20e0955a6 node_id=otel duration=2.763µs
Jun 05 18:23:18 R3 alloy[16469]: ts=2026-06-05T16:23:18.892962256Z level=info source=/__w/alloy/alloy/internal/runtime/internal/controller/loader.go:218 msg="finished node evaluation" controller_path=/ controller_id="" trace_id=1fc2a046b11f5f74c3f8d3c20e0955a6 node_id=labelstore duration=10.291µs
Jun 05 18:23:18 R3 alloy[16469]: ts=2026-06-05T16:23:18.892972036Z level=info source=/__w/alloy/alloy/internal/runtime/internal/controller/loader.go:205 msg="finished complete graph evaluation" controller_path=/ controller_id="" trace_id=1fc2a046b11f5f74c3f8d3c20e0955a6 duration=1.189005ms
Jun 05 18:23:18 R3 alloy[16469]: ts=2026-06-05T16:23:18.89309966Z level=info source=/__w/alloy/alloy/internal/runtime/alloy.go:287 msg="scheduling loaded components and services" controller_id=""
Jun 05 18:23:18 R3 alloy[16469]: ts=2026-06-05T16:23:18.893482193Z level=info msg="starting cluster node" service=cluster peers_count=0 peers="" advertise_addr=127.0.0.1:12345 minimum_cluster_size=0 minimum_size_wait_timeout=0s
Jun 05 18:23:18 R3 alloy[16469]: ts=2026-06-05T16:23:18.89378922Z level=info msg="failed to register collector with remote server" service=remotecfg id=b41b5ed7-dd6f-4d60-98de-003f016a5e21 name="" err="noop client"
Jun 05 18:23:18 R3 alloy[16469]: ts=2026-06-05T16:23:18.893821251Z level=info msg="peers changed" service=cluster peers_count=1 min_cluster_size=0 peers=R3
Jun 05 18:23:18 R3 alloy[16469]: ts=2026-06-05T16:23:18.894389756Z level=info msg="now listening for http traffic" service=http addr=127.0.0.1:12345
 etu@R3  ~  


 etu@management  ~  curl -G -s "http://10.99.0.66:3100/loki/api/v1/labels" | jq
curl -G -s "http://10.99.0.66:3100/loki/api/v1/label/node/values" | jq
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
 etu@management  ~  


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


 ✘ etu@management  ~  curl -s http://127.0.0.1:3000/api/health
curl -s http://127.0.0.1:9090/-/ready
curl -s http://127.0.0.1:3100/ready
{
  "database": "ok",
  "version": "13.0.2",
  "commit": "3fcdbc5a"
}Prometheus Server is Ready.
ready
 etu@management  ~  
