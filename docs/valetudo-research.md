# Valetudo Research — Roborock S5

## Device
- Model: Roborock S5 (roborock.vacuum.s5)
- HA entity: `vacuum.roborock_de_261412235_s5`
- MAC: 50:EC:50:14:1A:64
- DHCP reservation: 192.168.0.89 (configured 2026-05-02)

## Firmware Version
**Status: NOT YET CAPTURED**

Firmware must be read from entity attributes after vacuum reconnects to Xiaomi cloud.
Command to run once online:

```bash
curl -s -H "Authorization: Bearer $HA_TOKEN" \
  http://192.168.0.166:8123/api/states/vacuum.roborock_de_261412235_s5 \
  | python -c "import sys,json; d=json.load(sys.stdin); print(d.get('attributes',{}))"
```

Look for `firmware_version` in attributes. Record below once captured.

**Firmware version:** _TODO_
**Captured date:** _TODO_

## Root Eligibility Assessment

### Known Valetudo-supported S5 firmware ceiling
- DustBuilder root method: requires firmware **≤ v2034**
- Above v2034: root is blocked (Xiaomi patched the exploit)

### Assessment (fill in after firmware capture)
| Check | Status |
|-------|--------|
| Firmware ≤ v2034? | **Unknown** |
| Root eligible? | **Unknown** |
| Downgrade needed? | **Unknown** |

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
