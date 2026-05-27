# Addressing Plan

| Role | OSPF router-id | VLAN | Type | Addresses |
| --- | --- | ---: | --- | --- |
| R1 | OSPFv2 : `1.0.0.4`<br>OSPFv3 : `1.0.0.6` | 360 | Gateway | `192.168.104.129/29`<br>`fe80:168::1` |
|  |  | 99 | Management | `10.99.0.1/24`<br>`fd14:ca46:3864:99::1/64` |
|  |  | 440 | R1 -> R2 | `10.44.0.1/29`<br>`fe80::1b8:1/64` |
|  |  | 441 | R1 -> R3 | `10.44.1.1/29`<br>`fe80::1b9:1/64` |
|  |  | 10 | Hosting | `10.10.0.1/24`<br>`fd14:ca46:3864:a::1/64` |
| R2 | OSPFv2 : `2.0.0.4`<br>OSPFv3 : `2.0.0.6` | 440 | R2 -> R1 | `10.44.0.2/29`<br>`fe80::1b8:2/64` |
|  |  | 99 | Management | `10.99.0.2/24`<br>`fd14:ca46:3864:99::2/64` |
|  |  | 442 | R2 -> R3 | `10.44.2.2/29`<br>`fe80::1ba:2/64` |
|  |  | 20 | Hosting | `10.20.0.1/24`<br>`fd14:ca46:3864:14::1/64` |
| R3 | OSPFv2 : `3.0.0.4`<br>OSPFv3 : `3.0.0.6` | 441 | R3 -> R1 | `10.44.1.3/29`<br>`fe80::1b9:3/64` |
|  |  | 99 | Management | `10.99.0.3/24`<br>`fd14:ca46:3864:99::3/64` |
|  |  | 442 | R3 -> R2 | `10.44.2.3/29`<br>`fe80::1ba:3/64` |
|  |  | 30 | Hosting | `10.30.0.1/24`<br>`fd14:ca46:3864:1e::1/64` |
| Monitoring VM |  | 99 | IDS / monitoring management | `10.99.0.65/24`<br>`fd14:ca46:3864:99::65/64` |
| Management VM |  | 99 | Observability / dashboards | `10.99.0.66/24`<br>`fd14:ca46:3864:99::66/64` |

## VLAN Summary

| VLAN | Purpose | Notes |
| ---: | --- | --- |
| 360 | R1 gateway / infrastructure uplink | Used by R1 for the upstream/default route. |
| 99 | Management | Used for SSH, telemetry, monitoring, dashboards, and log collection. |
| 440 | R1 to R2 transit | OSPF backbone link. |
| 441 | R1 to R3 transit | OSPF backbone link. |
| 442 | R2 to R3 transit | OSPF backbone link. |
| 10 | R1 hosting | Hosting network behind R1. |
| 20 | R2 hosting | Hosting network behind R2. |
| 30 | R3 hosting | Hosting network behind R3. |

## Management VLAN

VLAN `99` is dedicated to internal lab management and observability traffic.

The management VLAN should be passive or excluded from OSPF neighbor formation. OSPF adjacencies should stay on the transit VLANs `440`, `441`, and `442`.

The Monitoring VM and Management VM use R1 as their default gateway on the management network:

| VM | Default Gateway |
| --- | --- |
| Monitoring VM | `10.99.0.1` |
| Management VM | `10.99.0.1` |
