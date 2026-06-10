# Phase 8 - Frontend Demo Interface

Network Security Lab

## Summary

This practical lab builds the demo interface for the Network Security Lab. The
previous phases created the routing foundation, observability layer, IDS layer,
local AI backend, assistant endpoints, and RAG knowledge layer. Phase 8 turns
that work into a clear interface that can be understood quickly during a demo.

The interface is not a marketing landing page. The first screen is an
operational demo surface:

- Topology status for `R1`, `R2`, `R3`, Monitoring, Management, and Mac AI.
- Network and security alerts.
- AI chat connected to `/rag/ask`, `/diagnostic`, and `/explain-alert`.
- Incident timeline.
- Small metrics and health panels.

The recommended stack is Vite, React, TypeScript, TanStack Query, Recharts, and
Lucide icons. The frontend calls the existing FastAPI backend through a local
Vite proxy so the browser does not need to know the backend token during
development.

At the end of this lab, the demo should make the project understandable in
less than five minutes without requiring the evaluator to read every document
first.

## Table Of Contents

1. Objectives
2. Demo Topology
3. Phase 8 Scope
4. Demo Design Rules
5. Frontend Stack Choice
6. Backend Readiness
7. Define The Demo Screens
8. Create The React Project
9. Configure Environment And Proxy
10. Add Frontend Types
11. Build The API Client
12. Add Query Provider And Routing
13. Create The App Layout
14. Add Visual Style
15. Build The Topology View
16. Add Health And Metric Panels
17. Build The Alerts View
18. Build The AI Assistant View
19. Build The Incident Timeline
20. Add Optional Demo Backend Endpoints
21. Run The Interface Manually
22. Validate End To End API Calls
23. Responsive And Visual Testing
24. Demo Script
25. Save Evidence
26. Troubleshooting
27. Conclusion
28. References

## 1. Objectives

After completing this practical lab, you should be able to:

1. Choose a frontend architecture suitable for a local infrastructure demo.
2. Create a Vite React TypeScript application.
3. Configure a local proxy to the FastAPI backend.
4. Build a readable first screen for topology, health, alerts, AI, and timeline.
5. Call the Phase 6 and Phase 7 backend endpoints from the browser.
6. Display loading, empty, error, and degraded states.
7. Keep the demo inside the lab safety boundary.
8. Test the interface at desktop and mobile widths.
9. Capture screenshots for the final portfolio phase.
10. Prepare a short demo script that does not depend on fragile manual steps.

## 2. Demo Topology

Phase 8 starts after the RAG layer:

- The Management VM runs FastAPI, Prometheus, Loki, Grafana, and ChromaDB.
- The MacBook Pro runs Ollama.
- The frontend runs locally during development, usually on the Management VM
  or the Mac.
- The browser talks to the frontend dev server.
- The frontend dev server proxies API calls to FastAPI.

```text
Browser
  |
  v
Vite dev server :5173
  |
  | /api/* proxy
  v
FastAPI backend :8080 ---- Prometheus :9090
       |                 ---- Loki :3100
       |                 ---- ChromaDB data/chroma
       v
MacBook Pro Ollama :11434

Lab network:
R1 tap62, R2 tap63, R3 tap64, Monitoring tap65, Management tap66
```

Recommended development placement:

| Component | Host | Purpose |
| --- | --- | --- |
| Frontend dev server | Management VM or Mac | Demo UI |
| FastAPI backend | Management VM | API bridge |
| Ollama | MacBook Pro | Chat and embeddings |
| Prometheus | Management VM | Metrics |
| Loki | Management VM | Logs |
| Grafana | Management VM | Manual validation |

## 3. Phase 8 Scope

Q1. What belongs in Phase 8?

Phase 8 includes:

- Frontend setup.
- API client.
- Topology visualization.
- Alerts dashboard.
- AI chat panel.
- Incident timeline.
- Responsive testing.
- Screenshot and demo proof capture.

Q2. What is explicitly deferred to Phase 9?

Phase 9 handles:

- Final GitHub cleanup.
- Final README polish.
- Demo video recording.
- Portfolio page.
- CV bullets.
- Final public packaging.

Phase 8 should create the interface and proof assets. Phase 9 turns them into
recruiter-facing material.

Q3. What is the minimum success criterion?

The demo interface is successful when:

- The first screen explains the project visually.
- A viewer can see topology, alert status, AI assistant, and timeline without
  navigating through many pages.
- At least one backend call works through the UI.
- Empty and error states are understandable.
- Desktop and mobile screenshots are captured.

## 4. Demo Design Rules

Q4. What should the interface feel like?

It should feel like a small network operations console:

- Dense but readable.
- Calm and technical.
- Focused on evidence.
- Clear about degraded or missing data.
- Useful for repeated demonstrations.

Avoid an oversized hero section. The project title can appear in the header,
but the first viewport must show the actual lab state.

Q5. What should be visible in the first viewport?

At desktop width, show:

- Topology panel.
- Health summary.
- Recent alerts.
- Assistant prompt box.
- Incident timeline preview.

At mobile width, show:

- Health summary.
- Topology.
- Alerts.
- Assistant.
- Timeline.

Use vertical stacking on mobile. Do not hide the core demo behind a marketing
page.

Q6. Which states must be designed?

Every API-powered panel needs:

| State | Required behavior |
| --- | --- |
| Loading | Show a small loading indicator or skeleton |
| Empty | Explain that no data was returned |
| Error | Show which backend call failed |
| Degraded | Show partial data and missing source |
| Healthy | Show the current value and source |

Q7. Which visual conventions are recommended?

Use:

- Green for healthy.
- Amber for warning.
- Red for critical.
- Blue or teal for informational AI/RAG status.
- Neutral backgrounds with strong text contrast.
- Icons for actions and status where they improve scanning.

Do not use a one-color theme. The interface should not be dominated by a single
purple, beige, brown, or dark blue palette.

## 5. Frontend Stack Choice

Q8. Which frontend stack is recommended?

Use:

| Purpose | Tool |
| --- | --- |
| Build tool | Vite |
| UI runtime | React |
| Language | TypeScript |
| Server state | TanStack Query |
| Routing | React Router |
| Icons | Lucide React |
| Small charts | Recharts |
| Browser tests | Playwright |

Q9. Why choose Vite React instead of Next.js?

Vite React is enough for this lab because:

- The demo is a local single-page app.
- The backend already exists in FastAPI.
- The UI does not need server-side rendering.
- Setup is smaller and easier to explain.
- The app can be served later as static files behind a reverse proxy.

Next.js remains valid if you later want server-side auth, file-based routing,
or a public deployment, but it is more than Phase 8 needs.

Q10. Why not use Open WebUI as the only demo?

Open WebUI is useful for generic model chat, but the project needs a demo
surface that shows the actual lab:

- Topology.
- Alerts.
- Incident timeline.
- Grafana-style metrics.
- Calls to custom FastAPI endpoints.

Open WebUI can be a fallback, not the primary Phase 8 interface.

## 6. Backend Readiness

Q11. Which backend endpoints should exist before frontend work?

From the Phase 5, 6, and 7 tutorials:

| Endpoint | Purpose |
| --- | --- |
| `GET /health` | Backend and dependency health |
| `POST /diagnostic` | OSPF, IDS, and generic diagnostics |
| `POST /explain-alert` | Alert explanation |
| `POST /summarize-incident` | Incident summary |
| `POST /ask-network` | General assistant question |
| `GET /rag/sources` | RAG index summary |
| `POST /rag/search` | Retrieval search |
| `POST /rag/ask` | Cited RAG answer |

Q12. How do we check backend routes?

On the Management VM:

```console
cd /path/to/network-security-lab/backend/phase5-ai
curl -s http://127.0.0.1:8080/health | jq
curl -s http://127.0.0.1:8080/openapi.json | jq '.paths | keys'
```

Expected result:

- `/health` returns JSON.
- The route list includes the Phase 6 and Phase 7 endpoints.

Q13. How do we export the API token for terminal tests?

```console
cd /path/to/network-security-lab/backend/phase5-ai
export API_TOKEN="$(grep '^API_TOKEN=' .env | cut -d= -f2-)"
```

Q14. What security warning matters for the frontend?

A browser-based frontend cannot hide a token if the token is shipped inside the
JavaScript bundle. For Phase 8 development, use a Vite dev proxy that injects
the backend bearer token from the dev server environment.

For a public deployment, add real backend-side session authentication or serve
the UI behind a trusted reverse proxy. Do not publish a static build with a
real bearer token embedded in client-side environment variables.

## 7. Define The Demo Screens

Q15. Which screens are required?

Use these screens:

| Screen | Route | Purpose |
| --- | --- | --- |
| Overview | `/` | First demo surface |
| Topology | `/topology` | Detailed lab topology |
| Alerts | `/alerts` | Network and IDS alert queue |
| Assistant | `/assistant` | AI/RAG chat and diagnostics |
| Incidents | `/incidents` | Timeline and summary |

Q16. What should the overview screen contain?

The overview screen should contain:

- Topology map.
- Health strip.
- Recent alerts list.
- Assistant prompt.
- Timeline preview.
- Last refresh time.

Q17. What should the topology screen contain?

The topology screen should show:

- `R1`, `R2`, `R3`.
- Transit VLANs `440`, `441`, `442`.
- Monitoring VM.
- Management VM.
- Mac AI endpoint.
- Health status for each node if available.
- Link state if metrics exist.

Q18. What should the alerts screen contain?

The alerts screen should show:

- Prometheus alert name.
- Severity.
- Source node or job.
- Status.
- Last update.
- A button to send the alert to `/explain-alert`.

Q19. What should the assistant screen contain?

The assistant screen should support:

- RAG question.
- OSPF diagnostic question.
- Alert explanation.
- Incident summary draft.
- Displayed citations.
- Missing evidence.
- Suggested verification commands.

Q20. What should the incidents screen contain?

The incident screen should show:

- Detection time.
- Alert source.
- Evidence collected.
- AI analysis.
- Response actions.
- Open gaps.
- Screenshot checklist.

## 8. Create The React Project

Q21. Where should the frontend live?

Create:

```text
frontend/demo-ui/
```

Q22. How do we create the Vite React TypeScript app?

From the repository root:

```console
cd /path/to/network-security-lab
npm create vite@latest frontend/demo-ui -- --template react-ts
cd frontend/demo-ui
npm install
```

Q23. Which dependencies are added?

```console
npm install react-router-dom @tanstack/react-query lucide-react recharts clsx
npm install -D @playwright/test
```

Q24. Which scripts should exist in `package.json`?

Check:

```console
npm pkg get scripts
```

Expected scripts:

```json
{
  "dev": "vite",
  "build": "tsc -b && vite build",
  "lint": "eslint .",
  "preview": "vite preview"
}
```

Add a Playwright script:

```console
npm pkg set scripts.test:e2e="playwright test"
```

Q25. Which folder structure is recommended?

Create:

```text
frontend/demo-ui/src/
  api/
  components/
  data/
  pages/
  styles/
  test/
```

Command:

```console
mkdir -p src/api src/components src/data src/pages src/styles src/test
```

## 9. Configure Environment And Proxy

Q26. Which frontend environment file is safe to commit?

Create `frontend/demo-ui/.env.example`:

```dotenv
API_TARGET=http://127.0.0.1:8080
API_TOKEN=replace-with-local-demo-token
```

Do not commit `.env.local`.

Q27. How do we create local frontend environment values?

```console
cd /path/to/network-security-lab/frontend/demo-ui
cp .env.example .env.local
```

Edit `.env.local`:

```dotenv
API_TARGET=http://127.0.0.1:8080
API_TOKEN=<backend-api-token>
```

Q28. How do we configure the Vite proxy?

Edit `frontend/demo-ui/vite.config.ts`:

```ts
import { defineConfig, loadEnv } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), '')
  const apiTarget = env.API_TARGET || 'http://127.0.0.1:8080'
  const apiToken = env.API_TOKEN || ''
  const proxyHeaders = apiToken ? { Authorization: `Bearer ${apiToken}` } : {}

  return {
    plugins: [react()],
    server: {
      host: '127.0.0.1',
      port: 5173,
      proxy: {
        '/api': {
          target: apiTarget,
          changeOrigin: true,
          rewrite: (path) => path.replace(/^\/api/, ''),
          headers: proxyHeaders,
        },
      },
    },
  }
})
```

Q29. Why use `/api` in the frontend?

The frontend can call:

```text
/api/health
/api/rag/ask
/api/diagnostic
```

The Vite dev server forwards those calls to FastAPI:

```text
http://127.0.0.1:8080/health
http://127.0.0.1:8080/rag/ask
http://127.0.0.1:8080/diagnostic
```

This keeps local development simple and avoids browser CORS work during the
demo.

Q30. What if the frontend is served without Vite later?

Use a reverse proxy such as Nginx or Caddy in front of FastAPI and the static
files. Do not put a real backend token into a public JavaScript bundle.

## 10. Add Frontend Types

Q31. Which API types are needed first?

Create `src/api/types.ts`:

```ts
export type HealthStatus = {
  app?: string
  ollama?: { ok?: boolean; status_code?: number; error?: string }
  prometheus?: { ok?: boolean; status_code?: number; error?: string }
  loki?: { ok?: boolean; status_code?: number; error?: string }
}

export type Severity = 'info' | 'warning' | 'critical'

export type LabNode = {
  id: string
  label: string
  role: string
  tap?: string
  ip?: string
  status: 'healthy' | 'warning' | 'critical' | 'unknown'
}

export type LabLink = {
  id: string
  source: string
  target: string
  label: string
  status: 'healthy' | 'warning' | 'critical' | 'unknown'
}

export type AlertItem = {
  id: string
  name: string
  severity: Severity
  source: string
  summary: string
  status: 'firing' | 'resolved' | 'unknown'
  startsAt?: string
}

export type RagSource = {
  id: string
  source_path: string
  source_type: string
  title?: string
  line_start?: number
  relevance?: number
  text: string
}

export type RagAnswer = {
  answer: string
  citations: string[]
  missing_sources: string[]
  verification_commands: string[]
  confidence: 'low' | 'medium' | 'high'
}

export type RagAskResponse = {
  model: string
  question: string
  retrieved_sources: RagSource[]
  answer: RagAnswer
}

export type IncidentEvent = {
  id: string
  time: string
  title: string
  detail: string
  status: 'observed' | 'investigating' | 'contained' | 'resolved'
}
```

Q32. Why keep frontend types small?

The frontend should display the demo clearly. It does not need to mirror every
backend field. Keep only the fields required by the UI, then add more when a
screen actually needs them.

## 11. Build The API Client

Q33. What should the API client handle?

It should:

- Prefix calls with `/api`.
- Parse JSON.
- Throw readable errors.
- Support `GET` and `POST`.
- Avoid duplicating fetch logic in components.

Q34. How do we create `src/api/client.ts`?

Create:

```ts
import type { HealthStatus, RagAskResponse } from './types'

const API_PREFIX = '/api'

async function requestJson<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_PREFIX}${path}`, {
    ...init,
    headers: {
      'Content-Type': 'application/json',
      ...((init?.headers ?? {}) as Record<string, string>),
    },
  })

  if (!response.ok) {
    const body = await response.text()
    throw new Error(`${response.status} ${response.statusText}: ${body}`)
  }

  return response.json() as Promise<T>
}

export function getHealth() {
  return requestJson<HealthStatus>('/health')
}

export function askRag(question: string) {
  return requestJson<RagAskResponse>('/rag/ask', {
    method: 'POST',
    body: JSON.stringify({ question, top_k: 6 }),
  })
}

export function askDiagnostic(question: string, node = 'R2') {
  return requestJson('/diagnostic', {
    method: 'POST',
    body: JSON.stringify({
      kind: 'ospf',
      question,
      node,
      protocol: 'ospfv2',
      lookback_minutes: 30,
    }),
  })
}

export function explainAlert(alertName: string, summary: string) {
  return requestJson('/explain-alert', {
    method: 'POST',
    body: JSON.stringify({
      alert_name: alertName,
      labels: { phase: 'phase-8-demo' },
      annotations: { summary },
      lookback_minutes: 30,
    }),
  })
}
```

Q35. How do we add a small mock fallback?

Create `src/data/demoData.ts`:

```ts
import type { AlertItem, IncidentEvent, LabLink, LabNode } from '../api/types'

export const labNodes: LabNode[] = [
  { id: 'R1', label: 'R1', role: 'Default route origin', tap: 'tap62', ip: '10.99.0.1', status: 'healthy' },
  { id: 'R2', label: 'R2', role: 'Router', tap: 'tap63', ip: '10.99.0.2', status: 'healthy' },
  { id: 'R3', label: 'R3', role: 'Router', tap: 'tap64', ip: '10.99.0.3', status: 'healthy' },
  { id: 'monitoring', label: 'Monitoring', role: 'IDS sensor', tap: 'tap65', ip: '10.99.0.65', status: 'warning' },
  { id: 'management', label: 'Management', role: 'Observability', tap: 'tap66', ip: '10.99.0.66', status: 'healthy' },
  { id: 'mac-ai', label: 'Mac AI', role: 'Ollama inference', status: 'healthy' },
]

export const labLinks: LabLink[] = [
  { id: 'vlan440', source: 'R1', target: 'R2', label: 'VLAN 440', status: 'healthy' },
  { id: 'vlan441', source: 'R1', target: 'R3', label: 'VLAN 441', status: 'healthy' },
  { id: 'vlan442', source: 'R2', target: 'R3', label: 'VLAN 442', status: 'healthy' },
  { id: 'mgmt', source: 'management', target: 'mac-ai', label: 'Ollama API', status: 'healthy' },
]

export const demoAlerts: AlertItem[] = [
  {
    id: 'ospf-r2',
    name: 'OSPFNeighborLoss',
    severity: 'warning',
    source: 'R2',
    summary: 'R2 has fewer than two Full OSPFv2 neighbors.',
    status: 'resolved',
    startsAt: 'Phase 3 replay',
  },
  {
    id: 'suricata-scan',
    name: 'LOCAL Phase4 TCP SYN scan candidate',
    severity: 'info',
    source: 'monitoring',
    summary: 'Controlled Nmap scan detected inside the lab.',
    status: 'firing',
    startsAt: 'Phase 4 scenario',
  },
]

export const incidentEvents: IncidentEvent[] = [
  { id: 'detect', time: 'T+00:00', title: 'Detection', detail: 'Alert observed in Prometheus or Suricata.', status: 'observed' },
  { id: 'collect', time: 'T+02:00', title: 'Evidence', detail: 'Grafana, Loki, command output, and optional PCAP collected.', status: 'investigating' },
  { id: 'ai', time: 'T+05:00', title: 'AI analysis', detail: 'Assistant summarizes evidence and missing data.', status: 'investigating' },
  { id: 'recover', time: 'T+08:00', title: 'Recovery', detail: 'Network or IDS scenario restored and proof saved.', status: 'resolved' },
]
```

Q36. Why include mock data?

Mock data keeps the visual demo usable when Prometheus, Loki, or Ollama are not
running. The UI must clearly label mock or sample data as demo data so it does
not pretend to be live evidence.

## 12. Add Query Provider And Routing

Q37. How should `src/main.tsx` be configured?

Replace `src/main.tsx`:

```tsx
import React from 'react'
import ReactDOM from 'react-dom/client'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { createBrowserRouter, RouterProvider } from 'react-router-dom'
import App from './App'
import { AlertsPage } from './pages/AlertsPage'
import { AssistantPage } from './pages/AssistantPage'
import { IncidentsPage } from './pages/IncidentsPage'
import { OverviewPage } from './pages/OverviewPage'
import { TopologyPage } from './pages/TopologyPage'
import './styles/app.css'

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchInterval: 30000,
      retry: 1,
    },
  },
})

const router = createBrowserRouter([
  {
    path: '/',
    element: <App />,
    children: [
      { index: true, element: <OverviewPage /> },
      { path: 'topology', element: <TopologyPage /> },
      { path: 'alerts', element: <AlertsPage /> },
      { path: 'assistant', element: <AssistantPage /> },
      { path: 'incidents', element: <IncidentsPage /> },
    ],
  },
])

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <QueryClientProvider client={queryClient}>
      <RouterProvider router={router} />
    </QueryClientProvider>
  </React.StrictMode>,
)
```

Q38. Why use TanStack Query?

The demo depends on server state:

- Backend health.
- Alerts.
- RAG answers.
- Diagnostics.
- Incident summaries.

TanStack Query provides loading, error, retry, refetch, and cache behavior
without writing that lifecycle logic in every component.

## 13. Create The App Layout

Q39. What should `src/App.tsx` contain?

Create:

```tsx
import { Activity, AlertTriangle, Bot, Clock3, GitBranch, LayoutDashboard } from 'lucide-react'
import { NavLink, Outlet } from 'react-router-dom'

const navItems = [
  { to: '/', label: 'Overview', icon: LayoutDashboard },
  { to: '/topology', label: 'Topology', icon: GitBranch },
  { to: '/alerts', label: 'Alerts', icon: AlertTriangle },
  { to: '/assistant', label: 'Assistant', icon: Bot },
  { to: '/incidents', label: 'Incidents', icon: Clock3 },
]

export default function App() {
  return (
    <div className="app-shell">
      <header className="topbar">
        <div>
          <p className="eyebrow">Network Security Lab</p>
          <h1>OSPF, IDS, Observability, AI</h1>
        </div>
        <div className="topbar-status">
          <Activity size={18} />
          Local demo console
        </div>
      </header>

      <div className="workspace">
        <nav className="sidebar" aria-label="Demo sections">
          {navItems.map((item) => (
            <NavLink key={item.to} to={item.to} end={item.to === '/'} className="nav-link">
              <item.icon size={18} />
              <span>{item.label}</span>
            </NavLink>
          ))}
        </nav>
        <main className="content">
          <Outlet />
        </main>
      </div>
    </div>
  )
}
```

Q40. Why put the project name in the header instead of a hero?

The evaluator should immediately see what the lab does. The header identifies
the project; the body shows the real demo. That is better for a technical
portfolio than a large decorative intro.

Q41. Which shared status component is useful?

Create `src/components/StatusPill.tsx`:

```tsx
import clsx from 'clsx'

type Status = 'healthy' | 'warning' | 'critical' | 'unknown' | 'info'

export function StatusPill({ status, label }: { status: Status; label?: string }) {
  return (
    <span className={clsx('status-pill', `status-${status}`)}>
      {label ?? status}
    </span>
  )
}
```

## 14. Add Visual Style

Q42. What base CSS should be used?

Create `src/styles/app.css`:

```css
:root {
  color: #172026;
  background: #f5f7f8;
  font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  font-synthesis: none;
  text-rendering: optimizeLegibility;
}

* {
  box-sizing: border-box;
}

body {
  margin: 0;
  min-width: 320px;
  min-height: 100vh;
  background: #f5f7f8;
}

button,
input,
textarea {
  font: inherit;
}

.app-shell {
  min-height: 100vh;
}

.topbar {
  min-height: 72px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  padding: 14px 24px;
  color: #ffffff;
  background: #152027;
  border-bottom: 4px solid #2a9d8f;
}

.topbar h1 {
  margin: 2px 0 0;
  font-size: clamp(20px, 3vw, 30px);
  line-height: 1.1;
  letter-spacing: 0;
}

.eyebrow {
  margin: 0;
  color: #9ecdc5;
  font-size: 12px;
  text-transform: uppercase;
  letter-spacing: 0;
  font-weight: 700;
}

.topbar-status {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  color: #d8f3ee;
  font-size: 14px;
}

.workspace {
  display: grid;
  grid-template-columns: 220px 1fr;
  min-height: calc(100vh - 76px);
}

.sidebar {
  padding: 16px;
  background: #ffffff;
  border-right: 1px solid #d9e2e6;
}

.nav-link {
  height: 42px;
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 0 12px;
  color: #34444c;
  text-decoration: none;
  border-radius: 8px;
  font-weight: 650;
}

.nav-link.active,
.nav-link:hover {
  color: #0c3b36;
  background: #dff4ef;
}

.content {
  padding: 20px;
}

.page-grid {
  display: grid;
  grid-template-columns: minmax(0, 1.5fr) minmax(320px, 0.9fr);
  gap: 16px;
  align-items: start;
}

.panel {
  background: #ffffff;
  border: 1px solid #d9e2e6;
  border-radius: 8px;
  box-shadow: 0 1px 2px rgb(15 23 42 / 0.05);
}

.panel-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  padding: 14px 16px;
  border-bottom: 1px solid #edf1f3;
}

.panel-title {
  margin: 0;
  font-size: 16px;
  letter-spacing: 0;
}

.panel-body {
  padding: 16px;
}

.status-pill {
  display: inline-flex;
  align-items: center;
  min-height: 24px;
  padding: 0 8px;
  border-radius: 999px;
  font-size: 12px;
  font-weight: 750;
  text-transform: uppercase;
}

.status-healthy {
  color: #075f49;
  background: #d9f7ed;
}

.status-warning {
  color: #7a4b00;
  background: #fff0c2;
}

.status-critical {
  color: #8b1e1e;
  background: #ffe0e0;
}

.status-unknown,
.status-info {
  color: #24455f;
  background: #dfefff;
}

.icon-button {
  width: 36px;
  height: 36px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border: 1px solid #cbd7dc;
  border-radius: 8px;
  color: #26343b;
  background: #ffffff;
  cursor: pointer;
}

.primary-button {
  min-height: 38px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 0 14px;
  border: 0;
  border-radius: 8px;
  color: #ffffff;
  background: #237b72;
  font-weight: 750;
  cursor: pointer;
}

.primary-button:disabled {
  opacity: 0.55;
  cursor: wait;
}

@media (max-width: 900px) {
  .workspace {
    grid-template-columns: 1fr;
  }

  .sidebar {
    display: flex;
    gap: 6px;
    overflow-x: auto;
    border-right: 0;
    border-bottom: 1px solid #d9e2e6;
  }

  .nav-link {
    flex: 0 0 auto;
  }

  .page-grid {
    grid-template-columns: 1fr;
  }

  .topbar {
    align-items: flex-start;
    flex-direction: column;
  }
}
```

Q43. Why use fixed panel radius and stable spacing?

The UI needs to look like an operations tool, not a decorative landing page.
Stable spacing, 8px radius, and restrained colors keep attention on topology,
alerts, and evidence.

## 15. Build The Topology View

Q44. How should topology data be displayed?

Use explicit nodes and links. Do not rely only on a screenshot. The UI should
make the network structure readable even if live metrics are down.

Q45. What topology component should be created?

Create `src/components/TopologyMap.tsx`:

```tsx
import { Cpu, Database, Monitor, Network, Router, Server } from 'lucide-react'
import { labLinks, labNodes } from '../data/demoData'
import { StatusPill } from './StatusPill'

const iconById = {
  R1: Router,
  R2: Router,
  R3: Router,
  monitoring: Monitor,
  management: Server,
  'mac-ai': Cpu,
}

export function TopologyMap() {
  return (
    <section className="panel topology-panel">
      <div className="panel-header">
        <h2 className="panel-title">Lab Topology</h2>
        <StatusPill status="healthy" label="demo" />
      </div>
      <div className="panel-body">
        <div className="topology-grid" aria-label="Network topology">
          {labNodes.map((node) => {
            const Icon = iconById[node.id as keyof typeof iconById] ?? Database
            return (
              <div key={node.id} className={`topology-node node-${node.id}`}>
                <div className="node-icon">
                  <Icon size={22} />
                </div>
                <div>
                  <h3>{node.label}</h3>
                  <p>{node.role}</p>
                  <span>{node.tap ?? node.ip ?? 'external'}</span>
                </div>
                <StatusPill status={node.status} />
              </div>
            )
          })}
        </div>

        <div className="link-list">
          {labLinks.map((link) => (
            <div key={link.id} className="link-row">
              <Network size={16} />
              <strong>{link.label}</strong>
              <span>{link.source} to {link.target}</span>
              <StatusPill status={link.status} />
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}
```

Q46. Which CSS supports the topology map?

Add:

```css
.topology-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(160px, 1fr));
  gap: 12px;
}

.topology-node {
  min-height: 124px;
  display: grid;
  grid-template-columns: 38px 1fr;
  gap: 10px;
  align-items: start;
  padding: 12px;
  border: 1px solid #d9e2e6;
  border-radius: 8px;
  background: #fbfcfd;
}

.topology-node h3 {
  margin: 0 0 4px;
  font-size: 16px;
  letter-spacing: 0;
}

.topology-node p {
  margin: 0 0 8px;
  color: #60727d;
  font-size: 13px;
}

.topology-node span {
  color: #34444c;
  font-size: 12px;
}

.node-icon {
  width: 36px;
  height: 36px;
  display: grid;
  place-items: center;
  border-radius: 8px;
  color: #0f544e;
  background: #dff4ef;
}

.link-list {
  display: grid;
  gap: 8px;
  margin-top: 14px;
}

.link-row {
  min-height: 40px;
  display: grid;
  grid-template-columns: 20px 90px 1fr auto;
  gap: 10px;
  align-items: center;
  padding: 8px 10px;
  border: 1px solid #edf1f3;
  border-radius: 8px;
}

@media (max-width: 720px) {
  .topology-grid {
    grid-template-columns: 1fr;
  }

  .link-row {
    grid-template-columns: 20px 1fr;
  }
}
```

Q47. How should the topology page use it?

Create `src/pages/TopologyPage.tsx`:

```tsx
import { TopologyMap } from '../components/TopologyMap'

export function TopologyPage() {
  return <TopologyMap />
}
```

## 16. Add Health And Metric Panels

Q48. How do we display backend health?

Create `src/components/HealthStrip.tsx`:

```tsx
import { useQuery } from '@tanstack/react-query'
import { getHealth } from '../api/client'
import { StatusPill } from './StatusPill'

function okStatus(ok?: boolean) {
  if (ok === true) return 'healthy'
  if (ok === false) return 'critical'
  return 'unknown'
}

export function HealthStrip() {
  const { data, isLoading, error } = useQuery({ queryKey: ['health'], queryFn: getHealth })

  if (isLoading) {
    return <div className="health-strip">Loading backend health...</div>
  }

  if (error) {
    return <div className="health-strip health-error">Backend health unavailable</div>
  }

  return (
    <div className="health-strip">
      <div>
        <span>FastAPI</span>
        <StatusPill status={data?.app === 'ok' ? 'healthy' : 'unknown'} />
      </div>
      <div>
        <span>Ollama</span>
        <StatusPill status={okStatus(data?.ollama?.ok)} />
      </div>
      <div>
        <span>Prometheus</span>
        <StatusPill status={okStatus(data?.prometheus?.ok)} />
      </div>
      <div>
        <span>Loki</span>
        <StatusPill status={okStatus(data?.loki?.ok)} />
      </div>
    </div>
  )
}
```

Q49. Which CSS supports the health strip?

Add:

```css
.health-strip {
  display: grid;
  grid-template-columns: repeat(4, minmax(130px, 1fr));
  gap: 10px;
  margin-bottom: 16px;
}

.health-strip > div {
  min-height: 58px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
  padding: 10px 12px;
  border: 1px solid #d9e2e6;
  border-radius: 8px;
  background: #ffffff;
  font-weight: 700;
}

.health-error {
  padding: 12px;
  color: #8b1e1e;
  background: #ffe0e0;
}

@media (max-width: 720px) {
  .health-strip {
    grid-template-columns: 1fr 1fr;
  }
}
```

Q50. How do we add a small metrics panel?

Create `src/components/MetricsPanel.tsx`:

```tsx
import { Line, LineChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts'

const sample = [
  { time: 'T-4', neighbors: 2 },
  { time: 'T-3', neighbors: 2 },
  { time: 'T-2', neighbors: 1 },
  { time: 'T-1', neighbors: 2 },
  { time: 'Now', neighbors: 2 },
]

export function MetricsPanel() {
  return (
    <section className="panel">
      <div className="panel-header">
        <h2 className="panel-title">Routing Signal</h2>
      </div>
      <div className="panel-body metric-chart">
        <ResponsiveContainer width="100%" height={180}>
          <LineChart data={sample} margin={{ top: 8, right: 12, left: 0, bottom: 0 }}>
            <XAxis dataKey="time" />
            <YAxis domain={[0, 2]} allowDecimals={false} />
            <Tooltip />
            <Line type="monotone" dataKey="neighbors" stroke="#237b72" strokeWidth={3} dot />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </section>
  )
}
```

Q51. Why is this panel sample data?

The first frontend iteration should not query Prometheus directly from the
browser. Either display a backend-provided metric endpoint or clearly mark the
chart as sample/demo data. Later, add `/demo/metrics` to FastAPI if live charts
are required.

## 17. Build The Alerts View

Q52. How should alerts be displayed first?

Use the existing sample alerts until a backend aggregation endpoint is added.
The UI can still call `/explain-alert` for an individual alert.

Q53. What component should display alerts?

Create `src/components/AlertList.tsx`:

```tsx
import { Bot, ShieldAlert } from 'lucide-react'
import { useState } from 'react'
import { explainAlert } from '../api/client'
import { demoAlerts } from '../data/demoData'
import { StatusPill } from './StatusPill'

export function AlertList() {
  const [answer, setAnswer] = useState<string>('')
  const [loadingId, setLoadingId] = useState<string | null>(null)

  async function handleExplain(id: string, name: string, summary: string) {
    setLoadingId(id)
    setAnswer('')
    try {
      const response = await explainAlert(name, summary)
      setAnswer(JSON.stringify(response, null, 2))
    } catch (error) {
      setAnswer(error instanceof Error ? error.message : 'Unknown error')
    } finally {
      setLoadingId(null)
    }
  }

  return (
    <section className="panel">
      <div className="panel-header">
        <h2 className="panel-title">Recent Alerts</h2>
        <StatusPill status="info" label="sample" />
      </div>
      <div className="panel-body alert-stack">
        {demoAlerts.map((alert) => (
          <article key={alert.id} className="alert-row">
            <ShieldAlert size={20} />
            <div>
              <h3>{alert.name}</h3>
              <p>{alert.summary}</p>
              <span>{alert.source} - {alert.startsAt}</span>
            </div>
            <StatusPill status={alert.severity === 'critical' ? 'critical' : alert.severity === 'warning' ? 'warning' : 'info'} />
            <button
              className="icon-button"
              title="Explain alert"
              onClick={() => handleExplain(alert.id, alert.name, alert.summary)}
              disabled={loadingId === alert.id}
            >
              <Bot size={18} />
            </button>
          </article>
        ))}

        {answer ? <pre className="answer-box">{answer}</pre> : null}
      </div>
    </section>
  )
}
```

Q54. Which CSS supports alerts?

Add:

```css
.alert-stack {
  display: grid;
  gap: 10px;
}

.alert-row {
  display: grid;
  grid-template-columns: 24px 1fr auto 38px;
  gap: 10px;
  align-items: start;
  padding: 12px;
  border: 1px solid #edf1f3;
  border-radius: 8px;
  background: #fbfcfd;
}

.alert-row h3 {
  margin: 0 0 4px;
  font-size: 15px;
  letter-spacing: 0;
}

.alert-row p {
  margin: 0 0 6px;
  color: #485b64;
}

.alert-row span {
  color: #6b7c85;
  font-size: 12px;
}

.answer-box {
  max-height: 280px;
  overflow: auto;
  margin: 0;
  padding: 12px;
  border-radius: 8px;
  color: #d8f3ee;
  background: #152027;
  font-size: 12px;
  white-space: pre-wrap;
}
```

Q55. How should the alerts page use it?

Create `src/pages/AlertsPage.tsx`:

```tsx
import { AlertList } from '../components/AlertList'

export function AlertsPage() {
  return <AlertList />
}
```

## 18. Build The AI Assistant View

Q56. Which assistant workflows are required?

For the first UI:

| Mode | Endpoint |
| --- | --- |
| RAG question | `POST /rag/ask` |
| OSPF diagnostic | `POST /diagnostic` |
| Alert explanation | `POST /explain-alert` |

Q57. What assistant component should be created?

Create `src/components/AssistantPanel.tsx`:

```tsx
import { Bot, Send } from 'lucide-react'
import { FormEvent, useState } from 'react'
import { askDiagnostic, askRag } from '../api/client'

type Mode = 'rag' | 'diagnostic'

export function AssistantPanel() {
  const [mode, setMode] = useState<Mode>('rag')
  const [question, setQuestion] = useState('Which VLAN connects R1 and R2?')
  const [answer, setAnswer] = useState('')
  const [loading, setLoading] = useState(false)

  async function handleSubmit(event: FormEvent) {
    event.preventDefault()
    setLoading(true)
    setAnswer('')
    try {
      const response = mode === 'rag'
        ? await askRag(question)
        : await askDiagnostic(question)
      setAnswer(JSON.stringify(response, null, 2))
    } catch (error) {
      setAnswer(error instanceof Error ? error.message : 'Unknown error')
    } finally {
      setLoading(false)
    }
  }

  return (
    <section className="panel assistant-panel">
      <div className="panel-header">
        <h2 className="panel-title">AI Assistant</h2>
        <Bot size={20} />
      </div>
      <div className="panel-body">
        <form className="assistant-form" onSubmit={handleSubmit}>
          <div className="segmented-control" aria-label="Assistant mode">
            <button type="button" className={mode === 'rag' ? 'active' : ''} onClick={() => setMode('rag')}>
              RAG
            </button>
            <button type="button" className={mode === 'diagnostic' ? 'active' : ''} onClick={() => setMode('diagnostic')}>
              Diagnostic
            </button>
          </div>

          <textarea
            value={question}
            onChange={(event) => setQuestion(event.target.value)}
            rows={5}
            aria-label="Assistant question"
          />

          <button className="primary-button" disabled={loading || !question.trim()}>
            <Send size={17} />
            {loading ? 'Asking...' : 'Ask'}
          </button>
        </form>

        {answer ? <pre className="answer-box assistant-answer">{answer}</pre> : null}
      </div>
    </section>
  )
}
```

Q58. Which CSS supports the assistant?

Add:

```css
.assistant-form {
  display: grid;
  gap: 12px;
}

.segmented-control {
  display: inline-grid;
  grid-template-columns: 1fr 1fr;
  width: min(260px, 100%);
  padding: 4px;
  border: 1px solid #cbd7dc;
  border-radius: 8px;
  background: #edf1f3;
}

.segmented-control button {
  min-height: 34px;
  border: 0;
  border-radius: 6px;
  color: #34444c;
  background: transparent;
  cursor: pointer;
  font-weight: 750;
}

.segmented-control button.active {
  color: #0c3b36;
  background: #ffffff;
}

.assistant-form textarea {
  width: 100%;
  resize: vertical;
  min-height: 120px;
  padding: 12px;
  border: 1px solid #cbd7dc;
  border-radius: 8px;
  color: #172026;
}

.assistant-answer {
  margin-top: 14px;
}
```

Q59. How should the assistant page use it?

Create `src/pages/AssistantPage.tsx`:

```tsx
import { AssistantPanel } from '../components/AssistantPanel'

export function AssistantPage() {
  return <AssistantPanel />
}
```

Q60. How should citations be improved later?

Instead of dumping JSON, parse `RagAskResponse` and display:

- Answer text.
- Citation chips.
- Retrieved source list.
- Missing sources.
- Verification commands.

JSON is acceptable for the first integration proof because it proves the API
contract. Polish the display after the end-to-end flow works.

## 19. Build The Incident Timeline

Q61. What timeline component should be created?

Create `src/components/IncidentTimeline.tsx`:

```tsx
import { CheckCircle2, Clock, Search, ShieldCheck } from 'lucide-react'
import { incidentEvents } from '../data/demoData'
import { StatusPill } from './StatusPill'

const icons = {
  observed: Search,
  investigating: Clock,
  contained: ShieldCheck,
  resolved: CheckCircle2,
}

export function IncidentTimeline() {
  return (
    <section className="panel">
      <div className="panel-header">
        <h2 className="panel-title">Incident Timeline</h2>
        <StatusPill status="info" label="template" />
      </div>
      <div className="panel-body timeline">
        {incidentEvents.map((event) => {
          const Icon = icons[event.status]
          return (
            <article key={event.id} className="timeline-event">
              <div className="timeline-icon">
                <Icon size={18} />
              </div>
              <div>
                <span>{event.time}</span>
                <h3>{event.title}</h3>
                <p>{event.detail}</p>
              </div>
            </article>
          )
        })}
      </div>
    </section>
  )
}
```

Q62. Which CSS supports the timeline?

Add:

```css
.timeline {
  display: grid;
  gap: 12px;
}

.timeline-event {
  display: grid;
  grid-template-columns: 34px 1fr;
  gap: 10px;
  padding: 12px;
  border: 1px solid #edf1f3;
  border-radius: 8px;
  background: #fbfcfd;
}

.timeline-icon {
  width: 32px;
  height: 32px;
  display: grid;
  place-items: center;
  border-radius: 8px;
  color: #8a5a00;
  background: #fff0c2;
}

.timeline-event span {
  color: #6b7c85;
  font-size: 12px;
  font-weight: 750;
}

.timeline-event h3 {
  margin: 2px 0 4px;
  font-size: 15px;
}

.timeline-event p {
  margin: 0;
  color: #485b64;
}
```

Q63. How should the incidents page use it?

Create `src/pages/IncidentsPage.tsx`:

```tsx
import { IncidentTimeline } from '../components/IncidentTimeline'

export function IncidentsPage() {
  return <IncidentTimeline />
}
```

## 20. Add Optional Demo Backend Endpoints

Q64. Why add demo-specific backend endpoints?

The browser should not query Prometheus, Loki, or ChromaDB directly. If live
topology and alert data are needed, aggregate them through FastAPI.

Q65. Which endpoints are useful?

Add later if needed:

| Endpoint | Purpose |
| --- | --- |
| `GET /demo/topology` | Nodes, links, and status |
| `GET /demo/alerts` | Recent Prometheus and IDS alerts |
| `GET /demo/incidents` | Timeline entries |
| `GET /demo/metrics/routing` | Small routing chart data |

Q66. What schema can support demo topology?

Create `app/demo_schemas.py` in the backend:

```python
from __future__ import annotations

from typing import Literal

from pydantic import BaseModel


Status = Literal["healthy", "warning", "critical", "unknown"]


class DemoNode(BaseModel):
    id: str
    label: str
    role: str
    tap: str | None = None
    ip: str | None = None
    status: Status = "unknown"


class DemoLink(BaseModel):
    id: str
    source: str
    target: str
    label: str
    status: Status = "unknown"


class DemoTopology(BaseModel):
    nodes: list[DemoNode]
    links: list[DemoLink]
```

Q67. What simple topology endpoint can be added?

Add to `app/main.py`:

```python
from .demo_schemas import DemoLink, DemoNode, DemoTopology


@app.get("/demo/topology", dependencies=[Depends(require_token)])
async def demo_topology():
    return DemoTopology(
        nodes=[
            DemoNode(id="R1", label="R1", role="Default route origin", tap="tap62", ip="10.99.0.1", status="healthy"),
            DemoNode(id="R2", label="R2", role="Router", tap="tap63", ip="10.99.0.2", status="healthy"),
            DemoNode(id="R3", label="R3", role="Router", tap="tap64", ip="10.99.0.3", status="healthy"),
            DemoNode(id="monitoring", label="Monitoring", role="IDS sensor", tap="tap65", ip="10.99.0.65", status="warning"),
            DemoNode(id="management", label="Management", role="Observability", tap="tap66", ip="10.99.0.66", status="healthy"),
            DemoNode(id="mac-ai", label="Mac AI", role="Ollama inference", status="healthy"),
        ],
        links=[
            DemoLink(id="vlan440", source="R1", target="R2", label="VLAN 440", status="healthy"),
            DemoLink(id="vlan441", source="R1", target="R3", label="VLAN 441", status="healthy"),
            DemoLink(id="vlan442", source="R2", target="R3", label="VLAN 442", status="healthy"),
            DemoLink(id="ollama", source="management", target="mac-ai", label="Ollama API", status="healthy"),
        ],
    )
```

Q68. Why start with a static endpoint?

A static endpoint proves the frontend/backend contract. Once the UI is stable,
replace status values with Prometheus or Loki derived status. Do not block the
demo interface on perfect live aggregation.

Q69. How do we test the optional endpoint?

```console
curl -s http://127.0.0.1:8080/demo/topology \
  -H "Authorization: Bearer $API_TOKEN" | jq
```

Expected result:

- JSON contains `nodes`.
- JSON contains `links`.
- Status values are explicit.

## 21. Run The Interface Manually

Q70. How do we start the backend?

On the Management VM:

```console
cd /path/to/network-security-lab/backend/phase5-ai
. .venv/bin/activate
uvicorn app.main:app --host 127.0.0.1 --port 8080 --reload
```

Q71. How do we start the frontend?

In another terminal:

```console
cd /path/to/network-security-lab/frontend/demo-ui
npm run dev -- --host 127.0.0.1 --port 5173
```

Open:

```text
http://127.0.0.1:5173
```

Q72. What should be visible?

Expected first screen:

- Header: `Network Security Lab`.
- Sidebar or mobile tabs.
- Health strip.
- Topology panel.
- Alerts panel.
- AI assistant panel.
- Timeline preview.

Q73. What if the backend is not running?

The UI should still load. Health and AI calls should show readable errors.
Sample topology, alerts, and timeline may remain visible with a `sample` or
`template` label.

## 22. Validate End To End API Calls

Q74. How do we test the proxy directly?

With the frontend dev server running:

```console
curl -s http://127.0.0.1:5173/api/health | jq
```

Expected result:

- The response is the FastAPI `/health` JSON.
- No browser CORS configuration is required.

Q75. How do we test RAG from the UI?

In the Assistant panel:

```text
Which VLAN connects R1 and R2, and what should I verify if adjacency fails?
```

Expected result:

- The UI receives JSON from `/rag/ask`.
- The answer cites a source if the RAG index exists.
- The response says what evidence is missing if retrieval is weak.

Q76. How do we test OSPF diagnostic mode?

Switch Assistant mode to `Diagnostic` and ask:

```text
Assess current R2 OSPFv2 neighbor health.
```

Expected result:

- The backend calls `/diagnostic`.
- If live metrics exist, the answer references them.
- If live metrics are missing, the answer states missing evidence.

Q77. How do we test alert explanation from the UI?

In the Recent Alerts panel, click the bot icon on the Suricata sample alert.

Expected result:

- The UI calls `/explain-alert`.
- The response identifies the alert as lab-only sample or controlled IDS
  scenario if the evidence says so.
- The response does not recommend external scanning.

Q78. What evidence should be copied into the proof report?

Save:

- Browser screenshot of the overview screen.
- Terminal output of `/api/health` through the proxy.
- JSON response from one RAG question.
- JSON response from one diagnostic question.
- Screenshot of an error state with backend stopped or unavailable.

## 23. Responsive And Visual Testing

Q79. How do we add Playwright?

From `frontend/demo-ui`:

```console
npx playwright install chromium
```

Q80. What Playwright test should be created?

Create `tests/demo.spec.ts`:

```ts
import { expect, test } from '@playwright/test'

test('overview renders on desktop', async ({ page }) => {
  await page.setViewportSize({ width: 1440, height: 960 })
  await page.goto('/')
  await expect(page.getByText('Network Security Lab')).toBeVisible()
  await expect(page.getByText('Lab Topology')).toBeVisible()
  await expect(page.getByText('AI Assistant')).toBeVisible()
  await page.screenshot({ path: 'test-results/phase8-overview-desktop.png', fullPage: true })
})

test('overview renders on mobile', async ({ page }) => {
  await page.setViewportSize({ width: 390, height: 844 })
  await page.goto('/')
  await expect(page.getByText('Network Security Lab')).toBeVisible()
  await expect(page.getByText('Lab Topology')).toBeVisible()
  await page.screenshot({ path: 'test-results/phase8-overview-mobile.png', fullPage: true })
})
```

Q81. How do we configure Playwright for Vite?

Create `playwright.config.ts`:

```ts
import { defineConfig } from '@playwright/test'

export default defineConfig({
  testDir: './tests',
  use: {
    baseURL: 'http://127.0.0.1:5173',
    screenshot: 'only-on-failure',
  },
  webServer: {
    command: 'npm run dev -- --host 127.0.0.1 --port 5173',
    url: 'http://127.0.0.1:5173',
    reuseExistingServer: true,
  },
})
```

Q82. How do we run responsive tests?

```console
cd /path/to/network-security-lab/frontend/demo-ui
npm run test:e2e
```

Expected result:

- Tests pass.
- Desktop screenshot is saved.
- Mobile screenshot is saved.

Q83. What visual issues must be fixed before finishing?

Check:

- Text does not overlap.
- Buttons do not resize unpredictably.
- The sidebar works on mobile.
- Panels stack cleanly under 900px.
- Long JSON responses scroll instead of breaking layout.
- Alert names wrap without overflowing.
- Topology nodes remain readable.

## 24. Demo Script

Q84. Why prepare a script?

A demo can fail if it depends on memory alone. A short script keeps the
presentation calm and repeatable.

Q85. What is the five-minute demo path?

Use this order:

1. Show the overview screen.
2. Point to the topology and explain `R1`, `R2`, `R3`, Monitoring,
   Management, and Mac AI.
3. Show recent alerts and explain one OSPF or Suricata example.
4. Ask the assistant a RAG question about VLAN `440`.
5. Ask the assistant a diagnostic question about `R2`.
6. Show the incident timeline.
7. Mention limitations and how live evidence is verified in Grafana,
   Prometheus, Loki, and FRR.

Q86. Which exact assistant questions should be prepared?

Use:

```text
Which VLAN connects R1 and R2, and what should I verify if adjacency fails?
```

```text
Assess current R2 OSPFv2 neighbor health.
```

```text
What evidence should I collect for a controlled Suricata Nmap scan incident?
```

Q87. What should be said about limitations?

Say:

- The UI is a demo surface, not the source of truth.
- Live state is verified through Prometheus, Loki, FRR commands, and Grafana.
- AI answers must cite evidence or state missing data.
- Controlled security tests stay inside the lab.
- The frontend is local and not exposed publicly.

## 25. Save Evidence

Q88. Which screenshots should be saved?

Save:

| Evidence | Suggested file |
| --- | --- |
| Desktop overview | `screenshots/phase8/phase8-overview-desktop.png` |
| Mobile overview | `screenshots/phase8/phase8-overview-mobile.png` |
| Topology view | `screenshots/phase8/phase8-topology.png` |
| Alerts view | `screenshots/phase8/phase8-alerts.png` |
| Assistant RAG answer | `screenshots/phase8/phase8-assistant-rag.png` |
| Assistant diagnostic answer | `screenshots/phase8/phase8-assistant-diagnostic.png` |
| Incident timeline | `screenshots/phase8/phase8-incident-timeline.png` |
| Backend error state | `screenshots/phase8/phase8-error-state.png` |

Q89. Which command outputs should be saved?

```console
cd /path/to/network-security-lab/frontend/demo-ui
npm run build
npm run test:e2e

curl -s http://127.0.0.1:5173/api/health | jq
curl -s http://127.0.0.1:8080/openapi.json | jq '.paths | keys'
```

Q90. Where should the proof report go?

Create:

```text
docs/proofs-phase8.md
```

Use this template:

```markdown
# Phase 8 Proofs - Frontend Demo Interface

## Interface

- Stack:
- Frontend path:
- Backend URL:
- Demo URL:

## Validation

| Check | Result | Evidence |
| --- | --- | --- |
| Vite dev server starts |  |  |
| FastAPI proxy works |  |  |
| Overview renders |  |  |
| RAG question works |  |  |
| Diagnostic question works |  |  |
| Alert explanation works |  |  |
| Mobile layout works |  |  |
| Build succeeds |  |  |

## Screenshots

| Evidence | File |
| --- | --- |
| Desktop overview | `screenshots/phase8/phase8-overview-desktop.png` |
| Mobile overview | `screenshots/phase8/phase8-overview-mobile.png` |
| Assistant answer | `screenshots/phase8/phase8-assistant-rag.png` |

## Limitations

- Add demo limitations here.
```

Q91. Which files should be backed up?

Back up:

| File or folder | Reason |
| --- | --- |
| `frontend/demo-ui/src/` | Interface source |
| `frontend/demo-ui/package.json` | Dependencies and scripts |
| `frontend/demo-ui/vite.config.ts` | Proxy behavior |
| `docs/proofs-phase8.md` | Validation record |
| `screenshots/phase8/` | Portfolio evidence |

Do not back up `.env.local` into the repository.

## 26. Troubleshooting

### Vite Cannot Start

Q92. What should be checked?

```console
cd /path/to/network-security-lab/frontend/demo-ui
node --version
npm --version
npm install
npm run dev -- --host 127.0.0.1 --port 5173
```

Common causes:

- Node.js is missing or too old.
- Dependencies were not installed.
- Port `5173` is already used.
- The command is run outside `frontend/demo-ui`.

### The Proxy Returns 401

Q93. What should be checked?

```console
cd /path/to/network-security-lab/frontend/demo-ui
grep -E 'API_TARGET|API_TOKEN' .env.local
curl -s http://127.0.0.1:5173/api/rag/sources | jq
```

Common causes:

- `.env.local` is missing.
- `API_TOKEN` does not match the backend `.env`.
- The frontend dev server was not restarted after editing `.env.local`.
- The backend authentication helper expects a different header format.

### The Proxy Cannot Reach FastAPI

Q94. What should be checked?

```console
curl -s http://127.0.0.1:8080/health | jq
curl -s http://127.0.0.1:5173/api/health | jq
```

If the first command fails, start FastAPI. If the first works and the second
fails, inspect `vite.config.ts`.

### The Assistant Returns Errors

Q95. What should be checked?

```console
curl -s http://127.0.0.1:8080/health | jq
curl -s http://127.0.0.1:8080/rag/sources \
  -H "Authorization: Bearer $API_TOKEN" | jq
```

Common causes:

- Ollama is not reachable.
- RAG index is empty.
- The request took longer than `REQUEST_TIMEOUT_SECONDS`.
- The model returned invalid structured JSON.

### Layout Breaks On Mobile

Q96. What should be checked?

Use browser developer tools or Playwright:

```console
npm run test:e2e
```

Check:

- `.workspace` switches to one column.
- `.page-grid` switches to one column.
- Alert rows do not overflow.
- Long JSON blocks scroll.
- Buttons remain at least 36px high.

### Recharts Panel Is Blank

Q97. What should be checked?

The parent container must have a stable height:

```css
.metric-chart {
  min-height: 200px;
}
```

Then refresh the page. If the chart is still blank, inspect the console for
React or Recharts errors.

### Playwright Tests Fail

Q98. What should be checked?

```console
npx playwright install chromium
npm run dev -- --host 127.0.0.1 --port 5173
npm run test:e2e -- --headed
```

Common causes:

- The dev server did not start.
- Text labels changed.
- The page is waiting on a slow backend call.
- The base URL in `playwright.config.ts` is wrong.

### The Demo Feels Too Fragile

Q99. What should be simplified?

Simplify in this order:

1. Keep topology and timeline as sample data.
2. Keep health as the only live status panel.
3. Keep one working RAG question.
4. Keep one working diagnostic question.
5. Link to Grafana for deep metrics instead of recreating every dashboard.

The goal is a reliable five-minute demo, not a full monitoring product.

## 27. Conclusion

Phase 8 turns the lab into a visible demo. The interface shows the topology,
recent alerts, AI/RAG assistant workflows, incident timeline, and health
signals in one place. It does not replace Grafana, Prometheus, Loki, FRR, or
Suricata; it makes the project easier to understand quickly.

The exit criteria are satisfied when:

- `frontend/demo-ui` runs locally.
- The first screen shows the operational lab, not a landing page.
- The UI reaches FastAPI through `/api`.
- At least one RAG question works from the UI.
- At least one diagnostic or alert explanation works from the UI.
- Desktop and mobile screenshots are saved.
- `docs/proofs-phase8.md` records results and limitations.

Phase 9 can now polish the public README, clean the repository, record the demo
video, and turn the screenshots into portfolio material.

## 28. References

- InetDoc OSPF practical lab style and structure: <https://inetdoc.net/travaux_pratiques/interco_05.ospf/>
- Vite getting started: <https://vite.dev/guide/>
- React build a React app from scratch: <https://react.dev/learn/build-a-react-app-from-scratch>
- React Router documentation: <https://reactrouter.com/>
- TanStack Query React installation: <https://tanstack.com/query/v5/docs/framework/react/installation>
- TanStack Query React quick start: <https://tanstack.com/query/v5/docs/framework/react/quick-start>
- Lucide React guide: <https://lucide.dev/guide/react>
- Recharts ResponsiveContainer: <https://recharts.github.io/en-US/api/ResponsiveContainer/>
- Playwright screenshots: <https://playwright.dev/docs/screenshots>
- Playwright emulation: <https://playwright.dev/docs/emulation>
