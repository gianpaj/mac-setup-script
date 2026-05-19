# Ubuntu Setup Script

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
