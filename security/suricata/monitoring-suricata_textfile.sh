#!/bin/sh
set -eu

HOST="$(hostname -s)"
DIR="/var/lib/prometheus/node-exporter"
EVE="/var/log/suricata/eve.json"
TMP="$DIR/suricata.prom.$$"
OUT="$DIR/suricata.prom"

if systemctl is-active --quiet suricata.service; then
    SURICATA_ACTIVE=1
else
    SURICATA_ACTIVE=0
fi

if [ -r "$EVE" ]; then
    ALERTS_TOTAL="$(jq -c 'select(.event_type=="alert")' "$EVE" 2>/dev/null | wc -l | awk '{print $1}')"
    LAST_ALERT_TS="$(jq -r 'select(.event_type=="alert") | .timestamp' "$EVE" 2>/dev/null | tail -n 1)"
else
    ALERTS_TOTAL=0
    LAST_ALERT_TS=""
fi

if [ -n "${LAST_ALERT_TS:-}" ] && [ "$LAST_ALERT_TS" != "null" ]; then
    LAST_ALERT_UNIX="$(date -d "$LAST_ALERT_TS" +%s 2>/dev/null || echo 0)"
else
    LAST_ALERT_UNIX=0
fi

cat > "$TMP" <<METRICS
# HELP suricata_service_active 1 if suricata.service is active, otherwise 0.
# TYPE suricata_service_active gauge
suricata_service_active{node="$HOST"} $SURICATA_ACTIVE
# HELP suricata_eve_alert_events_total Number of alert records in the current Suricata EVE file.
# TYPE suricata_eve_alert_events_total counter
suricata_eve_alert_events_total{node="$HOST"} $ALERTS_TOTAL
# HELP suricata_eve_last_alert_unixtime Unix timestamp of the last Suricata alert.
# TYPE suricata_eve_last_alert_unixtime gauge
suricata_eve_last_alert_unixtime{node="$HOST"} $LAST_ALERT_UNIX
# HELP suricata_eve_last_success_unixtime Unix timestamp of the last successful Suricata textfile collection.
# TYPE suricata_eve_last_success_unixtime gauge
suricata_eve_last_success_unixtime{node="$HOST"} $(date +%s)
METRICS

chmod 0644 "$TMP"
mv "$TMP" "$OUT"
