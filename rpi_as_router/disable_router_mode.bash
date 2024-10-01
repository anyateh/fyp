#!/usr/bin/env bash

WLAN_INTERFACE=wlan0
DHCPCD_CONF=/etc/dhcpcd.conf

echo "Removing dhcpcd configs..."                 >&2
sudo sed -i "/^interface $WLAN_INTERFACE/d"       "$DHCPCD_CONF"
sudo sed -i '/^\tstatic ip_address=192.168.4.1/d' "$DHCPCD_CONF"
sudo sed -i '/^\tnohook wpa_supplicant/d'         "$DHCPCD_CONF"

# Note that the following commands are configured
# specifically for Raspberry Pi.
sudo systemctl disable hostapd.service
sudo systemctl mask    hostapd.service
sudo systemctl enable  wpa_supplicant.service
sudo systemctl stop    hostapd.service
sudo systemctl restart dhcpcd.service
sudo systemctl start   wpa_supplicant.service
sudo systemctl restart dnsmasq.service

echo "WLAN Access Point mode should be disabled.."                        >&2
echo "Note that your Raspberry Pi can now connect to internet using WiFi" >&2

# echo "A reboot is needed for changes to take effect."                     >&2
# read -p "Reboot now? [Y/n] " res
# if [ "$res" != "n" ] && [ "$res" != "N" ];
# then
# 	systemctl reboot
# fi
