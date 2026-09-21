# Ubuntu Setup Script

## Automatic suspend

`install-autosuspend.sh` installs the activity checks and configuration in this directory.
It backs up `/etc/autosuspend.conf` and restarts autosuspend to load the settings.

```sh
sudo ./ubuntu/install-autosuspend.sh
```

The configuration checks activity every 30 seconds and waits 15 idle minutes
before suspending. CPU, GPU, network, connection, and job checks remain enabled.
The idle timeout applies to all activity, not just Codex.

### Codex activity

`codex-busy` connects to the existing app-server control socket. It checks all
loaded threads for active turns, including turns waiting for approval or input,
and reads persisted session update timestamps. It does not start a daemon,
resume threads, send prompts, or keep a subscription open.

A running turn blocks automatic suspend. A completed turn or new persisted
session update resets autosuspend's idle timer once. Sleep becomes eligible
about 15 minutes after activity stops, plus the 30-second polling granularity,
and only if the other checks are idle. There is no second grace timer.
Open but idle chats do not keep the server awake.

Remote clients attached to the configured app-server are included. Separate
app-server processes, standalone CLI sessions outside that daemon, and jobs on
other machines are outside this monitor's coverage.

The socket path is configured in `[check.Codex]`. The monitor stores only active
thread IDs and the latest persisted update time under `/run/autosuspend-codex/`.
It does not log chat content. API or state-read errors keep the server awake;
a missing daemon socket is treated as no active Codex work.

`python3-websockets` 15 or newer provides the local WebSocket transport.
Protocol reference: [Codex App Server](https://developers.openai.com/codex/app-server).

### Inspect and test

Inspect the installed check without changing its remembered activity:

```sh
sudo /usr/local/bin/autosuspend-codex-busy \
  --socket /home/gianpaj/.codex/app-server-control/app-server-control.sock \
  --inspect
journalctl -u autosuspend.service -n 50 --no-pager
```

Exit code 0 means busy or unavailable status; 1 means idle. Inspection never
suspends the machine. The monitor guards autosuspend, not explicit manual sleep.

Tests require the same WebSocket dependency and never call suspend:

```sh
cd ubuntu
python3 -m unittest -v test_codex_busy.py
```

## Essentials

```sh
sudo apt update && sudo apt install -y
```

## Add and check Swap

<https://www.digitalocean.com/community/tutorials/how-to-add-swap-space-on-ubuntu-22-04>

```sh
sudo swapon --show
```

## Tailscale

Go to tailscale -> Add device -> copy the auth script

```sh
curl -fsSL https://tailscale.com/install.sh | sh && sudo tailscale up --auth-key=XXX
```

### Setup Wake on LAN

```sh
ip link
sudo ethtool -s enp12s0 wol g
```

## Brew

```sh
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

## gogcli: Google Workspace in your terminal

```sh
brew install gogcli
```

### Auth

```sh
gog auth credentials ~/client_secret_yyy-xxx.apps.googleusercontent.com.json
gog auth add zzz@gmail.com --services gmail,calendar,drive,contacts,docs,sheets --remote --step 1
gog auth add zzz@gmail.com --remote --step 2 --auth-url "http://127.0.0.1:33387/oauth2/callback?..." --services gmail,calendar,drive,docs,sheets,contacts

# Set Key ring password

mkdir -p ~/.config/systemd/user/openclaw-gateway.service.d
chmod 700 ~/.config/systemd/user/openclaw-gateway.service.d

nano ~/.config/systemd/user/openclaw-gateway.service.d/gog-env.conf
```

Put this inside `gog-env.conf`

```sh
[Service]
Environment=GOG_KEYRING_BACKEND=file
Environment=GOG_KEYRING_PASSWORD=replace_with_your_real_password
Environment=HOME=/home/USERHOME
```

Then reload and restart:

```sh
systemctl --user daemon-reload
systemctl --user restart openclaw-gateway.service
# Verify
systemctl --user show openclaw-gateway.service --property=Environment | cat
```

```sh
# test
gog gmail search 'newer_than:7d' --max 10
```

## Docker

<https://docs.docker.com/engine/install/ubuntu/>

## Python

```sh
sudo apt install -y python3 python3-pip
# uv
```

## Cleanup

```sh
sudo apt autoremove
```

## Codex

For Codex to run on your always-on Ubuntu server (`gianrtx.local`), so you can start and continue work from its terminal, your Mac, or your phone.

| Piece              | Name and purpose                                                             | Configuration                                                                                     |
| ------------------ | ---------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------- |
| Ubuntu backend     | Codex app-server — runs agents and tools against Ubuntu’s files              | Currently v0.155.0, launched through the Mac’s SSH connection                                     |
| Ubuntu terminal    | Codex CLI — terminal interface to the backend                                | Run `codex`; `codex --remote unix://` explicitly connects to the shared server                    |
| Mac                | Codex desktop SSH connection — accesses Ubuntu’s backend over SSH            | Already configured as `gianrtx.local`; its Restart action successfully updated the running server |
| Phone              | Remote Control — connects a paired mobile client to a host                   | Documented route: pair with the Mac, then access its Ubuntu SSH projects                          |
| Persistent service | CLI-managed app-server daemon — manages the backend independently of the Mac | Optional migration for experimenting with direct phone access                                     |

Your working setup: Ubuntu CLI + Mac desktop app over SSH, both using the Ubuntu app-server v0.155.0.

For documented phone access: enable Remote Control in the Mac app’s connection settings and pair your phone. The Mac must stay awake and connected. [Official setup instructions](https://learn.chatgpt.com/docs/remote-connections)

For direct phone → Ubuntu access without the Mac: your CLI exposes experimental support. Disconnect the Mac and close active Codex sessions, stop the existing SSH-launched backend, then run:

```sh
# Launch the managed app-server with remote control enabled
codex app-server daemon bootstrap --remote-control

codex app-server daemon version

# Create and print a short-lived manual pairing code
codex remote-control pair
```

Use the resulting code if your phone app offers manual pairing.
