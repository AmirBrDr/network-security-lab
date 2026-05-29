# OSPF Lab Proofs

Status: OSPF lab completed.

Current evidence coverage:

- TAP/OVS topology is present.
- `R1`, `R2`, `R3`, `monitoring`, and `management` start on the expected TAPs.
- Transit VLANs `440`, `441`, and `442` are reachable.
- Transit routes are present on VLANs `440`, `441`, and `442`.
- OSPFv2 and OSPFv3 are active on the transit VLAN interfaces.
- `R1` advertises the IPv4 and IPv6 default routes through OSPF.
- Hosting VLANs `10`, `20`, and `30` are advertised as passive OSPF interfaces.
- Incus containers are running behind all three hosting VLANs.
- Hosted containers have IPv4 and IPv6 internet reachability.

Important follow-up:

- The older forwarding capture below shows forwarding enabled on `R1` and disabled on `R2`/`R3`. Later routing and container connectivity evidence proves the lab is working, but this command should be recaptured for a perfectly clean final evidence set.

## Evidence Index

| Area | Status | Evidence |
| --- | --- | --- |
| OVS trunks | OK | `tap62`, `tap63`, `tap64` trunks show the expected VLANs. |
| VM startup | OK | All five VMs start with expected TAPs and MAC addresses. |
| Transit IPv4 routes | OK | Kernel routes on `R1`, `R2`, and `R3` match VLANs `440`, `441`, `442`. |
| Transit IPv6 links | OK | Link-local IPv6 routes exist on the expected transit VLANs. |
| Neighbor cache | OK | ARP/NDP entries confirm live peers on the transit VLANs. |
| OSPFv2 transit interfaces | OK | `show ip ospf interface` lists transit VLANs `440`, `441`, `442`. |
| OSPF default route | OK | `R2` and `R3` learn `0.0.0.0/0`; OSPFv3 learns `::/0`. |
| Hosting SVIs | OK | `vlan10`, `vlan20`, and `vlan30` are configured and advertised passively. |
| Hosted containers | OK | Incus containers run behind `R1`, `R2`, and `R3` hosting VLANs. |
| Container reachability | OK | Hosted containers reach IPv4 and IPv6 internet targets. |

## OVS And VM Startup

```console
amirmahdighasemi@bob:~/vm/network-security-lab$ switch-conf.py -a switch.yaml
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
```

```console
amirmahdighasemi@bob:~/vm/network-security-lab$ lab-startup.py vms-startup.yaml
R1 started on tap62, trunk mode, MAC b8:ad:ca:fe:00:3e, console 2362
R2 started on tap63, trunk mode, MAC b8:ad:ca:fe:00:3f, console 2363
R3 started on tap64, trunk mode, MAC b8:ad:ca:fe:00:40, console 2364
monitoring started on tap65, access mode, MAC b8:ad:ca:fe:00:41, console 2365
management started on tap66, access mode, MAC b8:ad:ca:fe:00:42, console 2366
```

Note: the first OVS capture still shows temporary VLAN `28` in the trunks for `R2` and `R3`. Later route output confirms `enp0s1.28` is no longer active inside the routers.

## Forwarding State

```console
etu@R1:~$ sudo sysctl net.ipv4.ip_forward net.ipv6.conf.all.forwarding
net.ipv4.ip_forward = 1
net.ipv6.conf.all.forwarding = 1

etu@R2:~$ sudo sysctl net.ipv4.ip_forward net.ipv6.conf.all.forwarding
net.ipv4.ip_forward = 0
net.ipv6.conf.all.forwarding = 0

etu@R3:~$ sudo sysctl net.ipv4.ip_forward net.ipv6.conf.all.forwarding
net.ipv4.ip_forward = 0
net.ipv6.conf.all.forwarding = 0
```

Note: this is an older capture. The later OSPF routes and container reachability prove forwarding worked during final validation, but the `sysctl` command should be recaptured on `R2` and `R3` for the final portfolio evidence.

## R1 Connected Routes And Neighbors

```console
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
```

Key `R1` neighbors:

```console
10.44.0.2 dev enp0s1.440 lladdr b8:ad:ca:fe:00:3f STALE
fe80::1b8:2 dev enp0s1.440 lladdr b8:ad:ca:fe:00:3f STALE
fe80::baad:caff:fefe:40 dev enp0s1.441 lladdr b8:ad:ca:fe:00:40 STALE
10.99.0.2 dev enp0s1.99 lladdr b8:ad:ca:fe:00:3f STALE
10.99.0.3 dev enp0s1.99 lladdr b8:ad:ca:fe:00:40 STALE
10.99.0.65 dev enp0s1.99 lladdr b8:ad:ca:fe:00:41 STALE
10.99.0.66 dev enp0s1.99 lladdr b8:ad:ca:fe:00:42 STALE
192.168.104.129 dev enp0s1.360 lladdr 80:6a:00:dc:67:53 STALE
```

## R2 Connected Routes And Neighbors

```console
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
fe80::baad:caff:fefe:40 dev enp0s1.442 lladdr b8:ad:ca:fe:00:40 STALE
```

## R3 Connected Routes And Neighbors

```console
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
```

## Management And Monitoring Neighbors

```console
etu@management:~$ ip nei ls
10.99.0.1 dev enp0s1 lladdr b8:ad:ca:fe:00:3e REACHABLE
fe80::baad:caff:fefe:3e dev enp0s1 lladdr b8:ad:ca:fe:00:3e router STALE
fd14:ca46:3864:99::1 dev enp0s1 lladdr b8:ad:ca:fe:00:3e router STALE

etu@monitoring:~$ ip nei ls
10.99.0.1 dev enp0s1 lladdr b8:ad:ca:fe:00:3e DELAY
fe80::baad:caff:fefe:3e dev enp0s1 lladdr b8:ad:ca:fe:00:3e router STALE
fd14:ca46:3864:99::1 dev enp0s1 lladdr b8:ad:ca:fe:00:3e router STALE
```

## IPv6 Multicast Reachability

Expected transit interfaces:

- `R1`: `enp0s1.440`, `enp0s1.441`
- `R2`: `enp0s1.440`, `enp0s1.442`
- `R3`: `enp0s1.441`, `enp0s1.442`

```console
etu@R1:~$ ping -qc2 ff02::1%enp0s1.440
2 packets transmitted, 2 received, +1 duplicates, 0% packet loss

etu@R1:~$ ping -qc2 ff02::1%enp0s1.441
2 packets transmitted, 2 received, +1 duplicates, 0% packet loss

etu@R2:~$ ping -qc2 ff02::1%enp0s1.440
2 packets transmitted, 2 received, +1 duplicates, 0% packet loss

etu@R2:~$ ping -qc2 ff02::1%enp0s1.442
2 packets transmitted, 2 received, +1 duplicates, 0% packet loss

etu@R3:~$ ping -qc2 ff02::1%enp0s1.441
2 packets transmitted, 2 received, +1 duplicates, 0% packet loss

etu@R3:~$ ping -qc2 ff02::1%enp0s1.442
2 packets transmitted, 2 received, +1 duplicates, 0% packet loss
```

Expected negative checks:

```console
etu@R2:~$ ping -qc2 ff02::1%enp0s1.441
ping: ff02::1%enp0s1.441: Name or service not known

etu@R3:~$ ping -qc2 ff02::1%enp0s1.440
ping: ff02::1%enp0s1.440: Name or service not known
```

These failures are normal: `R2` does not have VLAN `441`, and `R3` does not have VLAN `440`.

## FRR Router IDs

```console
R1# sh run ospfd
router ospf
 ospf router-id 1.0.0.4
 log-adjacency-changes detail

R1# sh run ospf6d
router ospf6
 ospf6 router-id 1.0.0.6
 log-adjacency-changes detail

R2# sh run ospfd
router ospf
 ospf router-id 2.0.0.4
 log-adjacency-changes detail

R2# sh run ospf6d
router ospf6
 ospf6 router-id 2.0.0.6
 log-adjacency-changes detail

R3# sh run ospfd
router ospf
 ospf router-id 3.0.0.4
 log-adjacency-changes detail

R3# sh run ospf6d
router ospf6
 ospf6 router-id 3.0.0.6
 log-adjacency-changes detail
```

## OSPFv2 Transit Interfaces

This proves OSPF stays on VLANs `440`, `441`, and `442`.

```console
R1# show ip ospf interface
enp0s1.440 is up
  Internet Address 10.44.0.1/29, Area 0.0.0.0
  State DR
  Designated Router (ID) 1.0.0.4
  Backup Designated Router (ID) 2.0.0.4
  Neighbor Count is 1, Adjacent neighbor count is 1

enp0s1.441 is up
  Internet Address 10.44.1.1/29, Area 0.0.0.0
  State DR
  Designated Router (ID) 1.0.0.4
  Backup Designated Router (ID) 3.0.0.4
  Neighbor Count is 1, Adjacent neighbor count is 1

R2# show ip ospf interface
enp0s1.440 is up
  Internet Address 10.44.0.2/29, Area 0.0.0.0
  State Backup
  Designated Router (ID) 1.0.0.4
  Backup Designated Router (ID) 2.0.0.4
  Neighbor Count is 1, Adjacent neighbor count is 1

enp0s1.442 is up
  Internet Address 10.44.2.2/29, Area 0.0.0.0
  State DR
  Designated Router (ID) 2.0.0.4
  Backup Designated Router (ID) 3.0.0.4
  Neighbor Count is 1, Adjacent neighbor count is 1

R3# show ip ospf interface
enp0s1.441 is up
  Internet Address 10.44.1.3/29, Area 0.0.0.0
  State Backup
  Designated Router (ID) 1.0.0.4
  Backup Designated Router (ID) 3.0.0.4
  Neighbor Count is 1, Adjacent neighbor count is 1

enp0s1.442 is up
  Internet Address 10.44.2.3/29, Area 0.0.0.0
  State Backup
  Designated Router (ID) 2.0.0.4
  Backup Designated Router (ID) 3.0.0.4
  Neighbor Count is 1, Adjacent neighbor count is 1
```

## OSPF Default Route Propagation

`R1` originates the IPv6 default route as an external LSA:

```console
R1# sh ipv6 ospf6 database as-external

        AS Scoped Link State Database

Type LSId           AdvRouter       Age   SeqNum                        Payload
ASE  0.0.0.1        1.0.0.6          17 80000001                             ::
```

`R2` and `R3` learn the IPv4 default route from `R1`:

```console
R2# sh ip ospf route
N E2 0.0.0.0/0             [10/10] tag: 0
                           via 10.44.0.1, enp0s1.440

R3# sh ip ospf route
N E2 0.0.0.0/0             [10/10] tag: 0
                           via 10.44.1.1, enp0s1.441
```

`R2` and `R3` learn the IPv6 default route from `R1`:

```console
R2# sh ipv6 ospf6 route
*N E2 ::/0                           fe80::1b8:1               enp0s1.440 00:02:36

R3# sh ipv6 ospf6 route
*N E2 ::/0                           fe80::1b9:1               enp0s1.441 00:02:39
```

Transit routes are present in OSPFv2:

```console
R1# sh ip ospf route
N    10.44.0.0/29          [10] area: 0.0.0.0
                           directly attached to enp0s1.440
N    10.44.1.0/29          [10] area: 0.0.0.0
                           directly attached to enp0s1.441
N    10.44.2.0/29          [20] area: 0.0.0.0
                           via 10.44.0.2, enp0s1.440
                           via 10.44.1.3, enp0s1.441

R2# sh ip ospf route
N    10.44.0.0/29          [10] area: 0.0.0.0
                           directly attached to enp0s1.440
N    10.44.1.0/29          [20] area: 0.0.0.0
                           via 10.44.0.1, enp0s1.440
                           via 10.44.2.3, enp0s1.442
N    10.44.2.0/29          [10] area: 0.0.0.0
                           directly attached to enp0s1.442

R3# sh ip ospf route
N    10.44.0.0/29          [20] area: 0.0.0.0
                           via 10.44.1.1, enp0s1.441
                           via 10.44.2.2, enp0s1.442
N    10.44.1.0/29          [10] area: 0.0.0.0
                           directly attached to enp0s1.441
N    10.44.2.0/29          [10] area: 0.0.0.0
                           directly attached to enp0s1.442
```

## Hosting Bridges And SVIs

The hosting networks are present behind the routers and are advertised into OSPF as passive interfaces.

| Router | SVI | IPv4 gateway | IPv6 gateway |
| --- | --- | --- | --- |
| `R1` | `vlan10` | `10.10.0.1/24` | `fd14:ca46:3864:a::1/64` |
| `R2` | `vlan20` | `10.20.0.1/24` | `fd14:ca46:3864:14::1/64` |
| `R3` | `vlan30` | `10.30.0.1/24` | `fd14:ca46:3864:1e::1/64` |

## Incus Containers

```console
etu@R1:~$ incus ls
+------+---------+--------------------+---------------------------------------------+-----------+-----------+
| NAME |  STATE  |        IPV4        |                    IPV6                     |   TYPE    | SNAPSHOTS |
+------+---------+--------------------+---------------------------------------------+-----------+-----------+
| c0   | RUNNING | 10.10.0.169 (eth0) | fd14:ca46:3864:a:1266:6aff:fe8a:f053 (eth0) | CONTAINER | 0         |
+------+---------+--------------------+---------------------------------------------+-----------+-----------+
| c1   | RUNNING | 10.10.0.93 (eth0)  | fd14:ca46:3864:a:1266:6aff:fe84:92c2 (eth0) | CONTAINER | 0         |
+------+---------+--------------------+---------------------------------------------+-----------+-----------+
| c2   | RUNNING | 10.10.0.76 (eth0)  | fd14:ca46:3864:a:1266:6aff:fea9:6530 (eth0) | CONTAINER | 0         |
+------+---------+--------------------+---------------------------------------------+-----------+-----------+
```

```console
etu@R2:~$ incus ls
+------+---------+--------------------+----------------------------------------------+-----------+-----------+
| NAME |  STATE  |        IPV4        |                     IPV6                     |   TYPE    | SNAPSHOTS |
+------+---------+--------------------+----------------------------------------------+-----------+-----------+
| c0   | RUNNING | 10.20.0.156 (eth0) | fd14:ca46:3864:14:1266:6aff:fe64:ce54 (eth0) | CONTAINER | 0         |
+------+---------+--------------------+----------------------------------------------+-----------+-----------+
| c1   | RUNNING | 10.20.0.89 (eth0)  | fd14:ca46:3864:14:1266:6aff:fef1:fdcf (eth0) | CONTAINER | 0         |
+------+---------+--------------------+----------------------------------------------+-----------+-----------+
| c2   | RUNNING | 10.20.0.106 (eth0) | fd14:ca46:3864:14:1266:6aff:fe54:d44c (eth0) | CONTAINER | 0         |
+------+---------+--------------------+----------------------------------------------+-----------+-----------+
```

```console
etu@R3:~$ incus ls
+------+---------+--------------------+----------------------------------------------+-----------+-----------+
| NAME |  STATE  |        IPV4        |                     IPV6                     |   TYPE    | SNAPSHOTS |
+------+---------+--------------------+----------------------------------------------+-----------+-----------+
| c0   | RUNNING | 10.30.0.101 (eth0) | fd14:ca46:3864:1e:1266:6aff:fe9c:57cb (eth0) | CONTAINER | 0         |
+------+---------+--------------------+----------------------------------------------+-----------+-----------+
| c1   | RUNNING | 10.30.0.23 (eth0)  | fd14:ca46:3864:1e:1266:6aff:fe27:3b45 (eth0) | CONTAINER | 0         |
+------+---------+--------------------+----------------------------------------------+-----------+-----------+
| c2   | RUNNING | 10.30.0.74 (eth0)  | fd14:ca46:3864:1e:1266:6aff:fe1a:bf31 (eth0) | CONTAINER | 0         |
+------+---------+--------------------+----------------------------------------------+-----------+-----------+
```

## Passive OSPF Hosting Interface

`R2` shows `vlan20` advertised in OSPFv2 and OSPFv3 without forming neighbors on the hosting network.

```console
R2# sh ip ospf interface vlan20
vlan20 is up
  ifindex 9, MTU 1500 bytes, BW 0 Mbit <UP,LOWER_UP,BROADCAST,RUNNING,MULTICAST>
  Internet Address 10.20.0.1/24, Broadcast 10.20.0.255, Area 0.0.0.0
  MTU mismatch detection: enabled
  Router ID 2.0.0.4, Network Type BROADCAST, Cost: 10
  Transmit Delay is 1 sec, State DR, Priority 1
  Designated Router (ID) 2.0.0.4 Interface Address 10.20.0.1/24
  No backup designated router on this network
  Multicast group memberships: <None>
  Timer intervals configured, Hello 10s, Dead 40s, Wait 40s, Retransmit 5
    No Hellos (Passive interface)
  Neighbor Count is 0, Adjacent neighbor count is 0
  Graceful Restart hello delay: 10s
  LSA retransmissions: 0

R2# sh ipv6 ospf6 interface vlan20
vlan20 is up, type BROADCAST
  Interface ID: 9
  Internet Address:
    inet : 10.20.0.1/24
    inet6: fe80::58b7:f4ff:fe48:8a4f/64
    inet6: fd14:ca46:3864:14::1/64
  Instance ID 0, Interface MTU 1500 (autodetect: 1500)
  MTU mismatch detection: enabled
  Area ID 0.0.0.0, Cost 10
  State DR, Transmit Delay 1 sec, Priority 1
  Timer intervals configured:
   No Hellos (Passive interface)
  DR: 2.0.0.6 BDR: 0.0.0.0
  Number of I/F scoped LSAs is 1
    0 Pending LSAs for LSUpdate in Time 00:00:00 [thread off]
    0 Pending LSAs for LSAck in Time 00:00:00 [thread off]
  Graceful Restart hello delay: 10s
  Authentication Trailer is disabled
R2#
```

## Container Internet Reachability

```console
etu@R3:~$ for i in {0..2}
do
    echo ">>>>>>>>>>>>>>>>> c$i"
    incus exec c$i -- ping -qc2 9.9.9.9
done
>>>>>>>>>>>>>>>>> c0
PING 9.9.9.9 (9.9.9.9) 56(84) bytes of data.

--- 9.9.9.9 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1002ms
rtt min/avg/max/mdev = 17.721/18.047/18.373/0.326 ms
>>>>>>>>>>>>>>>>> c1
PING 9.9.9.9 (9.9.9.9) 56(84) bytes of data.

--- 9.9.9.9 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1002ms
rtt min/avg/max/mdev = 16.820/17.279/17.738/0.459 ms
>>>>>>>>>>>>>>>>> c2
PING 9.9.9.9 (9.9.9.9) 56(84) bytes of data.

--- 9.9.9.9 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1002ms
rtt min/avg/max/mdev = 16.567/16.898/17.230/0.331 ms
```

```console
etu@R3:~$ for i in {0..2}
do
    echo ">>>>>>>>>>>>>>>>> c$i"
    incus exec c$i -- ping -qc2 2620:fe::fe
done
>>>>>>>>>>>>>>>>> c0
PING 2620:fe::fe (2620:fe::fe) 56 data bytes

--- 2620:fe::fe ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1001ms
rtt min/avg/max/mdev = 36.845/37.375/37.905/0.530 ms
>>>>>>>>>>>>>>>>> c1
PING 2620:fe::fe (2620:fe::fe) 56 data bytes

--- 2620:fe::fe ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1002ms
rtt min/avg/max/mdev = 36.574/36.882/37.190/0.308 ms
>>>>>>>>>>>>>>>>> c2
PING 2620:fe::fe (2620:fe::fe) 56 data bytes

--- 2620:fe::fe ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1002ms
rtt min/avg/max/mdev = 37.225/37.354/37.484/0.129 ms
```

## Container Package Updates

```console
etu@R1:~$ for i in {0..2}
do
    echo ">>>>>>>>>>>>>>>>> c$i"
    incus exec c$i -- apt update
    incus exec c$i -- apt -y full-upgrade
done
>>>>>>>>>>>>>>>>> c0
Hit:1 http://deb.debian.org/debian trixie InRelease
Get:2 http://deb.debian.org/debian trixie-updates InRelease [47.3 kB]
Get:3 http://deb.debian.org/debian-security trixie-security InRelease [43.4 kB]
Fetched 90.7 kB in 0s (285 kB/s)
All packages are up to date.
Summary:
  Upgrading: 0, Installing: 0, Removing: 0, Not Upgrading: 0
>>>>>>>>>>>>>>>>> c1
Hit:1 http://deb.debian.org/debian trixie InRelease
Get:2 http://deb.debian.org/debian trixie-updates InRelease [47.3 kB]
Get:3 http://deb.debian.org/debian-security trixie-security InRelease [43.4 kB]
Fetched 90.7 kB in 0s (563 kB/s)
All packages are up to date.
Summary:
  Upgrading: 0, Installing: 0, Removing: 0, Not Upgrading: 0
>>>>>>>>>>>>>>>>> c2
Hit:1 http://deb.debian.org/debian trixie InRelease
Get:2 http://deb.debian.org/debian trixie-updates InRelease [47.3 kB]
Get:3 http://deb.debian.org/debian-security trixie-security InRelease [43.4 kB]
Fetched 90.7 kB in 0s (559 kB/s)
All packages are up to date.
Summary:
  Upgrading: 0, Installing: 0, Removing: 0, Not Upgrading: 0
```

## Hosting Routes Learned By OSPF

`R2` learns the `R1` and `R3` hosting networks over OSPFv2.

```console
R2# sh ip route
Codes: K - kernel route, C - connected, L - local, S - static,
       R - RIP, O - OSPF, I - IS-IS, B - BGP, E - EIGRP, N - NHRP,
       T - Table, v - VNC, V - VNC-Direct, A - Babel, F - PBR,
       f - OpenFabric, t - Table-Direct,
       > - selected route, * - FIB route, q - queued, r - rejected, b - backup
       t - trapped, o - offload failure

IPv4 unicast VRF default:
O>* 0.0.0.0/0 [110/10] via 10.44.0.1, enp0s1.440, weight 1, 04:31:25
O>* 10.10.0.0/24 [110/20] via 10.44.0.1, enp0s1.440, weight 1, 00:48:35
O   10.20.0.0/24 [110/10] is directly connected, vlan20, weight 1, 00:46:56
C>* 10.20.0.0/24 is directly connected, vlan20, weight 1, 03:57:59
L>* 10.20.0.1/32 is directly connected, vlan20, weight 1, 03:57:59
O>* 10.30.0.0/24 [110/20] via 10.44.2.3, enp0s1.442, weight 1, 00:44:05
C>* 10.44.0.0/29 is directly connected, enp0s1.440, weight 1, 03:57:59
O   10.44.0.0/29 [110/10] is directly connected, enp0s1.440, weight 1, 05:12:16
L>* 10.44.0.2/32 is directly connected, enp0s1.440, weight 1, 03:57:59
O>* 10.44.1.0/29 [110/20] via 10.44.0.1, enp0s1.440, weight 1, 05:09:52
  *                       via 10.44.2.3, enp0s1.442, weight 1, 05:09:52
C>* 10.44.2.0/29 is directly connected, enp0s1.442, weight 1, 03:57:59
O   10.44.2.0/29 [110/10] is directly connected, enp0s1.442, weight 1, 05:11:47
L>* 10.44.2.2/32 is directly connected, enp0s1.442, weight 1, 03:57:59
C>* 10.99.0.0/24 is directly connected, enp0s1.99, weight 1, 03:57:59
L>* 10.99.0.2/32 is directly connected, enp0s1.99, weight 1, 03:57:59
R2#
```

`R3` learns the `R1` and `R2` hosting IPv6 prefixes over OSPFv3.

```console
R3# sh ipv6 route
Codes: K - kernel route, C - connected, L - local, S - static,
       R - RIPng, O - OSPFv3, I - IS-IS, B - BGP, N - NHRP,
       T - Table, v - VNC, V - VNC-Direct, A - Babel, F - PBR,
       f - OpenFabric, t - Table-Direct,
       > - selected route, * - FIB route, q - queued, r - rejected, b - backup
       t - trapped, o - offload failure

IPv6 unicast VRF default:
O>* ::/0 [110/10] via fe80::1b9:1, enp0s1.441, weight 1, 00:44:45
O>* fd14:ca46:3864:a::/64 [110/20] via fe80::1b9:1, enp0s1.441, weight 1, 00:48:53
O>* fd14:ca46:3864:14::/64 [110/20] via fe80::baad:caff:fefe:3f, enp0s1.442, weight 1, 00:47:35
O   fd14:ca46:3864:1e::/64 [110/10] is directly connected, vlan30, weight 1, 00:44:46
C>* fd14:ca46:3864:1e::/64 is directly connected, vlan30, weight 1, 00:46:16
K * fd14:ca46:3864:1e::/64 [0/256] is directly connected, vlan30, weight 1, 00:46:18
L>* fd14:ca46:3864:1e::1/128 is directly connected, vlan30, weight 1, 00:46:16
C>* fd14:ca46:3864:99::/64 is directly connected, enp0s1.99, weight 1, 00:46:18
K * fd14:ca46:3864:99::/64 [0/256] is directly connected, enp0s1.99, weight 1, 05:55:30
L>* fd14:ca46:3864:99::3/128 is directly connected, enp0s1.99, weight 1, 00:46:18
C * fe80::/64 is directly connected, asw-host, weight 1, 00:46:16
C * fe80::/64 is directly connected, vlan30, weight 1, 00:46:16
C * fe80::/64 is directly connected, enp0s1.99, weight 1, 00:46:18
C * fe80::/64 is directly connected, enp0s1.28, weight 1, 04:07:47
C * fe80::/64 is directly connected, enp0s1, weight 1, 04:07:49
C * fe80::/64 is directly connected, enp0s1.442, weight 1, 05:55:28
C>* fe80::/64 is directly connected, enp0s1.441, weight 1, 05:55:28
R3#
```

Targeted route checks from `R1` confirm remote hosting networks are installed through OSPF.

```console
R1# sh ip route 10.20.0.0/24
Routing entry for 10.20.0.0/24
  Known via "ospf", distance 110, metric 80, best
  Last update 00:18:33 ago
  Flags: Selected
  Status: Installed
  * 10.44.0.2, via enp0s1.440, weight 1

R1#
```

```console
R1# sh ipv6 route fd14:ca46:3864:1e::/64
Routing entry for fd14:ca46:3864:1e::/64
  Known via "ospf6", distance 110, metric 80, best
  Last update 00:09:30 ago
  Flags: Selected
  Status: Installed
  * fe80::1b9:3, via enp0s1.441, weight 1

R1#
```

## Saved FRR Configurations

```console
etu@R1:~$ sudo cat /etc/frr/frr.conf
frr version 10.6.1
frr defaults traditional
hostname R1
log syslog informational
service integrated-vtysh-config
!
interface enp0s1.440
 ip ospf area 0
 ipv6 ospf6 area 0
exit
!
interface enp0s1.441
 ip ospf area 0
 ipv6 ospf6 area 0
exit
!
interface vlan10
 bandwidth 10000
 ip ospf area 0
 ip ospf passive
 ipv6 ospf6 area 0
 ipv6 ospf6 passive
exit
!
router ospf
 ospf router-id 1.0.0.4
 log-adjacency-changes detail
 auto-cost reference-bandwidth 400000
 default-information originate
exit
!
router ospf6
 ospf6 router-id 1.0.0.6
 log-adjacency-changes detail
 auto-cost reference-bandwidth 400000
 redistribute unknown
 default-information originate
exit
!
```

```console
etu@R2:~$ sudo cat /etc/frr/frr.conf
frr version 10.6.1
frr defaults traditional
hostname R2
log syslog informational
service integrated-vtysh-config
!
interface enp0s1.440
 ip ospf area 0
 ipv6 ospf6 area 0
exit
!
interface enp0s1.442
 ip ospf area 0
 ipv6 ospf6 area 0
exit
!
interface vlan20
 bandwidth 10000
 ip ospf area 0
 ip ospf passive
 ipv6 ospf6 area 0
 ipv6 ospf6 passive
exit
!
router ospf
 ospf router-id 2.0.0.4
 log-adjacency-changes detail
 auto-cost reference-bandwidth 400000
exit
!
router ospf6
 ospf6 router-id 2.0.0.6
 log-adjacency-changes detail
 auto-cost reference-bandwidth 400000
exit
!
```

```console
etu@R3:~$ sudo cat /etc/frr/frr.conf
frr version 10.6.1
frr defaults traditional
hostname R3
log syslog informational
service integrated-vtysh-config
!
interface enp0s1.441
 ip ospf area 0
 ipv6 ospf6 area 0
exit
!
interface enp0s1.442
 ip ospf area 0
 ipv6 ospf6 area 0
exit
!
interface vlan30
 bandwidth 10000
 ip ospf area 0
 ip ospf passive
 ipv6 ospf6 area 0
 ipv6 ospf6 passive
exit
!
router ospf
 ospf router-id 3.0.0.4
 log-adjacency-changes detail
 auto-cost reference-bandwidth 400000
exit
!
router ospf6
 ospf6 router-id 3.0.0.6
 log-adjacency-changes detail
 auto-cost reference-bandwidth 400000
exit
!
```
