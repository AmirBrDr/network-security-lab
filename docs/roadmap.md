# Project Roadmap

This roadmap tracks the AI Network Security Lab project.

The project starts with a complete OSPF lab, then builds observability, security monitoring, and a supporting local AI assistant around it. The final deadline is the end of August 2026.

## Project Scope

Primary goal:

Build a public, portfolio-ready network security lab that demonstrates routing, monitoring, detection, incident documentation, and AI-assisted troubleshooting.

Core principle:

The OSPF lab is the foundation. Observability, IDS, AI, RAG, and demo features are built only after the routing lab is stable and documented.

## Priority Levels

### Must Have

- [~] OSPFv2 and OSPFv3 routing lab using FRRouting.
- [x] Three-router OSPF triangle with `R1`, `R2`, and `R3`.
- [x] VLAN and TAP-based virtual topology.
- [~] IPv4 and IPv6 routing validation.
- [x] Default route advertisement from `R1`.
- [~] Hosting VLANs behind routers.
- [ ] Failure testing with measurable convergence results.
- [ ] Configuration backups and evidence collection.
- [ ] Clear documentation suitable for a public GitHub portfolio.

### Should Have

- [ ] Prometheus metrics collection.
- [ ] Grafana dashboards.
- [ ] Loki centralized logs.
- [ ] IDS VM on `tap65`.
- [ ] Suricata deployment and alert collection.
- [ ] Controlled attack simulations inside lab VMs only.
- [ ] Incident reports with logs, screenshots, packet captures, and conclusions.

### Nice To Have

- [ ] Local Ollama inference on the MacBook Pro.
- [ ] FastAPI backend connecting lab data to the local model.
- [ ] AI explanations for OSPF failures, IDS alerts, and logs.
- [ ] RAG over project documentation, configs, and selected references.

### Stretch

- [ ] Demo frontend with topology, alerts, AI chat, and incident timeline.
- [ ] Zeek integration after Suricata is stable.
- [ ] Additional client, DMZ, or expansion networks using reserved TAPs.
- [ ] Recruiter-focused demo video.

## Architecture Decisions

- Repository visibility: public GitHub repository for portfolio use.
- Tracker format: Markdown in the repository.
- Deadline: end of August 2026.
- OSPF source lab: complete the OSPF lab first, then adapt and extend around it.
- IDS recommendation: start with Suricata.
- Zeek status: future integration if resources and time allow.
- Demo fallback: Grafana plus documentation is acceptable if the frontend is not ready.
- AI role: supporting feature, not the main project.
- Attack simulation boundary: only inside lab VMs running in the type 2 hypervisor.

## Lab Resources

| Resource | Assignment | Status |
| --- | --- | --- |
| `tap62` | Router `R1` | Confirmed |
| `tap63` | Router `R2` | Confirmed |
| `tap64` | Router `R3` | Confirmed |
| `tap65` | Monitoring / IDS VM | Confirmed |
| `tap66` | Management / observability VM | Confirmed |
| `tap67` | Future integration | Reserved |
| `tap68` | Future integration | Reserved |
| `tap69` | Backup / debug / future integration | Reserved |
| MacBook Pro M3 Pro 18 GB | Ollama / local AI inference | Planned |
| University server | VMs and networking lab | Confirmed |

## Labels

Use these labels for GitHub issues, commits, roadmap tasks, or milestone notes.

### Phase Labels

- `phase-0-planning`
- `phase-1-ospf`
- `phase-2-failure-testing`
- `phase-3-observability`
- `phase-4-security`
- `phase-5-ai`
- `phase-6-rag`
- `phase-7-demo`
- `phase-8-portfolio`

### Type Labels

- `network`
- `security`
- `ai`
- `docs`
- `evidence`
- `config`
- `dashboard`
- `incident`
- `blocked`
- `question`
- `stretch`

## Status Legend

- `[ ]` Not started
- `[~]` In progress
- `[x]` Done
- `[!]` Blocked
- `[-]` Deferred

Markdown checkboxes do not support every status visually, so use the status marker at the start of a line when needed.

Example:

- `[~] Configure Prometheus targets.`
- `[!] Waiting for TAP access confirmation.`

## Milestones

### M0 - Planning and Scope

Goal: validate the scope, repository, tracker, architecture assumptions, TAP plan, and resource boundaries.

Labels: `phase-0-planning`, `docs`, `network`

- [x] Review `README.md`.
- [x] Review `docs/ospf-lab.txt`.
- [x] Review `docs/architecture.md`.
- [x] Review `docs/tap-plan.md`.
- [x] Review `docs/server-resources.md`.
- [x] Review `docs/project-calendar.md`.
- [x] Define the project as a portfolio project.
- [x] Confirm OSPF is the foundation of the project.
- [x] Confirm all deliverables are desired: infrastructure, documentation, screenshots, video, and portfolio packaging.
- [x] Choose Markdown as the primary tracker.
- [x] Confirm repository should be public.
- [x] Decide to track larger milestones instead of every small task.
- [x] Use both phase labels and type labels.
- [x] Confirm `tap62` through `tap66`.
- [x] Reserve `tap67` through `tap69` for future integrations.
- [x] Choose Suricata as the first IDS recommendation.
- [x] Define Grafana plus documentation as the fallback if the frontend is not finished.
- [x] Define AI as a supporting feature.
- [x] Confirm attack simulations stay inside lab VMs only.
- [x] Confirm no extra professor approval is needed.
- [x] Set final deadline to the end of August 2026.

Deliverable:

- [x] Validated scope.
- [x] GitHub repository verified.
- [x] Markdown roadmap created.

Exit criteria:

- [x] Project has a clear scope.
- [x] Project has a tracker.
- [x] The next milestone is ready to start.

### M1 - OSPF Foundation

Goal: build the complete FRRouting-based OSPF lab before adding security and AI features.

Labels: `phase-1-ospf`, `network`, `config`, `evidence`

Current status: TP completed through Q34. The OSPF transit triangle and default route advertisement are working. The hosting bridge/SVI step has been reached; Q35+ still covers passive OSPF publication of hosting VLANs, Incus, container tests, metrics, and final backups.

- [x] Create `R1` VM on `tap62`.
- [x] Create `R2` VM on `tap63`.
- [x] Create `R3` VM on `tap64`.
- [~] Configure hostnames, SSH, console access, and initial snapshots.
- [x] Configure TAP trunks and VLANs.
- [x] Configure VLAN `360` for infrastructure / default route.
- [x] Configure VLAN `440` for `R1` to `R2`.
- [x] Configure VLAN `441` for `R1` to `R3`.
- [x] Configure VLAN `442` for `R2` to `R3`.
- [x] Configure VLANs `10`, `20`, and `30` as hosting networks.
- [x] Configure IPv4 addressing.
- [x] Configure IPv6 addressing.
- [~] Enable IPv4 forwarding.
- [~] Enable IPv6 forwarding.
- [x] Install FRRouting on all routers.
- [x] Enable `zebra`, `ospfd`, `ospf6d`, and `staticd`.
- [x] Configure OSPFv2 in area `0`.
- [x] Configure OSPFv3 in area `0`.
- [x] Verify OSPF neighbors.
- [x] Verify IPv4 routes.
- [~] Verify IPv6 routes.
- [x] Configure default route on `R1`.
- [x] Advertise default route from `R1`.
- [ ] Configure passive interfaces for hosting VLANs.
- [ ] Tune OSPF metrics where needed.
- [~] Save router configurations.
- [~] Save Netplan configurations.
- [x] Save OVS or switch configurations.
- [~] Capture screenshots and command outputs as evidence.

Exit criteria:

- [~] `R1`, `R2`, and `R3` can route IPv4 traffic.
- [~] `R1`, `R2`, and `R3` can route IPv6 traffic.
- [x] OSPFv2 neighbors are stable.
- [~] OSPFv3 neighbors are stable.
- [x] Default route propagation works.
- [~] Configurations and evidence are saved.

### M2 - Failure Testing

Goal: prove that the network can recover from controlled failures and document the results.

Labels: `phase-2-failure-testing`, `network`, `evidence`, `incident`

- [ ] Define test scenarios.
- [ ] Capture baseline routes, neighbors, latency, and throughput.
- [ ] Test `R1` to `R2` link failure.
- [ ] Test `R1` to `R3` link failure.
- [ ] Test `R2` to `R3` link failure.
- [ ] Test FRR restart behavior.
- [ ] Test router reboot behavior.
- [ ] Measure convergence time.
- [ ] Measure packet loss.
- [ ] Compare before and after routing tables.
- [ ] Save packet captures if useful.
- [ ] Write failure testing report.

Exit criteria:

- [ ] Each failure scenario has evidence.
- [ ] Convergence behavior is documented.
- [ ] Limitations are documented honestly.

### M3 - Observability

Goal: collect metrics, logs, and alerts from the lab.

Labels: `phase-3-observability`, `network`, `dashboard`, `docs`

- [ ] Deploy management / observability VM on `tap66`.
- [ ] Install Prometheus.
- [ ] Install node exporters or equivalent collectors.
- [ ] Add router and VM scrape targets.
- [ ] Collect CPU, RAM, disk, and uptime metrics.
- [ ] Collect interface and bandwidth metrics.
- [ ] Monitor FRR service state.
- [ ] Install Loki or equivalent log storage.
- [ ] Collect system logs.
- [ ] Collect FRR logs.
- [ ] Install Grafana.
- [ ] Connect Prometheus data source.
- [ ] Connect Loki data source.
- [ ] Create network dashboard.
- [ ] Create system dashboard.
- [ ] Create OSPF dashboard or panels.
- [ ] Configure alerts for router down.
- [ ] Configure alerts for OSPF neighbor loss.
- [ ] Configure alerts for high CPU, RAM, and disk.
- [ ] Replay a network failure and confirm it appears in metrics and logs.
- [ ] Save dashboard screenshots.
- [ ] Document observability setup.

Exit criteria:

- [ ] Grafana shows useful live lab data.
- [ ] Logs are centralized.
- [ ] Important failures are visible.
- [ ] Setup is documented.

### M4 - Security / IDS

Goal: add controlled security monitoring with Suricata and document reproducible incidents.

Labels: `phase-4-security`, `security`, `incident`, `evidence`

- [ ] Deploy monitoring / IDS VM on `tap65`.
- [ ] Confirm which traffic the IDS VM can observe.
- [ ] Install Suricata.
- [ ] Configure live capture.
- [ ] Enable JSON logging.
- [ ] Send Suricata logs to Loki or local storage.
- [ ] Add IDS panels in Grafana.
- [ ] Create attacker VM or container inside the lab.
- [ ] Create victim VM or container inside the lab.
- [ ] Create test service targets such as web, SSH, or DNS.
- [ ] Run controlled Nmap scan inside the lab.
- [ ] Run controlled brute-force simulation inside the lab.
- [ ] Generate suspicious traffic inside the lab.
- [ ] Capture alerts, logs, screenshots, and packet evidence.
- [ ] Tune noisy rules if needed.
- [ ] Write incident reports.

Exit criteria:

- [ ] Suricata detects controlled lab activity.
- [ ] IDS alerts are visible in logs or dashboards.
- [ ] At least two security incidents are documented.
- [ ] No tests target systems outside the lab.

### M5 - AI Support Layer

Goal: add a local AI assistant that supports troubleshooting and incident explanation without becoming the main project risk.

Labels: `phase-5-ai`, `ai`, `security`, `network`

- [ ] Verify Ollama on the MacBook Pro.
- [ ] Test `qwen2.5:14b` for diagnostic explanations.
- [ ] Test `llama3.1:8b` as a fast fallback.
- [ ] Test `qwen2.5-coder:14b` for config and code help.
- [ ] Test `nomic-embed-text` for embeddings.
- [ ] Benchmark response quality and speed.
- [ ] Decide the default model for the assistant.
- [ ] Test Mac to server connectivity.
- [ ] Create FastAPI backend.
- [ ] Add health endpoint.
- [ ] Add log explanation endpoint.
- [ ] Add alert explanation endpoint.
- [ ] Add OSPF failure explanation endpoint.
- [ ] Add simple API protection.
- [ ] Add timeouts and fallback behavior.
- [ ] Test one full flow from lab event to AI explanation.

Exit criteria:

- [ ] AI can explain at least one OSPF failure.
- [ ] AI can explain at least one IDS alert.
- [ ] AI clearly says when evidence is missing.
- [ ] AI feature does not block the core lab.

### M6 - RAG Knowledge Layer

Goal: allow the assistant to answer questions using project docs, configs, and selected networking/security references.

Labels: `phase-6-rag`, `ai`, `docs`, `stretch`

- [ ] Choose vector database or local retrieval approach.
- [ ] Index project documentation.
- [ ] Index router configurations.
- [ ] Index selected OSPF and FRRouting references.
- [ ] Index selected Suricata references.
- [ ] Add source metadata.
- [ ] Connect retrieval to the FastAPI backend.
- [ ] Require answers to cite internal sources when possible.
- [ ] Test OSPF questions.
- [ ] Test IDS questions.
- [ ] Test configuration questions.
- [ ] Document RAG limitations.

Exit criteria:

- [ ] Assistant can retrieve relevant project context.
- [ ] Answers include sources or state when no source is available.
- [ ] RAG improves answers without hiding uncertainty.

### M7 - Demo Interface

Goal: create a simple demo surface if the core lab, observability, and security layers are stable.

Labels: `phase-7-demo`, `dashboard`, `ai`, `stretch`

- [ ] Decide whether a custom frontend is still worth the time.
- [ ] Define minimum screens.
- [ ] Show topology status.
- [ ] Show recent alerts.
- [ ] Show incident timeline.
- [ ] Add AI chat or explanation panel.
- [ ] Connect to FastAPI backend.
- [ ] Add screenshots for portfolio use.

Fallback:

- [ ] Use Grafana dashboards plus documentation if the custom frontend is not ready.

Exit criteria:

- [ ] Demo is understandable in less than five minutes.
- [ ] The first screen shows what the project is.
- [ ] The demo does not require fragile manual setup.

### M8 - Portfolio Packaging

Goal: make the project clear, credible, and easy to review publicly.

Labels: `phase-8-portfolio`, `docs`, `evidence`

- [ ] Rewrite `README.md` for portfolio readers.
- [ ] Add architecture explanation.
- [ ] Add topology diagram.
- [ ] Add setup overview.
- [ ] Add OSPF results.
- [ ] Add failure testing results.
- [ ] Add observability screenshots.
- [ ] Add IDS screenshots and incident summaries.
- [ ] Add AI assistant examples if ready.
- [ ] Add limitations and future work.
- [ ] Add final demo video if possible.
- [ ] Add recruiter-friendly project summary.
- [ ] Verify no secrets or unsafe details are committed.
- [ ] Verify repo is public and readable.

Exit criteria:

- [ ] A reviewer can understand the project from GitHub alone.
- [ ] Evidence is visible and organized.
- [ ] The project demonstrates networking, security, Linux, monitoring, and AI integration.

## Minimum Success Criteria

The project is successful even without the stretch features if it has:

- [ ] Stable OSPFv2 and OSPFv3 routing.
- [ ] Failure testing evidence.
- [ ] Grafana dashboards.
- [ ] Centralized logs.
- [ ] Suricata alerts from controlled lab attacks.
- [ ] Clear incident reports.
- [ ] Public documentation with screenshots and configs.

## Portfolio Story

Suggested one-sentence summary:

I built a virtual OSPF routing lab and extended it into a network security observability platform with monitoring, IDS alerts, incident evidence, and local AI-assisted troubleshooting.

Suggested resume bullet:

- Built a virtual OSPFv2/OSPFv3 network security lab with FRRouting, VLAN/TAP topology, Prometheus, Grafana, Loki, Suricata, and local Ollama-based troubleshooting support.

## References

- [Project calendar](project-calendar.md)
- [OSPF lab reference](ospf-lab.txt)
- [Architecture](architecture.md)
- [TAP plan](tap-plan.md)
- [Server resources](server-resources.md)
- [AI stack](ai-stack.md)
