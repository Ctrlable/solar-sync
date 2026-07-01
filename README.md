# Solar Sync

**Lighting that follows the sun.** Solar Sync continuously tunes the brightness and
color temperature of your lights to the position of the sun at your location —
cool and bright through the working day, warm and gentle into the evening — so your
home keeps pace with your natural circadian rhythm. Manual changes are always
respected.

Solar Sync is a Ctrlable product for **Ctrlable Pro**.

---

## Why circadian lighting

Bright, cool-white light in the morning helps you feel alert; warm, dim light at
night helps you wind down. Solar Sync automates that arc for every room — no
schedules to maintain, no scenes to juggle. It tracks the sun and keeps your lights
where they should be, minute to minute.

## How it works

1. Solar Sync calculates the sun's elevation for your configured location and time.
2. On a fixed interval it derives a target **brightness** and **color temperature**
   (or RGB) from that elevation and smoothly transitions each light to it.
3. **Sleep mode** overrides the curve with a minimal, very warm setting for winding
   down.
4. **Manual control detection** notices when you — or an automation — change a light
   by hand and steps back, leaving that light alone until it is turned off and on
   again (or reset via a service call).

## Installation

Install **Solar Sync** from the **Ctrlable Store** on your appliance (sidebar → **Ctrlable Store** → Solar Sync → **Install**), then restart. A Solar Sync license (from the Ctrlable portal) is required to run it.

## What you get

For each configured area, Solar Sync creates four switches (shown here for an area
named `living_room`):

| Switch | Purpose |
| --- | --- |
| `switch.solar_sync_living_room` | Master on/off; exposes the live target settings as attributes. |
| `switch.solar_sync_sleep_mode_living_room` | Toggle sleep mode (warm + dim). |
| `switch.solar_sync_adapt_brightness_living_room` | Enable/disable brightness adaptation. |
| `switch.solar_sync_adapt_color_living_room` | Enable/disable color adaptation. |

## Configuration

Solar Sync can be configured entirely from the UI, or in YAML — the option names are
identical in both. A minimal YAML entry:

```yaml
solar_sync:
  lights:
    - light.living_room
```

> If you configure through the UI, a bare `solar_sync:` line must still be present in
> `configuration.yaml`.

### Most-used options

| Option | What it does | Default |
| --- | --- | --- |
| `lights` | Light entities this area controls. | `[]` |
| `interval` | How often to re-adapt, in seconds. | `90` |
| `transition` | Fade duration when settings change, in seconds. | `45` |
| `min_brightness` / `max_brightness` | Brightness range, in percent. | `1` / `100` |
| `min_color_temp` / `max_color_temp` | Warmest / coolest white, in Kelvin. | `2000` / `5500` |
| `prefer_rgb_color` | Adapt via RGB rather than color temperature when supported. | `false` |
| `sleep_brightness` / `sleep_color_temp` | Brightness and warmth used in sleep mode. | `1` / `1000` |
| `sunrise_time` / `sunset_time` | Pin a virtual sunrise/sunset (`HH:MM:SS`) instead of the real sun. | `none` |
| `brightness_mode` | Brightness ramp shape: `default`, `linear`, or `tanh`. | `default` |
| `take_over_control` | Hand a light back to manual control when something else changes it. | `true` |
| `detect_non_ha_changes` | Also detect changes made outside Ctrlable Pro. | `false` |
| `adapt_delay` | Wait this many seconds after a light turns on before adapting (reduces flicker). | `0` |

The full option set — virtual sunrise/sunset windows and offsets, custom brightness
ramps (`brightness_mode_time_dark` / `_light`), `intercept` / `multi_light_intercept`,
split turn-on commands, auto-reset timers, and more — is available in the options flow
and the configuration card.

## Services

| Service | Description |
| --- | --- |
| `solar_sync.apply` | Apply an area's current settings to its lights on demand (optionally to a subset, or to turn lights on). |
| `solar_sync.set_manual_control` | Mark or clear a light as manually controlled, per attribute if you like. |
| `solar_sync.change_switch_settings` | Adjust any option live from a script or automation (resets on restart unless saved). |

## Manual control

With `take_over_control` enabled, Solar Sync detects `light.turn_on` calls from other
sources and pauses adaptation for the affected light, firing a
`solar_sync.manual_control` event you can hook into. Enable `detect_non_ha_changes` to
also catch state changes that originate outside Ctrlable Pro.

```yaml
- alias: "Solar Sync: clear manual control after an hour"
  trigger:
    - platform: event
      event_type: solar_sync.manual_control
  variables:
    light: "{{ trigger.event.data.entity_id }}"
    sw: "{{ trigger.event.data.switch }}"
  action:
    - delay: "01:00:00"
    - condition: template
      value_template: "{{ light in state_attr(sw, 'manual_control') }}"
    - service: solar_sync.set_manual_control
      data:
        entity_id: "{{ sw }}"
        lights: "{{ light }}"
        manual_control: false
```

## Getting the best results

- **Group your mesh-network bulbs.** On Zigbee/Z-Wave, add a single light *group*
  (created in your radio software) to Solar Sync rather than many individual bulbs, so
  one broadcast adapts them all and keeps them in sync.
- **Match bulb models within an area.** Color temperature calibration varies between
  manufacturers; mixing models can make "identical" settings look different.
- **Tune transitions for stubborn bulbs.** Some lights dislike long transitions or
  simultaneous color+brightness changes — shorten `transition`, raise the adaptation
  frequency, or enable `separate_turn_on_commands`.

## Troubleshooting

Enable debug logging in `configuration.yaml`, reproduce the issue, then capture the
log:

```yaml
logger:
  default: warning
  logs:
    custom_components.solar_sync: debug
```

## License & credits

Solar Sync is a commercial, licensed Ctrlable product. It is built on the open-source
adaptive-lighting engine, used under the **Apache License 2.0**; the full license text
is included in [`LICENSE`](LICENSE).
