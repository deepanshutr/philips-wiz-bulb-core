# CLAUDE.md — philips-wiz-bulb-core

Local HTTP daemon for Philips WiZ smart bulbs.

## Conventions

- Python 3.11+
- All identifiers (subnet, broadcast addr, bulb IPs) come from env or
  `~/.config/philips-wiz-bulb/state.json`. **Never hard-code IPs in source.**
- WiZ uses JSON over UDP 38899. `getPilot` / `setPilot` / `getSystemConfig`.
- Tests use `pytest`; `asyncio_mode = "auto"`.
- Run `ruff check`, `mypy`, `pytest -v` before commit.

## Local state (gitignored)

- `~/.config/philips-wiz-bulb/state.json` — bulb registry (mode 0600)
- `~/.config/philips-wiz-bulb/state.env` — env overrides

## systemd

- User unit: `~/.config/systemd/user/philips-wiz-bulb-core.service`
  (copied from `systemd/philips-wiz-bulb-core.service`)
- `systemctl --user restart philips-wiz-bulb-core`
- `journalctl --user -u philips-wiz-bulb-core -f`

## Don't repeat

- Only `NoNewPrivileges=true`, `PrivateTmp=true`, `ProtectSystem=strict`,
  `ReadWritePaths=` work in user-scope systemd. The heavier `Protect*`
  knobs trip `status=218`.
- The WiZ JSON-over-UDP protocol is undocumented; field names are case-sensitive
  (`sceneId` not `scene_id`, `dimming` 10-100 not 0-100).
