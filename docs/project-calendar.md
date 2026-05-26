# Project Calendar

Condensed and realistic calendar from Sunday, May 24, 2026 to Monday, August 3, 2026.

Goal: complete `AI Network Security Lab` as a portfolio-ready project: OSPF, failure testing, observability, IDS, local AI, RAG, demo interface, documentation, and recruiter packaging.

This plan keeps all required tasks, but groups quick or repetitive tasks into the same day. The most sensitive days remain separated: OVS/TAP/Netplan, OSPF, logs/metrics, IDS, and Mac <-> server connectivity.

## References

- Main lab: [Introduction to dynamic OSPF routing with FRRouting](https://inetdoc.net/travaux_pratiques/interco_05.ospf/)
- Local architecture: [architecture.md](architecture.md)
- TAP plan: [tap-plan.md](tap-plan.md)
- Server resources: [server-resources.md](server-resources.md)
- AI stack: [ai-stack.md](ai-stack.md)

## Working Assumptions

- The schedule starts on Sunday, May 24, 2026.
- The routers follow the InetDoc OSPF lab, adapted to the local TAP plan:
  - `tap62`: router `R1`
  - `tap63`: router `R2`
  - `tap64`: router `R3`
  - `tap65`: Monitoring / IDS VM
  - `tap66`: Management / Observability VM
- `tap67`, `tap68`, and `tap69` remain reserved for expansion, DMZ, an extra client, or debugging.
- The OSPF topology is a triangle using a single `area 0`.
- Base VLANs:
  - VLAN `360`: infrastructure / default route through `R1`
  - VLAN `440`: `R1` to `R2` link
  - VLAN `441`: `R1` to `R3` link
  - VLAN `442`: `R2` to `R3` link
  - VLAN `10`, `20`, `30`: container hosting networks behind `R1`, `R2`, and `R3`
- OSPFv2 and OSPFv3 are configured with FRRouting.
- `R1` advertises the default route to `R2` and `R3`.
- AI inference runs on the MacBook Pro with Ollama; the university server has no GPU.
- Test evidence, packet captures, configurations, and notes are saved continuously.

## Condensed Overview

| Phase | Dates | Duration | Estimated workload | Goal | Expected outcome |
| --- | --- | ---: | ---: | --- | --- |
| Phase 0 | May 24 -> May 26 | 3 days | 8h30 | Planning and preparation | Repository, tracker, architecture, TAPs, VM templates, AI stack |
| Phase 1 | May 27 -> June 7 | 12 days | 37h30 | OSPF foundation | Complete IPv4/IPv6 OSPF triangle and backups |
| Phase 2 | June 8 -> June 12 | 5 days | 16h | Network failure testing | Failover scenarios and convergence measurements |
| Phase 3 | June 13 -> June 22 | 10 days | 34h | Observability | Prometheus, Grafana, Loki, metrics, and logs |
| Phase 4 | June 23 -> July 1 | 9 days | 31h | Security layer | IDS, simulated attacks, alerts, and incidents |
| Phase 5 | July 2 -> July 8 | 7 days | 24h | Local AI infrastructure | Ollama, benchmarks, Mac API, FastAPI backend |
| Phase 6 | July 9 -> July 16 | 8 days | 25h | AI security/network assistant | Incident, log, alert, and failure explanations |
| Phase 7 | July 17 -> July 22 | 6 days | 19h30 | Documentation RAG | ChromaDB, indexed docs, configs, and RFCs |
| Phase 8 | July 23 -> July 29 | 7 days | 26h | Demo interface | Topology UI, alerts, AI chat, incident timeline |
| Phase 9 | July 30 -> August 3 | 5 days | 17h | Portfolio packaging | GitHub, README, video, screenshots, CV, portfolio |

Recommended buffer: keep Tuesday, August 4, 2026 to Monday, August 10, 2026 as a buffer if OSPF, IDS, logs, or AI work runs late.

Total estimated workload: about 238h30, with an average of about 3h20 per day over 72 days. Four-hour days are the technical or integration-risk days; two-hour to two-and-a-half-hour days are mostly planning, documentation, or stabilization.

## Phase 0 - Project Planning & Environment Prep

Dates: Sunday, May 24, 2026 -> Tuesday, May 26, 2026

Goal: prepare everything needed before changing the infrastructure.

| Date | Estimated workload | Goal | Actions | Deliverable |
| --- | ---: | --- | --- | --- |
| Sunday, May 24, 2026 | 2h30 | Scope, repository, and tracker | Review the OSPF lab, `README.md`, `architecture.md`, `tap-plan.md`, and `server-resources.md`. Define the final project scope. Initialize or verify GitHub. Create a Kanban board, Notion page, or roadmap tracker with project labels. | Validated scope, GitHub repository, and project tracker. |
| Monday, May 25, 2026 | 2h | Architecture and TAPs | Finalize the architecture diagram. | Final architecture and confirmed or requested TAP allocation. |
| Tuesday, May 26, 2026 | 4h | VM templates, communication, and AI stack | Prepare router, monitoring, and management VM templates. Install base tools. Test Mac <-> university server communication. Choose the AI stack: Ollama, Qwen, DeepSeek, embeddings, FastAPI. | VM templates ready, communication validated, AI stack selected. |

Phase deliverables:

- GitHub repository initialized.
- Project tracker ready.
- Final architecture diagram.
- TAP allocation confirmed or request sent.
- VM templates ready.
- Mac <-> server communication tested.
- Final AI stack selected.

## Phase 1 - Complete OSPF TP Foundation

Dates: Wednesday, May 27, 2026 -> Sunday, June 7, 2026

Goal: build the complete OSPF network foundation by following the InetDoc lab and adapting it to this project.

| Date | Estimated workload | Goal | Actions | Deliverable |
| --- | ---: | --- | --- | --- |
| Wednesday, May 27, 2026 | 3h | Create `R1` | Create the `R1` VM on `tap62`. Attach transit and hosting VLANs. Verify console, SSH, hostname, and initial snapshot. | `R1` operational. |
| Thursday, May 28, 2026 | 3h | Create `R2` and `R3` | Create `R2` on `tap63` and `R3` on `tap64`, reusing the model validated with `R1`. Verify console, SSH, hostname, and initial snapshots. | `R2` and `R3` operational. |
| Friday, May 29, 2026 | 4h | TAP trunks and OVS | Adapt `switch.yaml` to the local TAPs. Configure VLAN trunks `440`, `441`, `442`, `10`, `20`, `30`, and `360`. Verify the OVS forwarding database. | VLAN trunks working. |
| Saturday, May 30, 2026 | 4h | IPv4/IPv6 VLAN interfaces | Configure VLAN subinterfaces with Netplan on `R1`, `R2`, and `R3`. Enable IPv4 forwarding and IPv6 forwarding. | VLAN interfaces and forwarding enabled. |
| Sunday, May 31, 2026 | 3h | Underlay validation | Test IPv4/IPv6 pings between `R1-R2`, `R1-R3`, and `R2-R3`. Check VLANs in OVS and fix addressing or trunking errors. | Validated IP underlay. |
| Monday, June 1, 2026 | 2h30 | FRR installation and daemons | Install `frr` and `frr-pythontools` on the three routers. Enable `zebra`, `ospfd`, `ospf6d`, and `staticd`. Verify systemd. | FRR running on all three routers. |
| Tuesday, June 2, 2026 | 2h | FRR interfaces and baseline | Verify that FRR sees the VLAN interfaces. Prepare router IDs. Save the pre-OSPF baseline and snapshots. | FRR baseline saved. |
| Wednesday, June 3, 2026 | 3h | OSPFv2 | Configure OSPFv2 on transit links with router IDs, `area 0`, and adjacency logs. | OSPFv2 configured. |
| Thursday, June 4, 2026 | 3h30 | OSPFv3 | Configure OSPFv3 for IPv6 on transit links. Verify IPv6 neighbors and LSDB. | OSPFv3 configured. |
| Friday, June 5, 2026 | 3h | Neighbor and route validation | Verify OSPFv2/OSPFv3 neighbors, LSAs, IPv4/IPv6 routing tables, and FRR restart behavior. | Stable OSPF routing. |
| Saturday, June 6, 2026 | 4h | Default route and hosting VLANs | Configure the default route on `R1`. Advertise the default route. Create and advertise hosting networks `10`, `20`, and `30` with passive OSPF interfaces. | Default route and hosting VLANs working. |
| Sunday, June 7, 2026 | 2h30 | Metrics and backups | Adjust OSPF metrics, interface bandwidths, and `auto-cost reference-bandwidth`. Back up `frr.conf`, Netplan, OVS, snapshots, and evidence. | OSPF foundation complete. |

Phase deliverables:

- Complete OSPF topology.
- IPv4 and IPv6 routing.
- Hosting VLANs.
- Default route advertised.
- Configurations backed up.
- Infrastructure ready for failure testing.

## Phase 2 - Failure Simulation & Network Testing

Dates: Monday, June 8, 2026 -> Friday, June 12, 2026

Goal: intentionally break the network to measure resilience.

| Date | Estimated workload | Goal | Actions | Deliverable |
| --- | ---: | --- | --- | --- |
| Monday, June 8, 2026 | 2h30 | Test plan and baseline | Define scenarios: `R1-R2`, `R2-R3`, and `R1-R3` link failures, FRR restart, router reboot, VLAN loss, and latency. Capture nominal state: routes, neighbors, latency, and throughput. | Test plan and network baseline. |
| Tuesday, June 9, 2026 | 4h | `R1-R2` and `R2-R3` failures | Cut and restore `R1-R2`, then `R2-R3`. Measure packet loss, convergence time, before/after routes, and container impact. | `R1-R2` and `R2-R3` scenario reports. |
| Wednesday, June 10, 2026 | 4h | `R1-R3` failure and restarts | Cut `R1-R3`. Verify alternate path and default route behavior. Restart FRR, then reboot one router VM. | `R1-R3` and restart report. |
| Thursday, June 11, 2026 | 3h | Latency, throughput, and jitter | Measure ping, simple jitter, `iperf3` if available, and throughput between hosting networks. Compare before and after failure. | Latency/throughput/convergence table. |
| Friday, June 12, 2026 | 2h30 | Resilience documentation | Consolidate measurements, captures, before/after routes, conclusions, and limitations. | Network resilience documentation. |

Phase deliverables:

- Failover scenarios.
- OSPF convergence metrics.
- Resilience documentation.
- Reproducible test evidence.

## Phase 3 - Observability Stack

Dates: Saturday, June 13, 2026 -> Monday, June 22, 2026

Goal: make the network observable with metrics, logs, and dashboards.

| Date | Estimated workload | Goal | Actions | Deliverable |
| --- | ---: | --- | --- | --- |
| Saturday, June 13, 2026 | 4h | Observability design and management VM | Define data to collect: CPU, RAM, disk, interfaces, bandwidth, OSPF neighbors, FRR logs, and system logs. Deploy/configure the `tap66` VM. | Observability plan and management VM ready. |
| Sunday, June 14, 2026 | 4h | Prometheus and exporters | Install Prometheus. Configure router/VM targets. Install `node_exporter` on VMs. | Prometheus scraping active. |
| Monday, June 15, 2026 | 3h30 | Router and interface metrics | Add CPU, RAM, disk, interface health, traffic, uptime, and FRR service monitoring. Add exporters or scripts if needed. | Router metrics visible. |
| Tuesday, June 16, 2026 | 4h | Loki and centralized logs | Install Loki and a log collection agent. Centralize system, FRR, and critical service logs. | Centralized logs. |
| Wednesday, June 17, 2026 | 3h | Grafana and data sources | Install Grafana. Connect Prometheus and Loki. Create dashboard folders: Network, System, Security, AI. | Grafana connected to data sources. |
| Thursday, June 18, 2026 | 4h | System and network dashboards | Create dashboards for CPU, RAM, disk, uptime, services, interfaces, bandwidth, OSPF neighbors, and route changes. | System and network dashboards. |
| Friday, June 19, 2026 | 3h | Alerting | Configure alerts: router down, lost OSPF neighbor, interface down, high CPU/RAM, disk almost full, critical FRR logs. | Network/system alerts. |
| Saturday, June 20, 2026 | 3h30 | Failure-based validation | Replay an OSPF failure and verify metrics, logs, alerts, and dashboards. Capture screenshots. | Observability validated. |
| Sunday, June 21, 2026 | 2h | Observability documentation | Document installation, dashboards, alerts, ports, credentials, backups, and procedures. | Complete observability documentation. |
| Monday, June 22, 2026 | 3h | Stabilization | Fix monitoring gaps, broken panels, missing targets, log retention, or noisy alerts. | Stabilized observability stack. |

Phase deliverables:

- Grafana dashboards.
- Metrics collection.
- Centralized logs.
- Network/system alerts.

## Phase 4 - Security Layer

Dates: Tuesday, June 23, 2026 -> Wednesday, July 1, 2026

Goal: turn the network lab into a cybersecurity lab with reproducible detection and incidents.

| Date | Estimated workload | Goal | Actions | Deliverable |
| --- | ---: | --- | --- | --- |
| Tuesday, June 23, 2026 | 4h | Security design and IDS VM | Choose Suricata, Zeek, or both depending on resources. Define capture interfaces, observed flows, and attacker/victim/server roles. Deploy/configure the `tap65` VM. | IDS plan and IDS VM ready. |
| Wednesday, June 24, 2026 | 4h | IDS installation | Install Suricata or Zeek. Test live capture, JSON logs, rotation, and performance. | IDS operational. |
| Thursday, June 25, 2026 | 3h30 | IDS log integration | Send IDS logs to Loki or centralized storage. Create an IDS alerts dashboard in Grafana. | IDS alerts visible. |
| Friday, June 26, 2026 | 3h | Attacker/victim containers | Prepare internal containers: attacker, victim, fake web/SSH/DNS server. Isolate roles by hosting VLAN. | Attack/victim environment ready. |
| Saturday, June 27, 2026 | 4h | Nmap and brute-force simulations | Run Nmap scans and controlled SSH/service attempts. Capture packets, alerts, and logs. | Nmap and brute-force incidents documented. |
| Sunday, June 28, 2026 | 4h | Suspicious traffic and lateral movement | Simulate abnormal traffic, unusual ports, repeated connections, suspicious DNS if applicable, and controlled lateral movement. | Suspicious traffic and lateral movement incidents. |
| Monday, June 29, 2026 | 3h | IDS tuning | Adjust rules, false positives, severities, enrichment, and dashboards. | IDS usable. |
| Tuesday, June 30, 2026 | 2h30 | Incident report | Consolidate incidents, alerts, PCAPs, Grafana screenshots, logs, and known limitations. | Security report draft. |
| Wednesday, July 1, 2026 | 3h | Security validation | Replay a scan and a brute-force attempt. Verify detection, logs, dashboard, and documentation. | Security layer validated. |

Phase deliverables:

- IDS deployed.
- Security alerts.
- Reproducible incidents.
- Documented attack simulations.

## Phase 5 - Local AI Infrastructure

Dates: Thursday, July 2, 2026 -> Wednesday, July 8, 2026

Goal: connect the MacBook Pro as the AI inference machine and expose a backend usable by the lab.

| Date | Estimated workload | Goal | Actions | Deliverable |
| --- | ---: | --- | --- | --- |
| Thursday, July 2, 2026 | 3h | Ollama and Qwen | Install/verify Ollama on the MacBook Pro. Test the local endpoint. Install and benchmark Qwen for diagnostics, summarization, and code. | Ollama working and Qwen benchmark. |
| Friday, July 3, 2026 | 3h | DeepSeek and model choice | Install and benchmark DeepSeek if compatible with resources. Compare with Qwen and choose models by use case. | DeepSeek benchmark and model choice. |
| Saturday, July 4, 2026 | 4h | Embeddings and Mac API | Install/verify the embedding model, for example `nomic-embed-text`. Expose the Ollama API cleanly to the server over a controlled network. | Embeddings and Mac endpoint working. |
| Sunday, July 5, 2026 | 4h | FastAPI backend | Create the FastAPI backend on the server or management VM. Add `health`, `chat`, `summarize`, and `explain-log` endpoints. | Initial FastAPI backend. |
| Monday, July 6, 2026 | 4h | AI and lab data connection | Connect FastAPI to Ollama on the Mac. Connect the backend to Loki logs, Prometheus metrics, or local exports. | Backend connected to AI and lab data. |
| Tuesday, July 7, 2026 | 3h | API hardening | Add environment variables, network control or a simple key, audit logs, timeouts, error handling, and fast-model fallback. | API secured for demo. |
| Wednesday, July 8, 2026 | 3h | AI infrastructure validation | Test the complete scenario: network alert -> backend -> model on Mac -> response. | AI infrastructure operational. |

Phase deliverables:

- Mac inference working.
- Qwen and DeepSeek benchmarks.
- Server <-> Mac communication.
- FastAPI backend operational.

## Phase 6 - AI Security Assistant

Dates: Thursday, July 9, 2026 -> Thursday, July 16, 2026

Goal: make the AI useful for diagnosing network problems and explaining incidents.

| Date | Estimated workload | Goal | Actions | Deliverable |
| --- | ---: | --- | --- | --- |
| Thursday, July 9, 2026 | 3h | Assistant design and routing prompts | Define use cases: OSPF failure, FRR logs, IDS alert, incident summary, troubleshooting. Create prompts for "Why did R2 lose adjacency?" using routes, neighbors, logs, and timestamps. | Assistant spec and routing prompts. |
| Friday, July 10, 2026 | 3h | Log and alert prompts | Create prompts for system logs, FRR, Suricata/Zeek, Grafana, lost OSPF neighbor, interface down, Nmap scan, brute force, and suspicious traffic. | Log and alert prompts. |
| Saturday, July 11, 2026 | 3h | Incident summaries | Generate automatic incident summaries with timeline, impact, probable cause, and recommended actions. | Incident summary feature. |
| Sunday, July 12, 2026 | 4h | Troubleshooting flow | Implement the diagnostic flow: data collection, interpretation, hypothesis, verification command, next action. | Troubleshooting flow. |
| Monday, July 13, 2026 | 3h | Response evaluation | Test the assistant on known incidents. Evaluate accuracy, hallucinations, clarity, and usefulness. | AI evaluation matrix. |
| Tuesday, July 14, 2026 | 2h30 | Guardrails | Add instructions to cite internal sources, flag missing data, and avoid unsupported conclusions. | More reliable responses. |
| Wednesday, July 15, 2026 | 3h30 | Assistant API | Expose FastAPI endpoints for `diagnostic`, `explain-alert`, `summarize-incident`, and `ask-network`. | Assistant API ready. |
| Thursday, July 16, 2026 | 3h | Assistant tests and documentation | Replay an OSPF failure and an IDS incident, ask the AI to explain them, and document prompts, limits, examples, and endpoints. | AI assistant validated and documented. |

Phase deliverables:

- AI troubleshooting assistant.
- Incident explanations.
- Network/security prompts.
- Assistant API usable by the demo interface.

## Phase 7 - RAG Knowledge Layer

Dates: Friday, July 17, 2026 -> Wednesday, July 22, 2026

Goal: give the AI project and technology documentation knowledge.

| Date | Estimated workload | Goal | Actions | Deliverable |
| --- | ---: | --- | --- | --- |
| Friday, July 17, 2026 | 4h | RAG design and ChromaDB | Choose RAG architecture: ChromaDB, embeddings, chunking, metadata, allowed sources, and citation format. Install ChromaDB and test insertion/search. | RAG design and ChromaDB operational. |
| Saturday, July 18, 2026 | 3h | OSPF/FRR/config corpus | Index OSPF docs, lab notes, useful FRRouting docs, FRR configs, Netplan, and OVS. | Network corpus indexed. |
| Sunday, July 19, 2026 | 3h | Security/RFC corpus | Index Suricata or Zeek docs, runbooks, incidents, alerts, PCAP notes, and useful RFC excerpts. | Security and reference corpus indexed. |
| Monday, July 20, 2026 | 4h | RAG + assistant integration | Connect retrieval to the FastAPI backend. Add internal source citations to responses. | RAG assistant working. |
| Tuesday, July 21, 2026 | 3h | RAG evaluation | Test OSPF, FRR, Suricata/Zeek, config, and incident-summary questions. Measure precision and source quality. | RAG evaluation. |
| Wednesday, July 22, 2026 | 2h30 | RAG documentation | Document ingestion, reindexing, sources, limitations, and example questions. | RAG documented. |

Phase deliverables:

- ChromaDB deployed.
- Documents indexed.
- RAG assistant.
- Retrieval with sources.

## Phase 8 - Frontend / Demo Interface

Dates: Thursday, July 23, 2026 -> Wednesday, July 29, 2026

Goal: make the project easy to understand quickly during a demo or for a recruiter.

| Date | Estimated workload | Goal | Actions | Deliverable |
| --- | ---: | --- | --- | --- |
| Thursday, July 23, 2026 | 4h | UI design and frontend setup | Choose React, Next.js, or Open WebUI integration. Define screens: topology, alerts, AI chat, timeline, metrics. Initialize frontend, layout, routing, API client, and restrained theme. | UI spec and initial frontend. |
| Friday, July 24, 2026 | 4h | Topology visualization | Display `R1`, `R2`, `R3`, VLANs, monitoring, management, Mac AI, and link/router status if possible. | Topology view. |
| Saturday, July 25, 2026 | 3h30 | Alerts dashboard | Display IDS alerts, network alerts, service status, and simple filters. | Alerts dashboard. |
| Sunday, July 26, 2026 | 4h | AI chat interface | Add AI chat connected to the backend. Support RAG questions, alert explanation, and OSPF diagnostics. | AI chat working. |
| Monday, July 27, 2026 | 3h30 | Incident timeline | Display an incident timeline: detection, logs, metrics, AI analysis, recommended actions. | Incident timeline. |
| Tuesday, July 28, 2026 | 4h | Integration and responsive testing | Test API calls, empty states, backend errors, responsive layout, navigation, and demo readability. | Interface tested. |
| Wednesday, July 29, 2026 | 3h | Demo polish | Fix visual details, text, screenshots, API errors, and prepare the demo script. | Clean demo interface. |

Phase deliverables:

- Demo UI.
- Topology visualization.
- Alerts dashboard.
- AI chat.
- Incident timeline.

## Phase 9 - Portfolio & Recruiter Packaging

Dates: Thursday, July 30, 2026 -> Monday, August 3, 2026

Goal: turn the technical work into a visible, clear, and valuable project.

| Date | Estimated workload | Goal | Actions | Deliverable |
| --- | ---: | --- | --- | --- |
| Thursday, July 30, 2026 | 3h | GitHub cleanup | Clean the repository, remove secrets, organize folders, verify licenses, add `.gitignore`, sample configs, and instructions. | Clean repository. |
| Friday, July 31, 2026 | 4h | README, diagrams, and screenshots | Write a clear README: problem, architecture, technologies, demo, screenshots, results, limitations, and learnings. Finalize diagrams and Grafana, IDS, UI, AI/RAG captures. | Final README and portfolio assets. |
| Saturday, August 1, 2026 | 4h | Demo video | Record a short demo: topology, OSPF failure, IDS alert, AI explanation, dashboard, and UI. | Demo video. |
| Sunday, August 2, 2026 | 3h | Portfolio page and CV bullets | Create/update the portfolio page with pitch, architecture, results, GitHub link, and video. Write impact-focused CV bullets. | Portfolio page and CV bullets. |
| Monday, August 3, 2026 | 3h | Final delivery | Final review, Git tag, demo checklist, config backups, link verification, and oral rehearsal. | Recruiter-ready project. |

Phase deliverables:

- Clean and readable GitHub repository.
- Final README.
- Demo video.
- Portfolio page.
- CV bullets.
- Project ready for recruiters.

## OSPF Validation Checklist

- `sudo ovs-appctl fdb/show dsw-host`
- `sudo ovs-appctl fdb/show dsw-host | grep 440`
- `sudo ovs-appctl fdb/show dsw-host | grep 441`
- `sudo ovs-appctl fdb/show dsw-host | grep 442`
- `ip -br addr`
- `ip route`
- `ip -6 route`
- `ping -c 3 <IPv4 neighbor>`
- `ping -6 -c 3 <IPv6 neighbor>`
- `sudo sysctl net.ipv4.ip_forward net.ipv6.conf.all.forwarding`
- `sudo systemctl status frr`
- `sudo vtysh -c "show ip ospf neighbor"`
- `sudo vtysh -c "show ipv6 ospf6 neighbor"`
- `sudo vtysh -c "show ip route ospf"`
- `sudo vtysh -c "show ipv6 route ospf6"`
- `sudo vtysh -c "show ip ospf database"`
- `sudo vtysh -c "show ipv6 ospf6 database"`
- `sudo vtysh -c "show running-config"`
- `sudo vtysh -c "copy running-config startup-config"`

## Observability Validation Checklist

- Prometheus scrapes all expected VMs.
- Grafana shows at least one system dashboard and one network dashboard.
- Loki receives system, FRR, and IDS logs.
- An OSPF failure produces a visible alert.
- Dashboard screenshots are saved.

## Security Validation Checklist

- The IDS sees container traffic.
- An Nmap scan generates an alert.
- A brute-force simulation generates usable logs.
- An incident contains: timestamp, source, destination, alert, logs, capture, and explanation.
- Main false positives are noted.

## AI/RAG Validation Checklist

- The server reaches the Ollama API exposed by the Mac.
- FastAPI responds to `health`, `chat`, `explain-alert`, and `summarize-incident`.
- The assistant explains an OSPF failure using logs and routes.
- ChromaDB returns relevant documents.
- RAG answers cite internal sources.
- Limitations and failure cases are documented.

## Recommended Folders

```text
configs/
  ovs/
  kvm/
  netplan/
  frr/
captures/
evidence/
reports/
runbooks/
frontend/
backend/
rag/
portfolio/
```

## Definition Of Done

The project is complete only if:

- The GitHub repository is clean, documented, and contains no secrets.
- The project tracker shows phases and progress.
- The three routers `R1`, `R2`, and `R3` run OSPFv2 and OSPFv3.
- Transit routes, the default route, and hosting networks are learned dynamically.
- Containers behind each router can communicate with each other.
- `R1-R2`, `R2-R3`, and `R1-R3` failure scenarios are measured and documented.
- OSPF metrics are applied consistently across the three routers.
- FRR, Netplan, OVS, and KVM configurations are saved in the repository.
- Prometheus, Grafana, and Loki collect metrics, dashboards, and logs.
- The IDS VM detects and archives Nmap, brute-force, suspicious traffic, and simulated lateral movement scenarios.
- The Mac provides local AI inference with Qwen/DeepSeek benchmarks.
- FastAPI connects the lab to AI models and observability/security data.
- The AI assistant explains network failures, logs, alerts, and incidents.
- ChromaDB provides RAG over OSPF, FRRouting, IDS, RFCs, configs, and runbooks.
- The demo interface shows topology, alerts, AI chat, and incident timeline.
- The README, screenshots, demo video, portfolio page, and CV bullets are finalized.
