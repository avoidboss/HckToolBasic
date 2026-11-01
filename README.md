# aternos-port-hunter

Asynchronous Minecraft Server List Ping (`0x00`) scanner developed by **X**. Designed to identify unwhitelisted **Aternos** and **Minehut** instances running with `online-mode=false` or exposed BungeeCord backends.

### Features
- **Raw VarInt Packet Builder:** Zero overhead — builds raw Netty handshake packets without heavy external wrappers.
- **Offline-Mode Detection:** Filters out licensed servers and highlights cracked instances vulnerable to UUID spoofing.
- **JSON Dump Export:** Automatically saves active IP:Port combinations with player lists and server software versions.

### Usage
```bash
git clone [https://github.com/X/aternos-port-hunter.git](https://github.com/X/aternos-port-hunter.git)
cd aternos-port-hunter
pip install -r requirements.txt
python3 scanner.py --subnet 185.220.0.0/16 --threads 500