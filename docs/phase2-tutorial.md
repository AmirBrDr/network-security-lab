# Phase 2 Tutorial - Failure Simulation and Network Testing

## Summary

This tutorial extends the completed OSPF foundation with controlled failure tests.
The goal is to prove that the `R1`/`R2`/`R3` triangle can keep routing traffic when
a link, a routing daemon, a router, or a VLAN fails.

The method follows the same practical style as the reference InetDoc OSPF lab:
each section starts from a concrete question, gives the commands to run, explains
what must be observed, and ends with evidence to save.

Phase 2 covers Monday, June 8, 2026 to Friday, June 12, 2026 in the project
calendar.

Reference support:

- InetDoc OSPF TP: <https://inetdoc.net/travaux_pratiques/interco_05.ospf/>
- Local roadmap: [roadmap.md](roadmap.md)
- Local calendar: [project-calendar.md](project-calendar.md)
- Addressing plan: [addressing-plan.md](addressing-plan.md)
- Existing OSPF proofs: [proofs.md](proofs.md)

## Table of Contents

1. Objectives
2. Topology Used During The Tests
3. Preparation And Evidence Layout
4. Baseline Capture
5. Measurement Method
6. Scenario 1 - R1 To R2 Link Failure
7. Scenario 2 - R2 To R3 Link Failure
8. Scenario 3 - R1 To R3 Link Failure
9. Scenario 4 - FRR Restart
10. Scenario 5 - Router Reboot
11. Scenario 6 - VLAN Loss On The OVS Switch
12. Latency, Throughput, And Jitter Tests
13. Scenario Report Template
14. Final Phase 2 Deliverables
15. Troubleshooting Notes

## 1. Objectives

After completing this tutorial, the lab operator should be able to:

1. Capture a clean OSPFv2 and OSPFv3 baseline before any failure.
2. Simulate failures on the three transit VLANs of the OSPF triangle.
3. Measure packet loss, data-plane interruption time, and route convergence time.
4. Compare routing tables before, during, and after each failure.
5. Restart FRRouting and reboot a router while collecting useful evidence.
6. Document the resilience limits of the lab honestly and reproducibly.

The expected result is not "zero packet loss". The expected result is a measured
and explainable behavior:

- which traffic was interrupted,
- how long it was interrupted,
- which alternate path was selected,
- which logs and routing-table changes prove the recovery.

## 2. Topology Used During The Tests

The routing topology is the Phase 1 OSPF triangle.

| Link | VLAN | R1 side | R2 side | R3 side |
| --- | ---: | --- | --- | --- |
| `R1` to `R2` | `440` | `enp0s1.440` / `10.44.0.1` / `fe80::1b8:1` | `enp0s1.440` / `10.44.0.2` / `fe80::1b8:2` | |
| `R1` to `R3` | `441` | `enp0s1.441` / `10.44.1.1` / `fe80::1b9:1` | | `enp0s1.441` / `10.44.1.3` / `fe80::1b9:3` |
| `R2` to `R3` | `442` | | `enp0s1.442` / `10.44.2.2` / `fe80::1ba:2` | `enp0s1.442` / `10.44.2.3` / `fe80::1ba:3` |

The management and evidence access network is VLAN `99`.

| System | TAP | Management address |
| --- | --- | --- |
| `R1` | `tap62` | `10.99.0.1`, `fd14:ca46:3864:99::1` |
| `R2` | `tap63` | `10.99.0.2`, `fd14:ca46:3864:99::2` |
| `R3` | `tap64` | `10.99.0.3`, `fd14:ca46:3864:99::3` |
| `monitoring` | `tap65` | `10.99.0.65`, `fd14:ca46:3864:99::65` |
| `management` | `tap66` | `10.99.0.66`, `fd14:ca46:3864:99::66` |

The hosting networks are passive OSPF interfaces.

| Router | Hosting interface | IPv4 prefix | IPv6 prefix |
| --- | --- | --- | --- |
| `R1` | `vlan10` | `10.10.0.0/24` | `fd14:ca46:3864:a::/64` |
| `R2` | `vlan20` | `10.20.0.0/24` | `fd14:ca46:3864:14::/64` |
| `R3` | `vlan30` | `10.30.0.0/24` | `fd14:ca46:3864:1e::/64` |

Q1.

Which traffic is the most useful for failure testing?

Use traffic that crosses the OSPF triangle and traffic that uses the default route.
For example:

- container behind `R2` to container behind `R1`,
- container behind `R3` to container behind `R1`,
- container behind `R2` to `9.9.9.9`,
- container behind `R3` to `2620:fe::fe`,
- router to router transit pings for direct link checks.

This gives two views:

- the control plane: OSPF neighbors, LSDB, and route changes,
- the data plane: real packets from hosted networks.

## 3. Preparation And Evidence Layout

Q2.

How should the evidence for Phase 2 be organized?

Create one evidence directory for the phase, then one directory per scenario.

```console
mkdir -p evidence/phase2/00-baseline
mkdir -p evidence/phase2/01-r1-r2-link
mkdir -p evidence/phase2/02-r2-r3-link
mkdir -p evidence/phase2/03-r1-r3-link
mkdir -p evidence/phase2/04-frr-restart
mkdir -p evidence/phase2/05-router-reboot
mkdir -p evidence/phase2/06-vlan-loss
mkdir -p evidence/phase2/07-performance
```

If the repository should stay light, keep large packet captures and screenshots
outside Git, then reference them from the final report.

Q3.

Which terminals are useful during each test?

Use at least four terminals:

| Terminal | Host | Role |
| --- | --- | --- |
| A | traffic source router or container host | continuous `ping` with timestamps |
| B | router under observation | OSPF neighbors and routes before/during/after |
| C | router or hypervisor | failure command and restore command |
| D | router | `journalctl -u frr -f` or `tcpdump` |

For clean evidence, start a shell transcript before running commands.

```console
script -a evidence/phase2/00-baseline/R1-baseline.txt
```

Exit the transcript with `exit` or `Ctrl-D`.

Q4.

Which failure method should be used first?

Use router interface shutdowns for the first pass. They are simple, reversible,
and do not permanently edit Netplan or FRR configuration.

Example:

```console
sudo ip link set enp0s1.440 down
sudo ip link set enp0s1.440 up
```

Use OVS trunk changes later for the VLAN loss scenario.

Important measurement note: shutting only one VLAN subinterface is a one-sided
failure. The local router sees the interface go down immediately, while the
remote router may wait for the OSPF dead timer before declaring the neighbor
down. This is useful because it reveals real OSPF timer behavior. For the
cleanest data-plane measurement, shut the subinterface on the router that sends
the test traffic.

## 4. Baseline Capture

The baseline is the reference state used to compare all failures.
Do not skip it. A failure test without a before-state is only a story, not proof.

### 4.1 Verify The VMs And OVS Ports

Q5.

How do we verify that the hypervisor ports match the TAP plan?

On the hypervisor, inspect the OVS bridge and forwarding database.

```console
sudo ovs-vsctl show
sudo ovs-appctl fdb/show dsw-host
```

Expected ports:

| Port | Mode | VLANs |
| --- | --- | --- |
| `tap62` | trunk | `99`, `360`, `440`, `441` |
| `tap63` | trunk | `99`, `440`, `442` plus temporary VLAN `28` if still present |
| `tap64` | trunk | `99`, `441`, `442` plus temporary VLAN `28` if still present |
| `tap65` | access | `99` |
| `tap66` | access | `99` |

The temporary VLAN `28` on `R2` and `R3` is not part of the OSPF triangle.
If it is still present in `switch.yaml`, note it in the evidence and confirm
that OSPF testing only uses VLANs `440`, `441`, and `442`.

Save the output.

```console
sudo ovs-vsctl show > evidence/phase2/00-baseline/ovs-vsctl-show.txt
sudo ovs-appctl fdb/show dsw-host > evidence/phase2/00-baseline/ovs-fdb-dsw-host.txt
```

### 4.2 Verify Forwarding And FRR State

Q6.

How do we confirm that each router is ready for a failure test?

Run these commands on `R1`, `R2`, and `R3`.

```console
hostname
ip -brief address
ip route
ip -6 route
sudo sysctl net.ipv4.ip_forward net.ipv6.conf.all.forwarding
systemctl --no-pager status frr
vtysh -c "show daemons"
```

Expected result:

- `net.ipv4.ip_forward = 1`,
- `net.ipv6.conf.all.forwarding = 1`,
- `frr.service` is active,
- `zebra`, `ospfd`, `ospf6d`, `watchfrr`, and `staticd` are running.

If forwarding is disabled on `R2` or `R3`, fix it before testing. The older
proofs file notes that this command should be recaptured cleanly for the final
portfolio evidence.

### 4.3 Verify OSPF Neighbors

Q7.

How do we capture the OSPF control-plane baseline?

On each router:

```console
vtysh -c "show ip ospf neighbor"
vtysh -c "show ipv6 ospf6 neighbor"
vtysh -c "show ip ospf interface"
vtysh -c "show ipv6 ospf6 interface"
vtysh -c "show ip ospf database"
vtysh -c "show ipv6 ospf6 database"
```

Expected OSPFv2 neighbor relationships:

| Router | Expected OSPFv2 neighbors |
| --- | --- |
| `R1` | `2.0.0.4` on `enp0s1.440`, `3.0.0.4` on `enp0s1.441` |
| `R2` | `1.0.0.4` on `enp0s1.440`, `3.0.0.4` on `enp0s1.442` |
| `R3` | `1.0.0.4` on `enp0s1.441`, `2.0.0.4` on `enp0s1.442` |

Expected OSPFv3 neighbor relationships:

| Router | Expected OSPFv3 neighbors |
| --- | --- |
| `R1` | `2.0.0.6` on `enp0s1.440`, `3.0.0.6` on `enp0s1.441` |
| `R2` | `1.0.0.6` on `enp0s1.440`, `3.0.0.6` on `enp0s1.442` |
| `R3` | `1.0.0.6` on `enp0s1.441`, `2.0.0.6` on `enp0s1.442` |

### 4.4 Verify OSPF Routes

Q8.

Which routes prove that the OSPF triangle is complete before testing?

On each router, save the full routing table and targeted routes.

```console
vtysh -c "show ip route"
vtysh -c "show ipv6 route"
vtysh -c "show ip ospf route"
vtysh -c "show ipv6 ospf6 route"
```

Targeted IPv4 checks:

```console
vtysh -c "show ip route 10.10.0.0/24"
vtysh -c "show ip route 10.20.0.0/24"
vtysh -c "show ip route 10.30.0.0/24"
vtysh -c "show ip route 0.0.0.0/0"
```

Targeted IPv6 checks:

```console
vtysh -c "show ipv6 route fd14:ca46:3864:a::/64"
vtysh -c "show ipv6 route fd14:ca46:3864:14::/64"
vtysh -c "show ipv6 route fd14:ca46:3864:1e::/64"
vtysh -c "show ipv6 route ::/0"
```

Expected result:

- `R2` and `R3` learn `0.0.0.0/0` from `R1`.
- `R2` and `R3` learn `::/0` from `R1`.
- Each router sees the two remote hosting prefixes through OSPF.
- Hosting interfaces are passive and do not form OSPF neighbors.

### 4.5 Verify Container Addresses

Q9.

How do we select traffic sources and destinations?

On each router, list containers and choose one stable source per hosting network.

```console
incus ls
```

Write the selected addresses in the test notes.

| Router | Container | IPv4 | IPv6 |
| --- | --- | --- | --- |
| `R1` | | | |
| `R2` | | | |
| `R3` | | | |

If the container addresses changed since [proofs.md](proofs.md), use the current
addresses from `incus ls`.

### 4.6 Capture Baseline Latency

Q10.

How do we measure the baseline before a failure?

From one container behind `R2`, ping a container behind `R1`.

```console
incus exec c0 -- ping -D -i 0.2 -c 50 10.10.0.X
```

From one container behind `R3`, ping a container behind `R1`.

```console
incus exec c0 -- ping -D -i 0.2 -c 50 10.10.0.X
```

For default-route traffic, ping public resolver addresses from internal
containers.

```console
incus exec c0 -- ping -D -i 0.2 -c 50 9.9.9.9
incus exec c0 -- ping -6 -D -i 0.2 -c 50 2620:fe::fe
```

Expected result:

- `0%` packet loss during baseline,
- stable average latency,
- no OSPF neighbor changes in FRR logs during the baseline window.

## 5. Measurement Method

Q11.

What exactly is "convergence time" in this tutorial?

Use two complementary measurements.

| Metric | Meaning | How to measure |
| --- | --- | --- |
| Data-plane interruption | Time between the first lost ping and the first stable reply after the alternate route is used | `ping -D -i 0.2` |
| Control-plane convergence | Time between OSPF neighbor loss and route table stabilization | FRR logs, `show ip route`, `show ipv6 route`, `ip -ts monitor route` |

The data-plane value is the most useful for a portfolio demo because it shows
user impact. The control-plane value is the most useful for explaining why the
network recovered.

Q12.

How do we timestamp a failure test?

In the failure terminal, print the date immediately before and after the command.

```console
date -Ins
sudo ip link set enp0s1.440 down
date -Ins
```

For route events, run this on the router being observed:

```console
ip -ts monitor route
```

For FRR events, run this on the router being observed:

```console
sudo journalctl -u frr -f --since now
```

Q13.

How do we capture OSPF packets during a failure?

On the affected transit interface, use `tcpdump`.

```console
sudo tcpdump -ni enp0s1.440 -vv "ip proto 89 or ip6 proto 89"
```

To save a PCAP:

```console
sudo tcpdump -ni enp0s1.440 -w evidence/phase2/01-r1-r2-link/r1-enp0s1.440-ospf.pcap "ip proto 89 or ip6 proto 89"
```

Stop the capture after the failure and restore are complete.

Q14.

How many times should each scenario be repeated?

Run every scenario at least three times:

1. first run to validate the commands,
2. second run to capture clean evidence,
3. third run to confirm the measurement is repeatable.

For the final report, keep the cleanest run and summarize the range of observed
convergence times.

## 6. Scenario 1 - R1 To R2 Link Failure

This scenario tests VLAN `440`.

### 6.1 Expected Behavior

Q15.

What should happen when the direct `R1` to `R2` link fails?

The direct OSPF adjacency between `R1` and `R2` should drop.
Traffic between `R1` and `R2` networks should move through `R3`.

Expected alternate path:

```text
R1 -> VLAN 441 -> R3 -> VLAN 442 -> R2
```

Examples:

| Traffic | Before failure | During failure after convergence |
| --- | --- | --- |
| `R2` to `R1` hosting network `10.10.0.0/24` | `R2 -> R1` over VLAN `440` | `R2 -> R3 -> R1` |
| `R1` to `R2` hosting network `10.20.0.0/24` | `R1 -> R2` over VLAN `440` | `R1 -> R3 -> R2` |
| `R2` default route | via `10.44.0.1` on `enp0s1.440` | via `R3`, then `R1` |

### 6.2 Baseline Before The Cut

Q16.

Which commands should be saved before cutting VLAN `440`?

On `R1`:

```console
vtysh -c "show ip ospf neighbor"
vtysh -c "show ipv6 ospf6 neighbor"
vtysh -c "show ip route 10.20.0.0/24"
vtysh -c "show ipv6 route fd14:ca46:3864:14::/64"
```

On `R2`:

```console
vtysh -c "show ip ospf neighbor"
vtysh -c "show ipv6 ospf6 neighbor"
vtysh -c "show ip route 10.10.0.0/24"
vtysh -c "show ip route 0.0.0.0/0"
vtysh -c "show ipv6 route fd14:ca46:3864:a::/64"
vtysh -c "show ipv6 route ::/0"
```

Start a continuous ping from a container behind `R2` to a container behind `R1`.

```console
incus exec c0 -- ping -D -i 0.2 10.10.0.X
```

### 6.3 Cut The Link

Q17.

How do we simulate the `R1` to `R2` link failure from the router?

On `R2`, because the traffic source is behind `R2` in this scenario:

```console
date -Ins
sudo ip link set enp0s1.440 down
date -Ins
```

Observe the ping stream. Then capture the new route state.

On `R2`:

```console
vtysh -c "show ip ospf neighbor"
vtysh -c "show ipv6 ospf6 neighbor"
vtysh -c "show ip route 10.10.0.0/24"
vtysh -c "show ip route 0.0.0.0/0"
vtysh -c "show ipv6 route fd14:ca46:3864:a::/64"
vtysh -c "show ipv6 route ::/0"
```

Expected result:

- `R2` no longer lists `R1` as neighbor on `enp0s1.440`,
- `R2` still lists `R3` as neighbor on `enp0s1.442`,
- remote `R1` prefixes are reachable through `R3`,
- default traffic from `R2` recovers through `R3` and then `R1`.

### 6.4 Restore The Link

Q18.

How do we restore the `R1` to `R2` link?

On `R2`:

```console
date -Ins
sudo ip link set enp0s1.440 up
date -Ins
```

Wait until the adjacency is full again.

```console
vtysh -c "show ip ospf neighbor"
vtysh -c "show ipv6 ospf6 neighbor"
```

Expected result:

- the `R1`/`R2` OSPFv2 adjacency returns to `Full`,
- the `R1`/`R2` OSPFv3 adjacency returns,
- routes return to the best direct path if metrics prefer it.

### 6.5 Evidence To Save

Save:

- ping output with timestamps,
- `show ip ospf neighbor` before/during/after,
- `show ipv6 ospf6 neighbor` before/during/after,
- `show ip route` targeted prefixes before/during/after,
- `show ipv6 route` targeted prefixes before/during/after,
- FRR journal lines showing adjacency down/up,
- optional PCAP from `enp0s1.440`.

## 7. Scenario 2 - R2 To R3 Link Failure

This scenario tests VLAN `442`.

### 7.1 Expected Behavior

Q19.

What should happen when the direct `R2` to `R3` link fails?

The direct OSPF adjacency between `R2` and `R3` should drop.
Traffic between `R2` and `R3` networks should move through `R1`.

Expected alternate path:

```text
R2 -> VLAN 440 -> R1 -> VLAN 441 -> R3
```

This scenario is less disruptive for default-route traffic because both `R2`
and `R3` can still reach `R1` directly.

### 7.2 Baseline Before The Cut

On `R2`:

```console
vtysh -c "show ip ospf neighbor"
vtysh -c "show ipv6 ospf6 neighbor"
vtysh -c "show ip route 10.30.0.0/24"
vtysh -c "show ipv6 route fd14:ca46:3864:1e::/64"
```

On `R3`:

```console
vtysh -c "show ip ospf neighbor"
vtysh -c "show ipv6 ospf6 neighbor"
vtysh -c "show ip route 10.20.0.0/24"
vtysh -c "show ipv6 route fd14:ca46:3864:14::/64"
```

Start a continuous ping from a container behind `R2` to a container behind `R3`.

```console
incus exec c0 -- ping -D -i 0.2 10.30.0.X
```

### 7.3 Cut The Link

Q20.

How do we simulate the `R2` to `R3` link failure?

On `R2`:

```console
date -Ins
sudo ip link set enp0s1.442 down
date -Ins
```

Then check the routes.

```console
vtysh -c "show ip ospf neighbor"
vtysh -c "show ipv6 ospf6 neighbor"
vtysh -c "show ip route 10.30.0.0/24"
vtysh -c "show ipv6 route fd14:ca46:3864:1e::/64"
```

Expected result:

- `R2` no longer lists `R3` as neighbor on `enp0s1.442`,
- `R2` still lists `R1` as neighbor on `enp0s1.440`,
- `R3` prefixes are reachable through `R1`.

### 7.4 Restore The Link

On `R2`:

```console
date -Ins
sudo ip link set enp0s1.442 up
date -Ins
```

Validate that the adjacency returns.

```console
vtysh -c "show ip ospf neighbor"
vtysh -c "show ipv6 ospf6 neighbor"
```

### 7.5 Evidence To Save

Save the same categories as Scenario 1, with the PCAP on `enp0s1.442`.

## 8. Scenario 3 - R1 To R3 Link Failure

This scenario tests VLAN `441`.

### 8.1 Expected Behavior

Q21.

What should happen when the direct `R1` to `R3` link fails?

The direct OSPF adjacency between `R1` and `R3` should drop.
Traffic between `R1` and `R3` networks should move through `R2`.

Expected alternate path:

```text
R1 -> VLAN 440 -> R2 -> VLAN 442 -> R3
```

Examples:

| Traffic | Before failure | During failure after convergence |
| --- | --- | --- |
| `R3` to `R1` hosting network `10.10.0.0/24` | `R3 -> R1` over VLAN `441` | `R3 -> R2 -> R1` |
| `R1` to `R3` hosting network `10.30.0.0/24` | `R1 -> R3` over VLAN `441` | `R1 -> R2 -> R3` |
| `R3` default route | via `R1` on `enp0s1.441` | via `R2`, then `R1` |

### 8.2 Baseline Before The Cut

On `R1`:

```console
vtysh -c "show ip ospf neighbor"
vtysh -c "show ipv6 ospf6 neighbor"
vtysh -c "show ip route 10.30.0.0/24"
vtysh -c "show ipv6 route fd14:ca46:3864:1e::/64"
```

On `R3`:

```console
vtysh -c "show ip ospf neighbor"
vtysh -c "show ipv6 ospf6 neighbor"
vtysh -c "show ip route 10.10.0.0/24"
vtysh -c "show ip route 0.0.0.0/0"
vtysh -c "show ipv6 route fd14:ca46:3864:a::/64"
vtysh -c "show ipv6 route ::/0"
```

Start a continuous ping from a container behind `R3` to a container behind `R1`.

```console
incus exec c0 -- ping -D -i 0.2 10.10.0.X
```

### 8.3 Cut The Link

Q22.

How do we simulate the `R1` to `R3` link failure?

On `R3`, because the traffic source is behind `R3` in this scenario:

```console
date -Ins
sudo ip link set enp0s1.441 down
date -Ins
```

Then check the route change from `R3`.

```console
vtysh -c "show ip ospf neighbor"
vtysh -c "show ipv6 ospf6 neighbor"
vtysh -c "show ip route 10.10.0.0/24"
vtysh -c "show ip route 0.0.0.0/0"
vtysh -c "show ipv6 route fd14:ca46:3864:a::/64"
vtysh -c "show ipv6 route ::/0"
```

Expected result:

- `R3` no longer lists `R1` as neighbor on `enp0s1.441`,
- `R3` still lists `R2` as neighbor on `enp0s1.442`,
- `R1` prefixes and default route recover through `R2`.

### 8.4 Restore The Link

On `R3`:

```console
date -Ins
sudo ip link set enp0s1.441 up
date -Ins
```

Validate that both OSPF versions return to the expected neighbor state.

```console
vtysh -c "show ip ospf neighbor"
vtysh -c "show ipv6 ospf6 neighbor"
```

### 8.5 Evidence To Save

Save the same categories as Scenario 1, with the PCAP on `enp0s1.441`.

## 9. Scenario 4 - FRR Restart

This scenario tests the routing stack without shutting down the whole router.

### 9.1 Expected Behavior

Q23.

What should happen when FRR is restarted on one router?

For the restarted router:

- `zebra`, `ospfd`, and `ospf6d` stop,
- OSPF adjacencies drop,
- learned OSPF routes may disappear temporarily,
- OSPF adjacencies reform after FRR starts again,
- routes are reinstalled.

For the two other routers:

- the direct adjacency to the restarted router drops,
- if the physical topology still has an alternate path, the two non-restarted
  routers should continue to route between each other.

### 9.2 Restart FRR On R2

Q24.

How do we test FRR restart behavior on `R2`?

Use `R2` because it sits between the other two routers and has one hosting
network behind it.

On `R1`, start a ping to a container behind `R2`.

```console
incus exec c0 -- ping -D -i 0.2 10.20.0.X
```

On `R2`, capture FRR status and restart.

```console
systemctl --no-pager status frr
date -Ins
sudo systemctl restart frr
date -Ins
systemctl --no-pager status frr
```

On `R1`, check routes after the restart.

```console
vtysh -c "show ip ospf neighbor"
vtysh -c "show ipv6 ospf6 neighbor"
vtysh -c "show ip route 10.20.0.0/24"
vtysh -c "show ipv6 route fd14:ca46:3864:14::/64"
```

Expected result:

- traffic to `R2` hosting may fail while FRR restarts,
- `R1` and `R3` should remain neighbors if their direct link is healthy,
- `R2` rejoins the OSPF topology after FRR starts,
- routes to `10.20.0.0/24` and `fd14:ca46:3864:14::/64` return.

### 9.3 Evidence To Save

Save:

- systemd status before and after,
- FRR journal output,
- ping output,
- OSPF neighbors before and after,
- route entries before and after.

## 10. Scenario 5 - Router Reboot

This scenario is more disruptive than a daemon restart.
Run it only after the three link-failure scenarios are documented.

### 10.1 Expected Behavior

Q25.

What should happen when one router reboots?

If `R2` reboots:

- `R2` hosting network is down while the router is unavailable,
- `R1` and `R3` should remain connected through VLAN `441`,
- OSPF routes that depend on `R2` disappear and return after boot,
- management access to `R2` disappears and returns.

### 10.2 Reboot R2

Q26.

How do we test router reboot behavior?

Start a ping from `R1` to a container behind `R2`.

```console
incus exec c0 -- ping -D -i 0.2 10.20.0.X
```

Start a second ping from `R1` to a container behind `R3`.

```console
incus exec c0 -- ping -D -i 0.2 10.30.0.X
```

On `R2`:

```console
date -Ins
sudo reboot
```

When `R2` returns, capture:

```console
uptime
systemctl --no-pager status frr
vtysh -c "show ip ospf neighbor"
vtysh -c "show ipv6 ospf6 neighbor"
vtysh -c "show ip route"
vtysh -c "show ipv6 route"
```

Expected result:

- traffic to `R2` hosted containers fails during the reboot,
- traffic between `R1` and `R3` continues,
- `R2` returns to full OSPF adjacency after boot,
- routes to `R2` hosting networks return.

### 10.3 Evidence To Save

Save:

- reboot timestamp,
- ping to the rebooted router hosting network,
- ping that should stay available through the rest of the topology,
- FRR status after boot,
- OSPF neighbors and route tables after recovery.

## 11. Scenario 6 - VLAN Loss On The OVS Switch

This scenario simulates a switching or trunking mistake on the hypervisor.
It is close to a real operational incident: a VLAN disappears from a trunk.

### 11.1 Expected Behavior

Q27.

What is different between shutting a router subinterface and removing a VLAN
from an OVS trunk?

Shutting a router subinterface creates a local router-side failure.
Removing a VLAN from a trunk creates a switch-side failure.

From the OSPF perspective, both can break adjacency. From the operations
perspective, the evidence is different:

- router-side failure appears in `ip link`, system logs, and FRR interface state,
- switch-side failure appears in OVS configuration and forwarding behavior.

### 11.2 Remove VLAN 440 From R1 Trunk

Q28.

How do we simulate accidental VLAN loss for the `R1` to `R2` link?

On the hypervisor, remove VLAN `440` from `tap62`.

```console
date -Ins
sudo ovs-vsctl remove port tap62 trunks 440
date -Ins
sudo ovs-vsctl list port tap62
```

Observe the same behavior as Scenario 1.

On `R2`:

```console
vtysh -c "show ip ospf neighbor"
vtysh -c "show ipv6 ospf6 neighbor"
vtysh -c "show ip route 10.10.0.0/24"
vtysh -c "show ip route 0.0.0.0/0"
```

Expected result:

- the `R1`/`R2` adjacency drops,
- `R2` reaches `R1` networks through `R3`,
- OVS shows that `tap62` no longer carries VLAN `440`.

### 11.3 Restore VLAN 440

Q29.

How do we restore the OVS trunk?

On the hypervisor:

```console
date -Ins
sudo ovs-vsctl add port tap62 trunks 440
date -Ins
sudo ovs-vsctl list port tap62
```

If the trunk list looks wrong, reapply the known-good `switch.yaml`.

```console
switch-conf.py -a scripts/switch.yaml
```

Validate from `R1` and `R2`:

```console
vtysh -c "show ip ospf neighbor"
vtysh -c "show ipv6 ospf6 neighbor"
```

### 11.4 Evidence To Save

Save:

- `ovs-vsctl list port tap62` before/during/after,
- `ovs-appctl fdb/show dsw-host` before/during/after,
- OSPF neighbor changes,
- route changes,
- traffic interruption and recovery.

## 12. Latency, Throughput, And Jitter Tests

This section produces the performance table requested in the calendar.

### 12.1 Latency

Q30.

How do we compare latency before and after failover?

Use the same source, destination, packet interval, and packet count every time.

Example from `R2` hosting to `R1` hosting:

```console
incus exec c0 -- ping -D -i 0.2 -c 100 10.10.0.X
```

Run it in three states:

1. normal topology,
2. link failed after convergence,
3. restored topology.

Record:

- packet loss,
- min/avg/max/mdev,
- number of visibly lost packets during failure,
- first lost timestamp,
- first stable recovered timestamp.

### 12.2 Simple Jitter

Q31.

How do we estimate jitter without installing extra tools?

Use the `mdev` value from Linux `ping` as a simple jitter indicator.
It is not a full voice-grade jitter metric, but it is enough for a Phase 2 lab
comparison.

For each scenario, record:

| Scenario | State | avg RTT | mdev | packet loss |
| --- | --- | ---: | ---: | ---: |
| `R1-R2` link | normal | | | |
| `R1-R2` link | failed converged | | | |
| `R1-R2` link | restored | | | |

### 12.3 Throughput With iperf3

Q32.

How do we measure throughput if `iperf3` is available?

Install `iperf3` only inside lab systems.

On the destination container:

```console
iperf3 -s
```

On the source container:

```console
iperf3 -c 10.10.0.X -t 20
```

For IPv6:

```console
iperf3 -6 -c fd14:ca46:3864:a:XXXX:XXXX:XXXX:XXXX -t 20
```

Run the same test in the three states:

1. normal topology,
2. failed converged topology,
3. restored topology.

Record:

| Scenario | State | Source | Destination | Throughput | Retransmits |
| --- | --- | --- | --- | ---: | ---: |
| `R1-R2` link | normal | | | | |
| `R1-R2` link | failed converged | | | | |
| `R1-R2` link | restored | | | | |

If `iperf3` is not available, note that throughput testing was deferred and keep
the ping latency/jitter results.

## 13. Scenario Report Template

Copy this template into the final Phase 2 report for each scenario.

```markdown
## Scenario Name

Date:

Operator:

Failure tested:

Failure command:

Restore command:

Traffic source:

Traffic destination:

Expected alternate path:

### Baseline

- OSPFv2 neighbors:
- OSPFv3 neighbors:
- IPv4 route before failure:
- IPv6 route before failure:
- Baseline ping result:
- Baseline throughput result:

### Failure Window

- Failure timestamp:
- First lost packet timestamp:
- First recovered packet timestamp:
- Estimated data-plane interruption:
- OSPF neighbor down timestamp:
- Route changed timestamp:
- Alternate route observed:

### Recovery

- Restore timestamp:
- OSPF neighbor up timestamp:
- Route restored timestamp:
- Packet loss during restoration:

### Evidence

- Command transcript:
- FRR logs:
- PCAP:
- Screenshots:

### Conclusion

- Result:
- Limitations:
- Follow-up:
```

## 14. Final Phase 2 Deliverables

Q33.

What must be complete before Phase 2 is considered done?

Phase 2 is complete when the following items are available:

- baseline route, neighbor, latency, and throughput evidence,
- `R1-R2` link failure report,
- `R2-R3` link failure report,
- `R1-R3` link failure report,
- FRR restart report,
- router reboot report,
- VLAN loss report,
- convergence table,
- packet-loss table,
- before/after route comparisons,
- documented limitations.

Use this final summary table.

| Scenario | Traffic tested | Packet loss | Data-plane interruption | Control-plane convergence | Alternate path | Result |
| --- | --- | ---: | ---: | ---: | --- | --- |
| `R1-R2` link failure | | | | | `R1-R3-R2` | |
| `R2-R3` link failure | | | | | `R2-R1-R3` | |
| `R1-R3` link failure | | | | | `R1-R2-R3` | |
| FRR restart on `R2` | | | | | topology dependent | |
| Router reboot on `R2` | | | | | topology dependent | |
| VLAN `440` loss on `tap62` | | | | | `R1-R3-R2` | |

## 15. Troubleshooting Notes

Q34.

What if OSPF does not reconverge?

Check the interface state first.

```console
ip -brief link
ip -brief address
```

Then check FRR.

```console
systemctl --no-pager status frr
vtysh -c "show daemons"
vtysh -c "show ip ospf interface"
vtysh -c "show ipv6 ospf6 interface"
```

Common causes:

- the interface was not restored with `ip link set ... up`,
- a VLAN was removed from OVS and not added back,
- `switch.yaml` still contains a temporary or wrong trunk list,
- forwarding is disabled,
- FRR restarted but a daemon did not come back,
- the route is present in the LSDB but not installed in the kernel FIB.

Q35.

What if IPv4 recovers but IPv6 does not?

Check OSPFv3 separately.

```console
vtysh -c "show ipv6 ospf6 neighbor"
vtysh -c "show ipv6 ospf6 interface"
vtysh -c "show ipv6 ospf6 route"
vtysh -c "show ipv6 route"
```

Then verify IPv6 forwarding.

```console
sudo sysctl net.ipv6.conf.all.forwarding
```

Q36.

What if traffic from containers fails while router-to-router pings work?

Check the hosting bridge and passive OSPF publication.

```console
incus ls
ip route
ip -6 route
vtysh -c "show ip ospf interface vlan10"
vtysh -c "show ip ospf interface vlan20"
vtysh -c "show ip ospf interface vlan30"
vtysh -c "show ipv6 ospf6 interface vlan10"
vtysh -c "show ipv6 ospf6 interface vlan20"
vtysh -c "show ipv6 ospf6 interface vlan30"
```

Use the interface that exists on the router being checked. For example, `R1`
has `vlan10`, `R2` has `vlan20`, and `R3` has `vlan30`.

Q37.

What should be written in the limitations section?

Be precise and honest. Good limitations include:

- convergence measurements were taken from `ping`, not a dedicated routing
  telemetry system,
- `mdev` from `ping` is used as a simple jitter approximation,
- container IP addresses can change and must be captured per run,
- packet captures may be large and stored outside Git,
- OSPF timer values were not tuned during Phase 2 unless explicitly documented,
- temporary VLAN `28` may still appear in OVS config but is not part of the
  OSPF failure tests.

## Conclusion

At the end of this tutorial, the lab should have a documented resilience profile.
The important deliverable is not just that OSPF "works"; it is a reproducible
set of tests showing how the network behaves when something breaks.

The next phase can then add observability with a clear purpose: dashboards and
alerts should make these same failures visible without manually watching every
terminal.
