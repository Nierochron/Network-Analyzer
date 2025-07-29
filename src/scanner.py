import subprocess
import re

class NetworkScanner:
    def __init__(self):
        self.networks = []

    def scan(self):
        self.networks = []
        result = subprocess.run(
            ['netsh', 'wlan', 'show', 'networks', 'mode=bssid'],
            capture_output=True, text=True
        )
        output = result.stdout

        ssid = None
        auth = None
        encrypt = None
        channel = None

        for line in output.splitlines():
            ssid_match = re.match(r'\s*SSID\s+\d+\s+:\s+(.*)', line)
            auth_match = re.match(r'\s*Authentication\s+:\s+(.*)', line)
            encrypt_match = re.match(r'\s*Encryption\s+:\s+(.*)', line)
            channel_match = re.match(r'\s*Channel\s+:\s+(\d+)', line)
            bssid_match = re.match(r'\s*BSSID\s+\d+\s+:\s+([0-9A-Fa-f:]+)', line)
            signal_match = re.match(r'\s*Signal\s+:\s+(\d+)%', line)

            if ssid_match:
                ssid = ssid_match.group(1).strip()
            elif auth_match:
                auth = auth_match.group(1).strip()
            elif encrypt_match:
                encrypt = encrypt_match.group(1).strip()
            elif channel_match:
                channel = channel_match.group(1).strip()
            elif bssid_match and ssid:
                bssid = bssid_match.group(1).strip()
                # Find the next signal line
                signal = None
                signal_line = next((l for l in output.splitlines()[output.splitlines().index(line)+1:] if 'Signal' in l), None)
                if signal_line:
                    signal_match2 = re.match(r'\s*Signal\s+:\s+(\d+)%', signal_line)
                    if signal_match2:
                        signal = signal_match2.group(1).strip()
                self.networks.append({
                    'SSID': ssid,
                    'MAC Address': bssid,
                    'Signal Strength': signal if signal else 'N/A',
                    'Channel': channel if channel else 'N/A',
                    'Authentication': auth if auth else 'N/A',
                    'Encryption': encrypt if encrypt else 'N/A'
                })

    def get_networks(self):
        return self.networks