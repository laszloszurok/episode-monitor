# episode-monitor

## Installation

### From PyPI

```console
pipx install episode-monitor
```

### From source

```console
git clone https://github.com/laszloszurok/episode-monitor
cd episode-monitor
python -m build
pipx install dist/episode-monitor-0.0.1-py3-none-any.whl
```

## Usage

Frist run creates a config file on `$XDG_CONFIG_HOME/episode_monitor/config.yaml` (defaults to `~/.config/episode_monitor/config.yaml`).
The default config file:
```yaml
interval: 300
shows:
- The Simpsons
- Family Guy
- South Park
```
Without any parameters the script will run continously and poll the configured pages evry `interval` minutes.

```console
episode-monitor
```
If the `--once` flag is given to the script, it will run a check for the configured pages and exit.
```console
episode-monitor --once
```

Episode counts will be stored at `$XDG_STATE_HOME/episode_monitor/episode_counts.json` (`~/.local/state/episode_monitor/episode_counts.json` by default).

Logs will be stored at `$XDG_CACHE_HOME/episode_monitor/episode_log.txt` (`~/.cache/episode_monitor/episode_log.txt` by default).

## License

`episode-monitor` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
