#!/bin/sh
set -eu

HOST="$(hostname -s)"
DIR="/var/lib/prometheus/node-exporter"
TMP="$DIR/frr.prom.$$"
OUT="$DIR/frr.prom"

if systemctl is-active --quiet frr.service; then
    FRR_ACTIVE=1
else
    FRR_ACTIVE=0
fi

if command -v vtysh >/dev/null 2>&1; then
    OSPFV2_FULL="$(vtysh -c 'show ip ospf neighbor' 2>/dev/null | awk '/Full/ {c++} END {print c+0}')"
    OSPFV3_FULL="$(vtysh -c 'show ipv6 ospf6 neighbor' 2>/dev/null | awk '/Full/ {c++} END {print c+0}')"
else
    OSPFV2_FULL=0
    OSPFV3_FULL=0
fi

cat > "$TMP" <<METRICS
# HELP frr_service_active 1 if frr.service is active, otherwise 0.
# TYPE frr_service_active gauge
frr_service_active{node="$HOST"} $FRR_ACTIVE
# HELP frr_ospf_neighbor_full_total Number of OSPF neighbors in Full state.
# TYPE frr_ospf_neighbor_full_total gauge
frr_ospf_neighbor_full_total{node="$HOST",protocol="ospfv2"} $OSPFV2_FULL
frr_ospf_neighbor_full_total{node="$HOST",protocol="ospfv3"} $OSPFV3_FULL
# HELP frr_textfile_last_success_unixtime Unix timestamp of the last successful FRR textfile collection.
# TYPE frr_textfile_last_success_unixtime gauge
frr_textfile_last_success_unixtime{node="$HOST"} $(date +%s)
METRICS

chmod 0644 "$TMP"
mv "$TMP" "$OUT"