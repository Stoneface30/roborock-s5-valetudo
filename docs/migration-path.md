# Migration Path — Cloud → Local (Valetudo)

**Status: Firmware building — job j69f74e8396070 queued 2026-05-03. Awaiting download link email.**

## Overview

Current: Xiaomi Home HACS cloud integration → unreliable, drops offline, requires cloud auth.
Target: Valetudo on-device MQTT → local, no cloud dependency, instant response.

## Prerequisites Checklist

- [x] Firmware version captured: `3.5.8_002034` (2026-05-03)
- [x] Firmware ≤ v2034 confirmed — exactly v2034, root eligible, no downgrade needed
- [ ] **OTA updates disabled in Xiaomi Home app** — BLOCK THIS FIRST or root is permanently lost (app shows "up to date" 2026-05-03 — no pending update, but still disable auto-update)
- [x] Device token extracted — `4153794a65734d616339323569583865` (2026-05-03, from HA backup)
- [x] Full HA backup taken and verified — slug `f5a79289`, "Pre-Valetudo-flash-2026-05-03", 100.2 MB (2026-05-03)
- [ ] Roborock app backup taken (map + settings saved to phone)
- [~] DustBuilder rooted firmware image — **job j69f74e8396070 submitted 2026-05-03** (Valetudo 2026.02.0, v2034, OTA format). Awaiting download link at jeanbenoit.pilon@gmail.com. Once received: download `.pkg`, verify SHA256, store at `F:\ROBOROCK_CLAUDED\firmware\`
- [ ] Rollback procedure documented and understood

### Device Token

The token is needed to flash. Retrieve it before starting:

```bash
# Option 1 — python-miio discover (run while vacuum is on the dock/same Wi-Fi)
pip install python-miio
python3 -m miio discover
# Look for 192.168.0.89 — token is the 32-char hex string

# Option 2 — from HA Xiaomi Home integration logs
# HA → Settings → System → Logs → filter "roborock" → look for token in auth/init lines
```

Store the token here once found: `TOKEN=4153794a65734d616339323569583865`

**Token extracted 2026-05-03** from HA backup (`f5a79289`) `.storage/xiaomi_home/miot_devices/6288372713_de.dict`. Confirmed device did=261412235, model=roborock.vacuum.s5, fw=3.5.8_002034.

## Phase 1 — Root & Flash

1. **Backup**: HA → Settings → System → Backups → Create backup. Verify NAS backup received.
2. **Roborock app backup**: Export map + preferences.
3. **Create firmware**: DustBuilder → select S5 → add Valetudo → download image.
4. **Flash**: Follow the exact command printed on the DustBuilder download page.
   The typical command is:
   ```bash
   # python-miio >= 0.5.12
   miiocli roborockvacuum --ip 192.168.0.89 --token <32_char_token> update_firmware image.pkg
   # If the above fails, try:
   python3 -m miio.rockrobo --ip 192.168.0.89 --token <32_char_token> --firmware image.pkg
   ```
   **Do NOT use `miio flash` — that syntax does not exist in python-miio.**
5. **Verify**: `curl http://192.168.0.89/api/v2/robot/state` → should return JSON state.
6. **Valetudo web UI**: http://192.168.0.89 → configure map, zones, MQTT broker.

## Phase 2 — MQTT Wiring

1. **Configure Valetudo MQTT** (in Valetudo web UI):
   - Broker: `192.168.0.166:1883`
   - Username: `mqtt_user`
   - Password: see `.env`
   - Topic prefix: `vacuum/conchita`

2. **Add MQTT vacuum entity to HA** (see `mqtt-contract.md` for YAML snippet).

3. **Verify topics** via Developer Tools → MQTT:
   - Subscribe to `vacuum/conchita/#` and confirm messages arrive on dock/clean.

## Phase 3 — Automation Migration

1. Update all 4 duplex automations:
   - Replace `vacuum.roborock_de_261412235_s5` → `vacuum.conchita_local`
   - Keep all state machine logic (helpers, conditions, actions) identical.

2. Update `sensor.conchita_mirror_status` template:
   - Replace entity references from cloud entity to `vacuum.conchita_local`.

3. **Disable** (not delete) Xiaomi Home integration config entry for the S5 device.

4. **Test** full relay cycle: house_away → downstairs → carry → upstairs → carry back.

## Phase 4 — Mirror

1. Update `ConchitaVacuum` WebSocket module on stonypi:
   - Subscribe to `vacuum/conchita/map` MQTT topic for live map PNG tiles.
   - Update state subscription entity to `vacuum.conchita_local`.

2. Verify mirror shows live cleaning map when Conchita is running.

## Rollback

If anything goes wrong during Phase 1:
- Original firmware is not stored on device — must re-flash from Roborock official image.
- Valetudo does NOT modify hardware, only software — device is recoverable.
- Worst case: hold reset → re-pair to Xiaomi cloud → all automations fall back to cloud entity.
- Cloud entity name: `vacuum.roborock_de_261412235_s5` (keep in automations as comments for rollback).

## Timeline Estimate
- Phase 1: 1–2 hours (assuming eligible firmware)
- Phase 2: 30 min
- Phase 3: 30 min
- Phase 4: 30 min (requires stonypi SSH access)
