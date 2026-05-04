# MQTT Contract — Conchita Local Control

**Status: Design only — Valetudo flash pending (CP2102 UART adapter ordered). Implement after successful flash.**

Broker: `mqtt://192.168.0.166:1883` (Mosquitto addon on HA OS)
Auth: `mqtt_user` / see `.env`

## Topics

### Outbound (Valetudo → HA)

| Topic | Payload | Description |
|-------|---------|-------------|
| `vacuum/conchita/state` | `docked` \| `cleaning` \| `returning` \| `error` \| `idle` | Vacuum state (replaces HA cloud entity state) |
| `vacuum/conchita/battery` | Integer 0–100 | Battery level % |
| `vacuum/conchita/map` | Base64 PNG | Current floor map tile (for mirror live map) |
| `vacuum/conchita/zones` | JSON array | Named zone segment list `[{id, name, x, y}]` |
| `vacuum/conchita/error` | String or `""` | Error message, empty string when no error |

### Inbound (HA → Valetudo)

| Topic | Payload | Description |
|-------|---------|-------------|
| `vacuum/conchita/command` | `start` | Start full clean |
| `vacuum/conchita/command` | `stop` | Stop cleaning |
| `vacuum/conchita/command` | `return` | Return to dock |
| `vacuum/conchita/command` | `start_zone/ZONE_ID` | Start zone-specific clean |
| `vacuum/conchita/command` | `locate` | Play locate sound |

## HA Migration (post-root)

### Entities to replace
| Old (cloud) | New (MQTT) | Notes |
|-------------|------------|-------|
| `vacuum.roborock_de_261412235_s5` | `vacuum.conchita_local` | MQTT vacuum entity |
| `sensor.roborock_de_261412235_s5_battery_level_p_3_1` | Embedded in `vacuum.conchita_local` attributes | Battery from MQTT payload |

### HA MQTT vacuum config snippet (for `configuration.yaml` or package)
```yaml
mqtt:
  vacuum:
    - name: "Conchita Local"
      unique_id: conchita_local
      schema: legacy
      state_topic: "vacuum/conchita/state"
      command_topic: "vacuum/conchita/command"
      battery_level_topic: "vacuum/conchita/battery"
      battery_level_template: "{{ value }}"
      availability_topic: "vacuum/conchita/state"
      payload_available: "docked"
      payload_not_available: "error"
```

### Automation migration
All 4 duplex relay automations replace `vacuum.roborock_de_261412235_s5` with `vacuum.conchita_local`:
- `conchita_downstairs_auto` — `vacuum.start` → `mqtt.publish` on `vacuum/conchita/command` with `start`
- `conchita_carry_upstairs_reminder` — state trigger on `vacuum.conchita_local`
- `conchita_upstairs_start` — `vacuum.start` → `mqtt.publish`
- `conchita_carry_back_reminder` — state trigger on `vacuum.conchita_local`

### Template sensor migration
`sensor.conchita_mirror_status` — update `state` template to reference `vacuum.conchita_local` instead of `vacuum.roborock_de_261412235_s5`.

## Mirror Integration
Mirror module `ConchitaVacuum` (WebSocket) — subscribe to `vacuum/conchita/map` for live map tiles.
`ConchitaVrai` REST endpoint — update to read from `sensor.conchita_mirror_status` (already done).
