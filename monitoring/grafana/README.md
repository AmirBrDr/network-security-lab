# Grafana Dashboards

These files define the Phase 3 dashboards for the Network Security Lab.
They expect the Grafana data sources from `docs/phase3-tutorial.md`:

- Prometheus datasource UID: `prometheus`
- Loki datasource UID: `loki`

There are two dashboard JSON formats here:

| Path | Use |
| --- | --- |
| `dashboards/*/*.json` | Classic Grafana JSON for file provisioning or dashboard import. |
| `schema-v2/*.json` | Grafana v13 dashboard schema for the `Edit as code` dialog. |

From a checkout of this repository on the Management VM, install them with:

```console
sudo install -d -m 0755 \
  /etc/grafana/provisioning/dashboards/system \
  /etc/grafana/provisioning/dashboards/network \
  /etc/grafana/provisioning/dashboards/routing

sudo cp monitoring/grafana/provisioning/dashboards/network-security-lab.yml \
  /etc/grafana/provisioning/dashboards/network-security-lab.yml

sudo cp monitoring/grafana/dashboards/system/system.json \
  /etc/grafana/provisioning/dashboards/system/system.json

sudo cp monitoring/grafana/dashboards/network/network.json \
  /etc/grafana/provisioning/dashboards/network/network.json

sudo cp monitoring/grafana/dashboards/routing/routing.json \
  /etc/grafana/provisioning/dashboards/routing/routing.json

sudo systemctl restart grafana-server
```

For Grafana v13 `Edit as code`, paste the matching file from `schema-v2/`
instead of the classic provisioning JSON.

Grafana will create these folders and dashboards:

| Folder | Dashboard |
| --- | --- |
| `System` | `Network Security Lab - System` |
| `Network` | `Network Security Lab - Network` |
| `Routing` | `Network Security Lab - Routing` |
