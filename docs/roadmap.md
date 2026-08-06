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

- [x] OSPFv2 and OSPFv3 routing lab using FRRouting.
- [x] Three-router OSPF triangle with `R1`, `R2`, and `R3`.
- [x] VLAN and TAP-based virtual topology.
- [x] IPv4 and IPv6 routing validation.
- [x] Default route advertisement from `R1`.
- [x] Hosting VLANs behind routers.
- [~] Failure testing with measurable convergence results.
- [x] Configuration backups and evidence collection.
- [~] Clear documentation suitable for a public GitHub portfolio.

### Should Have

- [x] Prometheus metrics collection.
- [x] Grafana dashboards.
- [x] Loki centralized logs.
- [x] IDS VM on `tap65`.
- [x] Suricata deployment and alert collection.
- [x] Controlled attack simulations inside lab VMs only.
- [x] Incident reports with logs, screenshots, packet captures, and conclusions.

### Nice To Have

- [x] Local Ollama inference on the MacBook Pro.
- [x] FastAPI backend connecting lab data to the local model.
- [x] AI explanations for OSPF failures, IDS alerts, and logs.
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
| MacBook Pro M3 Pro 18 GB | Ollama / local AI inference | Confirmed |
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

Current status: complete. The OSPFv2/OSPFv3 transit triangle, default route advertisement, passive hosting VLAN publication, Incus container hosting networks, IPv4/IPv6 route validation, and final FRR evidence are documented.

- [x] Create `R1` VM on `tap62`.
- [x] Create `R2` VM on `tap63`.
- [x] Create `R3` VM on `tap64`.
- [x] Configure hostnames, SSH, console access, and initial snapshots.
- [x] Configure TAP trunks and VLANs.
- [x] Configure VLAN `360` for infrastructure / default route.
- [x] Configure VLAN `440` for `R1` to `R2`.
- [x] Configure VLAN `441` for `R1` to `R3`.
- [x] Configure VLAN `442` for `R2` to `R3`.
- [x] Configure VLANs `10`, `20`, and `30` as hosting networks.
- [x] Configure IPv4 addressing.
- [x] Configure IPv6 addressing.
- [x] Enable IPv4 forwarding.
- [x] Enable IPv6 forwarding.
- [x] Install FRRouting on all routers.
- [x] Enable `zebra`, `ospfd`, `ospf6d`, and `staticd`.
- [x] Configure OSPFv2 in area `0`.
- [x] Configure OSPFv3 in area `0`.
- [x] Verify OSPF neighbors.
- [x] Verify IPv4 routes.
- [x] Verify IPv6 routes.
- [x] Configure default route on `R1`.
- [x] Advertise default route from `R1`.
- [x] Configure passive interfaces for hosting VLANs.
- [x] Tune OSPF metrics where needed.
- [x] Save router configurations.
- [x] Save Netplan configurations.
- [x] Save OVS or switch configurations.
- [x] Capture screenshots and command outputs as evidence.

Exit criteria:

- [x] `R1`, `R2`, and `R3` can route IPv4 traffic.
- [x] `R1`, `R2`, and `R3` can route IPv6 traffic.
- [x] OSPFv2 neighbors are stable.
- [x] OSPFv3 neighbors are stable.
- [x] Default route propagation works.
- [x] Configurations and evidence are saved.

### M2 - Failure Testing

Goal: prove that the network can recover from controlled failures and document the results.

Labels: `phase-2-failure-testing`, `network`, `evidence`, `incident`

Current status: in progress. The Phase 2 tutorial is written, and the current
proof report in `docs/proofs-phase2.md` documents the baseline, `R1` to `R2`
failure, OVS VLAN `440` loss, FRR restart, router reboot, latency, jitter, and
throughput. The remaining evidence gaps are the direct `R1` to `R3` and
`R2` to `R3` link-failure captures.

- [x] Define test scenarios.
- [x] Capture baseline routes, neighbors, latency, and throughput.
- [x] Test `R1` to `R2` link failure.
- [x] Test OVS VLAN `440` loss on `tap62`.
- [x] Test FRR restart behavior.
- [x] Test router reboot behavior.
- [~] Measure convergence time for captured scenarios.
- [~] Measure packet loss for captured scenarios.
- [x] Compare before and after routing tables for captured scenarios.
- [-] Save packet captures if useful.
- [~] Write failure testing report.

Exit criteria:

- [~] Each captured failure scenario has evidence.
- [~] Convergence behavior is documented.
- [x] Limitations are documented honestly.

### M3 - Observability

Goal: collect metrics, logs, and alerts from the lab.

Labels: `phase-3-observability`, `network`, `dashboard`, `docs`

Current status: complete. Prometheus, Loki, Alloy, Grafana data sources,
Grafana dashboards, FRR textfile metrics, and Prometheus alert rules are
documented in `docs/proofs-phase3.md`.

- [x] Deploy management / observability VM on `tap66`.
- [x] Install Prometheus.
- [x] Install node exporters or equivalent collectors.
- [x] Add router and VM scrape targets.
- [x] Collect CPU, RAM, disk, and uptime metrics.
- [x] Collect interface and bandwidth metrics.
- [x] Monitor FRR service state.
- [x] Install Loki or equivalent log storage.
- [x] Collect system logs.
- [x] Collect FRR logs.
- [x] Install Grafana.
- [x] Connect Prometheus data source.
- [x] Connect Loki data source.
- [x] Create network dashboard.
- [x] Create system dashboard.
- [x] Create OSPF dashboard or panels.
- [x] Configure alerts for router down.
- [x] Configure alerts for OSPF neighbor loss.
- [x] Configure alerts for high CPU, RAM, and disk.
- [x] Replay a network failure and confirm it appears in metrics and logs.
- [x] Save dashboard screenshots.
- [x] Document observability setup.

Exit criteria:

- [x] Grafana shows useful live lab data.
- [x] Logs are centralized.
- [x] Important failures are visible.
- [x] Setup is documented.

### M4 - Security / IDS

Goal: add controlled security monitoring with Suricata and document reproducible incidents.

Labels: `phase-4-security`, `security`, `incident`, `evidence`

Current status: complete. Suricata, the OVS mirror, Alloy-to-Loki forwarding,
Prometheus metrics and alert rules, the Grafana Security dashboard, and four
documented incidents are captured in `docs/evidence/proofs-phase4.md`.

- [x] Deploy monitoring / IDS VM on `tap65`.
- [x] Confirm which traffic the IDS VM can observe.
- [x] Install Suricata.
- [x] Configure live capture.
- [x] Enable JSON logging.
- [x] Send Suricata logs to Loki or local storage.
- [x] Add IDS panels in Grafana.
- [x] Create attacker VM or container inside the lab.
- [x] Create victim VM or container inside the lab.
- [x] Create test service targets such as web, SSH, or DNS.
- [x] Run controlled Nmap scan inside the lab.
- [x] Run controlled brute-force simulation inside the lab.
- [x] Generate suspicious traffic inside the lab.
- [x] Capture alerts, logs, screenshots, and packet evidence.
- [x] Tune noisy rules if needed.
- [x] Write incident reports.

Exit criteria:

- [x] Suricata detects controlled lab activity.
- [x] IDS alerts are visible in logs or dashboards.
- [x] At least two security incidents are documented.
- [x] No tests target systems outside the lab.

### M5 - AI Support Layer

Goal: add a local AI assistant that supports troubleshooting and incident explanation without becoming the main project risk.

Labels: `phase-5-ai`, `ai`, `security`, `network`

Current status: complete. Ollama, the reverse SSH tunnel, the FastAPI
backend, its systemd service, and one full OSPF and one full IDS explanation
flow are documented in `docs/evidence/proofs-phase5.md`.

- [x] Verify Ollama on the MacBook Pro.
- [x] Test `qwen2.5-coder:7b-instruct` as the single default model for diagnostic explanations, alert/log parsing, and config help.
- [x] Test `llama3.2:3b` as an optional fast fallback for trivial queries.
- [x] Test `nomic-embed-text` for embeddings.
- [x] Benchmark response quality, speed, and resident memory (`ollama ps`) on the 18 GB MacBook Pro.
- [x] Confirm the single-model approach holds, or fall back to a second model only if benchmarks require it.
- [x] Test Mac to server connectivity.
- [x] Create FastAPI backend.
- [x] Add health endpoint.
- [x] Add log explanation endpoint.
- [x] Add alert explanation endpoint.
- [x] Add OSPF failure explanation endpoint.
- [x] Add simple API protection.
- [x] Add timeouts and fallback behavior.
- [x] Test one full flow from lab event to AI explanation.

Exit criteria:

- [x] AI can explain at least one OSPF failure.
- [x] AI can explain at least one IDS alert.
- [x] AI clearly says when evidence is missing.
- [x] AI feature does not block the core lab.

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

- [x] Stable OSPFv2 and OSPFv3 routing.
- [~] Failure testing evidence.
- [x] Grafana dashboards.
- [x] Centralized logs.
- [x] Suricata alerts from controlled lab attacks.
- [x] Clear incident reports.
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
