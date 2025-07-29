from collections import Counter


class NetworkAnalyzer:
    def __init__(self, networks):
        self.networks = networks

    def ssid_stats(self):
        ssids = [n["SSID"] for n in self.networks]
        return Counter(ssids)

    def vendor_stats(self):
        vendors = [n["MAC Address"][:8] for n in self.networks]
        return Counter(vendors)

    def strongest_network(self):
        nets = [n for n in self.networks if n["Signal Strength"].isdigit()]
        if not nets:
            return None
        return max(nets, key=lambda n: int(n["Signal Strength"]))

    def weakest_network(self):
        nets = [n for n in self.networks if n["Signal Strength"].isdigit()]
        if not nets:
            return None
        return min(nets, key=lambda n: int(n["Signal Strength"]))

    def open_networks(self):
        return [n for n in self.networks if "open" in n["Authentication"].lower()]