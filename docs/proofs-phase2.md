R1# sh ip os nei

Neighbor ID     Pri State           Up Time         Dead Time Address         Interface                        RXmtL RqstL DBsmL
2.0.0.4           1 Full/Backup     1d06h54m          36.079s 10.44.0.2       enp0s1.440:10.44.0.1                 0     0     0
3.0.0.4           1 Full/Backup     1d06h53m          36.080s 10.44.1.3       enp0s1.441:10.44.1.1                 0     0     0

R1# sh ipv os nei
Neighbor ID     Pri    DeadTime    State/IfState         Duration I/F[State]
2.0.0.6           1    00:00:32     Full/BDR           1d06:54:52 enp0s1.440[DR]
3.0.0.6           1    00:00:37     Full/BDR           1d06:53:35 enp0s1.441[DR]
R1# sh ip os in
enp0s1.440 is up
  ifindex 4, MTU 1500 bytes, BW 0 Mbit <UP,LOWER_UP,BROADCAST,RUNNING,MULTICAST>
  Internet Address 10.44.0.1/29, Broadcast 10.44.0.7, Area 0.0.0.0
  MTU mismatch detection: enabled
  Router ID 1.0.0.4, Network Type BROADCAST, Cost: 40
  Transmit Delay is 1 sec, State DR, Priority 1
  Designated Router (ID) 1.0.0.4 Interface Address 10.44.0.1/29
  Backup Designated Router (ID) 2.0.0.4, Interface Address 10.44.0.2
  Saved Network-LSA sequence number 0x80000041
  Multicast group memberships: OSPFAllRouters OSPFDesignatedRouters
  Timer intervals configured, Hello 10s, Dead 40s, Wait 40s, Retransmit 5
    Hello due in 4.927s
  Neighbor Count is 1, Adjacent neighbor count is 1
  Graceful Restart hello delay: 10s
  LSA retransmissions: 2
enp0s1.441 is up
  ifindex 6, MTU 1500 bytes, BW 0 Mbit <UP,LOWER_UP,BROADCAST,RUNNING,MULTICAST>
  Internet Address 10.44.1.1/29, Broadcast 10.44.1.7, Area 0.0.0.0
  MTU mismatch detection: enabled
  Router ID 1.0.0.4, Network Type BROADCAST, Cost: 40
  Transmit Delay is 1 sec, State DR, Priority 1
  Designated Router (ID) 1.0.0.4 Interface Address 10.44.1.1/29
  Backup Designated Router (ID) 3.0.0.4, Interface Address 10.44.1.3
  Saved Network-LSA sequence number 0x80000042
  Multicast group memberships: OSPFAllRouters OSPFDesignatedRouters
  Timer intervals configured, Hello 10s, Dead 40s, Wait 40s, Retransmit 5
    Hello due in 4.927s
  Neighbor Count is 1, Adjacent neighbor count is 1
  Graceful Restart hello delay: 10s
  LSA retransmissions: 2
vlan10 is up
  ifindex 9, MTU 1500 bytes, BW 10000 Mbit <UP,LOWER_UP,BROADCAST,RUNNING,MULTICAST>
  Internet Address 10.10.0.1/24, Broadcast 10.10.0.255, Area 0.0.0.0
  MTU mismatch detection: enabled
  Router ID 1.0.0.4, Network Type BROADCAST, Cost: 40
  Transmit Delay is 1 sec, State DR, Priority 1
  Designated Router (ID) 1.0.0.4 Interface Address 10.10.0.1/24
  No backup designated router on this network
  Multicast group memberships: <None>
  Timer intervals configured, Hello 10s, Dead 40s, Wait 40s, Retransmit 5
    No Hellos (Passive interface)
  Neighbor Count is 0, Adjacent neighbor count is 0
  Graceful Restart hello delay: 10s
  LSA retransmissions: 0

R1# sh ipv os in
asw-host is up, type BROADCAST
  Interface ID: 8
   OSPF not enabled on this interface
enp0s1 is up, type BROADCAST
  Interface ID: 2
   OSPF not enabled on this interface
enp0s1.99 is up, type BROADCAST
  Interface ID: 5
   OSPF not enabled on this interface
enp0s1.360 is up, type BROADCAST
  Interface ID: 3
   OSPF not enabled on this interface
enp0s1.440 is up, type BROADCAST
  Interface ID: 4
  Internet Address:
    inet : 10.44.0.1/29
    inet6: fe80::baad:caff:fefe:3e/64
    inet6: fe80::1b8:1/64
  Instance ID 0, Interface MTU 1500 (autodetect: 1500)
  MTU mismatch detection: enabled
  Area ID 0.0.0.0, Cost 40
  State DR, Transmit Delay 1 sec, Priority 1
  Timer intervals configured:
   Hello 10(5.278), Dead 40, Retransmit 5
  DR: 1.0.0.6 BDR: 2.0.0.6
  Number of I/F scoped LSAs is 2
    0 Pending LSAs for LSUpdate in Time 00:00:00 [thread off]
    0 Pending LSAs for LSAck in Time 00:00:00 [thread off]
  Graceful Restart hello delay: 10s
  Authentication Trailer is disabled
enp0s1.441 is up, type BROADCAST
  Interface ID: 6
  Internet Address:
    inet : 10.44.1.1/29
    inet6: fe80::baad:caff:fefe:3e/64
    inet6: fe80::1b9:1/64
  Instance ID 0, Interface MTU 1500 (autodetect: 1500)
  MTU mismatch detection: enabled
  Area ID 0.0.0.0, Cost 40
  State DR, Transmit Delay 1 sec, Priority 1
  Timer intervals configured:
   Hello 10(5.278), Dead 40, Retransmit 5
  DR: 1.0.0.6 BDR: 3.0.0.6
  Number of I/F scoped LSAs is 2
    0 Pending LSAs for LSUpdate in Time 00:00:00 [thread off]
    0 Pending LSAs for LSAck in Time 00:00:00 [thread off]
  Graceful Restart hello delay: 10s
  Authentication Trailer is disabled
lo is up, type LOOPBACK
  Interface ID: 1
   OSPF not enabled on this interface
ovs-system is down, type BROADCAST
  Interface ID: 7
   OSPF not enabled on this interface
veth241d140d is up, type BROADCAST
  Interface ID: 13
   OSPF not enabled on this interface
veth8385cb05 is up, type BROADCAST
  Interface ID: 11
   OSPF not enabled on this interface
veth46328f3d is up, type BROADCAST
  Interface ID: 15
   OSPF not enabled on this interface
vlan10 is up, type BROADCAST
  Interface ID: 9
  Internet Address:
    inet : 10.10.0.1/24
    inet6: fe80::7460:e5ff:fec8:524f/64
    inet6: fd14:ca46:3864:a::1/64
  Instance ID 0, Interface MTU 1500 (autodetect: 1500)
  MTU mismatch detection: enabled
  Area ID 0.0.0.0, Cost 40
  State DR, Transmit Delay 1 sec, Priority 1
  Timer intervals configured:
   No Hellos (Passive interface)
  DR: 1.0.0.6 BDR: 0.0.0.0
  Number of I/F scoped LSAs is 1
    0 Pending LSAs for LSUpdate in Time 00:00:00 [thread off]
    0 Pending LSAs for LSAck in Time 00:00:00 [thread off]
  Graceful Restart hello delay: 10s
  Authentication Trailer is disabled
R1# sh ip os data

       OSPF Router with ID (1.0.0.4)

                Router Link States (Area 0.0.0.0)

Link ID         ADV Router      Age  Seq#       CkSum  Link count
1.0.0.4        1.0.0.4         1323 0x8000004a 0x3341 3
2.0.0.4        2.0.0.4         1344 0x8000004a 0xc4a0 3
3.0.0.4        3.0.0.4          828 0x8000004b 0x2c28 3

                Net Link States (Area 0.0.0.0)

Link ID         ADV Router      Age  Seq#       CkSum
10.44.0.1      1.0.0.4         1643 0x80000041 0x9445
10.44.1.1      1.0.0.4          223 0x80000042 0x9244
10.44.2.2      2.0.0.4         1344 0x80000041 0x7d56

                AS External Link States

Link ID         ADV Router      Age  Seq#       CkSum  Route
0.0.0.0        1.0.0.4          913 0x80000040 0xa7dc E2 0.0.0.0/0 [0x0]


R1# sh ipv os data

        Area Scoped Link State Database (Area 0)

Type LSId           AdvRouter       Age   SeqNum                        Payload
Rtr  0.0.0.0        1.0.0.6         617 80000042                1.0.0.6/0.0.0.4
Rtr  0.0.0.0        1.0.0.6         617 80000042                1.0.0.6/0.0.0.6
Rtr  0.0.0.0        2.0.0.6         559 80000041                1.0.0.6/0.0.0.4
Rtr  0.0.0.0        2.0.0.6         559 80000041                2.0.0.6/0.0.0.3
Rtr  0.0.0.0        3.0.0.6        1741 80000040                1.0.0.6/0.0.0.6
Rtr  0.0.0.0        3.0.0.6        1741 80000040                2.0.0.6/0.0.0.3
Net  0.0.0.4        1.0.0.6        1660 8000003e                        1.0.0.6
Net  0.0.0.4        1.0.0.6        1660 8000003e                        2.0.0.6
Net  0.0.0.6        1.0.0.6        1583 8000003e                        1.0.0.6
Net  0.0.0.6        1.0.0.6        1583 8000003e                        3.0.0.6
Net  0.0.0.3        2.0.0.6        1518 8000003e                        2.0.0.6
Net  0.0.0.3        2.0.0.6        1518 8000003e                        3.0.0.6
INP  0.0.0.0        1.0.0.6         617 80000036          fd14:ca46:3864:a::/64
INP  0.0.0.0        2.0.0.6         559 80000036         fd14:ca46:3864:14::/64
INP  0.0.0.0        3.0.0.6        1741 80000036         fd14:ca46:3864:1e::/64

        I/F Scoped Link State Database (I/F enp0s1.440 in Area 0)

Type LSId           AdvRouter       Age   SeqNum                        Payload
Lnk  0.0.0.4        1.0.0.6          40 8000003f                    fe80::1b8:1
Lnk  0.0.0.4        2.0.0.6        1663 8000003e        fe80::baad:caff:fefe:3f

        I/F Scoped Link State Database (I/F enp0s1.441 in Area 0)

Type LSId           AdvRouter       Age   SeqNum                        Payload
Lnk  0.0.0.6        1.0.0.6        1793 8000003e                    fe80::1b9:1
Lnk  0.0.0.5        3.0.0.6        1588 8000003e                    fe80::1b9:3

        I/F Scoped Link State Database (I/F vlan10 in Area 0)

Type LSId           AdvRouter       Age   SeqNum                        Payload
Lnk  0.0.0.9        1.0.0.6         215 80000036      fe80::7460:e5ff:fec8:524f

        AS Scoped Link State Database

Type LSId           AdvRouter       Age   SeqNum                        Payload
ASE  0.0.0.1        1.0.0.6         756 8000003d                             ::

R1# 



R2# sh ip os nei

Neighbor ID     Pri State           Up Time         Dead Time Address         Interface                        RXmtL RqstL DBsmL
1.0.0.4           1 Full/DR         1d06h55m          33.854s 10.44.0.1       enp0s1.440:10.44.0.2                 0     0     0
3.0.0.4           1 Full/Backup     1d06h52m          33.855s 10.44.2.3       enp0s1.442:10.44.2.2                 0     0     0

R2# sh ipv os nei
Neighbor ID     Pri    DeadTime    State/IfState         Duration I/F[State]
1.0.0.6           1    00:00:38     Full/DR            1d06:55:16 enp0s1.440[BDR]
3.0.0.6           1    00:00:32     Full/BDR           1d06:52:53 enp0s1.442[DR]
R2# sh ip os in
enp0s1.440 is up
  ifindex 4, MTU 1500 bytes, BW 0 Mbit <UP,LOWER_UP,BROADCAST,RUNNING,MULTICAST>
  Internet Address 10.44.0.2/29, Broadcast 10.44.0.7, Area 0.0.0.0
  MTU mismatch detection: enabled
  Router ID 2.0.0.4, Network Type BROADCAST, Cost: 40
  Transmit Delay is 1 sec, State Backup, Priority 1
  Designated Router (ID) 1.0.0.4 Interface Address 10.44.0.1/29
  Backup Designated Router (ID) 2.0.0.4, Interface Address 10.44.0.2
  Multicast group memberships: OSPFAllRouters OSPFDesignatedRouters
  Timer intervals configured, Hello 10s, Dead 40s, Wait 40s, Retransmit 5
    Hello due in 7.302s
  Neighbor Count is 1, Adjacent neighbor count is 1
  Graceful Restart hello delay: 10s
  LSA retransmissions: 2
enp0s1.442 is up
  ifindex 3, MTU 1500 bytes, BW 0 Mbit <UP,LOWER_UP,BROADCAST,RUNNING,MULTICAST>
  Internet Address 10.44.2.2/29, Broadcast 10.44.2.7, Area 0.0.0.0
  MTU mismatch detection: enabled
  Router ID 2.0.0.4, Network Type BROADCAST, Cost: 40
  Transmit Delay is 1 sec, State DR, Priority 1
  Designated Router (ID) 2.0.0.4 Interface Address 10.44.2.2/29
  Backup Designated Router (ID) 3.0.0.4, Interface Address 10.44.2.3
  Saved Network-LSA sequence number 0x80000041
  Multicast group memberships: OSPFAllRouters OSPFDesignatedRouters
  Timer intervals configured, Hello 10s, Dead 40s, Wait 40s, Retransmit 5
    Hello due in 7.302s
  Neighbor Count is 1, Adjacent neighbor count is 1
  Graceful Restart hello delay: 10s
  LSA retransmissions: 1
vlan20 is up
  ifindex 9, MTU 1500 bytes, BW 10000 Mbit <UP,LOWER_UP,BROADCAST,RUNNING,MULTICAST>
  Internet Address 10.20.0.1/24, Broadcast 10.20.0.255, Area 0.0.0.0
  MTU mismatch detection: enabled
  Router ID 2.0.0.4, Network Type BROADCAST, Cost: 40
  Transmit Delay is 1 sec, State DR, Priority 1
  Designated Router (ID) 2.0.0.4 Interface Address 10.20.0.1/24
  No backup designated router on this network
  Multicast group memberships: <None>
  Timer intervals configured, Hello 10s, Dead 40s, Wait 40s, Retransmit 5
    No Hellos (Passive interface)
  Neighbor Count is 0, Adjacent neighbor count is 0
  Graceful Restart hello delay: 10s
  LSA retransmissions: 0

R2# sh ipv os in
asw-host is up, type BROADCAST
  Interface ID: 8
   OSPF not enabled on this interface
enp0s1 is up, type BROADCAST
  Interface ID: 2
   OSPF not enabled on this interface
enp0s1.28 is up, type BROADCAST
  Interface ID: 6
   OSPF not enabled on this interface
enp0s1.99 is up, type BROADCAST
  Interface ID: 5
   OSPF not enabled on this interface
enp0s1.440 is up, type BROADCAST
  Interface ID: 4
  Internet Address:
    inet : 10.44.0.2/29
    inet6: fe80::1b8:2/64
    inet6: fe80::baad:caff:fefe:3f/64
  Instance ID 0, Interface MTU 1500 (autodetect: 1500)
  MTU mismatch detection: enabled
  Area ID 0.0.0.0, Cost 40
  State BDR, Transmit Delay 1 sec, Priority 1
  Timer intervals configured:
   Hello 10(0.178), Dead 40, Retransmit 5
  DR: 1.0.0.6 BDR: 2.0.0.6
  Number of I/F scoped LSAs is 2
    0 Pending LSAs for LSUpdate in Time 00:00:00 [thread off]
    0 Pending LSAs for LSAck in Time 00:00:00 [thread off]
  Graceful Restart hello delay: 10s
  Authentication Trailer is disabled
enp0s1.442 is up, type BROADCAST
  Interface ID: 3
  Internet Address:
    inet : 10.44.2.2/29
    inet6: fe80::1ba:2/64
    inet6: fe80::baad:caff:fefe:3f/64
  Instance ID 0, Interface MTU 1500 (autodetect: 1500)
  MTU mismatch detection: enabled
  Area ID 0.0.0.0, Cost 40
  State DR, Transmit Delay 1 sec, Priority 1
  Timer intervals configured:
   Hello 10(5.032), Dead 40, Retransmit 5
  DR: 2.0.0.6 BDR: 3.0.0.6
  Number of I/F scoped LSAs is 2
    0 Pending LSAs for LSUpdate in Time 00:00:00 [thread off]
    0 Pending LSAs for LSAck in Time 00:00:00 [thread off]
  Graceful Restart hello delay: 10s
  Authentication Trailer is disabled
lo is up, type LOOPBACK
  Interface ID: 1
   OSPF not enabled on this interface
ovs-system is down, type BROADCAST
  Interface ID: 7
   OSPF not enabled on this interface
veth3b509a15 is up, type BROADCAST
  Interface ID: 11
   OSPF not enabled on this interface
veth6e525474 is up, type BROADCAST
  Interface ID: 15
   OSPF not enabled on this interface
vethd4eac04a is up, type BROADCAST
  Interface ID: 13
   OSPF not enabled on this interface
vlan20 is up, type BROADCAST
  Interface ID: 9
  Internet Address:
    inet : 10.20.0.1/24
    inet6: fe80::58b7:f4ff:fe48:8a4f/64
    inet6: fd14:ca46:3864:14::1/64
  Instance ID 0, Interface MTU 1500 (autodetect: 1500)
  MTU mismatch detection: enabled
  Area ID 0.0.0.0, Cost 40
  State DR, Transmit Delay 1 sec, Priority 1
  Timer intervals configured:
   No Hellos (Passive interface)
  DR: 2.0.0.6 BDR: 0.0.0.0
  Number of I/F scoped LSAs is 1
    0 Pending LSAs for LSUpdate in Time 00:00:00 [thread off]
    0 Pending LSAs for LSAck in Time 00:00:00 [thread off]
  Graceful Restart hello delay: 10s
  Authentication Trailer is disabled
R2# sh ip os data

       OSPF Router with ID (2.0.0.4)

                Router Link States (Area 0.0.0.0)

Link ID         ADV Router      Age  Seq#       CkSum  Link count
1.0.0.4        1.0.0.4         1347 0x8000004a 0x3341 3
2.0.0.4        2.0.0.4         1366 0x8000004a 0xc4a0 3
3.0.0.4        3.0.0.4          850 0x8000004b 0x2c28 3

                Net Link States (Area 0.0.0.0)

Link ID         ADV Router      Age  Seq#       CkSum
10.44.0.1      1.0.0.4         1667 0x80000041 0x9445
10.44.1.1      1.0.0.4          246 0x80000042 0x9244
10.44.2.2      2.0.0.4         1366 0x80000041 0x7d56

                AS External Link States

Link ID         ADV Router      Age  Seq#       CkSum  Route
0.0.0.0        1.0.0.4          937 0x80000040 0xa7dc E2 0.0.0.0/0 [0x0]


R2# sh ipv os data

        Area Scoped Link State Database (Area 0)

Type LSId           AdvRouter       Age   SeqNum                        Payload
Rtr  0.0.0.0        1.0.0.6         634 80000042                1.0.0.6/0.0.0.4
Rtr  0.0.0.0        1.0.0.6         634 80000042                1.0.0.6/0.0.0.6
Rtr  0.0.0.0        2.0.0.6         574 80000041                1.0.0.6/0.0.0.4
Rtr  0.0.0.0        2.0.0.6         574 80000041                2.0.0.6/0.0.0.3
Rtr  0.0.0.0        3.0.0.6        1757 80000040                1.0.0.6/0.0.0.6
Rtr  0.0.0.0        3.0.0.6        1757 80000040                2.0.0.6/0.0.0.3
Net  0.0.0.4        1.0.0.6        1677 8000003e                        1.0.0.6
Net  0.0.0.4        1.0.0.6        1677 8000003e                        2.0.0.6
Net  0.0.0.6        1.0.0.6        1600 8000003e                        1.0.0.6
Net  0.0.0.6        1.0.0.6        1600 8000003e                        3.0.0.6
Net  0.0.0.3        2.0.0.6        1533 8000003e                        2.0.0.6
Net  0.0.0.3        2.0.0.6        1533 8000003e                        3.0.0.6
INP  0.0.0.0        1.0.0.6         634 80000036          fd14:ca46:3864:a::/64
INP  0.0.0.0        2.0.0.6         574 80000036         fd14:ca46:3864:14::/64
INP  0.0.0.0        3.0.0.6        1757 80000036         fd14:ca46:3864:1e::/64

        I/F Scoped Link State Database (I/F enp0s1.440 in Area 0)

Type LSId           AdvRouter       Age   SeqNum                        Payload
Lnk  0.0.0.4        1.0.0.6          57 8000003f                    fe80::1b8:1
Lnk  0.0.0.4        2.0.0.6        1678 8000003e        fe80::baad:caff:fefe:3f

        I/F Scoped Link State Database (I/F enp0s1.442 in Area 0)

Type LSId           AdvRouter       Age   SeqNum                        Payload
Lnk  0.0.0.3        2.0.0.6        1643 8000003e        fe80::baad:caff:fefe:3f
Lnk  0.0.0.4        3.0.0.6        1543 8000003e                    fe80::1ba:3

        I/F Scoped Link State Database (I/F vlan20 in Area 0)

Type LSId           AdvRouter       Age   SeqNum                        Payload
Lnk  0.0.0.9        2.0.0.6         153 80000036      fe80::58b7:f4ff:fe48:8a4f

        AS Scoped Link State Database

Type LSId           AdvRouter       Age   SeqNum                        Payload
ASE  0.0.0.1        1.0.0.6         773 8000003d                             ::

R2# 



R3# sh ip os nei

Neighbor ID     Pri State           Up Time         Dead Time Address         Interface                        RXmtL RqstL DBsmL
1.0.0.4           1 Full/DR         1d06h47m          39.593s 10.44.1.1       enp0s1.441:10.44.1.3                 0     0     0
2.0.0.4           1 Full/DR         1d06h46m          39.594s 10.44.2.2       enp0s1.442:10.44.2.3                 0     0     0

R3# sh ipv os nei
Neighbor ID     Pri    DeadTime    State/IfState         Duration I/F[State]
1.0.0.6           1    00:00:38     Full/DR            1d06:54:09 enp0s1.441[BDR]
2.0.0.6           1    00:00:33     Full/DR            1d06:53:02 enp0s1.442[BDR]
R3# sh ip os in
enp0s1.441 is up
  ifindex 5, MTU 1500 bytes, BW 0 Mbit <UP,LOWER_UP,BROADCAST,RUNNING,MULTICAST>
  Internet Address 10.44.1.3/29, Broadcast 10.44.1.7, Area 0.0.0.0
  MTU mismatch detection: enabled
  Router ID 3.0.0.4, Network Type BROADCAST, Cost: 40
  Transmit Delay is 1 sec, State Backup, Priority 1
  Designated Router (ID) 1.0.0.4 Interface Address 10.44.1.1/29
  Backup Designated Router (ID) 3.0.0.4, Interface Address 10.44.1.3
  Multicast group memberships: OSPFAllRouters OSPFDesignatedRouters
  Timer intervals configured, Hello 10s, Dead 40s, Wait 40s, Retransmit 5
    Hello due in 3.912s
  Neighbor Count is 1, Adjacent neighbor count is 1
  Graceful Restart hello delay: 10s
  LSA retransmissions: 3
enp0s1.442 is up
  ifindex 4, MTU 1500 bytes, BW 0 Mbit <UP,LOWER_UP,BROADCAST,RUNNING,MULTICAST>
  Internet Address 10.44.2.3/29, Broadcast 10.44.2.7, Area 0.0.0.0
  MTU mismatch detection: enabled
  Router ID 3.0.0.4, Network Type BROADCAST, Cost: 40
  Transmit Delay is 1 sec, State Backup, Priority 1
  Designated Router (ID) 2.0.0.4 Interface Address 10.44.2.2/29
  Backup Designated Router (ID) 3.0.0.4, Interface Address 10.44.2.3
  Multicast group memberships: OSPFAllRouters OSPFDesignatedRouters
  Timer intervals configured, Hello 10s, Dead 40s, Wait 40s, Retransmit 5
    Hello due in 3.912s
  Neighbor Count is 1, Adjacent neighbor count is 1
  Graceful Restart hello delay: 10s
  LSA retransmissions: 2
vlan30 is up
  ifindex 9, MTU 1500 bytes, BW 10000 Mbit <UP,LOWER_UP,BROADCAST,RUNNING,MULTICAST>
  Internet Address 10.30.0.1/24, Broadcast 10.30.0.255, Area 0.0.0.0
  MTU mismatch detection: enabled
  Router ID 3.0.0.4, Network Type BROADCAST, Cost: 40
  Transmit Delay is 1 sec, State DR, Priority 1
  Designated Router (ID) 3.0.0.4 Interface Address 10.30.0.1/24
  No backup designated router on this network
  Multicast group memberships: <None>
  Timer intervals configured, Hello 10s, Dead 40s, Wait 40s, Retransmit 5
    No Hellos (Passive interface)
  Neighbor Count is 0, Adjacent neighbor count is 0
  Graceful Restart hello delay: 10s
  LSA retransmissions: 0

R3# sh ipv os in
asw-host is up, type BROADCAST
  Interface ID: 8
   OSPF not enabled on this interface
enp0s1 is up, type BROADCAST
  Interface ID: 2
   OSPF not enabled on this interface
enp0s1.28 is up, type BROADCAST
  Interface ID: 6
   OSPF not enabled on this interface
enp0s1.99 is up, type BROADCAST
  Interface ID: 3
   OSPF not enabled on this interface
enp0s1.441 is up, type BROADCAST
  Interface ID: 5
  Internet Address:
    inet : 10.44.1.3/29
    inet6: fe80::baad:caff:fefe:40/64
    inet6: fe80::1b9:3/64
  Instance ID 0, Interface MTU 1500 (autodetect: 1500)
  MTU mismatch detection: enabled
  Area ID 0.0.0.0, Cost 40
  State BDR, Transmit Delay 1 sec, Priority 1
  Timer intervals configured:
   Hello 10(7.801), Dead 40, Retransmit 5
  DR: 1.0.0.6 BDR: 3.0.0.6
  Number of I/F scoped LSAs is 2
    0 Pending LSAs for LSUpdate in Time 00:00:00 [thread off]
    0 Pending LSAs for LSAck in Time 00:00:00 [thread off]
  Graceful Restart hello delay: 10s
  Authentication Trailer is disabled
enp0s1.442 is up, type BROADCAST
  Interface ID: 4
  Internet Address:
    inet : 10.44.2.3/29
    inet6: fe80::baad:caff:fefe:40/64
    inet6: fe80::1ba:3/64
  Instance ID 0, Interface MTU 1500 (autodetect: 1500)
  MTU mismatch detection: enabled
  Area ID 0.0.0.0, Cost 40
  State BDR, Transmit Delay 1 sec, Priority 1
  Timer intervals configured:
   Hello 10(7.801), Dead 40, Retransmit 5
  DR: 2.0.0.6 BDR: 3.0.0.6
  Number of I/F scoped LSAs is 2
    0 Pending LSAs for LSUpdate in Time 00:00:00 [thread off]
    0 Pending LSAs for LSAck in Time 00:00:00 [thread off]
  Graceful Restart hello delay: 10s
  Authentication Trailer is disabled
lo is up, type LOOPBACK
  Interface ID: 1
   OSPF not enabled on this interface
ovs-system is down, type BROADCAST
  Interface ID: 7
   OSPF not enabled on this interface
veth17d6baa3 is up, type BROADCAST
  Interface ID: 15
   OSPF not enabled on this interface
veth54535ff5 is up, type BROADCAST
  Interface ID: 11
   OSPF not enabled on this interface
vethbfe14a4d is up, type BROADCAST
  Interface ID: 13
   OSPF not enabled on this interface
vl is down, type BROADCAST
  Interface ID: 0
   OSPF not enabled on this interface
vlan30 is up, type BROADCAST
  Interface ID: 9
  Internet Address:
    inet : 10.30.0.1/24
    inet6: fe80::4855:57ff:fe6e:534a/64
    inet6: fd14:ca46:3864:1e::1/64
  Instance ID 0, Interface MTU 1500 (autodetect: 1500)
  MTU mismatch detection: enabled
  Area ID 0.0.0.0, Cost 40
  State DR, Transmit Delay 1 sec, Priority 1
  Timer intervals configured:
   No Hellos (Passive interface)
  DR: 3.0.0.6 BDR: 0.0.0.0
  Number of I/F scoped LSAs is 1
    0 Pending LSAs for LSUpdate in Time 00:00:00 [thread off]
    0 Pending LSAs for LSAck in Time 00:00:00 [thread off]
  Graceful Restart hello delay: 10s
  Authentication Trailer is disabled
R3# sh ip os data

       OSPF Router with ID (3.0.0.4)

                Router Link States (Area 0.0.0.0)

Link ID         ADV Router      Age  Seq#       CkSum  Link count
1.0.0.4        1.0.0.4         1361 0x8000004a 0x3341 3
2.0.0.4        2.0.0.4         1381 0x8000004a 0xc4a0 3
3.0.0.4        3.0.0.4          864 0x8000004b 0x2c28 3

                Net Link States (Area 0.0.0.0)

Link ID         ADV Router      Age  Seq#       CkSum
10.44.0.1      1.0.0.4         1681 0x80000041 0x9445
10.44.1.1      1.0.0.4          261 0x80000042 0x9244
10.44.2.2      2.0.0.4         1381 0x80000041 0x7d56

                AS External Link States

Link ID         ADV Router      Age  Seq#       CkSum  Route
0.0.0.0        1.0.0.4          951 0x80000040 0xa7dc E2 0.0.0.0/0 [0x0]


R3# sh ipv os data

        Area Scoped Link State Database (Area 0)

Type LSId           AdvRouter       Age   SeqNum                        Payload
Rtr  0.0.0.0        1.0.0.6         654 80000042                1.0.0.6/0.0.0.4
Rtr  0.0.0.0        1.0.0.6         654 80000042                1.0.0.6/0.0.0.6
Rtr  0.0.0.0        2.0.0.6         595 80000041                1.0.0.6/0.0.0.4
Rtr  0.0.0.0        2.0.0.6         595 80000041                2.0.0.6/0.0.0.3
Rtr  0.0.0.0        3.0.0.6        1776 80000040                1.0.0.6/0.0.0.6
Rtr  0.0.0.0        3.0.0.6        1776 80000040                2.0.0.6/0.0.0.3
Net  0.0.0.4        1.0.0.6        1697 8000003e                        1.0.0.6
Net  0.0.0.4        1.0.0.6        1697 8000003e                        2.0.0.6
Net  0.0.0.6        1.0.0.6        1621 8000003e                        1.0.0.6
Net  0.0.0.6        1.0.0.6        1621 8000003e                        3.0.0.6
Net  0.0.0.3        2.0.0.6        1554 8000003e                        2.0.0.6
Net  0.0.0.3        2.0.0.6        1554 8000003e                        3.0.0.6
INP  0.0.0.0        1.0.0.6         654 80000036          fd14:ca46:3864:a::/64
INP  0.0.0.0        2.0.0.6         595 80000036         fd14:ca46:3864:14::/64
INP  0.0.0.0        3.0.0.6        1776 80000036         fd14:ca46:3864:1e::/64

        I/F Scoped Link State Database (I/F enp0s1.441 in Area 0)

Type LSId           AdvRouter       Age   SeqNum                        Payload
Lnk  0.0.0.6        1.0.0.6          31 8000003f                    fe80::1b9:1
Lnk  0.0.0.5        3.0.0.6        1623 8000003e                    fe80::1b9:3

        I/F Scoped Link State Database (I/F enp0s1.442 in Area 0)

Type LSId           AdvRouter       Age   SeqNum                        Payload
Lnk  0.0.0.3        2.0.0.6        1664 8000003e        fe80::baad:caff:fefe:3f
Lnk  0.0.0.4        3.0.0.6        1562 8000003e                    fe80::1ba:3

        I/F Scoped Link State Database (I/F vlan30 in Area 0)

Type LSId           AdvRouter       Age   SeqNum                        Payload
Lnk  0.0.0.9        3.0.0.6           4 80000036      fe80::4855:57ff:fe6e:534a

        AS Scoped Link State Database

Type LSId           AdvRouter       Age   SeqNum                        Payload
ASE  0.0.0.1        1.0.0.6         793 8000003d                             ::

R3# 





R1# sh ip route
Codes: K - kernel route, C - connected, L - local, S - static,
       R - RIP, O - OSPF, I - IS-IS, B - BGP, E - EIGRP, N - NHRP,
       T - Table, v - VNC, V - VNC-Direct, A - Babel, F - PBR,
       f - OpenFabric, t - Table-Direct,
       > - selected route, * - FIB route, q - queued, r - rejected, b - backup
       t - trapped, o - offload failure

IPv4 unicast VRF default:
K>* 0.0.0.0/0 [0/0] via 192.168.104.129, enp0s1.360, weight 1, 1d08h07m
O   10.10.0.0/24 [110/40] is directly connected, vlan10, weight 1, 1d01h43m
C>* 10.10.0.0/24 is directly connected, vlan10, weight 1, 1d02h37m
L>* 10.10.0.1/32 is directly connected, vlan10, weight 1, 1d02h37m
O>* 10.20.0.0/24 [110/80] via 10.44.0.2, enp0s1.440, weight 1, 1d01h41m
O>* 10.30.0.0/24 [110/80] via 10.44.1.3, enp0s1.441, weight 1, 1d01h31m
O   10.44.0.0/29 [110/40] is directly connected, enp0s1.440, weight 1, 1d01h43m
C>* 10.44.0.0/29 is directly connected, enp0s1.440, weight 1, 1d02h37m
L>* 10.44.0.1/32 is directly connected, enp0s1.440, weight 1, 1d02h37m
O   10.44.1.0/29 [110/40] is directly connected, enp0s1.441, weight 1, 1d01h43m
C>* 10.44.1.0/29 is directly connected, enp0s1.441, weight 1, 1d02h37m
L>* 10.44.1.1/32 is directly connected, enp0s1.441, weight 1, 1d02h37m
O>* 10.44.2.0/29 [110/80] via 10.44.0.2, enp0s1.440, weight 1, 1d01h31m
  *                       via 10.44.1.3, enp0s1.441, weight 1, 1d01h31m
C>* 10.99.0.0/24 is directly connected, enp0s1.99, weight 1, 1d02h37m
L>* 10.99.0.1/32 is directly connected, enp0s1.99, weight 1, 1d02h37m
C>* 192.168.104.128/29 is directly connected, enp0s1.360, weight 1, 1d02h37m
L>* 192.168.104.130/32 is directly connected, enp0s1.360, weight 1, 1d02h37m
R1# sh ipv route
Codes: K - kernel route, C - connected, L - local, S - static,
       R - RIPng, O - OSPFv3, I - IS-IS, B - BGP, N - NHRP,
       T - Table, v - VNC, V - VNC-Direct, A - Babel, F - PBR,
       f - OpenFabric, t - Table-Direct,
       > - selected route, * - FIB route, q - queued, r - rejected, b - backup
       t - trapped, o - offload failure

IPv6 unicast VRF default:
K>* ::/0 [0/1024] via fe80::168:1, enp0s1.360 onlink, weight 1, 1d08h07m
C>* 2001:678:3fc:168::/64 is directly connected, enp0s1.360, weight 1, 1d02h37m
L>* 2001:678:3fc:168::82/128 is directly connected, enp0s1.360, weight 1, 1d02h37m
O   fd14:ca46:3864:a::/64 [110/40] is directly connected, vlan10, weight 1, 1d01h42m
C>* fd14:ca46:3864:a::/64 is directly connected, vlan10, weight 1, 1d02h37m
K * fd14:ca46:3864:a::/64 [0/256] is directly connected, vlan10, weight 1, 1d02h37m
L>* fd14:ca46:3864:a::1/128 is directly connected, vlan10, weight 1, 1d02h37m
O>* fd14:ca46:3864:14::/64 [110/80] via fe80::baad:caff:fefe:3f, enp0s1.440, weight 1, 1d01h41m
O>* fd14:ca46:3864:1e::/64 [110/80] via fe80::1b9:3, enp0s1.441, weight 1, 1d01h31m
C>* fd14:ca46:3864:99::/64 is directly connected, enp0s1.99, weight 1, 1d02h37m
L>* fd14:ca46:3864:99::1/128 is directly connected, enp0s1.99, weight 1, 1d02h37m
C * fe80::/64 is directly connected, vlan10, weight 1, 1d02h37m
C * fe80::/64 is directly connected, asw-host, weight 1, 1d02h37m
C * fe80::/64 is directly connected, enp0s1.360, weight 1, 1d02h37m
C * fe80::/64 is directly connected, enp0s1.99, weight 1, 1d02h37m
C * fe80::/64 is directly connected, enp0s1.441, weight 1, 1d08h07m
C * fe80::/64 is directly connected, enp0s1.440, weight 1, 1d08h07m
C>* fe80::/64 is directly connected, enp0s1, weight 1, 1d08h07m
R1# sh ip os route
============ OSPF network routing table ============
N    10.10.0.0/24          [40] area: 0.0.0.0
                           directly attached to vlan10
N    10.20.0.0/24          [80] area: 0.0.0.0
                           via 10.44.0.2, enp0s1.440
N    10.30.0.0/24          [80] area: 0.0.0.0
                           via 10.44.1.3, enp0s1.441
N    10.44.0.0/29          [40] area: 0.0.0.0
                           directly attached to enp0s1.440
N    10.44.1.0/29          [40] area: 0.0.0.0
                           directly attached to enp0s1.441
N    10.44.2.0/29          [80] area: 0.0.0.0
                           via 10.44.0.2, enp0s1.440
                           via 10.44.1.3, enp0s1.441

============ OSPF router routing table =============

============ OSPF external routing table ===========


R1# sh ipv os route
*N IA fd14:ca46:3864:a::/64          ::                        vlan10 1d01:43:05
*N IA fd14:ca46:3864:14::/64         fe80::baad:caff:fefe:3f   enp0s1.440 1d01:42:06
*N IA fd14:ca46:3864:1e::/64         fe80::1b9:3               enp0s1.441 1d01:31:47
R1# 



R2# sh ip route
Codes: K - kernel route, C - connected, L - local, S - static,
       R - RIP, O - OSPF, I - IS-IS, B - BGP, E - EIGRP, N - NHRP,
       T - Table, v - VNC, V - VNC-Direct, A - Babel, F - PBR,
       f - OpenFabric, t - Table-Direct,
       > - selected route, * - FIB route, q - queued, r - rejected, b - backup
       t - trapped, o - offload failure

IPv4 unicast VRF default:
O>* 0.0.0.0/0 [110/10] via 10.44.0.1, enp0s1.440, weight 1, 1d01h43m
O>* 10.10.0.0/24 [110/80] via 10.44.0.1, enp0s1.440, weight 1, 1d01h43m
O   10.20.0.0/24 [110/40] is directly connected, vlan20, weight 1, 1d01h43m
C>* 10.20.0.0/24 is directly connected, vlan20, weight 1, 1d05h47m
L>* 10.20.0.1/32 is directly connected, vlan20, weight 1, 1d05h47m
O>* 10.30.0.0/24 [110/80] via 10.44.2.3, enp0s1.442, weight 1, 1d01h33m
O   10.44.0.0/29 [110/40] is directly connected, enp0s1.440, weight 1, 1d01h43m
C>* 10.44.0.0/29 is directly connected, enp0s1.440, weight 1, 1d05h47m
L>* 10.44.0.2/32 is directly connected, enp0s1.440, weight 1, 1d05h47m
O>* 10.44.1.0/29 [110/80] via 10.44.0.1, enp0s1.440, weight 1, 1d01h33m
  *                       via 10.44.2.3, enp0s1.442, weight 1, 1d01h33m
O   10.44.2.0/29 [110/40] is directly connected, enp0s1.442, weight 1, 1d01h43m
C>* 10.44.2.0/29 is directly connected, enp0s1.442, weight 1, 1d05h47m
L>* 10.44.2.2/32 is directly connected, enp0s1.442, weight 1, 1d05h47m
C>* 10.99.0.0/24 is directly connected, enp0s1.99, weight 1, 1d05h47m
L>* 10.99.0.2/32 is directly connected, enp0s1.99, weight 1, 1d05h47m
R2# sh ipv route
Codes: K - kernel route, C - connected, L - local, S - static,
       R - RIPng, O - OSPFv3, I - IS-IS, B - BGP, N - NHRP,
       T - Table, v - VNC, V - VNC-Direct, A - Babel, F - PBR,
       f - OpenFabric, t - Table-Direct,
       > - selected route, * - FIB route, q - queued, r - rejected, b - backup
       t - trapped, o - offload failure

IPv6 unicast VRF default:
O>* ::/0 [110/10] via fe80::1b8:1, enp0s1.440, weight 1, 1d01h33m
O>* fd14:ca46:3864:a::/64 [110/80] via fe80::1b8:1, enp0s1.440, weight 1, 1d01h43m
O   fd14:ca46:3864:14::/64 [110/40] is directly connected, vlan20, weight 1, 1d01h43m
C>* fd14:ca46:3864:14::/64 is directly connected, vlan20, weight 1, 1d05h47m
K * fd14:ca46:3864:14::/64 [0/256] is directly connected, vlan20, weight 1, 1d05h47m
L>* fd14:ca46:3864:14::1/128 is directly connected, vlan20, weight 1, 1d05h47m
O>* fd14:ca46:3864:1e::/64 [110/80] via fe80::1ba:3, enp0s1.442, weight 1, 1d01h33m
C>* fd14:ca46:3864:99::/64 is directly connected, enp0s1.99, weight 1, 1d05h47m
K * fd14:ca46:3864:99::/64 [0/256] is directly connected, enp0s1.99, weight 1, 1d07h44m
L>* fd14:ca46:3864:99::2/128 is directly connected, enp0s1.99, weight 1, 1d05h47m
C * fe80::/64 is directly connected, vlan20, weight 1, 1d05h47m
C * fe80::/64 is directly connected, asw-host, weight 1, 1d05h47m
C * fe80::/64 is directly connected, enp0s1.99, weight 1, 1d05h47m
C * fe80::/64 is directly connected, enp0s1.28, weight 1, 1d05h56m
C * fe80::/64 is directly connected, enp0s1, weight 1, 1d05h56m
C * fe80::/64 is directly connected, enp0s1.442, weight 1, 1d07h44m
C>* fe80::/64 is directly connected, enp0s1.440, weight 1, 1d07h44m
R2# sh ip os route
============ OSPF network routing table ============
N    10.10.0.0/24          [80] area: 0.0.0.0
                           via 10.44.0.1, enp0s1.440
N    10.20.0.0/24          [40] area: 0.0.0.0
                           directly attached to vlan20
N    10.30.0.0/24          [80] area: 0.0.0.0
                           via 10.44.2.3, enp0s1.442
N    10.44.0.0/29          [40] area: 0.0.0.0
                           directly attached to enp0s1.440
N    10.44.1.0/29          [80] area: 0.0.0.0
                           via 10.44.0.1, enp0s1.440
                           via 10.44.2.3, enp0s1.442
N    10.44.2.0/29          [40] area: 0.0.0.0
                           directly attached to enp0s1.442

============ OSPF router routing table =============
R    1.0.0.4               [40] area: 0.0.0.0, ASBR
                           via 10.44.0.1, enp0s1.440

============ OSPF external routing table ===========
N E2 0.0.0.0/0             [40/10] tag: 0
                           via 10.44.0.1, enp0s1.440


R2# sh ipv os route
*N E2 ::/0                           fe80::1b8:1               enp0s1.440 1d01:33:26
*N IA fd14:ca46:3864:a::/64          fe80::1b8:1               enp0s1.440 1d01:43:45
*N IA fd14:ca46:3864:14::/64         ::                        vlan20 1d01:43:45
*N IA fd14:ca46:3864:1e::/64         fe80::1ba:3               enp0s1.442 1d01:33:26
R2# 



R3# sh ip route
Codes: K - kernel route, C - connected, L - local, S - static,
       R - RIP, O - OSPF, I - IS-IS, B - BGP, E - EIGRP, N - NHRP,
       T - Table, v - VNC, V - VNC-Direct, A - Babel, F - PBR,
       f - OpenFabric, t - Table-Direct,
       > - selected route, * - FIB route, q - queued, r - rejected, b - backup
       t - trapped, o - offload failure

IPv4 unicast VRF default:
O>* 0.0.0.0/0 [110/10] via 10.44.1.1, enp0s1.441, weight 1, 1d01h37m
O>* 10.10.0.0/24 [110/80] via 10.44.1.1, enp0s1.441, weight 1, 1d01h37m
O>* 10.20.0.0/24 [110/80] via 10.44.2.2, enp0s1.442, weight 1, 1d01h37m
O   10.30.0.0/24 [110/40] is directly connected, vlan30, weight 1, 1d01h37m
C>* 10.30.0.0/24 is directly connected, vlan30, weight 1, 1d02h38m
L>* 10.30.0.1/32 is directly connected, vlan30, weight 1, 1d02h38m
O>* 10.44.0.0/29 [110/80] via 10.44.1.1, enp0s1.441, weight 1, 1d01h37m
  *                       via 10.44.2.2, enp0s1.442, weight 1, 1d01h37m
O   10.44.1.0/29 [110/40] is directly connected, enp0s1.441, weight 1, 1d01h37m
C>* 10.44.1.0/29 is directly connected, enp0s1.441, weight 1, 1d02h38m
L>* 10.44.1.3/32 is directly connected, enp0s1.441, weight 1, 1d02h38m
O   10.44.2.0/29 [110/40] is directly connected, enp0s1.442, weight 1, 1d01h37m
C>* 10.44.2.0/29 is directly connected, enp0s1.442, weight 1, 1d02h38m
L>* 10.44.2.3/32 is directly connected, enp0s1.442, weight 1, 1d02h38m
C>* 10.99.0.0/24 is directly connected, enp0s1.99, weight 1, 1d02h38m
L>* 10.99.0.3/32 is directly connected, enp0s1.99, weight 1, 1d02h38m
R3# sh ipv route
Codes: K - kernel route, C - connected, L - local, S - static,
       R - RIPng, O - OSPFv3, I - IS-IS, B - BGP, N - NHRP,
       T - Table, v - VNC, V - VNC-Direct, A - Babel, F - PBR,
       f - OpenFabric, t - Table-Direct,
       > - selected route, * - FIB route, q - queued, r - rejected, b - backup
       t - trapped, o - offload failure

IPv6 unicast VRF default:
O>* ::/0 [110/10] via fe80::1b9:1, enp0s1.441, weight 1, 1d01h37m
O>* fd14:ca46:3864:a::/64 [110/80] via fe80::1b9:1, enp0s1.441, weight 1, 1d01h37m
O>* fd14:ca46:3864:14::/64 [110/80] via fe80::baad:caff:fefe:3f, enp0s1.442, weight 1, 1d01h37m
O   fd14:ca46:3864:1e::/64 [110/40] is directly connected, vlan30, weight 1, 1d01h37m
C>* fd14:ca46:3864:1e::/64 is directly connected, vlan30, weight 1, 1d02h39m
K * fd14:ca46:3864:1e::/64 [0/256] is directly connected, vlan30, weight 1, 1d02h39m
L>* fd14:ca46:3864:1e::1/128 is directly connected, vlan30, weight 1, 1d02h39m
C>* fd14:ca46:3864:99::/64 is directly connected, enp0s1.99, weight 1, 1d02h39m
K * fd14:ca46:3864:99::/64 [0/256] is directly connected, enp0s1.99, weight 1, 1d07h48m
L>* fd14:ca46:3864:99::3/128 is directly connected, enp0s1.99, weight 1, 1d02h39m
C * fe80::/64 is directly connected, asw-host, weight 1, 1d02h39m
C * fe80::/64 is directly connected, vlan30, weight 1, 1d02h39m
C * fe80::/64 is directly connected, enp0s1.99, weight 1, 1d02h39m
C * fe80::/64 is directly connected, enp0s1.28, weight 1, 1d06h00m
C * fe80::/64 is directly connected, enp0s1, weight 1, 1d06h00m
C * fe80::/64 is directly connected, enp0s1.442, weight 1, 1d07h48m
C>* fe80::/64 is directly connected, enp0s1.441, weight 1, 1d07h48m
R3# sh ip os route
============ OSPF network routing table ============
N    10.10.0.0/24          [80] area: 0.0.0.0
                           via 10.44.1.1, enp0s1.441
N    10.20.0.0/24          [80] area: 0.0.0.0
                           via 10.44.2.2, enp0s1.442
N    10.30.0.0/24          [40] area: 0.0.0.0
                           directly attached to vlan30
N    10.44.0.0/29          [80] area: 0.0.0.0
                           via 10.44.1.1, enp0s1.441
                           via 10.44.2.2, enp0s1.442
N    10.44.1.0/29          [40] area: 0.0.0.0
                           directly attached to enp0s1.441
N    10.44.2.0/29          [40] area: 0.0.0.0
                           directly attached to enp0s1.442

============ OSPF router routing table =============
R    1.0.0.4               [40] area: 0.0.0.0, ASBR
                           via 10.44.1.1, enp0s1.441

============ OSPF external routing table ===========
N E2 0.0.0.0/0             [40/10] tag: 0
                           via 10.44.1.1, enp0s1.441


R3# sh ipv os route
*N E2 ::/0                           fe80::1b9:1               enp0s1.441 1d01:37:17
*N IA fd14:ca46:3864:a::/64          fe80::1b9:1               enp0s1.441 1d01:37:17
*N IA fd14:ca46:3864:14::/64         fe80::baad:caff:fefe:3f   enp0s1.442 1d01:37:17
*N IA fd14:ca46:3864:1e::/64         ::                        vlan30 1d01:37:17



R1# show ip route 10.10.0.0/24
Routing entry for 10.10.0.0/24
  Known via "ospf", distance 110, metric 40
  Last update 1d01h52m ago
  Flags: None 
  Status: None 
    directly connected, vlan10, weight 1

Routing entry for 10.10.0.0/24
  Known via "connected", distance 0, metric 0, best
  Last update 1d02h46m ago
  Flags: Selected 
  Status: Installed 
  * directly connected, vlan10, weight 1

R1# show ip route 10.20.0.0/24
Routing entry for 10.20.0.0/24
  Known via "ospf", distance 110, metric 80, best
  Last update 1d01h51m ago
  Flags: Selected 
  Status: Installed 
  * 10.44.0.2, via enp0s1.440, weight 1

R1# show ip route 10.30.0.0/24
Routing entry for 10.30.0.0/24
  Known via "ospf", distance 110, metric 80, best
  Last update 1d01h40m ago
  Flags: Selected 
  Status: Installed 
  * 10.44.1.3, via enp0s1.441, weight 1

R1# show ip route 0.0.0.0/0 
Routing entry for 0.0.0.0/0
  Known via "kernel", distance 0, metric 0, best
  Last update 1d08h16m ago
  Flags: Selected 
  Status: Installed 
  * 192.168.104.129, via enp0s1.360, weight 1

R1# 



R2# show ipv6 route fd14:ca46:3864:a::/64
Routing entry for fd14:ca46:3864:a::/64
  Known via "ospf6", distance 110, metric 80, best
  Last update 1d01h53m ago
  Flags: Selected 
  Status: Installed 
  * fe80::1b8:1, via enp0s1.440, weight 1

R2# show ipv6 route fd14:ca46:3864:14::/64
Routing entry for fd14:ca46:3864:14::/64
  Known via "ospf6", distance 110, metric 40
  Last update 1d01h53m ago
  Flags: None 
  Status: None 
    directly connected, vlan20, weight 1

Routing entry for fd14:ca46:3864:14::/64
  Known via "connected", distance 0, metric 0, best
  Last update 1d05h57m ago
  Flags: Selected 
  Status: Installed 
  * directly connected, vlan20, weight 1

Routing entry for fd14:ca46:3864:14::/64
  Known via "kernel", distance 0, metric 256
  Last update 1d05h57m ago
  Flags: None 
  Status: Installed 
  * directly connected, vlan20, weight 1

R2# show ipv6 route fd14:ca46:3864:1e::/64
Routing entry for fd14:ca46:3864:1e::/64
  Known via "ospf6", distance 110, metric 80, best
  Last update 1d01h43m ago
  Flags: Selected 
  Status: Installed 
  * fe80::1ba:3, via enp0s1.442, weight 1

R2# show ipv6 route ::/0 
Routing entry for ::/0
  Known via "ospf6", distance 110, metric 10, best
  Last update 1d01h43m ago
  Flags: Selected 
  Status: Installed 
  * fe80::1b8:1, via enp0s1.440, weight 1

R2# 




 etu@R1  ~  incus ls
+------+---------+--------------------+---------------------------------------------+-----------+-----------+
| NAME |  STATE  |        IPV4        |                    IPV6                     |   TYPE    | SNAPSHOTS |
+------+---------+--------------------+---------------------------------------------+-----------+-----------+
| c0   | RUNNING | 10.10.0.169 (eth0) | fd14:ca46:3864:a:1266:6aff:fe8a:f053 (eth0) | CONTAINER | 0         |
+------+---------+--------------------+---------------------------------------------+-----------+-----------+
| c1   | RUNNING | 10.10.0.93 (eth0)  | fd14:ca46:3864:a:1266:6aff:fe84:92c2 (eth0) | CONTAINER | 0         |
+------+---------+--------------------+---------------------------------------------+-----------+-----------+
| c2   | RUNNING | 10.10.0.76 (eth0)  | fd14:ca46:3864:a:1266:6aff:fea9:6530 (eth0) | CONTAINER | 0         |
+------+---------+--------------------+---------------------------------------------+-----------+-----------+
 etu@R1  ~  


 etu@R2  ~  incus ls
+------+---------+--------------------+----------------------------------------------+-----------+-----------+
| NAME |  STATE  |        IPV4        |                     IPV6                     |   TYPE    | SNAPSHOTS |
+------+---------+--------------------+----------------------------------------------+-----------+-----------+
| c0   | RUNNING | 10.20.0.156 (eth0) | fd14:ca46:3864:14:1266:6aff:fe64:ce54 (eth0) | CONTAINER | 0         |
+------+---------+--------------------+----------------------------------------------+-----------+-----------+
| c1   | RUNNING | 10.20.0.89 (eth0)  | fd14:ca46:3864:14:1266:6aff:fef1:fdcf (eth0) | CONTAINER | 0         |
+------+---------+--------------------+----------------------------------------------+-----------+-----------+
| c2   | RUNNING | 10.20.0.106 (eth0) | fd14:ca46:3864:14:1266:6aff:fe54:d44c (eth0) | CONTAINER | 0         |
+------+---------+--------------------+----------------------------------------------+-----------+-----------+
 etu@R2  ~  


  etu@R3  ~  incus ls
+------+---------+--------------------+----------------------------------------------+-----------+-----------+
| NAME |  STATE  |        IPV4        |                     IPV6                     |   TYPE    | SNAPSHOTS |
+------+---------+--------------------+----------------------------------------------+-----------+-----------+
| c0   | RUNNING | 10.30.0.101 (eth0) | fd14:ca46:3864:1e:1266:6aff:fe9c:57cb (eth0) | CONTAINER | 0         |
+------+---------+--------------------+----------------------------------------------+-----------+-----------+
| c1   | RUNNING | 10.30.0.23 (eth0)  | fd14:ca46:3864:1e:1266:6aff:fe27:3b45 (eth0) | CONTAINER | 0         |
+------+---------+--------------------+----------------------------------------------+-----------+-----------+
| c2   | RUNNING | 10.30.0.74 (eth0)  | fd14:ca46:3864:1e:1266:6aff:fe1a:bf31 (eth0) | CONTAINER | 0         |
+------+---------+--------------------+----------------------------------------------+-----------+-----------+
 etu@R3  ~  




 etu@R2  ~  incus exec c0 -- ping -D -i 0.2 -c 50 10.10.0.93
PING 10.10.0.93 (10.10.0.93) 56(84) bytes of data.
[1780155456.219259] 64 bytes from 10.10.0.93: icmp_seq=1 ttl=62 time=3.20 ms
[1780155456.417649] 64 bytes from 10.10.0.93: icmp_seq=2 ttl=62 time=0.971 ms
[1780155456.617990] 64 bytes from 10.10.0.93: icmp_seq=3 ttl=62 time=0.934 ms
[1780155456.818483] 64 bytes from 10.10.0.93: icmp_seq=4 ttl=62 time=1.08 ms
[1780155457.018808] 64 bytes from 10.10.0.93: icmp_seq=5 ttl=62 time=0.906 ms
[1780155457.219074] 64 bytes from 10.10.0.93: icmp_seq=6 ttl=62 time=0.852 ms
[1780155457.420711] 64 bytes from 10.10.0.93: icmp_seq=7 ttl=62 time=1.02 ms
[1780155457.620991] 64 bytes from 10.10.0.93: icmp_seq=8 ttl=62 time=0.925 ms
[1780155457.821404] 64 bytes from 10.10.0.93: icmp_seq=9 ttl=62 time=1.00 ms
[1780155458.021780] 64 bytes from 10.10.0.93: icmp_seq=10 ttl=62 time=0.954 ms
[1780155458.222241] 64 bytes from 10.10.0.93: icmp_seq=11 ttl=62 time=1.04 ms
[1780155458.422543] 64 bytes from 10.10.0.93: icmp_seq=12 ttl=62 time=0.882 ms
[1780155458.624724] 64 bytes from 10.10.0.93: icmp_seq=13 ttl=62 time=1.00 ms
[1780155458.825042] 64 bytes from 10.10.0.93: icmp_seq=14 ttl=62 time=0.897 ms
[1780155459.028803] 64 bytes from 10.10.0.93: icmp_seq=15 ttl=62 time=0.978 ms
[1780155459.229197] 64 bytes from 10.10.0.93: icmp_seq=16 ttl=62 time=0.991 ms
[1780155459.429623] 64 bytes from 10.10.0.93: icmp_seq=17 ttl=62 time=1.01 ms
[1780155459.630007] 64 bytes from 10.10.0.93: icmp_seq=18 ttl=62 time=0.971 ms
[1780155459.830465] 64 bytes from 10.10.0.93: icmp_seq=19 ttl=62 time=1.04 ms
[1780155460.030770] 64 bytes from 10.10.0.93: icmp_seq=20 ttl=62 time=0.884 ms
[1780155460.232792] 64 bytes from 10.10.0.93: icmp_seq=21 ttl=62 time=1.03 ms
[1780155460.433209] 64 bytes from 10.10.0.93: icmp_seq=22 ttl=62 time=0.996 ms
[1780155460.633638] 64 bytes from 10.10.0.93: icmp_seq=23 ttl=62 time=1.01 ms
[1780155460.834004] 64 bytes from 10.10.0.93: icmp_seq=24 ttl=62 time=0.945 ms
[1780155461.034386] 64 bytes from 10.10.0.93: icmp_seq=25 ttl=62 time=0.965 ms
[1780155461.234751] 64 bytes from 10.10.0.93: icmp_seq=26 ttl=62 time=0.942 ms
[1780155461.434948] 64 bytes from 10.10.0.93: icmp_seq=27 ttl=62 time=0.780 ms
[1780155461.636755] 64 bytes from 10.10.0.93: icmp_seq=28 ttl=62 time=1.00 ms
[1780155461.837137] 64 bytes from 10.10.0.93: icmp_seq=29 ttl=62 time=0.972 ms
[1780155462.037456] 64 bytes from 10.10.0.93: icmp_seq=30 ttl=62 time=0.966 ms
[1780155462.237919] 64 bytes from 10.10.0.93: icmp_seq=31 ttl=62 time=1.03 ms
[1780155462.438349] 64 bytes from 10.10.0.93: icmp_seq=32 ttl=62 time=1.01 ms
[1780155462.638751] 64 bytes from 10.10.0.93: icmp_seq=33 ttl=62 time=0.987 ms
[1780155462.838870] 64 bytes from 10.10.0.93: icmp_seq=34 ttl=62 time=0.710 ms
[1780155463.040826] 64 bytes from 10.10.0.93: icmp_seq=35 ttl=62 time=0.991 ms
[1780155463.241069] 64 bytes from 10.10.0.93: icmp_seq=36 ttl=62 time=0.824 ms
[1780155463.444661] 64 bytes from 10.10.0.93: icmp_seq=37 ttl=62 time=0.940 ms
[1780155463.644987] 64 bytes from 10.10.0.93: icmp_seq=38 ttl=62 time=0.909 ms
[1780155463.845254] 64 bytes from 10.10.0.93: icmp_seq=39 ttl=62 time=0.865 ms
[1780155464.048719] 64 bytes from 10.10.0.93: icmp_seq=40 ttl=62 time=1.01 ms
[1780155464.249130] 64 bytes from 10.10.0.93: icmp_seq=41 ttl=62 time=0.988 ms
[1780155464.449510] 64 bytes from 10.10.0.93: icmp_seq=42 ttl=62 time=0.964 ms
[1780155464.649886] 64 bytes from 10.10.0.93: icmp_seq=43 ttl=62 time=0.955 ms
[1780155464.850360] 64 bytes from 10.10.0.93: icmp_seq=44 ttl=62 time=1.06 ms
[1780155465.050707] 64 bytes from 10.10.0.93: icmp_seq=45 ttl=62 time=0.935 ms
[1780155465.250922] 64 bytes from 10.10.0.93: icmp_seq=46 ttl=62 time=0.789 ms
[1780155465.452820] 64 bytes from 10.10.0.93: icmp_seq=47 ttl=62 time=0.968 ms
[1780155465.653160] 64 bytes from 10.10.0.93: icmp_seq=48 ttl=62 time=0.923 ms
[1780155465.853523] 64 bytes from 10.10.0.93: icmp_seq=49 ttl=62 time=0.936 ms
[1780155466.053949] 64 bytes from 10.10.0.93: icmp_seq=50 ttl=62 time=1.01 ms

--- 10.10.0.93 ping statistics ---
50 packets transmitted, 50 received, 0% packet loss, time 9837ms
rtt min/avg/max/mdev = 0.710/0.998/3.204/0.323 ms
 etu@R2  ~  


 etu@R3  ~  incus exec c0 -- ping -D -i 0.2 -c 50 10.10.0.76
PING 10.10.0.76 (10.10.0.76) 56(84) bytes of data.
[1780155504.525047] 64 bytes from 10.10.0.76: icmp_seq=1 ttl=62 time=2.93 ms
[1780155504.723448] 64 bytes from 10.10.0.76: icmp_seq=2 ttl=62 time=0.992 ms
[1780155504.923791] 64 bytes from 10.10.0.76: icmp_seq=3 ttl=62 time=0.908 ms
[1780155505.124220] 64 bytes from 10.10.0.76: icmp_seq=4 ttl=62 time=1.02 ms
[1780155505.324598] 64 bytes from 10.10.0.76: icmp_seq=5 ttl=62 time=0.947 ms
[1780155505.525024] 64 bytes from 10.10.0.76: icmp_seq=6 ttl=62 time=1.01 ms
[1780155505.725452] 64 bytes from 10.10.0.76: icmp_seq=7 ttl=62 time=1.00 ms
[1780155505.925709] 64 bytes from 10.10.0.76: icmp_seq=8 ttl=62 time=0.847 ms
[1780155506.127513] 64 bytes from 10.10.0.76: icmp_seq=9 ttl=62 time=0.975 ms
[1780155506.327888] 64 bytes from 10.10.0.76: icmp_seq=10 ttl=62 time=0.963 ms
[1780155506.528183] 64 bytes from 10.10.0.76: icmp_seq=11 ttl=62 time=0.945 ms
[1780155506.728571] 64 bytes from 10.10.0.76: icmp_seq=12 ttl=62 time=0.959 ms
[1780155506.929018] 64 bytes from 10.10.0.76: icmp_seq=13 ttl=62 time=0.975 ms
[1780155507.129449] 64 bytes from 10.10.0.76: icmp_seq=14 ttl=62 time=0.974 ms
[1780155507.329655] 64 bytes from 10.10.0.76: icmp_seq=15 ttl=62 time=0.822 ms
[1780155507.531447] 64 bytes from 10.10.0.76: icmp_seq=16 ttl=62 time=0.921 ms
[1780155507.731852] 64 bytes from 10.10.0.76: icmp_seq=17 ttl=62 time=0.959 ms
[1780155507.932240] 64 bytes from 10.10.0.76: icmp_seq=18 ttl=62 time=0.971 ms
[1780155508.132580] 64 bytes from 10.10.0.76: icmp_seq=19 ttl=62 time=0.926 ms
[1780155508.332794] 64 bytes from 10.10.0.76: icmp_seq=20 ttl=62 time=0.795 ms
[1780155508.535489] 64 bytes from 10.10.0.76: icmp_seq=21 ttl=62 time=0.951 ms
[1780155508.735850] 64 bytes from 10.10.0.76: icmp_seq=22 ttl=62 time=0.935 ms
[1780155508.936325] 64 bytes from 10.10.0.76: icmp_seq=23 ttl=62 time=1.05 ms
[1780155509.136692] 64 bytes from 10.10.0.76: icmp_seq=24 ttl=62 time=0.947 ms
[1780155509.337056] 64 bytes from 10.10.0.76: icmp_seq=25 ttl=62 time=0.951 ms
[1780155509.537397] 64 bytes from 10.10.0.76: icmp_seq=26 ttl=62 time=0.930 ms
[1780155509.737636] 64 bytes from 10.10.0.76: icmp_seq=27 ttl=62 time=0.834 ms
[1780155509.939536] 64 bytes from 10.10.0.76: icmp_seq=28 ttl=62 time=1.00 ms
[1780155510.139949] 64 bytes from 10.10.0.76: icmp_seq=29 ttl=62 time=0.998 ms
[1780155510.340310] 64 bytes from 10.10.0.76: icmp_seq=30 ttl=62 time=0.938 ms
[1780155510.540663] 64 bytes from 10.10.0.76: icmp_seq=31 ttl=62 time=0.920 ms
[1780155510.741069] 64 bytes from 10.10.0.76: icmp_seq=32 ttl=62 time=0.988 ms
[1780155510.941449] 64 bytes from 10.10.0.76: icmp_seq=33 ttl=62 time=0.952 ms
[1780155511.141690] 64 bytes from 10.10.0.76: icmp_seq=34 ttl=62 time=0.834 ms
[1780155511.343641] 64 bytes from 10.10.0.76: icmp_seq=35 ttl=62 time=0.949 ms
[1780155511.543983] 64 bytes from 10.10.0.76: icmp_seq=36 ttl=62 time=0.927 ms
[1780155511.744375] 64 bytes from 10.10.0.76: icmp_seq=37 ttl=62 time=0.968 ms
[1780155511.944714] 64 bytes from 10.10.0.76: icmp_seq=38 ttl=62 time=0.924 ms
[1780155512.145085] 64 bytes from 10.10.0.76: icmp_seq=39 ttl=62 time=0.936 ms
[1780155512.345486] 64 bytes from 10.10.0.76: icmp_seq=40 ttl=62 time=0.986 ms
[1780155512.546060] 64 bytes from 10.10.0.76: icmp_seq=41 ttl=62 time=1.01 ms
[1780155512.746340] 64 bytes from 10.10.0.76: icmp_seq=42 ttl=62 time=0.861 ms
[1780155512.951519] 64 bytes from 10.10.0.76: icmp_seq=43 ttl=62 time=1.01 ms
[1780155513.151855] 64 bytes from 10.10.0.76: icmp_seq=44 ttl=62 time=0.964 ms
[1780155513.352209] 64 bytes from 10.10.0.76: icmp_seq=45 ttl=62 time=0.952 ms
[1780155513.552508] 64 bytes from 10.10.0.76: icmp_seq=46 ttl=62 time=0.945 ms
[1780155513.752951] 64 bytes from 10.10.0.76: icmp_seq=47 ttl=62 time=1.01 ms
[1780155513.953278] 64 bytes from 10.10.0.76: icmp_seq=48 ttl=62 time=0.916 ms
[1780155514.153641] 64 bytes from 10.10.0.76: icmp_seq=49 ttl=62 time=0.948 ms
[1780155514.353947] 64 bytes from 10.10.0.76: icmp_seq=50 ttl=62 time=0.843 ms

--- 10.10.0.76 ping statistics ---
50 packets transmitted, 50 received, 0% packet loss, time 9831ms
rtt min/avg/max/mdev = 0.795/0.984/2.925/0.282 ms
 etu@R3  ~  



 etu@R2  ~  incus exec c0 -- ping -D -i 0.2 -c 50 9.9.9.9
PING 9.9.9.9 (9.9.9.9) 56(84) bytes of data.
[1780155546.687712] 64 bytes from 9.9.9.9: icmp_seq=1 ttl=50 time=19.6 ms
[1780155546.886537] 64 bytes from 9.9.9.9: icmp_seq=2 ttl=50 time=17.4 ms
[1780155547.086760] 64 bytes from 9.9.9.9: icmp_seq=3 ttl=50 time=16.8 ms
[1780155547.287807] 64 bytes from 9.9.9.9: icmp_seq=4 ttl=50 time=16.6 ms
[1780155547.489179] 64 bytes from 9.9.9.9: icmp_seq=5 ttl=50 time=17.0 ms
[1780155547.689503] 64 bytes from 9.9.9.9: icmp_seq=6 ttl=50 time=16.9 ms
[1780155547.889652] 64 bytes from 9.9.9.9: icmp_seq=7 ttl=50 time=16.7 ms
[1780155548.091185] 64 bytes from 9.9.9.9: icmp_seq=8 ttl=50 time=17.1 ms
[1780155548.291697] 64 bytes from 9.9.9.9: icmp_seq=9 ttl=50 time=17.1 ms
[1780155548.492060] 64 bytes from 9.9.9.9: icmp_seq=10 ttl=50 time=17.0 ms
[1780155548.693106] 64 bytes from 9.9.9.9: icmp_seq=11 ttl=50 time=17.6 ms
[1780155548.893526] 64 bytes from 9.9.9.9: icmp_seq=12 ttl=50 time=17.0 ms
[1780155549.093927] 64 bytes from 9.9.9.9: icmp_seq=13 ttl=50 time=17.0 ms
[1780155549.294536] 64 bytes from 9.9.9.9: icmp_seq=14 ttl=50 time=17.2 ms
[1780155549.495591] 64 bytes from 9.9.9.9: icmp_seq=15 ttl=50 time=17.6 ms
[1780155549.695949] 64 bytes from 9.9.9.9: icmp_seq=16 ttl=50 time=17.0 ms
[1780155549.896334] 64 bytes from 9.9.9.9: icmp_seq=17 ttl=50 time=16.9 ms
[1780155550.096934] 64 bytes from 9.9.9.9: icmp_seq=18 ttl=50 time=17.2 ms
[1780155550.297359] 64 bytes from 9.9.9.9: icmp_seq=19 ttl=50 time=17.1 ms
[1780155550.498343] 64 bytes from 9.9.9.9: icmp_seq=20 ttl=50 time=17.6 ms
[1780155550.699497] 64 bytes from 9.9.9.9: icmp_seq=21 ttl=50 time=17.7 ms
[1780155550.900276] 64 bytes from 9.9.9.9: icmp_seq=22 ttl=50 time=17.3 ms
[1780155551.100901] 64 bytes from 9.9.9.9: icmp_seq=23 ttl=50 time=17.2 ms
[1780155551.301631] 64 bytes from 9.9.9.9: icmp_seq=24 ttl=50 time=17.3 ms
[1780155551.502177] 64 bytes from 9.9.9.9: icmp_seq=25 ttl=50 time=17.1 ms
[1780155551.702684] 64 bytes from 9.9.9.9: icmp_seq=26 ttl=50 time=17.1 ms
[1780155551.903407] 64 bytes from 9.9.9.9: icmp_seq=27 ttl=50 time=17.3 ms
[1780155552.104038] 64 bytes from 9.9.9.9: icmp_seq=28 ttl=50 time=17.2 ms
[1780155552.305855] 64 bytes from 9.9.9.9: icmp_seq=29 ttl=50 time=18.4 ms
[1780155552.505652] 64 bytes from 9.9.9.9: icmp_seq=30 ttl=50 time=17.4 ms
[1780155552.705690] 64 bytes from 9.9.9.9: icmp_seq=31 ttl=50 time=16.6 ms
[1780155552.907751] 64 bytes from 9.9.9.9: icmp_seq=32 ttl=50 time=17.6 ms
[1780155553.107847] 64 bytes from 9.9.9.9: icmp_seq=33 ttl=50 time=16.6 ms
[1780155553.309966] 64 bytes from 9.9.9.9: icmp_seq=34 ttl=50 time=17.7 ms
[1780155553.510446] 64 bytes from 9.9.9.9: icmp_seq=35 ttl=50 time=17.1 ms
[1780155553.710778] 64 bytes from 9.9.9.9: icmp_seq=36 ttl=50 time=16.9 ms
[1780155553.913203] 64 bytes from 9.9.9.9: icmp_seq=37 ttl=50 time=19.0 ms
[1780155554.112553] 64 bytes from 9.9.9.9: icmp_seq=38 ttl=50 time=17.9 ms
[1780155554.312101] 64 bytes from 9.9.9.9: icmp_seq=39 ttl=50 time=17.1 ms
[1780155554.512504] 64 bytes from 9.9.9.9: icmp_seq=40 ttl=50 time=17.0 ms
[1780155554.712967] 64 bytes from 9.9.9.9: icmp_seq=41 ttl=50 time=17.0 ms
[1780155554.913090] 64 bytes from 9.9.9.9: icmp_seq=42 ttl=50 time=16.7 ms
[1780155555.114445] 64 bytes from 9.9.9.9: icmp_seq=43 ttl=50 time=16.9 ms
[1780155555.314588] 64 bytes from 9.9.9.9: icmp_seq=44 ttl=50 time=16.7 ms
[1780155555.516057] 64 bytes from 9.9.9.9: icmp_seq=45 ttl=50 time=17.1 ms
[1780155555.716791] 64 bytes from 9.9.9.9: icmp_seq=46 ttl=50 time=17.3 ms
[1780155555.917617] 64 bytes from 9.9.9.9: icmp_seq=47 ttl=50 time=17.4 ms
[1780155556.117832] 64 bytes from 9.9.9.9: icmp_seq=48 ttl=50 time=16.8 ms
[1780155556.318840] 64 bytes from 9.9.9.9: icmp_seq=49 ttl=50 time=16.6 ms
[1780155556.519771] 64 bytes from 9.9.9.9: icmp_seq=50 ttl=50 time=16.5 ms

--- 9.9.9.9 ping statistics ---
50 packets transmitted, 50 received, 0% packet loss, time 9835ms
rtt min/avg/max/mdev = 16.496/17.221/19.586/0.565 ms
 etu@R2  ~  incus exec c0 -- ping -6 -D -i 0.2 -c 50 2620:fe::fe
PING 2620:fe::fe (2620:fe::fe) 56 data bytes
[1780155566.013136] 64 bytes from 2620:fe::fe: icmp_seq=1 ttl=57 time=38.4 ms
[1780155566.212862] 64 bytes from 2620:fe::fe: icmp_seq=2 ttl=57 time=37.4 ms
[1780155566.413279] 64 bytes from 2620:fe::fe: icmp_seq=3 ttl=57 time=37.0 ms
[1780155566.613806] 64 bytes from 2620:fe::fe: icmp_seq=4 ttl=57 time=37.2 ms
[1780155566.814698] 64 bytes from 2620:fe::fe: icmp_seq=5 ttl=57 time=37.5 ms
[1780155567.016934] 64 bytes from 2620:fe::fe: icmp_seq=6 ttl=57 time=38.8 ms
[1780155567.216455] 64 bytes from 2620:fe::fe: icmp_seq=7 ttl=57 time=37.1 ms
[1780155567.416894] 64 bytes from 2620:fe::fe: icmp_seq=8 ttl=57 time=37.1 ms
[1780155567.617812] 64 bytes from 2620:fe::fe: icmp_seq=9 ttl=57 time=37.5 ms
[1780155567.818272] 64 bytes from 2620:fe::fe: icmp_seq=10 ttl=57 time=37.1 ms
[1780155568.019011] 64 bytes from 2620:fe::fe: icmp_seq=11 ttl=57 time=37.3 ms
[1780155568.219709] 64 bytes from 2620:fe::fe: icmp_seq=12 ttl=57 time=37.3 ms
[1780155568.420331] 64 bytes from 2620:fe::fe: icmp_seq=13 ttl=57 time=37.2 ms
[1780155568.620366] 64 bytes from 2620:fe::fe: icmp_seq=14 ttl=57 time=36.6 ms
[1780155568.821656] 64 bytes from 2620:fe::fe: icmp_seq=15 ttl=57 time=36.9 ms
[1780155569.022184] 64 bytes from 2620:fe::fe: icmp_seq=16 ttl=57 time=37.1 ms
[1780155569.223484] 64 bytes from 2620:fe::fe: icmp_seq=17 ttl=57 time=37.9 ms
[1780155569.422656] 64 bytes from 2620:fe::fe: icmp_seq=18 ttl=57 time=36.8 ms
[1780155569.628106] 64 bytes from 2620:fe::fe: icmp_seq=19 ttl=57 time=41.1 ms
[1780155569.824144] 64 bytes from 2620:fe::fe: icmp_seq=20 ttl=57 time=36.6 ms
[1780155570.027306] 64 bytes from 2620:fe::fe: icmp_seq=21 ttl=57 time=38.8 ms
[1780155570.227302] 64 bytes from 2620:fe::fe: icmp_seq=22 ttl=57 time=37.6 ms
[1780155570.427642] 64 bytes from 2620:fe::fe: icmp_seq=23 ttl=57 time=36.9 ms
[1780155570.627789] 64 bytes from 2620:fe::fe: icmp_seq=24 ttl=57 time=37.8 ms
[1780155570.828583] 64 bytes from 2620:fe::fe: icmp_seq=25 ttl=57 time=37.4 ms
[1780155571.029732] 64 bytes from 2620:fe::fe: icmp_seq=26 ttl=57 time=37.8 ms
[1780155571.230328] 64 bytes from 2620:fe::fe: icmp_seq=27 ttl=57 time=37.2 ms
[1780155571.430822] 64 bytes from 2620:fe::fe: icmp_seq=28 ttl=57 time=37.1 ms
[1780155571.631144] 64 bytes from 2620:fe::fe: icmp_seq=29 ttl=57 time=37.9 ms
[1780155571.831081] 64 bytes from 2620:fe::fe: icmp_seq=30 ttl=57 time=37.6 ms
[1780155572.032027] 64 bytes from 2620:fe::fe: icmp_seq=31 ttl=57 time=37.5 ms
[1780155572.232990] 64 bytes from 2620:fe::fe: icmp_seq=32 ttl=57 time=37.5 ms
[1780155572.432587] 64 bytes from 2620:fe::fe: icmp_seq=33 ttl=57 time=36.2 ms
[1780155572.633158] 64 bytes from 2620:fe::fe: icmp_seq=34 ttl=57 time=37.2 ms
[1780155572.833132] 64 bytes from 2620:fe::fe: icmp_seq=35 ttl=57 time=36.6 ms
[1780155573.035147] 64 bytes from 2620:fe::fe: icmp_seq=36 ttl=57 time=37.6 ms
[1780155573.235029] 64 bytes from 2620:fe::fe: icmp_seq=37 ttl=57 time=36.4 ms
[1780155573.437393] 64 bytes from 2620:fe::fe: icmp_seq=38 ttl=57 time=37.9 ms
[1780155573.635659] 64 bytes from 2620:fe::fe: icmp_seq=39 ttl=57 time=36.9 ms
[1780155573.838189] 64 bytes from 2620:fe::fe: icmp_seq=40 ttl=57 time=38.2 ms
[1780155574.038192] 64 bytes from 2620:fe::fe: icmp_seq=41 ttl=57 time=37.6 ms
[1780155574.238418] 64 bytes from 2620:fe::fe: icmp_seq=42 ttl=57 time=36.8 ms
[1780155574.439910] 64 bytes from 2620:fe::fe: icmp_seq=43 ttl=57 time=37.1 ms
[1780155574.639263] 64 bytes from 2620:fe::fe: icmp_seq=44 ttl=57 time=36.9 ms
[1780155574.840879] 64 bytes from 2620:fe::fe: icmp_seq=45 ttl=57 time=38.2 ms
[1780155575.039790] 64 bytes from 2620:fe::fe: icmp_seq=46 ttl=57 time=36.5 ms
[1780155575.241948] 64 bytes from 2620:fe::fe: icmp_seq=47 ttl=57 time=37.8 ms
[1780155575.441916] 64 bytes from 2620:fe::fe: icmp_seq=48 ttl=57 time=36.6 ms
[1780155575.642517] 64 bytes from 2620:fe::fe: icmp_seq=49 ttl=57 time=37.2 ms
[1780155575.843404] 64 bytes from 2620:fe::fe: icmp_seq=50 ttl=57 time=37.5 ms

--- 2620:fe::fe ping statistics ---
50 packets transmitted, 50 received, 0% packet loss, time 9831ms
rtt min/avg/max/mdev = 36.198/37.406/41.057/0.767 ms
 etu@R2  ~  



Scenario 1 - R1 To R2 Link Failure
Baseline Before The Cut


R1# show ip route 10.20.0.0/24
Routing entry for 10.20.0.0/24
  Known via "ospf", distance 110, metric 80, best
  Last update 1d02h18m ago
  Flags: Selected 
  Status: Installed 
  * 10.44.0.2, via enp0s1.440, weight 1

R1# show ipv6 route fd14:ca46:3864:14::/64
Routing entry for fd14:ca46:3864:14::/64
  Known via "ospf6", distance 110, metric 80, best
  Last update 1d02h18m ago
  Flags: Selected 
  Status: Installed 
  * fe80::baad:caff:fefe:3f, via enp0s1.440, weight 1

R1# 


R2# show ip route 10.10.0.0/24
Routing entry for 10.10.0.0/24
  Known via "ospf", distance 110, metric 80, best
  Last update 1d02h19m ago
  Flags: Selected 
  Status: Installed 
  * 10.44.0.1, via enp0s1.440, weight 1

R2# show ip route 0.0.0.0/0 
Routing entry for 0.0.0.0/0
  Known via "ospf", distance 110, metric 10, best
  Last update 1d02h19m ago
  Flags: Selected 
  Status: Installed 
  * 10.44.0.1, via enp0s1.440, weight 1

R2# show ipv6 route fd14:ca46:3864:a::/64
Routing entry for fd14:ca46:3864:a::/64
  Known via "ospf6", distance 110, metric 80, best
  Last update 1d02h19m ago
  Flags: Selected 
  Status: Installed 
  * fe80::1b8:1, via enp0s1.440, weight 1

R2# show ipv6 route ::/0
Routing entry for ::/0
  Known via "ospf6", distance 110, metric 10, best
  Last update 1d02h09m ago
  Flags: Selected 
  Status: Installed 
  * fe80::1b8:1, via enp0s1.440, weight 1

R2# 


Cut The Link


 etu@R2  ~  date -Ins
sudo ip link set enp0s1.440 down
date -Ins
2026-05-30T18:07:57,171000993+02:00
2026-05-30T18:07:57,230359639+02:00


[1780157275.260418] 64 bytes from 10.10.0.169: icmp_seq=821 ttl=62 time=0.980 ms
[1780157275.460816] 64 bytes from 10.10.0.169: icmp_seq=822 ttl=62 time=1.00 ms
[1780157275.661169] 64 bytes from 10.10.0.169: icmp_seq=823 ttl=62 time=0.980 ms
[1780157275.861630] 64 bytes from 10.10.0.169: icmp_seq=824 ttl=62 time=0.967 ms
[1780157276.061992] 64 bytes from 10.10.0.169: icmp_seq=825 ttl=62 time=0.948 ms
[1780157276.262368] 64 bytes from 10.10.0.169: icmp_seq=826 ttl=62 time=0.986 ms
[1780157276.462617] 64 bytes from 10.10.0.169: icmp_seq=827 ttl=62 time=0.830 ms
[1780157276.664793] 64 bytes from 10.10.0.169: icmp_seq=828 ttl=62 time=0.951 ms
[1780157276.865150] 64 bytes from 10.10.0.169: icmp_seq=829 ttl=62 time=0.969 ms
[1780157277.065499] 64 bytes from 10.10.0.169: icmp_seq=830 ttl=62 time=0.957 ms
[1780157277.267274] 64 bytes from 10.10.0.169: icmp_seq=831 ttl=61 time=2.42 ms
[1780157277.467680] 64 bytes from 10.10.0.169: icmp_seq=832 ttl=61 time=2.00 ms
[1780157277.667953] 64 bytes from 10.10.0.169: icmp_seq=833 ttl=61 time=1.86 ms
[1780157277.869293] 64 bytes from 10.10.0.169: icmp_seq=834 ttl=61 time=1.95 ms
[1780157278.069554] 64 bytes from 10.10.0.169: icmp_seq=835 ttl=61 time=1.86 ms
[1780157278.270706] 64 bytes from 10.10.0.169: icmp_seq=836 ttl=61 time=1.75 ms
[1780157278.471995] 64 bytes from 10.10.0.169: icmp_seq=837 ttl=61 time=1.89 ms
[1780157278.673288] 64 bytes from 10.10.0.169: icmp_seq=838 ttl=61 time=1.86 ms
[1780157278.874699] 64 bytes from 10.10.0.169: icmp_seq=839 ttl=61 time=2.01 ms



R2# show ip ospf neighbor

Neighbor ID     Pri State           Up Time         Dead Time Address         Interface                        RXmtL RqstL DBsmL
3.0.0.4           1 Full/Backup     1d07h45m          36.917s 10.44.2.3       enp0s1.442:10.44.2.2                 0     0     0

R2# show ipv6 ospf6 neighbor
Neighbor ID     Pri    DeadTime    State/IfState         Duration I/F[State]
3.0.0.6           1    00:00:35     Full/BDR           1d07:45:41 enp0s1.442[DR]
R2# show ip route 10.10.0.0/24
Routing entry for 10.10.0.0/24
  Known via "ospf", distance 110, metric 120, best
  Last update 00:02:26 ago
  Flags: Selected 
  Status: Installed 
  * 10.44.2.3, via enp0s1.442, weight 1

R2# show ip route 0.0.0.0/0
Routing entry for 0.0.0.0/0
  Known via "ospf", distance 110, metric 10, best
  Last update 00:02:38 ago
  Flags: Selected 
  Status: Installed 
  * 10.44.2.3, via enp0s1.442, weight 1

R2# show ipv6 route fd14:ca46:3864:a::/64
Routing entry for fd14:ca46:3864:a::/64
  Known via "ospf6", distance 110, metric 120, best
  Last update 00:02:47 ago
  Flags: Selected 
  Status: Installed 
  * fe80::1ba:3, via enp0s1.442, weight 1

R2# show ipv6 route ::/0
Routing entry for ::/0
  Known via "ospf6", distance 110, metric 10, best
  Last update 00:01:54 ago
  Flags: Selected 
  Status: Installed 
  * fe80::1ba:3, via enp0s1.442, weight 1

R2# 



Restore The Link


 etu@R2  ~  date -Ins
sudo ip link set enp0s1.440 up
date -Ins
2026-05-30T18:12:30,658261754+02:00
2026-05-30T18:12:30,716995936+02:00
 etu@R2  ~  



[1780157534.238119] 64 bytes from 10.10.0.169: icmp_seq=2109 ttl=61 time=1.90 ms
[1780157534.438328] 64 bytes from 10.10.0.169: icmp_seq=2110 ttl=61 time=1.80 ms
[1780157534.639323] 64 bytes from 10.10.0.169: icmp_seq=2111 ttl=61 time=1.56 ms
[1780157534.840406] 64 bytes from 10.10.0.169: icmp_seq=2112 ttl=61 time=1.66 ms
[1780157535.041476] 64 bytes from 10.10.0.169: icmp_seq=2113 ttl=61 time=1.67 ms
[1780157535.242562] 64 bytes from 10.10.0.169: icmp_seq=2114 ttl=61 time=1.68 ms
[1780157535.443669] 64 bytes from 10.10.0.169: icmp_seq=2115 ttl=61 time=1.70 ms
[1780157535.644790] 64 bytes from 10.10.0.169: icmp_seq=2116 ttl=61 time=1.68 ms
[1780157535.845851] 64 bytes from 10.10.0.169: icmp_seq=2117 ttl=61 time=1.66 ms
[1780157536.046885] 64 bytes from 10.10.0.169: icmp_seq=2118 ttl=61 time=1.63 ms
[1780157536.247987] 64 bytes from 10.10.0.169: icmp_seq=2119 ttl=61 time=1.69 ms
[1780157536.449037] 64 bytes from 10.10.0.169: icmp_seq=2120 ttl=61 time=1.64 ms
[1780157536.650100] 64 bytes from 10.10.0.169: icmp_seq=2121 ttl=61 time=1.67 ms
[1780157536.851147] 64 bytes from 10.10.0.169: icmp_seq=2122 ttl=61 time=1.64 ms
[1780157537.052301] 64 bytes from 10.10.0.169: icmp_seq=2123 ttl=61 time=1.74 ms
[1780157537.253496] 64 bytes from 10.10.0.169: icmp_seq=2124 ttl=61 time=1.78 ms
[1780157537.454555] 64 bytes from 10.10.0.169: icmp_seq=2125 ttl=61 time=1.68 ms
[1780157537.655621] 64 bytes from 10.10.0.169: icmp_seq=2126 ttl=61 time=1.66 ms
[1780157537.856673] 64 bytes from 10.10.0.169: icmp_seq=2127 ttl=61 time=1.63 ms
[1780157538.057719] 64 bytes from 10.10.0.169: icmp_seq=2128 ttl=61 time=1.65 ms
[1780157538.258741] 64 bytes from 10.10.0.169: icmp_seq=2129 ttl=61 time=1.61 ms
[1780157538.459743] 64 bytes from 10.10.0.169: icmp_seq=2130 ttl=61 time=1.58 ms
[1780157538.660816] 64 bytes from 10.10.0.169: icmp_seq=2131 ttl=61 time=1.67 ms
[1780157538.861859] 64 bytes from 10.10.0.169: icmp_seq=2132 ttl=61 time=1.68 ms
[1780157539.062994] 64 bytes from 10.10.0.169: icmp_seq=2133 ttl=61 time=1.74 ms
[1780157539.264142] 64 bytes from 10.10.0.169: icmp_seq=2134 ttl=61 time=1.73 ms
[1780157539.465212] 64 bytes from 10.10.0.169: icmp_seq=2135 ttl=61 time=1.68 ms
[1780157539.666294] 64 bytes from 10.10.0.169: icmp_seq=2136 ttl=61 time=1.68 ms
[1780157539.867403] 64 bytes from 10.10.0.169: icmp_seq=2137 ttl=61 time=1.71 ms
[1780157540.068535] 64 bytes from 10.10.0.169: icmp_seq=2138 ttl=61 time=1.67 ms
[1780157540.269592] 64 bytes from 10.10.0.169: icmp_seq=2139 ttl=61 time=1.66 ms
[1780157540.470655] 64 bytes from 10.10.0.169: icmp_seq=2140 ttl=61 time=1.66 ms
[1780157540.671720] 64 bytes from 10.10.0.169: icmp_seq=2141 ttl=61 time=1.67 ms
[1780157540.872767] 64 bytes from 10.10.0.169: icmp_seq=2142 ttl=61 time=1.66 ms
[1780157541.073815] 64 bytes from 10.10.0.169: icmp_seq=2143 ttl=61 time=1.65 ms
[1780157541.274761] 64 bytes from 10.10.0.169: icmp_seq=2144 ttl=61 time=1.54 ms
[1780157541.475725] 64 bytes from 10.10.0.169: icmp_seq=2145 ttl=61 time=1.57 ms
[1780157541.676854] 64 bytes from 10.10.0.169: icmp_seq=2146 ttl=61 time=1.71 ms
[1780157541.877969] 64 bytes from 10.10.0.169: icmp_seq=2147 ttl=61 time=1.68 ms
[1780157542.079052] 64 bytes from 10.10.0.169: icmp_seq=2148 ttl=61 time=1.67 ms
[1780157542.280193] 64 bytes from 10.10.0.169: icmp_seq=2149 ttl=61 time=1.72 ms
[1780157542.481287] 64 bytes from 10.10.0.169: icmp_seq=2150 ttl=61 time=1.66 ms
[1780157542.682361] 64 bytes from 10.10.0.169: icmp_seq=2151 ttl=61 time=1.67 ms
[1780157542.883381] 64 bytes from 10.10.0.169: icmp_seq=2152 ttl=61 time=1.65 ms
[1780157543.084526] 64 bytes from 10.10.0.169: icmp_seq=2153 ttl=61 time=1.74 ms
[1780157543.285559] 64 bytes from 10.10.0.169: icmp_seq=2154 ttl=61 time=1.63 ms
[1780157543.486655] 64 bytes from 10.10.0.169: icmp_seq=2155 ttl=61 time=1.69 ms
[1780157543.687716] 64 bytes from 10.10.0.169: icmp_seq=2156 ttl=61 time=1.64 ms
[1780157543.888832] 64 bytes from 10.10.0.169: icmp_seq=2157 ttl=61 time=1.71 ms
[1780157544.089918] 64 bytes from 10.10.0.169: icmp_seq=2158 ttl=61 time=1.69 ms
[1780157544.290917] 64 bytes from 10.10.0.169: icmp_seq=2159 ttl=61 time=1.59 ms
[1780157544.492061] 64 bytes from 10.10.0.169: icmp_seq=2160 ttl=61 time=1.73 ms
[1780157544.693146] 64 bytes from 10.10.0.169: icmp_seq=2161 ttl=61 time=1.66 ms
[1780157544.894167] 64 bytes from 10.10.0.169: icmp_seq=2162 ttl=61 time=1.65 ms
[1780157545.095094] 64 bytes from 10.10.0.169: icmp_seq=2163 ttl=61 time=1.54 ms
[1780157545.296195] 64 bytes from 10.10.0.169: icmp_seq=2164 ttl=61 time=1.70 ms
[1780157545.497274] 64 bytes from 10.10.0.169: icmp_seq=2165 ttl=61 time=1.64 ms
[1780157545.698297] 64 bytes from 10.10.0.169: icmp_seq=2166 ttl=61 time=1.62 ms
[1780157545.899102] 64 bytes from 10.10.0.169: icmp_seq=2167 ttl=61 time=1.39 ms
[1780157546.100178] 64 bytes from 10.10.0.169: icmp_seq=2168 ttl=61 time=1.64 ms
[1780157546.301240] 64 bytes from 10.10.0.169: icmp_seq=2169 ttl=61 time=1.60 ms
[1780157546.502421] 64 bytes from 10.10.0.169: icmp_seq=2170 ttl=61 time=1.73 ms
[1780157546.703373] 64 bytes from 10.10.0.169: icmp_seq=2171 ttl=61 time=1.57 ms
[1780157546.904395] 64 bytes from 10.10.0.169: icmp_seq=2172 ttl=61 time=1.64 ms
[1780157547.105504] 64 bytes from 10.10.0.169: icmp_seq=2173 ttl=61 time=1.71 ms
[1780157547.306646] 64 bytes from 10.10.0.169: icmp_seq=2174 ttl=61 time=1.74 ms
[1780157547.507717] 64 bytes from 10.10.0.169: icmp_seq=2175 ttl=61 time=1.67 ms
[1780157547.708829] 64 bytes from 10.10.0.169: icmp_seq=2176 ttl=61 time=1.73 ms
[1780157547.909899] 64 bytes from 10.10.0.169: icmp_seq=2177 ttl=61 time=1.66 ms
[1780157548.110757] 64 bytes from 10.10.0.169: icmp_seq=2178 ttl=61 time=1.46 ms
[1780157548.311631] 64 bytes from 10.10.0.169: icmp_seq=2179 ttl=61 time=1.51 ms
[1780157548.512769] 64 bytes from 10.10.0.169: icmp_seq=2180 ttl=61 time=1.73 ms
[1780157548.713811] 64 bytes from 10.10.0.169: icmp_seq=2181 ttl=61 time=1.64 ms
[1780157548.914894] 64 bytes from 10.10.0.169: icmp_seq=2182 ttl=61 time=1.66 ms
[1780157549.115979] 64 bytes from 10.10.0.169: icmp_seq=2183 ttl=61 time=1.65 ms
[1780157549.317008] 64 bytes from 10.10.0.169: icmp_seq=2184 ttl=61 time=1.63 ms
[1780157549.518025] 64 bytes from 10.10.0.169: icmp_seq=2185 ttl=61 time=1.65 ms
[1780157549.719166] 64 bytes from 10.10.0.169: icmp_seq=2186 ttl=61 time=1.72 ms
[1780157549.920242] 64 bytes from 10.10.0.169: icmp_seq=2187 ttl=61 time=1.64 ms
[1780157550.121302] 64 bytes from 10.10.0.169: icmp_seq=2188 ttl=61 time=1.65 ms
[1780157550.322304] 64 bytes from 10.10.0.169: icmp_seq=2189 ttl=61 time=1.62 ms
[1780157550.523427] 64 bytes from 10.10.0.169: icmp_seq=2190 ttl=61 time=1.71 ms
[1780157550.724632] 64 bytes from 10.10.0.169: icmp_seq=2191 ttl=61 time=1.71 ms
[1780157550.925743] 64 bytes from 10.10.0.169: icmp_seq=2192 ttl=61 time=1.70 ms
[1780157551.126835] 64 bytes from 10.10.0.169: icmp_seq=2193 ttl=61 time=1.68 ms
[1780157551.327906] 64 bytes from 10.10.0.169: icmp_seq=2194 ttl=61 time=1.65 ms
[1780157551.528983] 64 bytes from 10.10.0.169: icmp_seq=2195 ttl=61 time=1.69 ms
[1780157551.730053] 64 bytes from 10.10.0.169: icmp_seq=2196 ttl=61 time=1.67 ms
[1780157551.931020] 64 bytes from 10.10.0.169: icmp_seq=2197 ttl=61 time=1.54 ms
[1780157552.132123] 64 bytes from 10.10.0.169: icmp_seq=2198 ttl=61 time=1.69 ms
[1780157552.333154] 64 bytes from 10.10.0.169: icmp_seq=2199 ttl=61 time=1.65 ms
[1780157552.534207] 64 bytes from 10.10.0.169: icmp_seq=2200 ttl=61 time=1.65 ms
[1780157552.735374] 64 bytes from 10.10.0.169: icmp_seq=2201 ttl=61 time=1.72 ms
[1780157552.936450] 64 bytes from 10.10.0.169: icmp_seq=2202 ttl=61 time=1.68 ms
[1780157553.137537] 64 bytes from 10.10.0.169: icmp_seq=2203 ttl=61 time=1.68 ms
[1780157553.338654] 64 bytes from 10.10.0.169: icmp_seq=2204 ttl=61 time=1.71 ms
[1780157553.539678] 64 bytes from 10.10.0.169: icmp_seq=2205 ttl=61 time=1.60 ms
[1780157553.740820] 64 bytes from 10.10.0.169: icmp_seq=2206 ttl=61 time=1.68 ms
[1780157553.942004] 64 bytes from 10.10.0.169: icmp_seq=2207 ttl=61 time=1.74 ms
[1780157554.143137] 64 bytes from 10.10.0.169: icmp_seq=2208 ttl=61 time=1.73 ms
[1780157554.344244] 64 bytes from 10.10.0.169: icmp_seq=2209 ttl=61 time=1.71 ms
[1780157554.545428] 64 bytes from 10.10.0.169: icmp_seq=2210 ttl=61 time=1.76 ms
[1780157554.746382] 64 bytes from 10.10.0.169: icmp_seq=2211 ttl=61 time=1.54 ms
[1780157554.947343] 64 bytes from 10.10.0.169: icmp_seq=2212 ttl=61 time=1.56 ms
[1780157555.148336] 64 bytes from 10.10.0.169: icmp_seq=2213 ttl=61 time=1.59 ms
[1780157555.348960] 64 bytes from 10.10.0.169: icmp_seq=2214 ttl=61 time=1.18 ms
[1780157555.549595] 64 bytes from 10.10.0.169: icmp_seq=2215 ttl=61 time=1.23 ms
[1780157555.750139] 64 bytes from 10.10.0.169: icmp_seq=2216 ttl=61 time=1.11 ms
[1780157555.950710] 64 bytes from 10.10.0.169: icmp_seq=2217 ttl=61 time=1.19 ms
[1780157556.151275] 64 bytes from 10.10.0.169: icmp_seq=2218 ttl=61 time=1.18 ms
[1780157556.351936] 64 bytes from 10.10.0.169: icmp_seq=2219 ttl=61 time=1.28 ms
[1780157556.552675] 64 bytes from 10.10.0.169: icmp_seq=2220 ttl=61 time=1.32 ms
[1780157556.753377] 64 bytes from 10.10.0.169: icmp_seq=2221 ttl=61 time=1.31 ms
[1780157556.953980] 64 bytes from 10.10.0.169: icmp_seq=2222 ttl=61 time=1.20 ms
[1780157557.154669] 64 bytes from 10.10.0.169: icmp_seq=2223 ttl=61 time=1.27 ms
[1780157557.355279] 64 bytes from 10.10.0.169: icmp_seq=2224 ttl=61 time=1.20 ms
[1780157557.555971] 64 bytes from 10.10.0.169: icmp_seq=2225 ttl=61 time=1.30 ms
[1780157557.756705] 64 bytes from 10.10.0.169: icmp_seq=2226 ttl=61 time=1.31 ms
[1780157557.957441] 64 bytes from 10.10.0.169: icmp_seq=2227 ttl=61 time=1.33 ms
[1780157558.158124] 64 bytes from 10.10.0.169: icmp_seq=2228 ttl=61 time=1.29 ms
[1780157558.358753] 64 bytes from 10.10.0.169: icmp_seq=2229 ttl=61 time=1.23 ms
[1780157558.559486] 64 bytes from 10.10.0.169: icmp_seq=2230 ttl=61 time=1.32 ms
[1780157558.760215] 64 bytes from 10.10.0.169: icmp_seq=2231 ttl=61 time=1.33 ms
[1780157558.961038] 64 bytes from 10.10.0.169: icmp_seq=2232 ttl=61 time=1.39 ms
[1780157559.161755] 64 bytes from 10.10.0.169: icmp_seq=2233 ttl=61 time=1.31 ms
[1780157559.362369] 64 bytes from 10.10.0.169: icmp_seq=2234 ttl=61 time=1.23 ms
[1780157559.563066] 64 bytes from 10.10.0.169: icmp_seq=2235 ttl=61 time=1.29 ms
[1780157559.763659] 64 bytes from 10.10.0.169: icmp_seq=2236 ttl=61 time=1.19 ms
[1780157559.964403] 64 bytes from 10.10.0.169: icmp_seq=2237 ttl=61 time=1.33 ms
[1780157560.164824] 64 bytes from 10.10.0.169: icmp_seq=2238 ttl=62 time=1.02 ms
[1780157560.365176] 64 bytes from 10.10.0.169: icmp_seq=2239 ttl=62 time=0.943 ms
[1780157560.565535] 64 bytes from 10.10.0.169: icmp_seq=2240 ttl=62 time=1.01 ms
[1780157560.765811] 64 bytes from 10.10.0.169: icmp_seq=2241 ttl=62 time=0.869 ms
[1780157560.968807] 64 bytes from 10.10.0.169: icmp_seq=2242 ttl=62 time=0.967 ms
[1780157561.169170] 64 bytes from 10.10.0.169: icmp_seq=2243 ttl=62 time=0.949 ms
[1780157561.369525] 64 bytes from 10.10.0.169: icmp_seq=2244 ttl=62 time=0.933 ms
[1780157561.569897] 64 bytes from 10.10.0.169: icmp_seq=2245 ttl=62 time=0.988 ms
[1780157561.770292] 64 bytes from 10.10.0.169: icmp_seq=2246 ttl=62 time=0.985 ms
[1780157561.970719] 64 bytes from 10.10.0.169: icmp_seq=2247 ttl=62 time=1.03 ms



R2# show ip ospf neighbor

Neighbor ID     Pri State           Up Time         Dead Time Address         Interface                        RXmtL RqstL DBsmL
3.0.0.4           1 Full/Backup     1d07h50m          34.495s 10.44.2.3       enp0s1.442:10.44.2.2                 0     0     0
1.0.0.4           1 Full/DR         1m55s             34.496s 10.44.0.1       enp0s1.440:10.44.0.2                 0     0     0

R2# show ipv6 ospf6 neighbor
Neighbor ID     Pri    DeadTime    State/IfState         Duration I/F[State]
1.0.0.6           1    00:00:32     Full/DR              00:02:07 enp0s1.440[BDR]
3.0.0.6           1    00:00:37     Full/BDR           1d07:50:09 enp0s1.442[DR]
R2# 




Scenario 2 - FRR Restart

 etu@R2  ~  systemctl --no-pager status frr
date -Ins
sudo systemctl restart frr
date -Ins
systemctl --no-pager status frr
● frr.service - FRRouting
     Loaded: loaded (/usr/lib/systemd/system/frr.service; enabled; preset: enabled)
     Active: active (running) since Fri 2026-05-29 09:39:29 CEST; 1 day 8h ago
 Invocation: c2c28266a6bd49b5a1a41a2d2aa72bf3
       Docs: https://frrouting.readthedocs.io/en/latest/setup.html
   Main PID: 953 (watchfrr)
     Status: "FRR Operational"
      Tasks: 12 (limit: 4594)
     Memory: 54.9M (peak: 68.1M)
        CPU: 1min 48.809s
     CGroup: /system.slice/frr.service
             ├─ 953 /usr/lib/frr/watchfrr -d mgmtd zebra ospfd ospf6d staticd
             ├─ 974 /usr/lib/frr/mgmtd -d -F traditional -A 127.0.0.1
             ├─1014 /usr/lib/frr/zebra -d -F traditional -A 127.0.0.1 -s 90000000
             ├─1022 /usr/lib/frr/ospfd -d -F traditional -A 127.0.0.1
             ├─1026 /usr/lib/frr/ospf6d -d -F traditional -A ::1
             └─1029 /usr/lib/frr/staticd -d -F traditional -A 127.0.0.1

May 30 18:12:35 R2 ospfd[1022]: [Y05P2-YJVXY] AdjChg: Nbr 1.0.0.4, NbrIP 10.44.0.1 (default) on enp0s1.440:10.44.0.2: Ex…ationDone)
May 30 18:12:35 R2 ospfd[1022]: [YPCA4-JHA8Q] default:Packet[DD]: 1.0.0.4 DB Desc send with seqnum:3bda26fb , flags:1
May 30 18:12:35 R2 ospfd[1022]: [SXPB9-WR7E3] default:Packet[DD]: Neighbor 1.0.0.4 state is Exchange, seq_num:0x3bda26fb…0x3bda26fb
May 30 18:12:35 R2 ospfd[1022]: [Y05P2-YJVXY] AdjChg: Nbr 1.0.0.4, NbrIP 10.44.0.1 (default) on enp0s1.440:10.44.0.2: Ex…hangeDone)
May 30 18:12:35 R2 ospfd[1022]: [S3578-FNEB0] nsm_change_state:[1.0.0.4:default], Exchange -> Full): scheduling new rout…rigination
May 30 18:12:35 R2 ospf6d[1026]: [GHN28-AMRE7] AdjChg: Nbr 1.0.0.6(default) on 1.0.0.6%enp0s1.440: Down -> Init (HelloReceived)
May 30 18:12:35 R2 ospf6d[1026]: [GHN28-AMRE7] AdjChg: Nbr 1.0.0.6(default) on 1.0.0.6%enp0s1.440: Init -> Twoway (2-WayReceived)
May 30 18:12:35 R2 ospf6d[1026]: [GHN28-AMRE7] AdjChg: Nbr 1.0.0.6(default) on 1.0.0.6%enp0s1.440: Twoway -> ExStart (AdjOK?)
May 30 18:12:36 R2 ospf6d[1026]: [GHN28-AMRE7] AdjChg: Nbr 1.0.0.6(default) on 1.0.0.6%enp0s1.440: ExStart -> ExChange (…ationDone)
May 30 18:12:36 R2 ospf6d[1026]: [GHN28-AMRE7] AdjChg: Nbr 1.0.0.6(default) on 1.0.0.6%enp0s1.440: ExChange -> Full (ExchangeDone)
Hint: Some lines were ellipsized, use -l to show in full.
2026-05-30T18:23:04,442071692+02:00
2026-05-30T18:23:05,198437393+02:00
● frr.service - FRRouting
     Loaded: loaded (/usr/lib/systemd/system/frr.service; enabled; preset: enabled)
     Active: active (running) since Sat 2026-05-30 18:23:05 CEST; 53ms ago
 Invocation: 3b37a04846ad48e788fd0afd6ee0c805
       Docs: https://frrouting.readthedocs.io/en/latest/setup.html
    Process: 13973 ExecStart=/usr/lib/frr/frrinit.sh start (code=exited, status=0/SUCCESS)
   Main PID: 13982 (watchfrr)
     Status: "FRR Operational"
      Tasks: 12 (limit: 4594)
     Memory: 24.9M (peak: 40.2M)
        CPU: 423ms
     CGroup: /system.slice/frr.service
             ├─13982 /usr/lib/frr/watchfrr -d mgmtd zebra ospfd ospf6d staticd
             ├─13995 /usr/lib/frr/mgmtd -d -F traditional -A 127.0.0.1
             ├─13997 /usr/lib/frr/zebra -d -F traditional -A 127.0.0.1 -s 90000000
             ├─14002 /usr/lib/frr/ospfd -d -F traditional -A 127.0.0.1
             ├─14005 /usr/lib/frr/ospf6d -d -F traditional -A ::1
             └─14008 /usr/lib/frr/staticd -d -F traditional -A 127.0.0.1

May 30 18:23:05 R2 ospf6d[14005]: [VTVCM-Y2NW3] Configuration Read in Took: 00:00:00
May 30 18:23:05 R2 frrinit.sh[14017]: [14017|ospf6d] done
May 30 18:23:05 R2 watchfrr[13982]: [QDG3Y-BY5TN] mgmtd state -> up : connect succeeded
May 30 18:23:05 R2 watchfrr[13982]: [QDG3Y-BY5TN] zebra state -> up : connect succeeded
May 30 18:23:05 R2 watchfrr[13982]: [QDG3Y-BY5TN] ospfd state -> up : connect succeeded
May 30 18:23:05 R2 watchfrr[13982]: [QDG3Y-BY5TN] ospf6d state -> up : connect succeeded
May 30 18:23:05 R2 watchfrr[13982]: [QDG3Y-BY5TN] staticd state -> up : connect succeeded
May 30 18:23:05 R2 watchfrr[13982]: [KWE5Q-QNGFC] all daemons up, doing startup-complete notify
May 30 18:23:05 R2 frrinit.sh[13973]: Started watchfrr.
May 30 18:23:05 R2 systemd[1]: Started frr.service - FRRouting.
 etu@R2  ~  



[1780158183.139310] 64 bytes from 10.20.0.89: icmp_seq=166 ttl=62 time=1.02 ms
[1780158183.339731] 64 bytes from 10.20.0.89: icmp_seq=167 ttl=62 time=0.970 ms
[1780158183.540084] 64 bytes from 10.20.0.89: icmp_seq=168 ttl=62 time=0.933 ms
[1780158183.740517] 64 bytes from 10.20.0.89: icmp_seq=169 ttl=62 time=1.00 ms
[1780158183.940896] 64 bytes from 10.20.0.89: icmp_seq=170 ttl=62 time=0.950 ms
[1780158184.141261] 64 bytes from 10.20.0.89: icmp_seq=171 ttl=62 time=0.945 ms
[1780158184.341623] 64 bytes from 10.20.0.89: icmp_seq=172 ttl=62 time=0.973 ms
[1780158184.541842] 64 bytes from 10.20.0.89: icmp_seq=173 ttl=62 time=0.795 ms
[1780158190.455491] 64 bytes from 10.20.0.89: icmp_seq=202 ttl=62 time=1.07 ms
[1780158190.655875] 64 bytes from 10.20.0.89: icmp_seq=203 ttl=62 time=0.957 ms
[1780158190.856340] 64 bytes from 10.20.0.89: icmp_seq=204 ttl=62 time=1.04 ms
[1780158191.056741] 64 bytes from 10.20.0.89: icmp_seq=205 ttl=62 time=0.980 ms
[1780158191.257099] 64 bytes from 10.20.0.89: icmp_seq=206 ttl=62 time=0.944 ms
[1780158191.457502] 64 bytes from 10.20.0.89: icmp_seq=207 ttl=62 time=0.992 ms
[1780158191.657923] 64 bytes from 10.20.0.89: icmp_seq=208 ttl=62 time=0.998 ms
[1780158191.858506] 64 bytes from 10.20.0.89: icmp_seq=209 ttl=62 time=1.15 ms
[1780158192.058924] 64 bytes from 10.20.0.89: icmp_seq=210 ttl=62 time=1.00 ms
[1780158192.259433] 64 bytes from 10.20.0.89: icmp_seq=211 ttl=62 time=1.08 ms
[1780158192.459820] 64 bytes from 10.20.0.89: icmp_seq=212 ttl=62 time=0.972 ms
[1780158192.660195] 64 bytes from 10.20.0.89: icmp_seq=213 ttl=62 time=0.952 ms
[1780158192.860457] 64 bytes from 10.20.0.89: icmp_seq=214 ttl=62 time=0.842 ms
[1780158193.063160] 64 bytes from 10.20.0.89: icmp_seq=215 ttl=62 time=0.813 ms
[1780158193.267107] 64 bytes from 10.20.0.89: icmp_seq=216 ttl=62 time=0.693 ms
[1780158193.471137] 64 bytes from 10.20.0.89: icmp_seq=217 ttl=62 time=0.745 ms



Scenario 3 - Router Reboot


 etu@R2  ~  date -Ins
sudo reboot
2026-05-30T18:28:28,770602581+02:00
 etu@R2  ~  Connection to 10.99.0.2 closed by remote host.
Connection to 10.99.0.2 closed.
 ✘ amir@Amirmahdis-MacBook-Pro  ~  ssh r2
Linux R2 7.0.9+deb14-cloud-amd64 #1 SMP PREEMPT_DYNAMIC Debian 7.0.9-1 (2026-05-22) x86_64

The programs included with the Debian GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.
Last login: Sat May 30 18:05:58 2026 from 10.99.0.1
-bash: avertissement :setlocale: LC_CTYPE: impossible de changer le paramètre de langue (UTF-8): Aucun fichier ou dossier de ce nom
-bash: avertissement :setlocale: LC_CTYPE: impossible de changer le paramètre de langue (UTF-8): Aucun fichier ou dossier de ce nom
-bash: avertissement :setlocale: LC_CTYPE: impossible de changer le paramètre de langue (UTF-8): Aucun fichier ou dossier de ce nom
-bash: avertissement :setlocale: LC_CTYPE: impossible de changer le paramètre de langue (UTF-8): Aucun fichier ou dossier de ce nom
-bash: avertissement :setlocale: LC_CTYPE: impossible de changer le paramètre de langue (UTF-8): Aucun fichier ou dossier de ce nom
-bash: avertissement :setlocale: LC_CTYPE: impossible de changer le paramètre de langue (UTF-8): Aucun fichier ou dossier de ce nom
-bash: avertissement :setlocale: LC_CTYPE: impossible de changer le paramètre de langue (UTF-8): Aucun fichier ou dossier de ce nom
-bash: avertissement :setlocale: LC_CTYPE: impossible de changer le paramètre de langue (UTF-8): Aucun fichier ou dossier de ce nom
 etu@R2  ~  uptime
systemctl --no-pager status frr
vtysh -c "show ip ospf neighbor"
vtysh -c "show ipv6 ospf6 neighbor"
vtysh -c "show ip route"
vtysh -c "show ipv6 route"
 18:30:10 up 1 min,  1 user,  load average: 0.00, 0.00, 0.00
● frr.service - FRRouting
     Loaded: loaded (/usr/lib/systemd/system/frr.service; enabled; preset: enabled)
     Active: active (running) since Sat 2026-05-30 18:28:52 CEST; 1min 17s ago
 Invocation: 99d63bf25d054c099b17682b6f2b1975
       Docs: https://frrouting.readthedocs.io/en/latest/setup.html
    Process: 955 ExecStart=/usr/lib/frr/frrinit.sh start (code=exited, status=0/SUCCESS)
   Main PID: 1037 (watchfrr)
     Status: "FRR Operational"
      Tasks: 12 (limit: 4597)
     Memory: 55M (peak: 68.7M)
        CPU: 547ms
     CGroup: /system.slice/frr.service
             ├─1037 /usr/lib/frr/watchfrr -d mgmtd zebra ospfd ospf6d staticd
             ├─1061 /usr/lib/frr/mgmtd -d -F traditional -A 127.0.0.1
             ├─1101 /usr/lib/frr/zebra -d -F traditional -A 127.0.0.1 -s 90000000
             ├─1110 /usr/lib/frr/ospfd -d -F traditional -A 127.0.0.1
             ├─1114 /usr/lib/frr/ospf6d -d -F traditional -A ::1
             └─1117 /usr/lib/frr/staticd -d -F traditional -A 127.0.0.1

May 30 18:29:32 R2 ospfd[1110]: [Y05P2-YJVXY] AdjChg: Nbr 3.0.0.4, NbrIP 10.44.2.3 (default) on enp0s1.442:10.44.2.2: Lo…adingDone)
May 30 18:29:32 R2 ospfd[1110]: [S3578-FNEB0] nsm_change_state:[3.0.0.4:default], Loading -> Full): scheduling new route…rigination
May 30 18:29:37 R2 ospfd[1110]: [XGKSD-28KJC] default:Packet[DD]: 1.0.0.4 DB Desc resend with seqnum:10bbd747 , flags:7
May 30 18:29:37 R2 ospfd[1110]: [SXPB9-WR7E3] default:Packet[DD]: Neighbor 1.0.0.4 state is ExStart, seq_num:0x10bbd747,…0x10bbd747
May 30 18:29:37 R2 ospfd[1110]: [S5PCG-77H23] Packet[DD]: Neighbor 1.0.0.4 Negotiation done (Master).
May 30 18:29:37 R2 ospfd[1110]: [Y05P2-YJVXY] AdjChg: Nbr 1.0.0.4, NbrIP 10.44.0.1 (default) on enp0s1.440:10.44.0.2: Ex…ationDone)
May 30 18:29:37 R2 ospfd[1110]: [YPCA4-JHA8Q] default:Packet[DD]: 1.0.0.4 DB Desc send with seqnum:10bbd748 , flags:1
May 30 18:29:37 R2 ospfd[1110]: [SXPB9-WR7E3] default:Packet[DD]: Neighbor 1.0.0.4 state is Exchange, seq_num:0x10bbd748…0x10bbd748
May 30 18:29:37 R2 ospfd[1110]: [Y05P2-YJVXY] AdjChg: Nbr 1.0.0.4, NbrIP 10.44.0.1 (default) on enp0s1.440:10.44.0.2: Ex…hangeDone)
May 30 18:29:37 R2 ospfd[1110]: [S3578-FNEB0] nsm_change_state:[1.0.0.4:default], Exchange -> Full): scheduling new rout…rigination
Hint: Some lines were ellipsized, use -l to show in full.
% Can't open configuration file /etc/frr/vtysh.conf due to 'Permission denied'.
Configuration file[/etc/frr/frr.conf] processing failure: 11

Neighbor ID     Pri State           Up Time         Dead Time Address         Interface                        RXmtL RqstL DBsmL
1.0.0.4           1 Full/DR         32.693s           34.999s 10.44.0.1       enp0s1.440:10.44.0.2                 0     0     0
3.0.0.4           1 Full/DR         37.689s           34.998s 10.44.2.3       enp0s1.442:10.44.2.2                 0     0     0

% Can't open configuration file /etc/frr/vtysh.conf due to 'Permission denied'.
Configuration file[/etc/frr/frr.conf] processing failure: 11
Neighbor ID     Pri    DeadTime    State/IfState         Duration I/F[State]
1.0.0.6           1    00:00:35     Full/DR              00:01:14 enp0s1.440[BDR]
3.0.0.6           1    00:00:30     Full/DR              00:01:09 enp0s1.442[BDR]
% Can't open configuration file /etc/frr/vtysh.conf due to 'Permission denied'.
Configuration file[/etc/frr/frr.conf] processing failure: 11
Codes: K - kernel route, C - connected, L - local, S - static,
       R - RIP, O - OSPF, I - IS-IS, B - BGP, E - EIGRP, N - NHRP,
       T - Table, v - VNC, V - VNC-Direct, A - Babel, F - PBR,
       f - OpenFabric, t - Table-Direct,
       > - selected route, * - FIB route, q - queued, r - rejected, b - backup
       t - trapped, o - offload failure

IPv4 unicast VRF default:
O>* 0.0.0.0/0 [110/10] via 10.44.0.1, enp0s1.440, weight 1, 00:00:32
O>* 10.10.0.0/24 [110/80] via 10.44.0.1, enp0s1.440, weight 1, 00:00:33
O   10.20.0.0/24 [110/40] is directly connected, vlan20, weight 1, 00:01:18
C>* 10.20.0.0/24 is directly connected, vlan20, weight 1, 00:01:18
L>* 10.20.0.1/32 is directly connected, vlan20, weight 1, 00:01:18
O>* 10.30.0.0/24 [110/80] via 10.44.2.3, enp0s1.442, weight 1, 00:00:33
O   10.44.0.0/29 [110/40] is directly connected, enp0s1.440, weight 1, 00:00:33
C>* 10.44.0.0/29 is directly connected, enp0s1.440, weight 1, 00:01:18
L>* 10.44.0.2/32 is directly connected, enp0s1.440, weight 1, 00:01:18
O>* 10.44.1.0/29 [110/80] via 10.44.0.1, enp0s1.440, weight 1, 00:00:33
  *                       via 10.44.2.3, enp0s1.442, weight 1, 00:00:33
O   10.44.2.0/29 [110/40] is directly connected, enp0s1.442, weight 1, 00:01:18
C>* 10.44.2.0/29 is directly connected, enp0s1.442, weight 1, 00:01:18
L>* 10.44.2.2/32 is directly connected, enp0s1.442, weight 1, 00:01:18
C>* 10.99.0.0/24 is directly connected, enp0s1.99, weight 1, 00:01:18
L>* 10.99.0.2/32 is directly connected, enp0s1.99, weight 1, 00:01:18
% Can't open configuration file /etc/frr/vtysh.conf due to 'Permission denied'.
Configuration file[/etc/frr/frr.conf] processing failure: 11
Codes: K - kernel route, C - connected, L - local, S - static,
       R - RIPng, O - OSPFv3, I - IS-IS, B - BGP, N - NHRP,
       T - Table, v - VNC, V - VNC-Direct, A - Babel, F - PBR,
       f - OpenFabric, t - Table-Direct,
       > - selected route, * - FIB route, q - queued, r - rejected, b - backup
       t - trapped, o - offload failure

IPv6 unicast VRF default:
O>* ::/0 [110/10] via fe80::1b8:1, enp0s1.440, weight 1, 00:00:13
O>* fd14:ca46:3864:a::/64 [110/80] via fe80::1b8:1, enp0s1.440, weight 1, 00:01:09
O   fd14:ca46:3864:14::/64 [110/40] is directly connected, vlan20, weight 1, 00:01:14
C>* fd14:ca46:3864:14::/64 is directly connected, vlan20, weight 1, 00:01:16
K * fd14:ca46:3864:14::/64 [0/256] is directly connected, vlan20, weight 1, 00:01:18
L>* fd14:ca46:3864:14::1/128 is directly connected, vlan20, weight 1, 00:01:16
O>* fd14:ca46:3864:1e::/64 [110/80] via fe80::1ba:3, enp0s1.442, weight 1, 00:01:09
C>* fd14:ca46:3864:99::/64 is directly connected, enp0s1.99, weight 1, 00:01:17
K * fd14:ca46:3864:99::/64 [0/256] is directly connected, enp0s1.99, weight 1, 00:01:18
L>* fd14:ca46:3864:99::2/128 is directly connected, enp0s1.99, weight 1, 00:01:17
C * fe80::/64 is directly connected, enp0s1.99, weight 1, 00:01:16
C * fe80::/64 is directly connected, vlan20, weight 1, 00:01:16
C * fe80::/64 is directly connected, enp0s1.440, weight 1, 00:01:17
C * fe80::/64 is directly connected, enp0s1.442, weight 1, 00:01:17
C * fe80::/64 is directly connected, asw-host, weight 1, 00:01:17
C>* fe80::/64 is directly connected, enp0s1, weight 1, 00:01:17


[1780158510.904889] 64 bytes from 10.20.0.89: icmp_seq=537 ttl=62 time=0.900 ms
[1780158511.105152] 64 bytes from 10.20.0.89: icmp_seq=538 ttl=62 time=0.862 ms
[1780158511.307444] 64 bytes from 10.20.0.89: icmp_seq=539 ttl=62 time=0.990 ms
[1780158511.507812] 64 bytes from 10.20.0.89: icmp_seq=540 ttl=62 time=0.944 ms
[1780158511.708233] 64 bytes from 10.20.0.89: icmp_seq=541 ttl=62 time=0.981 ms
[1780158511.908760] 64 bytes from 10.20.0.89: icmp_seq=542 ttl=62 time=1.06 ms
[1780158512.109225] 64 bytes from 10.20.0.89: icmp_seq=543 ttl=62 time=1.02 ms
[1780158512.309421] 64 bytes from 10.20.0.89: icmp_seq=544 ttl=62 time=0.780 ms
[1780158577.831799] From 10.44.1.3 icmp_seq=865 Time to live exceeded
[1780158578.032313] From 10.44.1.3 icmp_seq=866 Time to live exceeded
[1780158578.235850] From 10.44.1.3 icmp_seq=867 Time to live exceeded
[1780158578.432752] From 10.44.1.3 icmp_seq=868 Time to live exceeded
[1780158578.636299] From 10.44.1.3 icmp_seq=869 Time to live exceeded
[1780158578.834855] From 10.44.1.3 icmp_seq=870 Time to live exceeded
[1780158579.035980] From 10.44.1.3 icmp_seq=871 Time to live exceeded
[1780158579.840617] From 10.44.1.3 icmp_seq=875 Time to live exceeded
[1780158580.860399] From 10.44.1.3 icmp_seq=880 Time to live exceeded
[1780158581.876155] From 10.44.1.3 icmp_seq=885 Time to live exceeded
[1780158585.731993] From 10.44.0.2 icmp_seq=889 Destination Host Unreachable
[1780158585.732060] From 10.44.0.2 icmp_seq=890 Destination Host Unreachable
[1780158585.732083] From 10.44.0.2 icmp_seq=891 Destination Host Unreachable
[1780158585.732106] From 10.44.0.2 icmp_seq=892 Destination Host Unreachable
[1780158585.732128] From 10.44.0.2 icmp_seq=893 Destination Host Unreachable
[1780158585.732665] From 10.44.0.2 icmp_seq=894 Destination Host Unreachable
[1780158588.804131] From 10.44.0.2 icmp_seq=904 Destination Host Unreachable
[1780158588.804197] From 10.44.0.2 icmp_seq=905 Destination Host Unreachable
[1780158588.804221] From 10.44.0.2 icmp_seq=906 Destination Host Unreachable
[1780158592.068205] From 10.44.0.2 icmp_seq=920 Destination Host Unreachable
[1780158592.068268] From 10.44.0.2 icmp_seq=921 Destination Host Unreachable
[1780158592.068292] From 10.44.0.2 icmp_seq=922 Destination Host Unreachable
[1780158595.332188] From 10.44.0.2 icmp_seq=936 Destination Host Unreachable
[1780158595.332251] From 10.44.0.2 icmp_seq=937 Destination Host Unreachable
[1780158595.332275] From 10.44.0.2 icmp_seq=938 Destination Host Unreachable
[1780158598.596207] From 10.44.0.2 icmp_seq=952 Destination Host Unreachable
[1780158598.596273] From 10.44.0.2 icmp_seq=953 Destination Host Unreachable
[1780158598.596298] From 10.44.0.2 icmp_seq=954 Destination Host Unreachable
[1780158601.828299] From 10.44.0.2 icmp_seq=968 Destination Host Unreachable
[1780158601.828360] From 10.44.0.2 icmp_seq=969 Destination Host Unreachable
[1780158601.828384] From 10.44.0.2 icmp_seq=970 Destination Host Unreachable
[1780158601.828406] From 10.44.0.2 icmp_seq=971 Destination Host Unreachable
[1780158604.900233] From 10.44.0.2 icmp_seq=983 Destination Host Unreachable
[1780158604.900299] From 10.44.0.2 icmp_seq=984 Destination Host Unreachable
[1780158604.900323] From 10.44.0.2 icmp_seq=985 Destination Host Unreachable
[1780158608.164274] From 10.44.0.2 icmp_seq=999 Destination Host Unreachable
[1780158608.164336] From 10.44.0.2 icmp_seq=1000 Destination Host Unreachable
[1780158608.164362] From 10.44.0.2 icmp_seq=1001 Destination Host Unreachable
[1780158611.428409] From 10.44.0.2 icmp_seq=1015 Destination Host Unreachable
[1780158611.428472] From 10.44.0.2 icmp_seq=1016 Destination Host Unreachable
[1780158611.428495] From 10.44.0.2 icmp_seq=1017 Destination Host Unreachable
[1780158614.692470] From 10.44.0.2 icmp_seq=1031 Destination Host Unreachable
[1780158614.692532] From 10.44.0.2 icmp_seq=1032 Destination Host Unreachable
[1780158614.692556] From 10.44.0.2 icmp_seq=1033 Destination Host Unreachable
[1780158617.956407] From 10.44.0.2 icmp_seq=1047 Destination Host Unreachable
[1780158617.956468] From 10.44.0.2 icmp_seq=1048 Destination Host Unreachable
[1780158617.956492] From 10.44.0.2 icmp_seq=1049 Destination Host Unreachable
[1780158617.956514] From 10.44.0.2 icmp_seq=1050 Destination Host Unreachable
[1780158621.188494] From 10.44.0.2 icmp_seq=1063 Destination Host Unreachable
[1780158621.188557] From 10.44.0.2 icmp_seq=1064 Destination Host Unreachable
[1780158621.188581] From 10.44.0.2 icmp_seq=1065 Destination Host Unreachable
[1780158624.260470] From 10.44.0.2 icmp_seq=1078 Destination Host Unreachable
[1780158624.260535] From 10.44.0.2 icmp_seq=1079 Destination Host Unreachable
[1780158624.260559] From 10.44.0.2 icmp_seq=1080 Destination Host Unreachable
[1780158627.524570] From 10.44.0.2 icmp_seq=1094 Destination Host Unreachable
[1780158627.524631] From 10.44.0.2 icmp_seq=1095 Destination Host Unreachable
[1780158627.524655] From 10.44.0.2 icmp_seq=1096 Destination Host Unreachable
[1780158630.788582] From 10.44.0.2 icmp_seq=1110 Destination Host Unreachable
[1780158630.788644] From 10.44.0.2 icmp_seq=1111 Destination Host Unreachable
[1780158630.788667] From 10.44.0.2 icmp_seq=1112 Destination Host Unreachable
[1780158630.788690] From 10.44.0.2 icmp_seq=1113 Destination Host Unreachable
[1780158634.052633] From 10.44.0.2 icmp_seq=1126 Destination Host Unreachable
[1780158634.052702] From 10.44.0.2 icmp_seq=1127 Destination Host Unreachable
[1780158634.052725] From 10.44.0.2 icmp_seq=1128 Destination Host Unreachable
[1780158637.316628] From 10.44.0.2 icmp_seq=1142 Destination Host Unreachable
[1780158637.316692] From 10.44.0.2 icmp_seq=1143 Destination Host Unreachable
[1780158637.316716] From 10.44.0.2 icmp_seq=1144 Destination Host Unreachable
[1780158640.580673] From 10.44.0.2 icmp_seq=1158 Destination Host Unreachable
[1780158640.580764] From 10.44.0.2 icmp_seq=1159 Destination Host Unreachable
[1780158640.580788] From 10.44.0.2 icmp_seq=1160 Destination Host Unreachable
[1780158643.844713] From 10.44.0.2 icmp_seq=1174 Destination Host Unreachable
[1780158643.844777] From 10.44.0.2 icmp_seq=1175 Destination Host Unreachable
[1780158643.844800] From 10.44.0.2 icmp_seq=1176 Destination Host Unreachable
[1780158643.844823] From 10.44.0.2 icmp_seq=1177 Destination Host Unreachable
[1780158647.076748] From 10.44.0.2 icmp_seq=1190 Destination Host Unreachable
[1780158647.076813] From 10.44.0.2 icmp_seq=1191 Destination Host Unreachable
[1780158647.076836] From 10.44.0.2 icmp_seq=1192 Destination Host Unreachable
[1780158650.148772] From 10.44.0.2 icmp_seq=1205 Destination Host Unreachable
[1780158650.148838] From 10.44.0.2 icmp_seq=1206 Destination Host Unreachable
[1780158650.148863] From 10.44.0.2 icmp_seq=1207 Destination Host Unreachable
[1780158653.412815] From 10.44.0.2 icmp_seq=1221 Destination Host Unreachable
[1780158653.412879] From 10.44.0.2 icmp_seq=1222 Destination Host Unreachable
[1780158653.412903] From 10.44.0.2 icmp_seq=1223 Destination Host Unreachable
[1780158656.259953] 64 bytes from 10.20.0.89: icmp_seq=1250 ttl=62 time=1.58 ms
[1780158656.460161] 64 bytes from 10.20.0.89: icmp_seq=1251 ttl=62 time=0.793 ms
[1780158656.663407] 64 bytes from 10.20.0.89: icmp_seq=1252 ttl=62 time=1.00 ms
[1780158656.863784] 64 bytes from 10.20.0.89: icmp_seq=1253 ttl=62 time=0.977 ms
[1780158657.064164] 64 bytes from 10.20.0.89: icmp_seq=1254 ttl=62 time=0.960 ms
[1780158657.264551] 64 bytes from 10.20.0.89: icmp_seq=1255 ttl=62 time=0.961 ms
[1780158657.465030] 64 bytes from 10.20.0.89: icmp_seq=1256 ttl=62 time=1.07 ms
[1780158657.665384] 64 bytes from 10.20.0.89: icmp_seq=1257 ttl=62 time=0.936 ms
[1780158657.865719] 64 bytes from 10.20.0.89: icmp_seq=1258 ttl=62 time=0.922 ms
[1780158658.065944] 64 bytes from 10.20.0.89: icmp_seq=1259 ttl=62 time=0.834 ms
[1780158658.267388] 64 bytes from 10.20.0.89: icmp_seq=1260 ttl=62 time=0.904 ms
[1780158658.467748] 64 bytes from 10.20.0.89: icmp_seq=1261 ttl=62 time=0.937 ms
[1780158658.668083] 64 bytes from 10.20.0.89: icmp_seq=1262 ttl=62 time=0.935 ms
[1780158658.868466] 64 bytes from 10.20.0.89: icmp_seq=1263 ttl=62 time=0.966 ms
[1780158659.068831] 64 bytes from 10.20.0.89: icmp_seq=1264 ttl=62 time=0.951 ms
[1780158659.269139] 64 bytes from 10.20.0.89: icmp_seq=1265 ttl=62 time=0.887 ms


