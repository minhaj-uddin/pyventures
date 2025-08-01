import sys
from scapy.all import ARP, Ether, srp


def scan_network(ip_range: str):
    arp_request = ARP(pdst=ip_range)
    broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_packet = broadcast / arp_request

    print(f"Scanning network: {ip_range} ...\n")

    try:
        answered, _ = srp(arp_packet, timeout=2, verbose=0)
    except PermissionError:
        sys.exit(
            "Permission denied: run the script with sudo or Administrator privileges.")

    devices = []
    for sent, received in answered:
        devices.append({"ip": received.psrc, "mac": received.hwsrc})

    return devices


def display_devices(devices: list):
    if not devices:
        print("No devices found.")
        return

    print("Available devices in the network:\n")
    print(f"{'IP Address':<20}{'MAC Address'}")
    print("-" * 40)
    for device in devices:
        print(f"{device['ip']:<20}{device['mac']}")


def main():
    if len(sys.argv) != 2:
        print("Usage: python scanner.py <IP/CIDR>")
        print("Example: python scanner.py 192.168.1.0/24")
        sys.exit(1)

    ip_range = sys.argv[1]
    devices = scan_network(ip_range)
    display_devices(devices)


if __name__ == "__main__":
    main()
