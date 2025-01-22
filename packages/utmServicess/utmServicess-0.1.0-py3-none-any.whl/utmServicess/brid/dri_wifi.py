import subprocess
import sys

class dri_wifi_cfg:
    def __init__(self, ifname_ap, wifi_frequency, ssid_prefix, country_code, wpa_passphrase):
        self.ifname_ap = ifname_ap
        self.wifi_frequency = wifi_frequency
        self.ssid_prefix = ssid_prefix
        self.country_code = country_code
        self.wpa_passphrase = wpa_passphrase

    def calculate_wifi_channel(self, frequency):
        """Calculate wifi channel and band based on the frequency."""
        if 5160 <= frequency <= 5885:
            retval_band = "a"
            retval_channel = (frequency - 5000) // 5
        elif 2412 <= frequency <= 2472:
            retval_band = "g"
            retval_channel = (frequency - 2407) // 5
        else:
            print("ERROR! Frequency out of range!", file=sys.stderr)
            sys.exit(1)
        return retval_band, retval_channel

    def get_ap_interface_mac(self):
        """Retrieve the MAC address of the specified interface."""
        result = subprocess.run(["ip", "-brief", "link"], capture_output=True, text=True)
        for line in result.stdout.splitlines():
            if self.ifname_ap in line:
                return line.split()[2]
        return None

    def generate_hostapd_config(self, ssid, channel, band):
        config_content = f"""ctrl_interface=/var/run/hostapd
ctrl_interface_group=0
country_code={self.country_code}
interface={self.ifname_ap}
ssid={ssid}
hw_mode={band}
channel={channel}
macaddr_acl=0
auth_algs=1
ignore_broadcast_ssid=0
wpa=2
wpa_passphrase={self.wpa_passphrase}
wpa_key_mgmt=WPA-PSK
wpa_pairwise=TKIP
vendor_elements=dd1EFA0BBC0D00102038000058D6DF1D9055A308820DC10ACF072803D20F0100
rsn_pairwise=CCMP"""
        with open("/var/run/hostapd.conf", "w") as f:
            f.write(config_content)

    def setup_wifi(self):
        ap_if_mac = self.get_ap_interface_mac()
        if not ap_if_mac:
            print(f"ERROR! Unable to get MAC address for interface {self.ifname_ap}", file=sys.stderr)
            sys.exit(1)

        ssid = f"{self.ssid_prefix}#{ap_if_mac[12:14]}{ap_if_mac[15:17]}"

        # Set frequency band and channel from given frequency
        retval_band, retval_channel = self.calculate_wifi_channel(self.wifi_frequency)

        # Bring up the interface
        subprocess.run(["ifconfig", self.ifname_ap, "up"])

        # Generate hostapd configuration
        self.generate_hostapd_config(ssid, retval_channel, retval_band)

