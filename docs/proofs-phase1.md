# Phase 1 OSPF Foundation Report

Status: Phase 1 is complete. This report summarizes the captured evidence for
the FRRouting OSPF lab and keeps the raw command output for auditability.

## Executive Summary

Phase 1 built the routing foundation for the network security lab: a
three-router FRRouting triangle with IPv4 OSPFv2, IPv6 OSPFv3, default route
advertisement from `R1`, and passive hosting networks behind each router.

Key findings:

- The OVS/TAP topology starts the expected router, monitoring, and management
  VMs on `tap62` through `tap66`.
- Transit VLANs `440`, `441`, and `442` are present on the router trunks and
  visible inside the router operating systems.
- Each router has the expected connected transit routes and neighbor-cache
  entries for its adjacent routers.
- OSPFv2 is active on the transit VLAN interfaces, with one adjacent neighbor
  on each point-to-point transit segment.
- `R1` originates the IPv4 and IPv6 default routes; `R2` and `R3` learn those
  default routes through OSPF.
- Hosting VLANs `10`, `20`, and `30` are configured behind `R1`, `R2`, and
  `R3`, and are advertised into OSPF as passive interfaces.
- Incus containers are running behind all three hosting VLANs with IPv4 and
  IPv6 addresses.
- Captured traffic tests prove container reachability to IPv4 and IPv6
  internet targets, and package update output confirms external repository
  access from hosted containers.
- Final FRR configurations for `R1`, `R2`, and `R3` are saved in the evidence.

## Evidence Limitations

The lab is complete, but a few proof captures should be cleaned up before final
portfolio packaging:

- The forwarding-state capture is older and shows forwarding enabled on `R1`
  but disabled on `R2` and `R3`. Later route and traffic evidence proves the
  final lab worked, but the `sysctl` output should be recaptured.
- The first OVS trunk capture still shows temporary VLAN `28` on `tap63` and
  `tap64`. Later router route output confirms this VLAN was not part of the
  final transit design.
- OSPFv3 route and default-route evidence is present. A direct
  `show ipv6 ospf6 neighbor` capture would make the final OSPFv3 evidence set
  cleaner.

## Evidence Index

| Area | Status | Evidence |
| --- | --- | --- |
| OVS trunks | OK | `tap62`, `tap63`, `tap64` trunks show the expected VLANs. |
| VM startup | OK | All five VMs start with expected TAPs and MAC addresses. |
| Transit IPv4 routes | OK | Kernel routes on `R1`, `R2`, and `R3` match VLANs `440`, `441`, `442`. |
| Transit IPv6 links | OK | Link-local IPv6 routes exist on the expected transit VLANs. |
| Neighbor cache | OK | ARP/NDP entries confirm live peers on the transit VLANs. |
| OSPFv2 transit interfaces | OK | `show ip ospf interface` lists transit VLANs `440`, `441`, `442`. |
| OSPFv3 routing | OK | OSPFv3 default route and remote hosting routes are installed. |
| OSPF default route | OK | `R2` and `R3` learn `0.0.0.0/0`; OSPFv3 learns `::/0`. |
| Hosting SVIs | OK | `vlan10`, `vlan20`, and `vlan30` are configured and advertised passively. |
| Hosted containers | OK | Incus containers run behind `R1`, `R2`, and `R3` hosting VLANs. |
| Container reachability | OK | Captured container traffic reaches IPv4 and IPv6 internet targets. |

## Screenshot Evidence

These screenshots capture the initial SSH access state for the router,
monitoring, and management VMs used during the Phase 1 build.

![Router and monitoring SSH sessions](../screenshots/phase1/phase1-router-and-monitoring-ssh-sessions.png)

![Management SSH session](../screenshots/phase1/phase1-management-ssh-session.png)

## Scope And Topology Summary

Phase 1 proves that the base routing lab is stable enough to support later
failure testing, monitoring, IDS work, and AI-assisted troubleshooting.

Router roles:

| Node | Role | TAP | Transit VLANs | Hosting VLAN |
| --- | --- | --- | --- | --- |
| `R1` | Router and default route origin | `tap62` | `440`, `441` | `10` |
| `R2` | Router | `tap63` | `440`, `442` | `20` |
| `R3` | Router | `tap64` | `441`, `442` | `30` |
| Monitoring VM | IDS and security monitoring | `tap65` | None | Management VLAN `99` |
| Management VM | Observability and dashboards | `tap66` | None | Management VLAN `99` |

Transit links:

| Link | VLAN | IPv4 subnet | Purpose |
| --- | ---: | --- | --- |
| `R1` to `R2` | `440` | `10.44.0.0/29` | OSPF backbone transit |
| `R1` to `R3` | `441` | `10.44.1.0/29` | OSPF backbone transit |
| `R2` to `R3` | `442` | `10.44.2.0/29` | OSPF backbone transit |

Hosting networks:

| Router | VLAN | IPv4 prefix | IPv6 prefix |
| --- | ---: | --- | --- |
| `R1` | `10` | `10.10.0.0/24` | `fd14:ca46:3864:a::/64` |
| `R2` | `20` | `10.20.0.0/24` | `fd14:ca46:3864:14::/64` |
| `R3` | `30` | `10.30.0.0/24` | `fd14:ca46:3864:1e::/64` |

## Exit Criteria Assessment

| Exit criterion | Result | Evidence |
| --- | --- | --- |
| `R1`, `R2`, and `R3` can route IPv4 traffic. | Met | OSPFv2 routes include transit and hosting prefixes, plus container IPv4 reachability. |
| `R1`, `R2`, and `R3` can route IPv6 traffic. | Met | OSPFv3 default route and remote hosting prefixes are installed, plus container IPv6 reachability. |
| OSPFv2 neighbors are stable. | Met | Transit interfaces show one adjacent neighbor on each expected VLAN. |
| OSPFv3 routing works. | Met | OSPFv3 default-route and hosting-prefix evidence is present; direct neighbor capture is a polish item. |
| Default route propagation works. | Met | `R2` and `R3` learn IPv4 `0.0.0.0/0` and IPv6 `::/0` from `R1`. |
| Configurations and evidence are saved. | Met | Final FRR configuration blocks for all three routers are included. |

## Detailed Evidence

The following sections preserve the command output used to validate the Phase 1
foundation. Each block supports one part of the summary above.

### OVS And VM Startup

This proves the hypervisor switch and VM startup tooling attach each lab VM to
the expected TAP interface before routing validation begins.

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

Capture note: this first OVS output still shows temporary VLAN `28` on `R2`
and `R3` trunks. Later route output confirms it was not used in the final
transit design.

### Forwarding State

This historical capture is retained because it was part of the build log. It
should be recaptured for final portfolio polish, as noted in the limitations.

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

Later OSPF routes and traffic tests prove the final lab forwarded traffic, but
this exact `sysctl` output is stale.

### R1 Connected Routes And Neighbors

The next three router sections verify the local connected routes and neighbor
cache entries. Together they prove that each router sees its expected transit
peers at layer 3 and layer 2.

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

### R2 Connected Routes And Neighbors

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

### R3 Connected Routes And Neighbors

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

### Management And Monitoring Neighbors

The management and monitoring VMs are reachable on VLAN `99` through `R1`, which
keeps operational access separate from the OSPF transit VLANs.

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

### IPv6 Multicast Reachability

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

### FRR Router IDs

The router IDs are stable and explicit, which makes OSPF neighbor and route
evidence easier to read across IPv4 and IPv6.

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

### OSPFv2 Transit Interfaces

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

### OSPF Default Route Propagation

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

### Hosting Bridges And SVIs

The hosting networks are present behind the routers and are advertised into OSPF as passive interfaces.

| Router | SVI | IPv4 gateway | IPv6 gateway |
| --- | --- | --- | --- |
| `R1` | `vlan10` | `10.10.0.1/24` | `fd14:ca46:3864:a::1/64` |
| `R2` | `vlan20` | `10.20.0.1/24` | `fd14:ca46:3864:14::1/64` |
| `R3` | `vlan30` | `10.30.0.1/24` | `fd14:ca46:3864:1e::1/64` |

### Incus Containers

Each router hosts three Incus containers on its local hosting VLAN. These
containers provide real endpoints for traffic tests instead of only validating
router control-plane state.

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

### Passive OSPF Hosting Interface

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

### Container Internet Reachability

This captured sample shows hosted containers behind `R3` reaching external IPv4
and IPv6 test targets with `0%` packet loss.

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

### Container Package Updates

Package update output from hosted containers provides an additional practical
reachability check against real external repositories.

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

### Hosting Routes Learned By OSPF

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

### Saved FRR Configurations

The final FRR configurations are included so the proof report links behavior
back to the actual routing configuration on each router.

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

## Final Conclusion

The captured Phase 1 evidence proves that the base OSPF lab is operational.
The three routers are connected through the expected VLAN/TAP topology, OSPFv2
and OSPFv3 distribute transit, hosting, and default routes, and hosted
containers provide real traffic endpoints behind the routers.

This gives the project a stable routing foundation for Phase 2 failure testing
and for later observability, IDS, and AI-assisted troubleshooting work. The
remaining proof cleanup is documentation polish, not a blocker for the network
design itself.
