# MSI PRO B650M-P LED control on Linux

1. Install OpenRGB and tools:
  sudo apt-get install -y openrgb dmidecode i2c-tools

2. Load required kernel modules:
sudo modprobe i2c-dev
sudo modprobe i2c-nct6775    # for MSI super I/O chip

3. Make modules load at boot:
echo -e "i2c-dev\ni2c-nct6775" | sudo tee /etc/modules-load.d/openrgb.conf
echo -e "i2c-dev\ni2c-nct6775" | sudo tee /etc/modules-load.d/openrgb.conf

4. Install udev rules (so you don't need root every time):
# OpenRGB ships with udev rules
sudo cp /usr/lib/udev/rules.d/60-openrgb.rules /etc/udev/rules.d/
sudo udevadm control --reload-rules && sudo udevadm trigger

5. Add yourself to the i2c group:
sudo usermod -aG i2c $USER
# then log out and back in, or run: newgrp i2c

6. Run OpenRGB:
openrgb          # GUI mode
openrgb --list-devices   # list detected RGB devices
