# Valetudo Research — Roborock S5

## Device
- Model: Roborock S5 (roborock.vacuum.s5)
- HA entity: `vacuum.roborock_de_261412235_s5`
- MAC: 50:EC:50:14:1A:64
- DHCP reservation: 192.168.0.89 (configured 2026-05-02)

## Firmware Version

**Firmware version:** `3.5.8_002034`
**Captured date:** 2026-05-03
**Model:** `roborock.vacuum.s5`
**Source:** HA device registry `sw_version` via Xiaomi Home integration

## Root Eligibility Assessment

### Known Valetudo-supported S5 firmware ceiling
- DustBuilder root method: requires firmware **≤ v2034**
- Above v2034: root is blocked (Xiaomi patched the exploit)

### Assessment
| Check | Status |
|-------|--------|
| Firmware ≤ v2034? | ✅ **YES — exactly v2034 (3.5.8_002034)** |
| Root eligible? | ✅ **YES — DustBuilder method viable** |
| Downgrade needed? | ✅ **NO — already at ceiling, no downgrade required** |

> **Note:** v2034 is the last eligible firmware. Do NOT update Conchita via the Xiaomi app before flashing Valetudo — any OTA update will push past v2034 and permanently block root.

### If firmware > v2034
- Downgrade path exists but requires careful research
- Downgrade involves flashing older firmware via `miio` tool
- Risk: bricking if done incorrectly
- Document as blocked until safe downgrade path confirmed

## Root Procedure (DustBuilder method, if eligible)
1. Enable developer mode via Xiaomi Home app (usually done)
2. Download DustBuilder tool from GitHub
3. Create rooted firmware image targeting S5
4. Flash via `miio` tool over WiFi (no physical access needed)
5. Verify Valetudo is running: `curl http://192.168.0.89/api/v2/robot/state`

## References
- Valetudo supported devices: https://valetudo.cloud/pages/general/supported-robots.html
- DustBuilder: https://builder.dontvacuum.me/
- Roborock S5 root guide: community wiki
