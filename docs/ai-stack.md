* Default model: qwen2.5-coder:7b-instruct
* Fast fallback (optional): llama3.2:3b
* Embedding model: nomic-embed-text

## Notes

- A single model handles diagnostic explanation, log/alert parsing, and
  config help. There is no separate "code mode" model.
- Rationale: every planned use case (explain an OSPF failure, explain a
  Suricata alert, explain a log line, answer RAG questions grounded in
  configs) is the same task — parse structured/technical text and explain it
  in plain language. Coder-family instruct models are trained heavily on
  code, YAML, JSON, and log-shaped text, which fits this job better than a
  general chat model of the same size.
- Sizing constraint: the target hardware is a MacBook Pro M3 Pro with 18 GB
  unified memory (see `roadmap.md` Lab Resources). At Q4 quantization,
  `qwen2.5-coder:7b-instruct` is roughly 4.5 GB resident, leaving headroom
  for macOS, the FastAPI backend, and other tools running at the same time.
  A 14B model (~10-11 GB+ resident) fits alone but not alongside a second
  model, and running two 14B models in rotation causes a 10-30s reload every
  time the assistant switches "modes."
- `llama3.2:3b` is an optional lightweight tier for trivial queries (health
  checks, simple status questions) if routing everything through the 7B
  model proves slower than desired. Not required for the exit criteria.
- Before relying on these numbers, verify empirically on the actual machine:
  load the model, run `ollama ps` to see reported memory, and time a cold
  start.