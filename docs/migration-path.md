# Migration Path — Cloud → Local (Valetudo)

**Status: Planning only. Execute after root is confirmed viable.**

## Overview

Current: Xiaomi Home HACS cloud integration → unreliable, drops offline, requires cloud auth.
Target: Valetudo on-device MQTT → local, no cloud dependency, instant response.

## Prerequisites Checklist

- [x] Firmware version captured: `3.5.8_002034` (2026-05-03)
- [x] Firmware ≤ v2034 confirmed — exactly v2034, root eligible, no downgrade needed
- [ ] Full HA backup taken and verified (NAS WebDAV backup confirmed working)
- [ ] Roborock app backup taken (map + settings saved to phone)
- [ ] DustBuilder rooted firmware image created and tested checksum
- [ ] Rollback procedure documented and understood

## Phase 1 — Root & Flash

1. **Backup**: HA → Settings → System → Backups → Create backup. Verify NAS backup received.
2. **Roborock app backup**: Export map + preferences.
3. **Create firmware**: DustBuilder → select S5 → add Valetudo → download image.
4. **Flash**: `miio flash --ip 192.168.0.89 --token <device_token> --firmware <image.pkg>`
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
