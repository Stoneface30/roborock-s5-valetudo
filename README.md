# Roborock S5 — Valetudo Local Control

Kill the Xiaomi cloud dependency. "Conchita" gets local MQTT, full map control, no cloud.

## Status: [~] FLASH BLOCKED — UART ADAPTER ORDERED (2026-05-04)
- Firmware built: `v11_002034.pkg` (DustBuilder job j69f74e8396070) ✅
- WiFi OTA blocked: Xiaomi cloud locked on this device ❌
- UART flash: CP2102 adapter **ordered** — arriving soon
- Vacuum current IP: **192.168.0.202** (new DHCP lease, Xiaomi firmware still running)

## When the CP2102 arrives
```
UART wiring: CP2102 TX → Conchita mainboard RX
             CP2102 RX → Conchita mainboard TX
             CP2102 GND → Conchita GND
Baud: 115200
Firmware: F:\ROBOROCK_CLAUDED\firmware\v11_002034.pkg
```

## Pre-Flash Backup
HA backup slug: `f5a79289` ("Pre-Valetudo-flash-2026-05-03") — NAS WebDAV confirmed.

## Post-Flash Next Steps
1. Verify Valetudo at http://192.168.0.202 (or new IP after flash)
2. Create DHCP reservation for Conchita at .202 (verify MAC post-flash)
3. Configure Valetudo MQTT → Mosquitto at 192.168.0.166:1883
4. Remove Xiaomi Home integration from HA
5. Add `vacuum.conchita_local` MQTT entity
6. Update 4 duplex relay automations
7. Run first map
8. Wire map tile to Magic Mirror

## Parent project
`F:\HA_CLAUDED\docs\PROJECT_MASTERFILE.md` section A6.4
