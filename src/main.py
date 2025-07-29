import time
import os
from scanner import NetworkScanner
from analyzer import NetworkAnalyzer
from tabulate import tabulate

try:
    from colorama import Fore, Style, init
    init(autoreset=True)
    COLORAMA = True
except ImportError:
    COLORAMA = False

def color_signal(signal):
    if not COLORAMA or not signal or not signal.isdigit():
        return signal
    s = int(signal)
    if s >= 70:
        return Fore.GREEN + signal + "%" + Style.RESET_ALL
    elif s >= 40:
        return Fore.YELLOW + signal + "%" + Style.RESET_ALL
    else:
        return Fore.RED + signal + "%" + Style.RESET_ALL

def highlight(text, color):
    if COLORAMA:
        return color + text + Style.RESET_ALL
    return text

def scan_animation():
    anim = "|/-\\"
    for i in range(10):
        print(f"\rScanning networks... {anim[i % len(anim)]}", end="", flush=True)
        time.sleep(0.1)
    print("\r" + " " * 30, end="\r")

def summary(networks):
    total = len(networks)
    open_nets = sum(1 for n in networks if "open" in n['Authentication'].lower())
    channels = [n['Channel'] for n in networks if n['Channel'] != "N/A"]
    most_common_channel = max(set(channels), key=channels.count) if channels else "N/A"
    return total, open_nets, most_common_channel

def main():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        scan_animation()
        scanner = NetworkScanner()
        scanner.scan()
        networks = scanner.get_networks()
        print(f"Scan time: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        if not networks:
            print("No networks found or parsing failed.")
        else:
            analyzer = NetworkAnalyzer(networks)
            print("\nExtra Analysis:")
            print(f"  Duplicate SSIDs: {dict(analyzer.ssid_stats())}")
            print(f"  Open networks: {[n['SSID'] for n in analyzer.open_networks()]}")
            strongest = analyzer.strongest_network()
            if strongest:
                print(f"  Strongest: {strongest['SSID']} ({strongest['Signal Strength']}%)")

            signals = [int(n['Signal Strength']) for n in networks if n['Signal Strength'].isdigit()]
            strongest = max(signals) if signals else None
            weakest = min(signals) if signals else None

            table = []
            for net in networks:
                sig = color_signal(net['Signal Strength'])
                row = [
                    net['SSID'],
                    net['MAC Address'],
                    sig,
                    net['Channel'],
                    net['Authentication'],
                    net['Encryption']
                ]
                if net['Signal Strength'].isdigit():
                    s = int(net['Signal Strength'])
                    if s == strongest:
                        row = [highlight(str(x), Fore.CYAN) for x in row]
                    elif s == weakest:
                        row = [highlight(str(x), Fore.MAGENTA) for x in row]
                table.append(row)
            headers = ["SSID", "MAC Address", "Signal", "Channel", "Auth", "Encryption"]
            print(tabulate(table, headers, tablefmt="fancy_grid"))

            total, open_nets, most_common_channel = summary(networks)
            print(f"\n{highlight('Summary:', Fore.YELLOW)}")
            print(f"  Total networks: {highlight(str(total), Fore.GREEN)}")
            print(f"  Open networks: {highlight(str(open_nets), Fore.RED)}")
            print(f"  Most common channel: {highlight(str(most_common_channel), Fore.CYAN)}")

        print("\nPress [Enter] to rescan, [Q] to quit.")
        choice = input().strip().lower()
        if choice == "q":
            break

if __name__ == "__main__":
    main()