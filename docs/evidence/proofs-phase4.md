 etu@monitoring  ~  for host in 10.99.0.1 10.99.0.2 10.99.0.3 10.99.0.66; do
    ping -c 2 "$host"
done

curl -s http://10.99.0.66:3100/ready
curl -s http://10.99.0.66:9090/-/ready
PING 10.99.0.1 (10.99.0.1) 56(84) bytes of data.
64 bytes from 10.99.0.1: icmp_seq=1 ttl=64 time=0.839 ms
64 bytes from 10.99.0.1: icmp_seq=2 ttl=64 time=0.934 ms

--- 10.99.0.1 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1022ms
rtt min/avg/max/mdev = 0.839/0.886/0.934/0.047 ms
PING 10.99.0.2 (10.99.0.2) 56(84) bytes of data.
64 bytes from 10.99.0.2: icmp_seq=1 ttl=64 time=3.54 ms
64 bytes from 10.99.0.2: icmp_seq=2 ttl=64 time=0.888 ms

--- 10.99.0.2 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1002ms
rtt min/avg/max/mdev = 0.888/2.214/3.541/1.326 ms
PING 10.99.0.3 (10.99.0.3) 56(84) bytes of data.
64 bytes from 10.99.0.3: icmp_seq=1 ttl=64 time=3.45 ms
64 bytes from 10.99.0.3: icmp_seq=2 ttl=64 time=0.978 ms

--- 10.99.0.3 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1001ms
rtt min/avg/max/mdev = 0.978/2.213/3.449/1.235 ms
PING 10.99.0.66 (10.99.0.66) 56(84) bytes of data.
64 bytes from 10.99.0.66: icmp_seq=1 ttl=64 time=0.899 ms
64 bytes from 10.99.0.66: icmp_seq=2 ttl=64 time=0.722 ms

--- 10.99.0.66 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1001ms
rtt min/avg/max/mdev = 0.722/0.810/0.899/0.088 ms
ready
Prometheus Server is Ready.
 etu@monitoring  ~  


  amirmahdighasemi@bob  ~  sudo ovs-vsctl list Bridge dsw-host
sudo ovs-vsctl list Mirror ids-phase4 || sudo ovs-vsctl list Mirror
_uuid               : c3ec56c7-03a1-4ed4-95d6-473085486450
auto_attach         : []
controller          : []
datapath_id         : "00005c6f69707350"
datapath_type       : ""
datapath_version    : "<unknown>"
external_ids        : {}
fail_mode           : []
flood_vlans         : []
flow_tables         : {}
ipfix               : []
mcast_snooping_enable: false
mirrors             : [de7336df-ff02-4604-b14a-bb365ceabe1f]
name                : dsw-host
netflow             : []
other_config        : {forward-bpdu="true", rstp-enable="true"}
ports               : [0015c41d-b620-473f-bcb6-14e2aa151027, ...]
protocols           : []
rstp_enable         : false
rstp_status         : {}
sflow               : []
status              : {}
stp_enable          : false
_uuid               : de7336df-ff02-4604-b14a-bb365ceabe1f
external_ids        : {}
filter              : []
name                : ids-phase4
output_port         : 5a792604-dd4d-460a-9800-4e56d5de9d01
output_vlan         : []
select_all          : false
select_dst_port     : [3d2be126-c2f1-4286-898c-42bc358b1564, 925e4171-beda-476b-b645-1f6f7ad60b82, c318a2d0-8dcd-42a8-8fb7-2f6dc857abf1]
select_src_port     : [3d2be126-c2f1-4286-898c-42bc358b1564, 925e4171-beda-476b-b645-1f6f7ad60b82, c318a2d0-8dcd-42a8-8fb7-2f6dc857abf1]
select_vlan         : [10, 20, 30, 440, 441, 442]
snaplen             : []
statistics          : {tx_bytes=5004, tx_packets=54}
 amirmahdighasemi@bob  ~  

  etu@monitoring  ~  ip -br link
lo               UNKNOWN        00:00:00:00:00:00 <LOOPBACK,UP,LOWER_UP> 
enp0s1           UP             b8:ad:ca:fe:00:41 <BROADCAST,MULTICAST,UP,LOWER_UP> 
enp0s2           UP             b8:ad:ca:fe:00:43 <BROADCAST,MULTICAST,UP,LOWER_UP> 
 etu@monitoring  ~  ip -br addr
lo               UNKNOWN        127.0.0.1/8 ::1/128 
enp0s1           UP             10.99.0.65/24 fd14:ca46:3864:99::65/64 fe80::baad:caff:fefe:41/64 
enp0s2           UP             fe80::baad:caff:fefe:43/64 
 etu@monitoring  ~  

 ✘ etu@monitoring  ~  sudo timeout 30 tcpdump -eni enp0s2 -c 50
tcpdump: verbose output suppressed, use -v[v]... for full protocol decode
listening on enp0s2, link-type EN10MB (Ethernet), snapshot length 262144 bytes
17:27:31.779661 b8:ad:ca:fe:00:3e > b8:ad:ca:fe:00:3f, ethertype 802.1Q (0x8100), length 102: vlan 440, p 0, ethertype IPv4 (0x0800), 10.10.0.169 > 10.20.0.55: ICMP echo request, id 417, seq 8, length 64
17:27:31.780186 b8:ad:ca:fe:00:3f > b8:ad:ca:fe:00:3e, ethertype 802.1Q (0x8100), length 102: vlan 440, p 0, ethertype IPv4 (0x0800), 10.20.0.55 > 10.10.0.169: ICMP echo reply, id 417, seq 8, length 64
17:27:32.780950 b8:ad:ca:fe:00:3e > b8:ad:ca:fe:00:3f, ethertype 802.1Q (0x8100), length 102: vlan 440, p 0, ethertype IPv4 (0x0800), 10.10.0.169 > 10.20.0.55: ICMP echo request, id 417, seq 9, length 64
17:27:32.781558 b8:ad:ca:fe:00:3f > b8:ad:ca:fe:00:3e, ethertype 802.1Q (0x8100), length 102: vlan 440, p 0, ethertype IPv4 (0x0800), 10.20.0.55 > 10.10.0.169: ICMP echo reply, id 417, seq 9, length 64
17:27:32.785263 b8:ad:ca:fe:00:40 > 33:33:00:00:00:05, ethertype 802.1Q (0x8100), length 98: vlan 441, p 0, ethertype IPv6 (0x86dd), fe80::1b9:3 > ff02::5: OSPFv3, Hello, length 40
17:27:32.785515 b8:ad:ca:fe:00:40 > 33:33:00:00:00:05, ethertype 802.1Q (0x8100), length 98: vlan 442, p 0, ethertype IPv6 (0x86dd), fe80::1ba:3 > ff02::5: OSPFv3, Hello, length 40
17:27:32.786151 b8:ad:ca:fe:00:3e > 33:33:00:00:00:05, ethertype 802.1Q (0x8100), length 98: vlan 441, p 0, ethertype IPv6 (0x86dd), fe80::1b9:1 > ff02::5: OSPFv3, Hello, length 40
17:27:32.786479 b8:ad:ca:fe:00:3f > 33:33:00:00:00:05, ethertype 802.1Q (0x8100), length 98: vlan 440, p 0, ethertype IPv6 (0x86dd), fe80::1b8:2 > ff02::5: OSPFv3, Hello, length 40
17:27:32.786677 b8:ad:ca:fe:00:3f > 33:33:00:00:00:05, ethertype 802.1Q (0x8100), length 98: vlan 442, p 0, ethertype IPv6 (0x86dd), fe80::baad:caff:fefe:3f > ff02::5: OSPFv3, Hello, length 40
17:27:33.782373 b8:ad:ca:fe:00:3e > b8:ad:ca:fe:00:3f, ethertype 802.1Q (0x8100), length 102: vlan 440, p 0, ethertype IPv4 (0x0800), 10.10.0.169 > 10.20.0.55: ICMP echo request, id 417, seq 10, length 64
17:27:33.782938 b8:ad:ca:fe:00:3f > b8:ad:ca:fe:00:3e, ethertype 802.1Q (0x8100), length 102: vlan 440, p 0, ethertype IPv4 (0x0800), 10.20.0.55 > 10.10.0.169: ICMP echo reply, id 417, seq 10, length 64
17:27:34.783669 b8:ad:ca:fe:00:3e > b8:ad:ca:fe:00:3f, ethertype 802.1Q (0x8100), length 102: vlan 440, p 0, ethertype IPv4 (0x0800), 10.10.0.169 > 10.20.0.55: ICMP echo request, id 417, seq 11, length 64
17:27:34.784189 b8:ad:ca:fe:00:3f > b8:ad:ca:fe:00:3e, ethertype 802.1Q (0x8100), length 102: vlan 440, p 0, ethertype IPv4 (0x0800), 10.20.0.55 > 10.10.0.169: ICMP echo reply, id 417, seq 11, length 64
17:27:35.784939 b8:ad:ca:fe:00:3e > b8:ad:ca:fe:00:3f, ethertype 802.1Q (0x8100), length 102: vlan 440, p 0, ethertype IPv4 (0x0800), 10.10.0.169 > 10.20.0.55: ICMP echo request, id 417, seq 12, length 64
17:27:35.785449 b8:ad:ca:fe:00:3f > b8:ad:ca:fe:00:3e, ethertype 802.1Q (0x8100), length 102: vlan 440, p 0, ethertype IPv4 (0x0800), 10.20.0.55 > 10.10.0.169: ICMP echo reply, id 417, seq 12, length 64
17:27:36.786246 b8:ad:ca:fe:00:3e > b8:ad:ca:fe:00:3f, ethertype 802.1Q (0x8100), length 102: vlan 440, p 0, ethertype IPv4 (0x0800), 10.10.0.169 > 10.20.0.55: ICMP echo request, id 417, seq 13, length 64
17:27:36.786790 b8:ad:ca:fe:00:3f > b8:ad:ca:fe:00:3e, ethertype 802.1Q (0x8100), length 102: vlan 440, p 0, ethertype IPv4 (0x0800), 10.20.0.55 > 10.10.0.169: ICMP echo reply, id 417, seq 13, length 64
17:27:37.227493 b8:ad:ca:fe:00:3f > 01:00:5e:00:00:05, ethertype 802.1Q (0x8100), length 86: vlan 440, p 0, ethertype IPv4 (0x0800), 10.44.0.2 > 224.0.0.5: OSPFv2, Hello, length 48
17:27:37.227788 b8:ad:ca:fe:00:3f > 01:00:5e:00:00:05, ethertype 802.1Q (0x8100), length 86: vlan 442, p 0, ethertype IPv4 (0x0800), 10.44.2.2 > 224.0.0.5: OSPFv2, Hello, length 48
17:27:37.228494 b8:ad:ca:fe:00:3e > 01:00:5e:00:00:05, ethertype 802.1Q (0x8100), length 86: vlan 440, p 0, ethertype IPv4 (0x0800), 10.44.0.1 > 224.0.0.5: OSPFv2, Hello, length 48
17:27:37.228494 b8:ad:ca:fe:00:40 > 01:00:5e:00:00:05, ethertype 802.1Q (0x8100), length 86: vlan 441, p 0, ethertype IPv4 (0x0800), 10.44.1.3 > 224.0.0.5: OSPFv2, Hello, length 48
17:27:37.228592 b8:ad:ca:fe:00:3e > 01:00:5e:00:00:05, ethertype 802.1Q (0x8100), length 86: vlan 441, p 0, ethertype IPv4 (0x0800), 10.44.1.1 > 224.0.0.5: OSPFv2, Hello, length 48
17:27:37.228849 b8:ad:ca:fe:00:40 > 01:00:5e:00:00:05, ethertype 802.1Q (0x8100), length 86: vlan 442, p 0, ethertype IPv4 (0x0800), 10.44.2.3 > 224.0.0.5: OSPFv2, Hello, length 48
17:27:37.787517 b8:ad:ca:fe:00:3e > b8:ad:ca:fe:00:3f, ethertype 802.1Q (0x8100), length 102: vlan 440, p 0, ethertype IPv4 (0x0800), 10.10.0.169 > 10.20.0.55: ICMP echo request, id 417, seq 14, length 64
17:27:37.787984 b8:ad:ca:fe:00:3f > b8:ad:ca:fe:00:3e, ethertype 802.1Q (0x8100), length 102: vlan 440, p 0, ethertype IPv4 (0x0800), 10.20.0.55 > 10.10.0.169: ICMP echo reply, id 417, seq 14, length 64
17:27:38.788754 b8:ad:ca:fe:00:3e > b8:ad:ca:fe:00:3f, ethertype 802.1Q (0x8100), length 102: vlan 440, p 0, ethertype IPv4 (0x0800), 10.10.0.169 > 10.20.0.55: ICMP echo request, id 417, seq 15, length 64
17:27:38.789283 b8:ad:ca:fe:00:3f > b8:ad:ca:fe:00:3e, ethertype 802.1Q (0x8100), length 102: vlan 440, p 0, ethertype IPv4 (0x0800), 10.20.0.55 > 10.10.0.169: ICMP echo reply, id 417, seq 15, length 64
17:27:39.790040 b8:ad:ca:fe:00:3e > b8:ad:ca:fe:00:3f, ethertype 802.1Q (0x8100), length 102: vlan 440, p 0, ethertype IPv4 (0x0800), 10.10.0.169 > 10.20.0.55: ICMP echo request, id 417, seq 16, length 64
17:27:39.790543 b8:ad:ca:fe:00:3f > b8:ad:ca:fe:00:3e, ethertype 802.1Q (0x8100), length 102: vlan 440, p 0, ethertype IPv4 (0x0800), 10.20.0.55 > 10.10.0.169: ICMP echo reply, id 417, seq 16, length 64
17:27:40.031883 b8:ad:ca:fe:00:3e > 33:33:00:00:00:05, ethertype 802.1Q (0x8100), length 98: vlan 440, p 0, ethertype IPv6 (0x86dd), fe80::1b8:1 > ff02::5: OSPFv3, Hello, length 40
17:27:40.791335 b8:ad:ca:fe:00:3e > b8:ad:ca:fe:00:3f, ethertype 802.1Q (0x8100), length 102: vlan 440, p 0, ethertype IPv4 (0x0800), 10.10.0.169 > 10.20.0.55: ICMP echo request, id 417, seq 17, length 64
17:27:40.791848 b8:ad:ca:fe:00:3f > b8:ad:ca:fe:00:3e, ethertype 802.1Q (0x8100), length 102: vlan 440, p 0, ethertype IPv4 (0x0800), 10.20.0.55 > 10.10.0.169: ICMP echo reply, id 417, seq 17, length 64
17:27:41.792599 b8:ad:ca:fe:00:3e > b8:ad:ca:fe:00:3f, ethertype 802.1Q (0x8100), length 102: vlan 440, p 0, ethertype IPv4 (0x0800), 10.10.0.169 > 10.20.0.55: ICMP echo request, id 417, seq 18, length 64
17:27:41.793145 b8:ad:ca:fe:00:3f > b8:ad:ca:fe:00:3e, ethertype 802.1Q (0x8100), length 102: vlan 440, p 0, ethertype IPv4 (0x0800), 10.20.0.55 > 10.10.0.169: ICMP echo reply, id 417, seq 18, length 64
17:27:42.786280 b8:ad:ca:fe:00:40 > 33:33:00:00:00:05, ethertype 802.1Q (0x8100), length 98: vlan 441, p 0, ethertype IPv6 (0x86dd), fe80::1b9:3 > ff02::5: OSPFv3, Hello, length 40
17:27:42.786621 b8:ad:ca:fe:00:40 > 33:33:00:00:00:05, ethertype 802.1Q (0x8100), length 98: vlan 442, p 0, ethertype IPv6 (0x86dd), fe80::1ba:3 > ff02::5: OSPFv3, Hello, length 40
17:27:42.787208 b8:ad:ca:fe:00:3e > 33:33:00:00:00:05, ethertype 802.1Q (0x8100), length 98: vlan 441, p 0, ethertype IPv6 (0x86dd), fe80::1b9:1 > ff02::5: OSPFv3, Hello, length 40
17:27:42.787564 b8:ad:ca:fe:00:3f > 33:33:00:00:00:05, ethertype 802.1Q (0x8100), length 98: vlan 440, p 0, ethertype IPv6 (0x86dd), fe80::1b8:2 > ff02::5: OSPFv3, Hello, length 40
17:27:42.787791 b8:ad:ca:fe:00:3f > 33:33:00:00:00:05, ethertype 802.1Q (0x8100), length 98: vlan 442, p 0, ethertype IPv6 (0x86dd), fe80::baad:caff:fefe:3f > ff02::5: OSPFv3, Hello, length 40
17:27:42.793873 b8:ad:ca:fe:00:3e > b8:ad:ca:fe:00:3f, ethertype 802.1Q (0x8100), length 102: vlan 440, p 0, ethertype IPv4 (0x0800), 10.10.0.169 > 10.20.0.55: ICMP echo request, id 417, seq 19, length 64
17:27:42.794474 b8:ad:ca:fe:00:3f > b8:ad:ca:fe:00:3e, ethertype 802.1Q (0x8100), length 102: vlan 440, p 0, ethertype IPv4 (0x0800), 10.20.0.55 > 10.10.0.169: ICMP echo reply, id 417, seq 19, length 64
17:27:43.795240 b8:ad:ca:fe:00:3e > b8:ad:ca:fe:00:3f, ethertype 802.1Q (0x8100), length 102: vlan 440, p 0, ethertype IPv4 (0x0800), 10.10.0.169 > 10.20.0.55: ICMP echo request, id 417, seq 20, length 64
17:27:43.795770 b8:ad:ca:fe:00:3f > b8:ad:ca:fe:00:3e, ethertype 802.1Q (0x8100), length 102: vlan 440, p 0, ethertype IPv4 (0x0800), 10.20.0.55 > 10.10.0.169: ICMP echo reply, id 417, seq 20, length 64
17:27:44.796567 b8:ad:ca:fe:00:3e > b8:ad:ca:fe:00:3f, ethertype 802.1Q (0x8100), length 102: vlan 440, p 0, ethertype IPv4 (0x0800), 10.10.0.169 > 10.20.0.55: ICMP echo request, id 417, seq 21, length 64
17:27:44.797089 b8:ad:ca:fe:00:3f > b8:ad:ca:fe:00:3e, ethertype 802.1Q (0x8100), length 102: vlan 440, p 0, ethertype IPv4 (0x0800), 10.20.0.55 > 10.10.0.169: ICMP echo reply, id 417, seq 21, length 64
17:27:45.797856 b8:ad:ca:fe:00:3e > b8:ad:ca:fe:00:3f, ethertype 802.1Q (0x8100), length 102: vlan 440, p 0, ethertype IPv4 (0x0800), 10.10.0.169 > 10.20.0.55: ICMP echo request, id 417, seq 22, length 64
17:27:45.798061 b8:ad:ca:fe:00:3f > b8:ad:ca:fe:00:3e, ethertype 802.1Q (0x8100), length 102: vlan 440, p 0, ethertype IPv4 (0x0800), 10.20.0.55 > 10.10.0.169: ICMP echo reply, id 417, seq 22, length 64
17:27:46.799010 b8:ad:ca:fe:00:3e > b8:ad:ca:fe:00:3f, ethertype 802.1Q (0x8100), length 102: vlan 440, p 0, ethertype IPv4 (0x0800), 10.10.0.169 > 10.20.0.55: ICMP echo request, id 417, seq 23, length 64
17:27:46.799512 b8:ad:ca:fe:00:3f > b8:ad:ca:fe:00:3e, ethertype 802.1Q (0x8100), length 102: vlan 440, p 0, ethertype IPv4 (0x0800), 10.20.0.55 > 10.10.0.169: ICMP echo reply, id 417, seq 23, length 64
17:27:47.227734 b8:ad:ca:fe:00:3f > 01:00:5e:00:00:05, ethertype 802.1Q (0x8100), length 86: vlan 440, p 0, ethertype IPv4 (0x0800), 10.44.0.2 > 224.0.0.5: OSPFv2, Hello, length 48
50 packets captured
55 packets received by filter
0 packets dropped by kernel
 etu@monitoring  ~  


 etu@monitoring  ~  sudo suricata -T -c /etc/suricata/suricata.yaml -v
Notice: suricata: This is Suricata version 8.0.6 RELEASE running in SYSTEM mode
Info: cpu: CPUs/cores online: 8
Info: suricata: Running suricata under test mode
Info: suricata: Setting engine mode to IDS mode by default
Info: exception-policy: master exception-policy set to: auto
Info: suricata: Preparing unexpected signal handling
Info: logopenfile: fast output device (regular) initialized: fast.log
Info: logopenfile: eve-log output device (regular) initialized: eve.json
Info: logopenfile: stats output device (regular) initialized: stats.log
Info: detect: 1 rule files processed. 52158 rules successfully loaded, 0 rules failed, 0 rules skipped
Info: threshold-config: Threshold config parsed: 0 rule(s) found
Info: detect: 52163 signatures processed. 1292 are IP-only rules, 4510 are inspecting packet payload, 46126 inspect application layer, 110 are decoder event only
Notice: suricata: Configuration provided was successfully loaded. Exiting.
 etu@monitoring  ~  sudo ls -lh /var/lib/suricata/rules/
total 43M
-rw-r--r-- 1 root root 3.2K Aug  2 17:59 classification.config
-rw-r--r-- 1 root root  43M Aug  2 17:59 suricata.rules
 etu@monitoring  ~  


 etu@monitoring  ~  sudo jq -c 'select(.src_ip=="10.10.0.169" or .dest_ip=="10.10.0.169" or .src_ip=="10.20.0.55" or .dest_ip=="10.20.0.55")' /var/log/suricata/eve.json
{"timestamp":"2026-08-02T18:08:27.383631+0200","flow_id":1084736286633171,"in_iface":"enp0s2","event_type":"alert","vlan":[440],"src_ip":"10.10.0.169","dest_ip":"10.20.0.55","proto":"ICMP","ip_v":4,"icmp_type":8,"icmp_code":0,"pkt_src":"wire/pcap","alert":{"action":"allowed","gid":1,"signature_id":2100366,"rev":8,"signature":"GPL ICMP PING *NIX","category":"Misc activity","severity":3,"metadata":{"confidence":["Medium"],"created_at":["2010_09_23"],"signature_severity":["Informational"],"tag":["Description_Generated_By_Proofpoint_Nexus"],"updated_at":["2019_07_26"]}},"direction":"to_server","flow":{"pkts_toserver":1,"pkts_toclient":0,"bytes_toserver":102,"bytes_toclient":0,"start":"2026-08-02T18:08:27.383631+0200","src_ip":"10.10.0.169","dest_ip":"10.20.0.55"}}
...


 etu@monitoring  ~  sudo suricata --dump-config | grep -E "default-rule-path|local-phase4"
sudo grep -R "LOCAL Phase4" /var/lib/suricata/rules /etc/suricata/rules 2>/dev/null
default-rule-path = /var/lib/suricata/rules
rule-files.1 = local-phase4.rules
/var/lib/suricata/rules/local-phase4.rules:alert tcp $EXTERNAL_NET any -> $HOME_NET any (msg:"LOCAL Phase4 TCP SYN scan candidate"; flags:S; detection_filter: track by_src, count 25, seconds 60; classtype:attempted-recon; sid:1000401; rev:1;)
/var/lib/suricata/rules/local-phase4.rules:alert tcp $EXTERNAL_NET any -> $HOME_NET 22 (msg:"LOCAL Phase4 SSH connection burst"; flags:S; detection_filter: track by_src, count 5, seconds 60; classtype:attempted-recon; sid:1000402; rev:1;)
/var/lib/suricata/rules/local-phase4.rules:alert http $EXTERNAL_NET any -> $HOME_NET any (msg:"LOCAL Phase4 suspicious HTTP user agent"; flow:to_server,established; http.user_agent; content:"phase4-suspicious-curl"; nocase; classtype:policy-violation; sid:1000403; rev:1;)
/var/lib/suricata/rules/local-phase4.rules:alert icmp $EXTERNAL_NET any -> $HOME_NET any (msg:"LOCAL Phase4 ICMP sweep candidate"; itype:8; detection_filter: track by_src, count 10, seconds 60; classtype:attempted-recon; sid:1000404; rev:1;)
 etu@monitoring  ~  



 etu@management  ~  curl -G -s "http://10.99.0.66:3100/loki/api/v1/label/job/values" | jq
curl -G -s "http://10.99.0.66:3100/loki/api/v1/label/event_type/values" | jq
{
  "status": "success",
  "data": [
    "suricata-eve",
    "systemd-journal"
  ]
}
{
  "status": "success",
  "data": [
    "alert",
    "dns",
    "flow",
    "stats",
    "tls"
  ]
}
 etu@management  ~  



 etu@management  ~  curl -s "http://10.99.0.65:9100/metrics" | grep '^suricata_'
suricata_eve_alert_events_total{node="monitoring"} 357
suricata_eve_last_alert_unixtime{node="monitoring"} 1.785692072e+09
suricata_eve_last_success_unixtime{node="monitoring"} 1.785693006e+09
suricata_service_active{node="monitoring"} 1
 etu@management  ~  


 