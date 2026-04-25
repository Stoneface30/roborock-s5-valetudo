# Roborock S5 / Valetudo Project — Claude Instructions

## Project Context
Risk-isolated experiments on Roborock S5 "Conchita" — root via DustBuilder, install Valetudo, get local MQTT vacuum map in HA without cloud. Spun off from F:\HA_CLAUDED on 2026-04-25.

## Parent / Siblings
- **Parent**: F:\HA_CLAUDED
- **Siblings**: MAGIC_MIRROR_CLAUDED (vacuum map module) · others
- **Memory collection**: `roborock_clauded`

## Scope
- Check firmware version (sensor.roborock_firmware_version) — eligibility for DustBuilder root requires ≤v2034
- If eligible: full root + Valetudo install
- If not: research alternative paths or accept cloud dependency
- Post-root: local MQTT map publishing → HA `vacuum.conchita_local` entity → mirror MMM-ConchitaVacuum module

## Hardware State
- IP: 192.168.0.89 | MAC: 50:EC:50:14:1A:64
- Currently: cloud-paired (Roborock + Xiaomi Home), docked at 100%
- DHCP reservation: MISSING (TODO in HA_CLAUDED network audit)

## Contract with HA_CLAUDED
- **Publishes to HA**: `vacuum.conchita_local` (post-root), MQTT `vacuum/conchita/map`, `vacuum/conchita/state`
- **Replaces (post-root)**: cloud-based `vacuum.roborock_*` entity

## Risk Posture
- This is the only vacuum in the house — DO NOT brick it without rollback path documented
- Save factory firmware backup before flashing anything
- Test in single zone first (kitchen) before full clean post-root

## Reference
Masterfile A6.4: "Check `sensor.roborock_firmware_version`. If ≤v2034 → DustBuilder root candidate. Side project."
