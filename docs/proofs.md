 amirmahdighasemi@bob  ~/vm/network-security-lab  switch-conf.py -a switch.yaml
----------------------------------------
Switch dsw-host exists
>> Port tap62 vlan_mode is already set to trunk
>> Port tap62 trunks are already set to [99, 360, 440, 441]
>> Port tap63 vlan_mode is already set to trunk
>> Port tap63 trunks are already set to [28, 99, 440, 442]
>> Port tap64 vlan_mode is already set to trunk
>> Port tap64 trunks are already set to [28, 99, 441, 442]
>> Port tap65 vlan_mode is already set to access
>> Port tap65 tag is already set to 99
>> Port tap66 vlan_mode is already set to access
>> Port tap66 tag is already set to 99
----------------------------------------
 amirmahdighasemi@bob  ~/vm/network-security-lab  lab-startup.py vms-startup.yaml 
R1.qcow2 already exists!
Creating R1.qcow2_OVMF_VARS.fd file...
Starting R1...
~> Virtual machine filename   : R1.qcow2
~> RAM size                   : 4096
~> SPICE VDI port number      : 5962
~> telnet console port number : 2362
~> MAC address                : b8:ad:ca:fe:00:3e
~> Switch port interface      : tap62, trunk mode
~> IPv6 LL address            : fe80::baad:caff:fefe:3e%dsw-host
R1 started!
R2.qcow2 already exists!
Creating R2.qcow2_OVMF_VARS.fd file...
Starting R2...
~> Virtual machine filename   : R2.qcow2
~> RAM size                   : 4096
~> SPICE VDI port number      : 5963
~> telnet console port number : 2363
~> MAC address                : b8:ad:ca:fe:00:3f
~> Switch port interface      : tap63, trunk mode
~> IPv6 LL address            : fe80::baad:caff:fefe:3f%dsw-host
R2 started!
R3.qcow2 already exists!
Creating R3.qcow2_OVMF_VARS.fd file...
Starting R3...
~> Virtual machine filename   : R3.qcow2
~> RAM size                   : 4096
~> SPICE VDI port number      : 5964
~> telnet console port number : 2364
~> MAC address                : b8:ad:ca:fe:00:40
~> Switch port interface      : tap64, trunk mode
~> IPv6 LL address            : fe80::baad:caff:fefe:40%dsw-host
R3 started!
monitoring.qcow2 already exists!
Creating monitoring.qcow2_OVMF_VARS.fd file...
Starting monitoring...
~> Virtual machine filename   : monitoring.qcow2
~> RAM size                   : 12288
~> SPICE VDI port number      : 5965
~> telnet console port number : 2365
~> MAC address                : b8:ad:ca:fe:00:41
~> Switch port interface      : tap65, access mode
~> IPv6 LL address            : fe80::baad:caff:fefe:41%vlan99
monitoring started!
management.qcow2 already exists!
Creating management.qcow2_OVMF_VARS.fd file...
Starting management...
~> Virtual machine filename   : management.qcow2
~> RAM size                   : 12288
~> SPICE VDI port number      : 5966
~> telnet console port number : 2366
~> MAC address                : b8:ad:ca:fe:00:42
~> Switch port interface      : tap66, access mode
~> IPv6 LL address            : fe80::baad:caff:fefe:42%vlan99
management started!
 amirmahdighasemi@bob  ~/vm/network-security-lab  

 etu@R1:~$ sudo sysctl net.ipv4.ip_forward net.ipv6.conf.all.forwarding
net.ipv4.ip_forward = 1
net.ipv6.conf.all.forwarding = 1
etu@R1:~$ 

etu@R2:~$ sudo sysctl net.ipv4.ip_forward net.ipv6.conf.all.forwarding
net.ipv4.ip_forward = 0
net.ipv6.conf.all.forwarding = 0
etu@R2:~$ 

etu@R3:~$ sudo sysctl net.ipv4.ip_forward net.ipv6.conf.all.forwarding
net.ipv4.ip_forward = 0
net.ipv6.conf.all.forwarding = 0
etu@R3:~$ 

sudo netplsudo netplan status
     Online state: online
    DNS Addresses: 127.0.0.53 (stub)
       DNS Search: .

●  1: lo ethernet UNKNOWN/UP (unmanaged)
      MAC Address: 00:00:00:00:00:00
        Addresses: 127.0.0.1/8
                   ::1/128

●  2: enp0s1 ethernet UP (networkd: enp0s1)
      MAC Address: b8:ad:ca:fe:00:3e (Red Hat, Inc.)
        Addresses: fe80::baad:caff:fefe:3e/64 (link)
    DNS Addresses: 172.16.0.2
                   2001:678:3fc:3::2
           Routes: fe80::/64 metric 256

●  3: enp0s1.360 vlan UP (networkd: enp0s1.360)
      MAC Address: b8:ad:ca:fe:00:3e
        Addresses: 192.168.104.130/29
                   2001:678:3fc:168::82/64 (ra)
                   2001:678:3fc:168:baad:caff:fefe:3e/64 (dynamic, ra)
                   fe80::baad:caff:fefe:3e/64 (link)
    DNS Addresses: 2001:678:3fc:3::2
           Routes: default via 192.168.104.129 (static)
                   192.168.104.128/29 from 192.168.104.130 (link)
                   2001:678:3fc:168::/64 metric 256
                   2001:678:3fc:168::/64 metric 512 (ra)
                   fe80::/64 metric 256
                   default via fe80:168::1 metric 512 (ra)
                   default via fe80::168:1 metric 1024 (static)

●  4: enp0s1.440 vlan UP (networkd: enp0s1.440)
      MAC Address: b8:ad:ca:fe:00:3e
        Addresses: 10.44.0.1/29
                   fe80::baad:caff:fefe:3e/64 (link)
                   fe80::1b8:1/64 (link)
           Routes: 10.44.0.0/29 from 10.44.0.1 (link)
                   fe80::/64 metric 256

●  5: enp0s1.99 vlan UP (networkd: enp0s1.99)
      MAC Address: b8:ad:ca:fe:00:3e
        Addresses: 10.99.0.1/24
                   fd14:ca46:3864:99::1/64
                   fe80::baad:caff:fefe:3e/64 (link)
           Routes: 10.99.0.0/24 from 10.99.0.1 (link)
                   fd14:ca46:3864:99::/64 metric 256
                   fe80::/64 metric 256

●  6: enp0s1.441 vlan UP (networkd: enp0s1.441)
      MAC Address: b8:ad:ca:fe:00:3e
        Addresses: 10.44.1.1/29
                   fe80::baad:caff:fefe:3e/64 (link)
                   fe80::1b9:1/64 (link)
           Routes: 10.44.1.0/29 from 10.44.1.1 (link)
                   fe80::/64 metric 256




etu@R1:~$ ip route ls proto kernel
10.44.0.0/29 dev enp0s1.440 scope link src 10.44.0.1 
10.44.1.0/29 dev enp0s1.441 scope link src 10.44.1.1 
10.99.0.0/24 dev enp0s1.99 scope link src 10.99.0.1 
192.168.104.128/29 dev enp0s1.360 scope link src 192.168.104.130 
etu@R1:~$ ip -6 route ls proto kernel
2001:678:3fc:168::/64 dev enp0s1.360 metric 256 pref medium
fd14:ca46:3864:99::/64 dev enp0s1.99 metric 256 pref medium
fe80::/64 dev enp0s1 metric 256 pref medium
fe80::/64 dev enp0s1.360 metric 256 pref medium
fe80::/64 dev enp0s1.440 metric 256 pref medium
fe80::/64 dev enp0s1.99 metric 256 pref medium
fe80::/64 dev enp0s1.441 metric 256 pref medium
etu@R1:~$ ip nei ls
10.99.0.2 dev enp0s1.99 lladdr b8:ad:ca:fe:00:3f STALE 
10.99.0.65 dev enp0s1.99 lladdr b8:ad:ca:fe:00:41 STALE 
192.168.104.129 dev enp0s1.360 lladdr 80:6a:00:dc:67:53 STALE 
10.99.0.66 dev enp0s1.99 lladdr b8:ad:ca:fe:00:42 STALE 
10.44.0.2 dev enp0s1.440 lladdr b8:ad:ca:fe:00:3f STALE 
10.99.0.3 dev enp0s1.99 lladdr b8:ad:ca:fe:00:40 STALE 
fe80::baad:caff:fefe:41 dev enp0s1.99 lladdr b8:ad:ca:fe:00:41 STALE 
fe80::1b8:2 dev enp0s1.440 lladdr b8:ad:ca:fe:00:3f STALE 
fe80::baad:caff:fefe:40 dev enp0s1.99 lladdr b8:ad:ca:fe:00:40 STALE 
fe80::baad:caff:fefe:3f dev enp0s1.99 lladdr b8:ad:ca:fe:00:3f STALE 
fd14:ca46:3864:99::66 dev enp0s1.99 lladdr b8:ad:ca:fe:00:42 STALE 
fd14:ca46:3864:99::65 dev enp0s1.99 lladdr b8:ad:ca:fe:00:41 STALE 
fe80:168::1 dev enp0s1.360 lladdr 80:6a:00:dc:67:53 router DELAY 
fe80::baad:caff:fefe:40 dev enp0s1.441 lladdr b8:ad:ca:fe:00:40 STALE 
fe80::baad:caff:fefe:3f dev enp0s1.440 lladdr b8:ad:ca:fe:00:3f STALE 
fe80::baad:caff:fefe:42 dev enp0s1.99 lladdr b8:ad:ca:fe:00:42 STALE 
etu@R1:~$ 

etu@R2:~$ ip route ls proto kernel
10.44.0.0/29 dev enp0s1.440 scope link src 10.44.0.2 
10.44.2.0/29 dev enp0s1.442 scope link src 10.44.2.2 
10.99.0.0/24 dev enp0s1.99 scope link src 10.99.0.2 
etu@R2:~$ ip -6 route ls proto kernel
fd14:ca46:3864:99::/64 dev enp0s1.99 metric 256 pref medium
fe80::/64 dev enp0s1 metric 256 pref medium
fe80::/64 dev enp0s1.440 metric 256 pref medium
fe80::/64 dev enp0s1.442 metric 256 pref medium
fe80::/64 dev enp0s1.99 metric 256 pref medium
etu@R2:~$ ip nei ls
10.44.0.1 dev enp0s1.440 lladdr b8:ad:ca:fe:00:3e REACHABLE 
10.44.2.3 dev enp0s1.442 lladdr b8:ad:ca:fe:00:40 REACHABLE 
10.99.0.1 dev enp0s1.99 lladdr b8:ad:ca:fe:00:3e REACHABLE 
fe80::baad:caff:fefe:40 dev enp0s1.99 lladdr b8:ad:ca:fe:00:40 STALE 
fe80::baad:caff:fefe:40 dev enp0s1.442 lladdr b8:ad:ca:fe:00:40 STALE 
etu@R2:~$ 


etu@R3:~$ ip route ls proto kernel
10.44.1.0/29 dev enp0s1.441 scope link src 10.44.1.3 
10.44.2.0/29 dev enp0s1.442 scope link src 10.44.2.3 
10.99.0.0/24 dev enp0s1.99 scope link src 10.99.0.3 
etu@R3:~$ ip -6 route ls proto kernel
fd14:ca46:3864:99::/64 dev enp0s1.99 metric 256 pref medium
fe80::/64 dev enp0s1 metric 256 pref medium
fe80::/64 dev enp0s1.99 metric 256 pref medium
fe80::/64 dev enp0s1.442 metric 256 pref medium
fe80::/64 dev enp0s1.441 metric 256 pref medium
etu@R3:~$ ip nei ls
10.99.0.1 dev enp0s1.99 lladdr b8:ad:ca:fe:00:3e REACHABLE 
10.44.2.2 dev enp0s1.442 lladdr b8:ad:ca:fe:00:3f REACHABLE 
10.44.1.1 dev enp0s1.441 lladdr b8:ad:ca:fe:00:3e REACHABLE 
fe80::baad:caff:fefe:3f dev enp0s1.442 lladdr b8:ad:ca:fe:00:3f STALE 
fe80::baad:caff:fefe:3f dev enp0s1.99 lladdr b8:ad:ca:fe:00:3f STALE 
etu@R3:~$ 



etu@management:~$ ip nei ls
10.99.0.1 dev enp0s1 lladdr b8:ad:ca:fe:00:3e REACHABLE 
fe80::baad:caff:fefe:3e dev enp0s1 lladdr b8:ad:ca:fe:00:3e router STALE 
fd14:ca46:3864:99::1 dev enp0s1 lladdr b8:ad:ca:fe:00:3e router STALE 
etu@management:~$ 

etu@monitoring:~$ ip nei ls
10.99.0.1 dev enp0s1 lladdr b8:ad:ca:fe:00:3e DELAY 
fe80::baad:caff:fefe:3e dev enp0s1 lladdr b8:ad:ca:fe:00:3e router STALE 
fd14:ca46:3864:99::1 dev enp0s1 lladdr b8:ad:ca:fe:00:3e router STALE 
etu@monitoring:~$ 



etu@R1:~$ ping -qc2 ff02::1%enp0s1.440
PING ff02::1%enp0s1.440 (ff02::1%enp0s1.440) 56 data bytes

--- ff02::1%enp0s1.440 ping statistics ---
2 packets transmitted, 2 received, +1 duplicates, 0% packet loss, time 1001ms
rtt min/avg/max/mdev = 0.055/1.681/4.912/2.284 ms
etu@R1:~$ ping -qc2 ff02::1%enp0s1.441
PING ff02::1%enp0s1.441 (ff02::1%enp0s1.441) 56 data bytes

--- ff02::1%enp0s1.441 ping statistics ---
2 packets transmitted, 2 received, +1 duplicates, 0% packet loss, time 1002ms
rtt min/avg/max/mdev = 0.076/1.885/5.494/2.551 ms
etu@R1:~$ 


etu@R2:~$ ping -qc2 ff02::1%enp0s1.440
PING ff02::1%enp0s1.440 (ff02::1%enp0s1.440) 56 data bytes

--- ff02::1%enp0s1.440 ping statistics ---
2 packets transmitted, 2 received, +1 duplicates, 0% packet loss, time 1002ms
rtt min/avg/max/mdev = 0.056/0.851/2.429/1.115 ms
etu@R2:~$ ping -qc2 ff02::1%enp0s1.442
PING ff02::1%enp0s1.442 (ff02::1%enp0s1.442) 56 data bytes

--- ff02::1%enp0s1.442 ping statistics ---
2 packets transmitted, 2 received, +1 duplicates, 0% packet loss, time 1002ms
rtt min/avg/max/mdev = 0.055/0.836/2.379/1.090 ms
etu@R2:~$ ping -qc2 ff02::1%enp0s1.441
ping: ff02::1%enp0s1.441: Name or service not known
etu@R2:~$ 


etu@R3:~$ ping -qc2 ff02::1%enp0s1.440
ping: ff02::1%enp0s1.440: Name or service not known
etu@R3:~$ ping -qc2 ff02::1%enp0s1.441
PING ff02::1%enp0s1.441 (ff02::1%enp0s1.441) 56 data bytes

--- ff02::1%enp0s1.441 ping statistics ---
2 packets transmitted, 2 received, +1 duplicates, 0% packet loss, time 1002ms
rtt min/avg/max/mdev = 0.072/0.616/1.699/0.765 ms
etu@R3:~$ ping -qc2 ff02::1%enp0s1.442
PING ff02::1%enp0s1.442 (ff02::1%enp0s1.442) 56 data bytes

--- ff02::1%enp0s1.442 ping statistics ---
2 packets transmitted, 2 received, +1 duplicates, 0% packet loss, time 1002ms
rtt min/avg/max/mdev = 0.063/0.873/2.483/1.137 ms
etu@R3:~$ 

R1# sh run ospfd
Building configuration...

Current configuration:
!
frr version 10.6.1
frr defaults traditional
hostname R1
!
router ospf
 ospf router-id 1.0.0.4
 log-adjacency-changes detail
exit
!
end
R1# sh run ospf6d
Building configuration...

Current configuration:
!
frr version 10.6.1
frr defaults traditional
hostname R1
!
router ospf6
 ospf6 router-id 1.0.0.6
 log-adjacency-changes detail
exit
!
end
R1# 


R2# sh run ospfd
Building configuration...

Current configuration:
!
frr version 10.6.1
frr defaults traditional
hostname R2
!
router ospf
 ospf router-id 2.0.0.4
 log-adjacency-changes detail
exit
!
end
R2# sh run ospf6d
Building configuration...

Current configuration:
!
frr version 10.6.1
frr defaults traditional
hostname R2
!
router ospf6
 ospf6 router-id 2.0.0.6
 log-adjacency-changes detail
exit
!
end
R2# 


R3# sh run ospfd
Building configuration...

Current configuration:
!
frr version 10.6.1
frr defaults traditional
hostname R3
!
router ospf
 ospf router-id 3.0.0.4
 log-adjacency-changes detail
exit
!
end
R3# sh run ospf6d
Building configuration...

Current configuration:
!
frr version 10.6.1
frr defaults traditional
hostname R3
!
router ospf6
 ospf6 router-id 3.0.0.6
 log-adjacency-changes detail
exit
!
end
R3# 


R1# show ip ospf interface
enp0s1.440 is up
  ifindex 4, MTU 1500 bytes, BW 0 Mbit <UP,LOWER_UP,BROADCAST,RUNNING,MULTICAST>
  Internet Address 10.44.0.1/29, Broadcast 10.44.0.7, Area 0.0.0.0
  MTU mismatch detection: enabled
  Router ID 1.0.0.4, Network Type BROADCAST, Cost: 10
  Transmit Delay is 1 sec, State DR, Priority 1
  Designated Router (ID) 1.0.0.4 Interface Address 10.44.0.1/29
  Backup Designated Router (ID) 2.0.0.4, Interface Address 10.44.0.2
  Multicast group memberships: OSPFAllRouters OSPFDesignatedRouters
  Timer intervals configured, Hello 10s, Dead 40s, Wait 40s, Retransmit 5
    Hello due in 8.497s
  Neighbor Count is 1, Adjacent neighbor count is 1
  Graceful Restart hello delay: 10s
  LSA retransmissions: 1
enp0s1.441 is up
  ifindex 6, MTU 1500 bytes, BW 0 Mbit <UP,LOWER_UP,BROADCAST,RUNNING,MULTICAST>
  Internet Address 10.44.1.1/29, Broadcast 10.44.1.7, Area 0.0.0.0
  MTU mismatch detection: enabled
  Router ID 1.0.0.4, Network Type BROADCAST, Cost: 10
  Transmit Delay is 1 sec, State DR, Priority 1
  Designated Router (ID) 1.0.0.4 Interface Address 10.44.1.1/29
  Backup Designated Router (ID) 3.0.0.4, Interface Address 10.44.1.3
  Multicast group memberships: OSPFAllRouters OSPFDesignatedRouters
  Timer intervals configured, Hello 10s, Dead 40s, Wait 40s, Retransmit 5
    Hello due in 9.931s
  Neighbor Count is 1, Adjacent neighbor count is 1
  Graceful Restart hello delay: 10s
  LSA retransmissions: 1

R1# 


R2# show ip ospf interface
enp0s1.440 is up
  ifindex 4, MTU 1500 bytes, BW 0 Mbit <UP,LOWER_UP,BROADCAST,RUNNING,MULTICAST>
  Internet Address 10.44.0.2/29, Broadcast 10.44.0.7, Area 0.0.0.0
  MTU mismatch detection: enabled
  Router ID 2.0.0.4, Network Type BROADCAST, Cost: 10
  Transmit Delay is 1 sec, State Backup, Priority 1
  Designated Router (ID) 1.0.0.4 Interface Address 10.44.0.1/29
  Backup Designated Router (ID) 2.0.0.4, Interface Address 10.44.0.2
  Multicast group memberships: OSPFAllRouters OSPFDesignatedRouters
  Timer intervals configured, Hello 10s, Dead 40s, Wait 40s, Retransmit 5
    Hello due in 2.464s
  Neighbor Count is 1, Adjacent neighbor count is 1
  Graceful Restart hello delay: 10s
  LSA retransmissions: 1
enp0s1.442 is up
  ifindex 3, MTU 1500 bytes, BW 0 Mbit <UP,LOWER_UP,BROADCAST,RUNNING,MULTICAST>
  Internet Address 10.44.2.2/29, Broadcast 10.44.2.7, Area 0.0.0.0
  MTU mismatch detection: enabled
  Router ID 2.0.0.4, Network Type BROADCAST, Cost: 10
  Transmit Delay is 1 sec, State DR, Priority 1
  Designated Router (ID) 2.0.0.4 Interface Address 10.44.2.2/29
  Backup Designated Router (ID) 3.0.0.4, Interface Address 10.44.2.3
  Multicast group memberships: OSPFAllRouters OSPFDesignatedRouters
  Timer intervals configured, Hello 10s, Dead 40s, Wait 40s, Retransmit 5
    Hello due in 8.823s
  Neighbor Count is 1, Adjacent neighbor count is 1
  Graceful Restart hello delay: 10s
  LSA retransmissions: 0

R2# 


R3# show ip ospf interface
enp0s1.441 is up
  ifindex 5, MTU 1500 bytes, BW 0 Mbit <UP,LOWER_UP,BROADCAST,RUNNING,MULTICAST>
  Internet Address 10.44.1.3/29, Broadcast 10.44.1.7, Area 0.0.0.0
  MTU mismatch detection: enabled
  Router ID 3.0.0.4, Network Type BROADCAST, Cost: 10
  Transmit Delay is 1 sec, State Backup, Priority 1
  Designated Router (ID) 1.0.0.4 Interface Address 10.44.1.1/29
  Backup Designated Router (ID) 3.0.0.4, Interface Address 10.44.1.3
  Multicast group memberships: OSPFAllRouters OSPFDesignatedRouters
  Timer intervals configured, Hello 10s, Dead 40s, Wait 40s, Retransmit 5
    Hello due in 2.155s
  Neighbor Count is 1, Adjacent neighbor count is 1
  Graceful Restart hello delay: 10s
  LSA retransmissions: 2
enp0s1.442 is up
  ifindex 4, MTU 1500 bytes, BW 0 Mbit <UP,LOWER_UP,BROADCAST,RUNNING,MULTICAST>
  Internet Address 10.44.2.3/29, Broadcast 10.44.2.7, Area 0.0.0.0
  MTU mismatch detection: enabled
  Router ID 3.0.0.4, Network Type BROADCAST, Cost: 10
  Transmit Delay is 1 sec, State Backup, Priority 1
  Designated Router (ID) 2.0.0.4 Interface Address 10.44.2.2/29
  Backup Designated Router (ID) 3.0.0.4, Interface Address 10.44.2.3
  Multicast group memberships: OSPFAllRouters OSPFDesignatedRouters
  Timer intervals configured, Hello 10s, Dead 40s, Wait 40s, Retransmit 5
    Hello due in 2.647s
  Neighbor Count is 1, Adjacent neighbor count is 1
  Graceful Restart hello delay: 10s
  LSA retransmissions: 1

R3# 
