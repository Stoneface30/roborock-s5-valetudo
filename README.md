# Roborock S5 — Valetudo Local Control

Kill the Xiaomi cloud dependency. "Conchita" runs local MQTT, full map control, no cloud.

## Status: ✅ VALETUDO LIVE (2026-05-04)
- Firmware flashed: `v11_002034.pkg` (DustBuilder)
- Valetudo accessible: **http://192.168.0.202**
- SSH: `ssh -i firmware/j69f74e8396070.id_rsa root@192.168.0.202`

## ⚠️ IP Conflict
`.202` was previously the Nest Hello doorbell's DHCP reservation. Verify doorbell IP and update router DHCP table before adding the .202 reservation for Conchita.

## Next Steps
1. Resolve .202 DHCP conflict (doorbell vs vacuum)
2. Configure Valetudo MQTT → broker at 192.168.0.166:1883
3. Remove Xiaomi Home integration from HA
4. Add `vacuum.conchita_local` MQTT entity in HA
5. Update duplex relay automations (4 automations, swap entity IDs)
6. Run first full-house map in Valetudo
7. Wire live map tile to Magic Mirror

## Pre-Flash Backup
HA backup slug: `f5a79289` ("Pre-Valetudo-flash-2026-05-03") — NAS WebDAV confirmed.

## Parent project
`F:\HA_CLAUDED\docs\PROJECT_MASTERFILE.md` section A6.4
