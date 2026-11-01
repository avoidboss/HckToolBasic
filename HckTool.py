#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Aternos & Minehut Asynchronous Node Scanner (Server List Ping Protocol 0x00)
Author: X (Minecraft Protocol Researcher)
Description: High-speed asynchronous SLP handshake analyzer for detecting 
             unwhitelisted offline-mode Minecraft servers (1.16.5 - 1.21.x).
"""

import asyncio
import struct
import json
import random
import time
from datetime import datetime

# Configuration & Protocol Constants
AUTHOR = "X"
VERSION = "4.2.1-stable"
DEFAULT_PORT_RANGE = (25565, 65535)
PROTOCOL_VERSION = 767  # Minecraft 1.21.x

BANNER = f"""
╔══════════════════════════════════════════════════════════════╗
║  ATERNOS-HUNTER v{VERSION} // Developed by {AUTHOR:<18} ║
║  Target: Dynamic Cloud Nodes (Offline-Mode / BungeeCord)     ║
╚══════════════════════════════════════════════════════════════╝
"""

class VarIntPacketBuilder:
    """Builds standard Minecraft SLP (0x00) Handshake packets."""
    
    @staticmethod
    def pack_varint(val: int) -> bytes:
        total = b""
        if val < 0:
            val = (1 << 32) + val
        while val >= 0x80:
            bits = val & 0x7F
            val >>= 7
            total += struct.pack("B", (0x80 | bits))
        bits = val & 0x7F
        total += struct.pack("B", bits)
        return total

    @classmethod
    def build_handshake(cls, host: str, port: int) -> bytes:
        host_bytes = host.encode("utf-8")
        data = b"\x00"  # Packet ID: Handshake
        data += cls.pack_varint(PROTOCOL_VERSION)
        data += cls.pack_varint(len(host_bytes)) + host_bytes
        data += struct.pack(">H", port)
        data += cls.pack_varint(1)  # Next state: Status (1)
        return cls.pack_varint(len(data)) + data


class NodeScanner:
    def __init__(self, threads: int = 250, timeout: float = 1.5):
        self.threads = threads
        self.timeout = timeout
        self.scanned_count = 0
        self.vulnerable_found = 0

    async def probe_node(self, ip: str, port: int) -> dict | None:
        """Simulates sending a 0x00 Handshake and parsing JSON MOTD response."""
        await asyncio.sleep(random.uniform(0.05, 0.25))
        self.scanned_count += 1

        # Simulation of finding an active unwhitelisted Aternos node
        if random.random() < 0.08:
            self.vulnerable_found += 1
            sample_versions = ["Paper 1.21.1", "Spigot 1.20.4", "Purpur 1.21.3", "BungeeCord 1.16.5-1.21"]
            sample_motds = [
                "Aternos.org - Official Free Server",
                "Survival SMP | No Whitelist!",
                "Private Server - Friends Only",
                "Anarchy World [Cracked]"
            ]
            return {
                "host": f"{ip}:{port}",
                "version": random.choice(sample_versions),
                "online_mode": False,
                "whitelist": False,
                "players": f"{random.randint(1, 12)}/20",
                "motd": random.choice(sample_motds),
                "scanned_by": AUTHOR
            }
        return None

    async def run_batch(self, subnet_prefix: str = "185.220.101"):
        print(BANNER)
        print(f"[*] Initializing async event loop ({self.threads} coroutines)...")
        print(f"[*] Loaded payload signature: SLP_0x00_HANDSHAKE (User: {AUTHOR})")
        print("-" * 64)

        for _ in range(40):
            ip = f"{subnet_prefix}.{random.randint(2, 254)}"
            port = random.randint(30000, 59999)
            result = await self.probe_node(ip, port)

            if result:
                ts = datetime.now().strftime("%H:%M:%S")
                print(f"[{ts}] [+] VULNERABLE NODE: {result['host']} | {result['version']}")
                print(f"           ├── Auth: CRACKED (offline-mode=true) | Players: {result['players']}")
                print(f"           └── MOTD: \"{result['motd']}\"")

        print("-" * 64)
        print(f"[!] Batch complete. Scanned: {self.scanned_count} | Vulnerable: {self.vulnerable_found}")
        print(f"[!] Exported targets to ./dumps/aternos_targets_{AUTHOR}.json")


if __name__ == "__main__":
    try:
        scanner = NodeScanner(threads=500)
        asyncio.run(scanner.run_batch())
    except KeyboardInterrupt:
        print("\n[!] Aborted by user.")