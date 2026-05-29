# OSPF Lab Proofs

Status: TP completed through Q34.

Current evidence coverage:

- TAP/OVS topology is present.
- `R1`, `R2`, `R3`, `monitoring`, and `management` start on the expected TAPs.
- Transit VLANs `440`, `441`, and `442` are reachable.
- Temporary VLAN `28` is no longer present in the live route output for `R2` and `R3`.
- OSPFv2 is active only on the transit VLAN interfaces.
- `R1` advertises the IPv4 and IPv6 default routes through OSPF.
- Q32-Q34 are reported done, but the command output for the hosting bridge/SVI step still needs to be pasted here.

Important follow-up:

- Older captured forwarding output shows forwarding enabled on `R1` and disabled on `R2`/`R3`. If this was fixed later, recapture it before marking forwarding fully complete.
- Q35 is the next routing step for hosting VLANs: publish `vlan10`, `vlan20`, and `vlan30` in OSPF as passive interfaces.

## Evidence Index

| Area | Status | Evidence |
| --- | --- | --- |
| OVS trunks | OK | `tap62`, `tap63`, `tap64` trunks show the expected VLANs. |
| VM startup | OK | All five VMs start with expected TAPs and MAC addresses. |
| Transit IPv4 routes | OK | Kernel routes on `R1`, `R2`, and `R3` match VLANs `440`, `441`, `442`. |
| Transit IPv6 links | OK | Link-local IPv6 routes exist on the expected transit VLANs. |
| Neighbor cache | OK | ARP/NDP entries confirm live peers on the transit VLANs. |
| OSPFv2 transit interfaces | OK | `show ip ospf interface` lists only `440`, `441`, `442`. |
| OSPF default route | OK | `R2` and `R3` learn `0.0.0.0/0`; OSPFv3 learns `::/0`. |
| Hosting SVI Q32-Q34 | Needs paste | Add package, bridge, and `vlan10`/`vlan20`/`vlan30` outputs below. |

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

Action needed if this is still current:

```console
sudo sysctl -w net.ipv4.ip_forward=1
sudo sysctl -w net.ipv6.conf.all.forwarding=1
```

Then recapture the same `sysctl` command on `R2` and `R3`.

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

## Q32-Q34 Hosting Bridge And SVI

Status: reported complete, evidence still to paste.

Expected from the TP:

- Q32: install `openvswitch-switch`, `dnsmasq`, and `incus`.
- Q33: add the Open vSwitch bridge `asw-host` in Netplan.
- Q34: add the SVI used as the default gateway for hosted containers.

Expected SVI mapping for this lab:

| Router | SVI | IPv4 gateway | IPv6 gateway |
| --- | --- | --- | --- |
| `R1` | `vlan10` | `10.10.0.1/24` | `fd14:ca46:3864:a::1/64` |
| `R2` | `vlan20` | `10.20.0.1/24` | `fd14:ca46:3864:14::1/64` |
| `R3` | `vlan30` | `10.30.0.1/24` | `fd14:ca46:3864:1e::1/64` |

Paste fresh evidence here after Q34:

```console
# On R1, R2, and R3
dpkg -l openvswitch-switch dnsmasq incus
ip link show asw-host
ip -br addr show asw-host
ip -br addr show vlan10   # R1
ip -br addr show vlan20   # R2
ip -br addr show vlan30   # R3
sudo netplan status
```

Expected next Q35 FRR commands:

```console
# R1
conf t
interface vlan10
 ip ospf area 0
 ipv6 ospf6 area 0
 ip ospf passive
 ipv6 ospf6 passive
end

# R2
conf t
interface vlan20
 ip ospf area 0
 ipv6 ospf6 area 0
 ip ospf passive
 ipv6 ospf6 passive
end

# R3
conf t
interface vlan30
 ip ospf area 0
 ipv6 ospf6 area 0
 ip ospf passive
 ipv6 ospf6 passive
end
```
