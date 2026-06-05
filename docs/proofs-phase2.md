# Phase 2 Failure Testing Report

Status: Phase 2 report complete for the captured failure scenarios. Direct
`R1` to `R3` and `R2` to `R3` link-failure captures remain open evidence gaps.

This document records the failure tests captured for the OSPF triangle built in
Phase 1.


## Executive Summary

The captured tests prove that the OSPF triangle can survive the tested loss of
the `R1` to `R2` transit path. When VLAN `440` was removed either from the
router interface or from the OVS trunk, `R2` stopped using the direct path to
`R1` and rerouted traffic through `R3`.

Key findings:

- The baseline OSPF state is healthy: all three routers have full OSPFv2 and
  OSPFv3 adjacencies on the expected transit VLANs.
- `R2` learned the default route from `R1` through OSPFv2 and OSPFv3.
- During the `R1` to `R2` link failure, `R2` changed the next hop for
  `10.10.0.0/24`, `fd14:ca46:3864:a::/64`, `0.0.0.0/0`, and `::/0` from `R1`
  to `R3`.
- During the OVS VLAN loss test, `tap62` no longer carried VLAN `440`, and the
  network again converged through `R3`.
- The data-plane evidence confirms rerouting: ping TTL changed from `62` to
  `61`, which shows that the alternate path added one router hop.
- FRR restart and full router reboot on `R2` were also validated. Both caused
  expected control-plane interruption, then recovered to full OSPF adjacency.
- Performance stayed usable after convergence, but the alternate path increased
  latency and reduced throughput, especially for IPv6 throughput.

## Evidence Index

| Area | Status | Evidence |
| --- | --- | --- |
| OSPFv2 neighbors | OK | `R1`, `R2`, and `R3` show full IPv4 OSPF adjacencies. |
| OSPFv3 neighbors | OK | `R1`, `R2`, and `R3` show full IPv6 OSPF adjacencies. |
| OSPF routes | OK | Hosting VLANs and transit VLANs are present in OSPF route tables. |
| Default route propagation | OK | `R2` and `R3` learn default routes originated by `R1`. |
| Container baseline traffic | OK | Inter-router hosting traffic and external traffic have `0%` packet loss before failure. |
| `R1` to `R2` router-side link failure | OK | `R2` reroutes to `R1` networks and default route through `R3`. |
| FRR restart on `R2` | OK | FRR restarts cleanly; OSPF adjacencies return. |
| Router reboot on `R2` | OK | VM reboots; FRR returns; OSPF neighbors and routes are restored. |
| OVS VLAN `440` loss on `tap62` | OK | VLAN is removed from trunk, routes fail over, then recover after restore. |
| Latency and jitter | OK | Normal, failed, converged, and restored states were measured with timestamped ping. |
| Throughput | OK | IPv4 and IPv6 `iperf3` results were captured before, during, and after failure. |


## Scope And Objectives

Phase 2 validates controlled failure behavior for the Phase 1 routing
foundation. The objective is not only to show that OSPF neighbors return, but
also to prove what happens to real traffic, next-hop selection, default routes,
latency, and throughput during and after a failure.

The report covers these captured scenarios:

- baseline OSPFv2, OSPFv3, route, and container traffic validation,
- router-side shutdown of the `R1` to `R2` transit subinterface,
- FRR restart on `R2`,
- full VM reboot of `R2`,
- OVS-side loss of VLAN `440` on the `tap62` trunk,
- latency, jitter, packet-loss, and throughput measurements around the
  `R1` to `R2` failure path.

The report does not claim full triangle failure coverage yet. The direct
`R1` to `R3` and `R2` to `R3` link-failure captures still need to be collected
for a completely symmetric Phase 2 evidence set.

## Test Topology

The Phase 2 tests use the Phase 1 OSPF triangle.

| Link | VLAN | R1 interface | R2 interface | R3 interface |
| --- | ---: | --- | --- | --- |
| `R1` to `R2` | `440` | `enp0s1.440`, `10.44.0.1` | `enp0s1.440`, `10.44.0.2` | |
| `R1` to `R3` | `441` | `enp0s1.441`, `10.44.1.1` | | `enp0s1.441`, `10.44.1.3` |
| `R2` to `R3` | `442` | | `enp0s1.442`, `10.44.2.2` | `enp0s1.442`, `10.44.2.3` |

Hosting networks:

| Router | VLAN | IPv4 prefix | IPv6 prefix |
| --- | ---: | --- | --- |
| `R1` | `10` | `10.10.0.0/24` | `fd14:ca46:3864:a::/64` |
| `R2` | `20` | `10.20.0.0/24` | `fd14:ca46:3864:14::/64` |
| `R3` | `30` | `10.30.0.0/24` | `fd14:ca46:3864:1e::/64` |

Management addresses:

| Router | Management IPv4 | Management IPv6 |
| --- | --- | --- |
| `R1` | `10.99.0.1` | `fd14:ca46:3864:99::1` |
| `R2` | `10.99.0.2` | `fd14:ca46:3864:99::2` |
| `R3` | `10.99.0.3` | `fd14:ca46:3864:99::3` |

## Measurement Method

The tests used the same method as the Phase 2 tutorial:

- verify OSPF neighbors before the failure,
- start timestamped traffic with `ping -D -i 0.2`,
- trigger a controlled failure,
- capture route and neighbor changes,
- restore the failed component,
- verify the routing table and data plane after convergence.

For performance, the test used:

```console
incus exec c0 -- ping -D -i 0.2 -c 100 10.10.0.169
incus exec c0 -- iperf3 -c 10.10.0.169 -t 20
incus exec c0 -- iperf3 -6 -c fd14:ca46:3864:a:1266:6aff:fe8a:f053 -t 20
```

## Result Summary

| Test | Failure trigger | Main routing result | Traffic impact | Recovery result |
| --- | --- | --- | --- | --- |
| Baseline | None | All expected OSPFv2 and OSPFv3 neighbors full; default routes learned from `R1`. | `0%` loss for baseline container and external pings. | Not applicable. |
| `R1` to `R2` router-side link failure | `R2` interface `enp0s1.440` down | `R2` moved `R1` prefixes and default routes from VLAN `440` to next hop `R3` on VLAN `442`. | Path changed from `ttl=62` to `ttl=61`; performance test saw `1%` packet loss during failure. | Direct `R1` adjacency returned after `enp0s1.440` was restored. |
| FRR restart on `R2` | `systemctl restart frr` | OSPF routes were removed during daemon restart, then adjacencies reformed. | Captured ping gap was about `5.9 s`. | FRR returned active and OSPF converged again. |
| `R2` VM reboot | `sudo reboot` | Router disappeared, then FRR restarted automatically after boot. | Captured traffic outage to the `R2` hosting network was about `144 s`. | OSPFv2, OSPFv3, and routes returned after reboot. |
| OVS VLAN `440` loss | Removed VLAN `440` from `tap62` trunk | `R2` again rerouted `R1` prefixes and default route through `R3`. | Route failover confirmed; exact packet-loss timing was not captured in this test. | VLAN restore returned the direct adjacency. |

## Convergence And Impact Assessment

| Area | Finding |
| --- | --- |
| Control plane | OSPF detected the tested link and VLAN failures, removed the failed adjacency, and selected the alternate path through the remaining side of the triangle. |
| Data plane | Container traffic remained usable after convergence. The `ttl` change from `62` to `61` proves packets took one additional router hop through `R3`. |
| Packet loss | Baseline tests showed `0%` loss. The measured failure-window ping test showed `1%` loss during `R1` to `R2` failover and `0%` loss after convergence. |
| Latency | Average RTT increased from about `0.93 ms` in the normal topology to about `1.81 ms` after failover through `R3`. |
| Throughput | IPv4 throughput dropped from `28.1 Gbits/sec` to `23.0 Gbits/sec`; IPv6 throughput dropped from `25.5 Gbits/sec` to `15.6 Gbits/sec` on the failed, converged path. |
| Service restart | Restarting FRR on `R2` caused a short, expected route and adjacency interruption. The measured traffic gap was about `5.9 s`. |
| Router reboot | A full `R2` reboot caused a much larger outage for networks behind `R2`. The captured successful-reply gap was about `144 s`. |

## Baseline Proof

### OSPF Neighbors

The baseline shows two full neighbors per router for both OSPFv2 and OSPFv3.

```console
R1# show ip ospf neighbor
2.0.0.4  Full/Backup  10.44.0.2  enp0s1.440
3.0.0.4  Full/Backup  10.44.1.3  enp0s1.441

R2# show ip ospf neighbor
1.0.0.4  Full/DR      10.44.0.1  enp0s1.440
3.0.0.4  Full/Backup  10.44.2.3  enp0s1.442

R3# show ip ospf neighbor
1.0.0.4  Full/DR      10.44.1.1  enp0s1.441
2.0.0.4  Full/DR      10.44.2.2  enp0s1.442
```

```console
R1# show ipv6 ospf6 neighbor
2.0.0.6  Full/BDR  enp0s1.440[DR]
3.0.0.6  Full/BDR  enp0s1.441[DR]

R2# show ipv6 ospf6 neighbor
1.0.0.6  Full/DR   enp0s1.440[BDR]
3.0.0.6  Full/BDR  enp0s1.442[DR]

R3# show ipv6 ospf6 neighbor
1.0.0.6  Full/DR   enp0s1.441[BDR]
2.0.0.6  Full/DR   enp0s1.442[BDR]
```

### Baseline Routes

`R1` reaches `R2` and `R3` hosting networks through the expected direct transit
links.

```console
R1# show ip route
O>* 10.20.0.0/24 [110/80] via 10.44.0.2, enp0s1.440
O>* 10.30.0.0/24 [110/80] via 10.44.1.3, enp0s1.441

R1# show ipv6 route
O>* fd14:ca46:3864:14::/64 [110/80] via fe80::baad:caff:fefe:3f, enp0s1.440
O>* fd14:ca46:3864:1e::/64 [110/80] via fe80::1b9:3, enp0s1.441
```

`R2` reaches `R1`, `R3`, and the default route through OSPF.

```console
R2# show ip route
O>* 0.0.0.0/0     [110/10] via 10.44.0.1, enp0s1.440
O>* 10.10.0.0/24 [110/80] via 10.44.0.1, enp0s1.440
O>* 10.30.0.0/24 [110/80] via 10.44.2.3, enp0s1.442

R2# show ipv6 route
O>* ::/0                         [110/10] via fe80::1b8:1, enp0s1.440
O>* fd14:ca46:3864:a::/64        [110/80] via fe80::1b8:1, enp0s1.440
O>* fd14:ca46:3864:1e::/64       [110/80] via fe80::1ba:3, enp0s1.442
```

`R3` reaches `R1`, `R2`, and the default route through OSPF.

```console
R3# show ip route
O>* 0.0.0.0/0     [110/10] via 10.44.1.1, enp0s1.441
O>* 10.10.0.0/24 [110/80] via 10.44.1.1, enp0s1.441
O>* 10.20.0.0/24 [110/80] via 10.44.2.2, enp0s1.442

R3# show ipv6 route
O>* ::/0                         [110/10] via fe80::1b9:1, enp0s1.441
O>* fd14:ca46:3864:a::/64        [110/80] via fe80::1b9:1, enp0s1.441
O>* fd14:ca46:3864:14::/64       [110/80] via fe80::baad:caff:fefe:3f, enp0s1.442
```

### Baseline Container Traffic

The baseline ping tests show clean packet delivery before failure testing.

| Source | Destination | Result | RTT average |
| --- | --- | --- | ---: |
| `R2` container `c0` | `R1` container `10.10.0.93` | `50/50`, `0%` loss | `0.998 ms` |
| `R3` container `c0` | `R1` container `10.10.0.76` | `50/50`, `0%` loss | `0.984 ms` |
| `R2` container `c0` | `9.9.9.9` | `50/50`, `0%` loss | `17.221 ms` |
| `R2` container `c0` | `2620:fe::fe` | `50/50`, `0%` loss | `37.406 ms` |

```console
--- 10.10.0.93 ping statistics ---
50 packets transmitted, 50 received, 0% packet loss
rtt min/avg/max/mdev = 0.710/0.998/3.204/0.323 ms

--- 10.10.0.76 ping statistics ---
50 packets transmitted, 50 received, 0% packet loss
rtt min/avg/max/mdev = 0.795/0.984/2.925/0.282 ms

--- 9.9.9.9 ping statistics ---
50 packets transmitted, 50 received, 0% packet loss
rtt min/avg/max/mdev = 16.496/17.221/19.586/0.565 ms

--- 2620:fe::fe ping statistics ---
50 packets transmitted, 50 received, 0% packet loss
rtt min/avg/max/mdev = 36.198/37.406/41.057/0.767 ms
```

## Scenario 1 - `R1` To `R2` Link Failure

Target link: VLAN `440`, `R1` to `R2`.

Failure method: shut down `R2` subinterface `enp0s1.440`.

Expected alternate path:

```text
R2 -> VLAN 442 -> R3 -> VLAN 441 -> R1
```

### Baseline Before Failure

Before the failure, `R1` reached `R2` directly through VLAN `440`, and `R2`
reached `R1` and the default route directly through VLAN `440`.

```console
R1# show ip route 10.20.0.0/24
* 10.44.0.2, via enp0s1.440

R1# show ipv6 route fd14:ca46:3864:14::/64
* fe80::baad:caff:fefe:3f, via enp0s1.440

R2# show ip route 10.10.0.0/24
* 10.44.0.1, via enp0s1.440

R2# show ip route 0.0.0.0/0
* 10.44.0.1, via enp0s1.440

R2# show ipv6 route fd14:ca46:3864:a::/64
* fe80::1b8:1, via enp0s1.440

R2# show ipv6 route ::/0
* fe80::1b8:1, via enp0s1.440
```

### Failure Window

Failure command:

```console
date -Ins
sudo ip link set enp0s1.440 down
date -Ins

2026-05-30T18:07:57,171000993+02:00
2026-05-30T18:07:57,230359639+02:00
```

After the cut, `R2` kept only its `R3` adjacency.

```console
R2# show ip ospf neighbor
3.0.0.4  Full/Backup  10.44.2.3  enp0s1.442

R2# show ipv6 ospf6 neighbor
3.0.0.6  Full/BDR  enp0s1.442[DR]
```

The affected routes moved to `R3`.

```console
R2# show ip route 10.10.0.0/24
Routing entry for 10.10.0.0/24
  Known via "ospf", distance 110, metric 120, best
  * 10.44.2.3, via enp0s1.442

R2# show ip route 0.0.0.0/0
Routing entry for 0.0.0.0/0
  Known via "ospf", distance 110, metric 10, best
  * 10.44.2.3, via enp0s1.442

R2# show ipv6 route fd14:ca46:3864:a::/64
Routing entry for fd14:ca46:3864:a::/64
  Known via "ospf6", distance 110, metric 120, best
  * fe80::1ba:3, via enp0s1.442

R2# show ipv6 route ::/0
Routing entry for ::/0
  Known via "ospf6", distance 110, metric 10, best
  * fe80::1ba:3, via enp0s1.442
```

The continuous ping stream shows the path change. Before convergence, replies
had `ttl=62`; after convergence, replies had `ttl=61`, proving the path gained
one routed hop through `R3`.

```console
[1780157276.865150] 64 bytes from 10.10.0.169: icmp_seq=829 ttl=62 time=0.969 ms
[1780157277.065499] 64 bytes from 10.10.0.169: icmp_seq=830 ttl=62 time=0.957 ms
[1780157277.267274] 64 bytes from 10.10.0.169: icmp_seq=831 ttl=61 time=2.42 ms
[1780157277.467680] 64 bytes from 10.10.0.169: icmp_seq=832 ttl=61 time=2.00 ms
```

### Recovery

Restore command:

```console
date -Ins
sudo ip link set enp0s1.440 up
date -Ins

2026-05-30T18:12:30,658261754+02:00
2026-05-30T18:12:30,716995936+02:00
```

After restoration, both `R1` and `R3` were full neighbors again on `R2`.

```console
R2# show ip ospf neighbor
3.0.0.4  Full/Backup  10.44.2.3  enp0s1.442
1.0.0.4  Full/DR      10.44.0.1  enp0s1.440

R2# show ipv6 ospf6 neighbor
1.0.0.6  Full/DR   enp0s1.440[BDR]
3.0.0.6  Full/BDR  enp0s1.442[DR]
```

The data-plane evidence shows the route eventually returned to the direct path:

```console
[1780157560.164824] 64 bytes from 10.10.0.169: icmp_seq=2238 ttl=62 time=1.02 ms
[1780157560.365176] 64 bytes from 10.10.0.169: icmp_seq=2239 ttl=62 time=0.943 ms
```

### FRR Journal Evidence

```console
May 30 18:07:57 R2 ospfd[1022]: AdjChg: Nbr 1.0.0.4, NbrIP 10.44.0.1 on enp0s1.440: Full -> Deleted (KillNbr)
May 30 18:12:35 R2 ospfd[1022]: AdjChg: Nbr 1.0.0.4, NbrIP 10.44.0.1 on enp0s1.440: Down -> Init (HelloReceived)
May 30 18:12:35 R2 ospfd[1022]: AdjChg: Nbr 1.0.0.4, NbrIP 10.44.0.1 on enp0s1.440: Exchange -> Full (ExchangeDone)
May 30 18:12:35 R2 ospf6d[1026]: AdjChg: Nbr 1.0.0.6 on enp0s1.440: Down -> Init (HelloReceived)
May 30 18:12:36 R2 ospf6d[1026]: AdjChg: Nbr 1.0.0.6 on enp0s1.440: ExChange -> Full (ExchangeDone)
```

Conclusion: the `R1` to `R2` link failure was handled correctly. `R2` lost the
direct adjacency, rerouted through `R3`, preserved reachability to `R1`
networks and default routes, then returned to the direct path after recovery.

## Scenario 2 - FRR Restart On `R2`

Failure method: restart `frr.service` on `R2`.

### Restart Window

```console
date -Ins
sudo systemctl restart frr
date -Ins

2026-05-30T18:23:04,442071692+02:00
2026-05-30T18:23:05,198437393+02:00
```

`systemctl` reported FRR active immediately after the restart.

```console
frr.service - FRRouting
Loaded: loaded (/usr/lib/systemd/system/frr.service; enabled)
Active: active (running) since Sat 2026-05-30 18:23:05 CEST
Status: "FRR Operational"

watchfrr -d mgmtd zebra ospfd ospf6d staticd
mgmtd
zebra
ospfd
ospf6d
staticd
```

### Control-Plane Evidence

The journal confirms that FRR removed OSPF routes during shutdown, then brought
the daemons and adjacencies back.

```console
May 30 18:23:04 R2 systemd[1]: Stopping frr.service - FRRouting...
May 30 18:23:04 R2 zebra[1014]: client 34 disconnected 7 ospf routes removed from the rib
May 30 18:23:04 R2 ospfd[1022]: AdjChg: Nbr 3.0.0.4 on enp0s1.442: Full -> Deleted (KillNbr)
May 30 18:23:04 R2 ospfd[1022]: AdjChg: Nbr 1.0.0.4 on enp0s1.440: Full -> Deleted (KillNbr)
May 30 18:23:05 R2 watchfrr[13982]: all daemons up, doing startup-complete notify
May 30 18:23:05 R2 systemd[1]: Started frr.service - FRRouting.
May 30 18:23:05 R2 ospfd[14002]: AdjChg: Nbr 1.0.0.4 on enp0s1.440: Exchange -> Full (ExchangeDone)
May 30 18:23:10 R2 ospfd[14002]: AdjChg: Nbr 3.0.0.4 on enp0s1.442: Loading -> Full (LoadingDone)
May 30 18:23:10 R2 ospf6d[14005]: AdjChg: Nbr 3.0.0.6 on enp0s1.442: Loading -> Full (LoadingDone)
May 30 18:23:50 R2 ospf6d[14005]: AdjChg: Nbr 1.0.0.6 on enp0s1.440: ExChange -> Full (ExchangeDone)
```

### Data-Plane Evidence

The ping stream shows a short interruption during the FRR restart. The last
reply before the gap was sequence `173`; the next captured reply was sequence
`202`.

```console
[1780158184.541842] 64 bytes from 10.20.0.89: icmp_seq=173 ttl=62 time=0.795 ms
[1780158190.455491] 64 bytes from 10.20.0.89: icmp_seq=202 ttl=62 time=1.07 ms
```

Measured from the timestamps, the visible traffic gap was about `5.9 s`.

Conclusion: restarting FRR interrupts learned routes and adjacencies as
expected, but the service returns cleanly and OSPF converges again.

## Scenario 3 - Router Reboot On `R2`

Failure method: reboot the `R2` VM.

### Reboot Window

```console
date -Ins
sudo reboot

2026-05-30T18:28:28,770602581+02:00
Connection to 10.99.0.2 closed by remote host.
```

`R2` was reachable again by SSH and reported a short uptime.

```console
etu@R2:~$ uptime
18:30:10 up 1 min, 1 user, load average: 0.00, 0.00, 0.00
```

FRR restarted automatically after boot.

```console
frr.service - FRRouting
Active: active (running) since Sat 2026-05-30 18:28:52 CEST
Status: "FRR Operational"
```

### Recovery State

OSPFv2 and OSPFv3 returned to full adjacency.

```console
R2# show ip ospf neighbor
1.0.0.4  Full/DR  10.44.0.1  enp0s1.440
3.0.0.4  Full/DR  10.44.2.3  enp0s1.442

R2# show ipv6 ospf6 neighbor
1.0.0.6  Full/DR  enp0s1.440[BDR]
3.0.0.6  Full/DR  enp0s1.442[BDR]
```

Routes returned after the reboot.

```console
R2# show ip route
O>* 0.0.0.0/0     [110/10] via 10.44.0.1, enp0s1.440
O>* 10.10.0.0/24 [110/80] via 10.44.0.1, enp0s1.440
O>* 10.30.0.0/24 [110/80] via 10.44.2.3, enp0s1.442

R2# show ipv6 route
O>* ::/0                         [110/10] via fe80::1b8:1, enp0s1.440
O>* fd14:ca46:3864:a::/64        [110/80] via fe80::1b8:1, enp0s1.440
O>* fd14:ca46:3864:1e::/64       [110/80] via fe80::1ba:3, enp0s1.442
```

### FRR Journal Evidence

```console
May 30 18:28:33 R2 systemd[1]: Stopping frr.service - FRRouting...
May 30 18:28:33 R2 ospfd[14002]: AdjChg: Nbr 1.0.0.4 on enp0s1.440: Full -> Deleted (KillNbr)
May 30 18:28:33 R2 ospfd[14002]: AdjChg: Nbr 3.0.0.4 on enp0s1.442: Full -> Deleted (KillNbr)
-- Boot abbc7e5baf8a4a59a7f663f601646aee --
May 30 18:28:52 R2 systemd[1]: Starting frr.service - FRRouting...
May 30 18:28:52 R2 watchfrr[1037]: all daemons up, doing startup-complete notify
May 30 18:28:52 R2 systemd[1]: Started frr.service - FRRouting.
May 30 18:28:56 R2 ospf6d[1114]: AdjChg: Nbr 1.0.0.6 on enp0s1.440: ExChange -> Full (ExchangeDone)
May 30 18:29:00 R2 ospf6d[1114]: AdjChg: Nbr 3.0.0.6 on enp0s1.442: Loading -> Full (LoadingDone)
May 30 18:29:32 R2 ospfd[1110]: AdjChg: Nbr 3.0.0.4 on enp0s1.442: Loading -> Full (LoadingDone)
May 30 18:29:37 R2 ospfd[1110]: AdjChg: Nbr 1.0.0.4 on enp0s1.440: Exchange -> Full (ExchangeDone)
```

### Data-Plane Evidence

Traffic to a container behind `R2` was interrupted during the reboot. The last
captured successful reply before interruption was at timestamp `1780158512.309`;
the next successful reply was at `1780158656.259`, giving a visible outage of
about `144 s` in the captured stream.

```console
[1780158512.309421] 64 bytes from 10.20.0.89: icmp_seq=544 ttl=62 time=0.780 ms
[1780158577.831799] From 10.44.1.3 icmp_seq=865 Time to live exceeded
[1780158585.732188] From 10.44.0.2 icmp_seq=889 Destination Host Unreachable
[1780158656.259953] 64 bytes from 10.20.0.89: icmp_seq=1250 ttl=62 time=1.58 ms
```

Conclusion: a full `R2` reboot is disruptive for traffic that terminates behind
`R2`, but the router returns automatically, FRR starts, adjacencies reform, and
routes are restored.

## Scenario 4 - VLAN `440` Loss On The OVS Switch

Failure method: remove VLAN `440` from the `tap62` trunk on the hypervisor.

This simulates a switch-side configuration problem instead of a router-side
interface shutdown.

### Failure Window

```console
date -Ins
sudo ovs-vsctl remove port tap62 trunks 440
date -Ins
sudo ovs-vsctl list port tap62

2026-06-04T18:08:09,472257601+02:00
2026-06-04T18:08:09,675284013+02:00
trunks : [99, 360, 441]
vlan_mode : trunk
```

After VLAN `440` was removed from `tap62`, `R2` rerouted traffic toward `R1`
through `R3`.

```console
R2# show ip route 10.10.0.0/24
Routing entry for 10.10.0.0/24
  Known via "ospf", distance 110, metric 120, best
  * 10.44.2.3, via enp0s1.442

R2# show ip route 0.0.0.0/0
Routing entry for 0.0.0.0/0
  Known via "ospf", distance 110, metric 10, best
  * 10.44.2.3, via enp0s1.442
```

### Recovery

```console
date -Ins
sudo ovs-vsctl add port tap62 trunks 440
date -Ins
sudo ovs-vsctl list port tap62

2026-06-04T18:10:10,642301725+02:00
2026-06-04T18:10:10,844018872+02:00
trunks : [99, 360, 440, 441]
vlan_mode : trunk
```

After restoration, the `R1` to `R2` adjacency returned.

```console
R2# show ip ospf neighbor
1.0.0.4  Full/Backup  10.44.0.1  enp0s1.440
3.0.0.4  Full/DR      10.44.2.3  enp0s1.442

R2# show ipv6 ospf6 neighbor
1.0.0.6  Full/BDR  enp0s1.440[DR]
3.0.0.6  Full/DR   enp0s1.442[BDR]

R1# show ip ospf neighbor
2.0.0.4  Full/DR  10.44.0.2  enp0s1.440
3.0.0.4  Full/DR  10.44.1.3  enp0s1.441
```

### Journal Evidence

The R2 journal confirms the adjacency drop and recovery. Note that the R2
journal clock in this capture is about two hours ahead of the hypervisor shell
timestamps, so the event ordering is the reliable part of this proof.

```console
Jun 04 20:08:42 R2 ospfd[1117]: AdjChg: Nbr 1.0.0.4 on enp0s1.440: Full -> Deleted
Jun 04 20:08:44 R2 ospf6d[1120]: AdjChg: Nbr 1.0.0.6 on enp0s1.440: Full -> Deleted
Jun 04 20:10:15 R2 ospfd[1117]: AdjChg: Nbr 1.0.0.4 on enp0s1.440: Exchange -> Full
Jun 04 20:10:16 R2 ospf6d[1120]: AdjChg: Nbr 1.0.0.6 on enp0s1.440: ExChange -> Full
```

Conclusion: losing VLAN `440` from the OVS trunk creates the same operational
impact as the router-side link cut. OSPF detects the loss, reroutes through
`R3`, and returns to the direct path when the VLAN is restored.

## Performance Results

Performance was measured between `R2` container `c0` and `R1` container `c0`
at `10.10.0.169` / `fd14:ca46:3864:a:1266:6aff:fe8a:f053`.

### Latency And Jitter

| State | Path evidence | Packet loss | RTT min/avg/max/mdev |
| --- | --- | ---: | --- |
| Normal topology | `ttl=62`, direct `R2 -> R1` | `0%` | `0.751/0.930/2.742/0.267 ms` |
| During failure | `ttl` changes from `62` to `61` | `1%` | `0.732/1.675/2.641/0.331 ms` |
| Failed, converged topology | `ttl=61`, path via `R3` | `0%` | `1.638/1.811/3.709/0.200 ms` |
| During restoration | `ttl` changes from `61` to `62` | `0%` | `0.756/1.240/3.935/0.436 ms` |

Representative proof:

```console
Normal:
100 packets transmitted, 100 received, 0% packet loss
rtt min/avg/max/mdev = 0.751/0.930/2.742/0.267 ms

During failure:
100 packets transmitted, 99 received, 1% packet loss
rtt min/avg/max/mdev = 0.732/1.675/2.641/0.331 ms

Failed, converged:
100 packets transmitted, 100 received, 0% packet loss
rtt min/avg/max/mdev = 1.638/1.811/3.709/0.200 ms

During restoration:
100 packets transmitted, 100 received, 0% packet loss
rtt min/avg/max/mdev = 0.756/1.240/3.935/0.436 ms
```

The latency results match the expected topology behavior: the failed path is
one router hop longer, so average RTT rises from about `0.93 ms` to about
`1.81 ms` after convergence.

### Throughput

| State | Protocol | Transfer | Bitrate | Retransmits |
| --- | --- | ---: | ---: | ---: |
| Normal topology | IPv4 | `65.4 GBytes` | `28.1 Gbits/sec` | `45` |
| Normal topology | IPv6 | `59.4 GBytes` | `25.5 Gbits/sec` | `90` |
| Failed, converged topology | IPv4 | `53.6 GBytes` | `23.0 Gbits/sec` | `2958` |
| Failed, converged topology | IPv6 | `36.3 GBytes` | `15.6 Gbits/sec` | `664` |
| Restored topology | IPv4 | `61.7 GBytes` | `26.5 Gbits/sec` | `955` |
| Restored topology | IPv6 | `61.9 GBytes` | `26.6 Gbits/sec` | `2439` |

Representative proof:

```console
Normal IPv4:
[  5] 0.00-20.00 sec  65.4 GBytes  28.1 Gbits/sec    45 sender
[  5] 0.00-20.00 sec  65.3 GBytes  28.1 Gbits/sec       receiver

Normal IPv6:
[  5] 0.00-20.00 sec  59.4 GBytes  25.5 Gbits/sec    90 sender
[  5] 0.00-20.00 sec  59.4 GBytes  25.5 Gbits/sec       receiver

Failed IPv4:
[  5] 0.00-20.00 sec  53.6 GBytes  23.0 Gbits/sec  2958 sender
[  5] 0.00-20.00 sec  53.6 GBytes  23.0 Gbits/sec       receiver

Failed IPv6:
[  5] 0.00-20.00 sec  36.3 GBytes  15.6 Gbits/sec   664 sender
[  5] 0.00-20.00 sec  36.3 GBytes  15.6 Gbits/sec       receiver

Restored IPv4:
[  5] 0.00-20.00 sec  61.7 GBytes  26.5 Gbits/sec   955 sender
[  5] 0.00-20.00 sec  61.7 GBytes  26.5 Gbits/sec       receiver

Restored IPv6:
[  5] 0.00-20.00 sec  61.9 GBytes  26.6 Gbits/sec  2439 sender
[  5] 0.00-20.00 sec  61.9 GBytes  26.6 Gbits/sec       receiver
```

Conclusion: throughput remains high after convergence, but the failed path is
less efficient. IPv4 drops from `28.1 Gbits/sec` to `23.0 Gbits/sec`; IPv6 drops
from `25.5 Gbits/sec` to `15.6 Gbits/sec`.

## Final Conclusion

The captured Phase 2 evidence proves that the OSPF triangle has working
resilience for the tested `R1` to `R2` failure modes. The network detects the
loss of VLAN `440`, moves traffic through `R3`, preserves reachability after
convergence, and restores the direct path when the failure is repaired.

Phase 2 is strong enough to support the next observability phase because it has
a known, repeatable failure scenario: loss of VLAN `440` between `R1` and `R2`.
That scenario can now be replayed in Phase 3 to validate Prometheus metrics,
FRR logs, Loki queries, Grafana panels, and OSPF neighbor-loss alerts.

Remaining limitations are intentionally documented:

- direct `R1` to `R3` link-failure evidence is still missing,
- direct `R2` to `R3` link-failure evidence is still missing,
- OVS-side VLAN `440` loss has route and journal evidence, but not a precise
  packet-loss timing capture,
- no packet captures were saved because command output was sufficient for the
  current failure proof.
