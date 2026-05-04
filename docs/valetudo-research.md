# Valetudo Research — Roborock S5

## Status: ✅ FLASHED — VALETUDO LIVE (2026-05-04)

## Device
- Model: Roborock S5 (roborock.vacuum.s5)
- Old HA entity: `vacuum.roborock_de_261412235_s5` (cloud — to be removed)
- MAC: 50:EC:50:14:1A:64 (pre-flash Xiaomi firmware MAC)
- Old DHCP reservation: 192.168.0.89 (Xiaomi firmware)
- **Current IP: 192.168.0.202** (post-flash, Valetudo running)
- ⚠️ .202 was previously reserved for Nest Hello doorbell — check conflict and update DHCP reservations

## Firmware Version

**Original Xiaomi firmware:** `3.5.8_002034`
**Captured date:** 2026-05-03
**Flashed firmware:** `v11_002034.pkg` (DustBuilder rooted image, in `firmware/`)

## Flash — COMPLETED

### Files in `firmware/`
| File | Purpose |
|------|---------|
| `v11_002034.pkg` | DustBuilder rooted firmware package |
| `j69f74e8396070.id_rsa` | SSH private key (for root access) |
| `j69f74e8396070.id_rsa.pub` | SSH public key |
| `j69f74e8396070.ppk` | PuTTY format private key |
| `j69f74e8396070-keys.zip` | Key archive |
| `md5.txt` | Firmware checksum |
| `_buildflags.sh` | DustBuilder build configuration |

### SSH access (post-flash)
```bash
ssh -i F:/ROBOROCK_CLAUDED/firmware/j69f74e8396070.id_rsa root@192.168.0.202
```

### Verify Valetudo is running
```bash
curl http://192.168.0.202/api/v2/robot/state
```

## Root Eligibility Assessment (historical)

| Check | Status |
|-------|--------|
| Firmware ≤ v2034? | ✅ YES — exactly v2034 (3.5.8_002034) |
| Root eligible? | ✅ YES — DustBuilder method viable |
| Downgrade needed? | ✅ NO — already at ceiling, no downgrade required |

## HA Pre-Flash Backup
- Backup slug: `f5a79289`
- Label: "Pre-Valetudo-flash-2026-05-03"
- NAS WebDAV backup confirmed before flash

## Next Steps (now that Valetudo is live)

1. **Resolve .202 IP conflict** — Nest Hello doorbell was reserved at .202. Check if doorbell moved and update DHCP table.
2. **Create new DHCP reservation** for Conchita at .202 (verify MAC post-flash — may differ from old .89 MAC)
3. **SSH into Conchita** and verify Valetudo version + MQTT topic names
4. **Configure Valetudo MQTT** → point to Mosquitto broker at 192.168.0.166:1883 (mqtt_user)
5. **Run first map** — clean a room, verify map appears in Valetudo web UI at http://192.168.0.202
6. **Update HA** — remove Xiaomi Home integration, add MQTT vacuum entity (see mqtt-contract.md)
7. **Update duplex relay automations** — switch entity IDs to `vacuum.conchita_local`
8. **Update Mirror** — ConchitaVacuum module to subscribe MQTT map topic

## References
- Valetudo: https://valetudo.cloud/pages/general/supported-robots.html
- DustBuilder: https://builder.dontvacuum.me/
- MQTT contract: `docs/mqtt-contract.md`
- Migration plan: `docs/migration-path.md`
