# About the project

IKamand devices are no longer supported and their servers were shut down. This utility can be used to monitor state and start/stop cooking sessions on ikamand devices.

## How to use:

1) Install requirements

`pip install -r requirements.txt`


2) Make ikamand live again :)

`python3 ikamand_control.py <ip_address> <mode>`
- IKamand is probably broadcasting its existence over the network, but until we figure out how to find it, an IP address need to be retrieved from your router.
- Available modes:
  - `watch` - starts printing ikamands status every second
  - `start` - starts a cooking sessions with some default settings (TODO: make it configurable)
  - `stop`- stops current cooking session
