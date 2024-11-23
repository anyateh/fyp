#!/usr/bin/env bash

WLAN_INTERFACE=wlan0
DHCPCD_CONF=/etc/dhcpcd.conf
DHCPCD_CONF_BK=dhcpcd_backup.conf
echo "Backing up original $DHCPCD_CONF if any.." >&2
if [ -f "$DHCPCD_CONF" ];
then
	cp -v "$DHCPCD_CONF" "$DHCPCD_CONF_BK"
fi

echo "Inserting dhcpcd configs..."         >&2
echo -e "interface $WLAN_INTERFACE"        | sudo tee -a "$DHCPCD_CONF" >/dev/null
echo -e "\tstatic ip_address=192.168.4.1"  | sudo tee -a "$DHCPCD_CONF" >/dev/null
echo -e "\tnohook wpa_supplicant"          | sudo tee -a "$DHCPCD_CONF" >/dev/null

# Note that the following commands are configured
# specifically for Raspberry Pi.
sudo systemctl disable wpa_supplicant.service
sudo systemctl unmask  hostapd.service
sudo systemctl enable  hostapd.service
sudo systemctl stop    wpa_supplicant.service
sudo systemctl restart dhcpcd.service
sudo systemctl restart dnsmasq.service
sudo systemctl start   hostapd.service

echo "WLAN Access Point mode should be enabled.."                                       >&2
echo "Note that your Raspberry Pi can no longer connect to internet using WiFi anymore" >&2

# echo "A reboot is needed for changes to take effect."                                   >&2
# read -p "Reboot now? [Y/n] " res
# if [ "$res" != "n" ] && [ "$res" != "N" ];
# then
# 	systemctl reboot
# fi
