# Architecture

## Virtual Machines

| VM | Role | RAM | TAP Interface |
| --- | --- | --- | --- |
| VM 1 | Router R1 | 4096 MB | tap62 |
| VM 2 | Router R2 | 4096 MB | tap63 |
| VM 3 | Router R3 | 4096 MB | tap64 |
| VM 4 | Monitoring / Security | 12288 MB | tap65 |
| VM 5 | Management / Observability | 12288 MB | tap66 |

## Host

| System | Role |
| --- | --- |
| MacBook M3 Pro 18432 MB | Ollama / local LLM inference |

## Topology

![Network security lab topology](images/topology.svg)
