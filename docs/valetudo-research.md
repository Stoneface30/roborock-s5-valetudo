# Valetudo Research — Roborock S5

## Status: [~] FIRMWARE READY — UART FLASH PENDING (2026-05-04)

## Device
- Model: Roborock S5 (roborock.vacuum.s5)
- HA entity: `vacuum.roborock_de_261412235_s5` (Xiaomi cloud, still active)
- MAC: 50:EC:50:14:1A:64 (pre-flash MAC — may change post-flash)
- DHCP reservation: 192.168.0.89 (old reservation, stale — vacuum now leasing .202 dynamically)
- **Current IP: 192.168.0.202** (new DHCP lease as of 2026-05-04, still Xiaomi firmware)

## Firmware Version

**Original Xiaomi firmware:** `3.5.8_002034`
**Captured date:** 2026-05-03
**Root firmware built:** `v11_002034.pkg` (DustBuilder job j69f74e8396070, in `firmware/`)

## Root Eligibility Assessment

| Check | Status |
|-------|--------|
| Firmware ≤ v2034? | ✅ YES — exactly v2034 (3.5.8_002034) |
| Root eligible? | ✅ YES — DustBuilder method viable |
| Downgrade needed? | ✅ NO — already at ceiling |

> **DO NOT update Conchita via the Xiaomi app** — any OTA update will push past v2034 and permanently block root.

## Flash Method

### WiFi OTA — BLOCKED
DustBuilder submitted job, firmware built successfully. OTA flash failed: **Xiaomi cloud locked** on this device — the remote OTA trigger was rejected.

### UART Flash — REQUIRED
Physical access needed. CP2102 USB-UART adapter ordered.

```
Wiring:
  CP2102 TX → Conchita mainboard RX
  CP2102 RX → Conchita mainboard TX
  CP2102 GND → GND
  Baud: 115200
  Firmware: v11_002034.pkg
```

## Firmware Files (in `firmware/`)

| File | Purpose |
|------|---------|
| `v11_002034.pkg` | DustBuilder rooted firmware — ready to flash |
| `j69f74e8396070.id_rsa` | SSH private key (for post-flash root access) |
| `j69f74e8396070.id_rsa.pub` | SSH public key |
| `j69f74e8396070.ppk` | PuTTY format |
| `j69f74e8396070-keys.zip` | Key archive |
| `md5.txt` | Firmware checksum |
| `_buildflags.sh` | DustBuilder build config |

## Post-Flash Verification
```bash
# Verify Valetudo running
curl http://192.168.0.202/api/v2/robot/state

# SSH root access
ssh -i firmware/j69f74e8396070.id_rsa root@192.168.0.202
```

## References
- Valetudo: https://valetudo.cloud/pages/general/supported-robots.html
- DustBuilder: https://builder.dontvacuum.me/
- MQTT contract: `docs/mqtt-contract.md`
- Migration plan: `docs/migration-path.md`
