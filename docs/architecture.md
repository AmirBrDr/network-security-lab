# Architecture

## Virtual Machines

| VM | Role | RAM | TAP Interface |
| --- | --- | --- | --- |
| VM 1 | Router R1 | 4 GB | tap62 |
| VM 2 | Router R2 | 4 GB | tap63 |
| VM 3 | Router R3 | 4 GB | tap64 |
| VM 4 | Monitoring / Security | 12 GB | tap65 |
| VM 5 | Management / Observability | 12 GB | tap66 |

## Host

| System | Role |
| --- | --- |
| MacBook M3 Pro 18 GB | Ollama / local LLM inference |

## Topology

![Network security lab topology](images/topology.svg)
