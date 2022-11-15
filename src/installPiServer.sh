#!/bin/sh
cd ~
sudo apt update
sudo apt --yes install git python-smbus
sudo raspi-config nonint do_boot_behaviour B2
sudo raspi-config nonint do_i2c 0

#git clone https://github.com/Saint-Francis-Robotics-Team2367/yunServerSoftware.git

echo "#!/bin/sh
cd /home/pi/
while :
do
su pi -c 'python /home/pi/Documents/yunServerSoftware/src/pi/server.py' 
done" > startServer.sh

chmod a+x startServer.sh

echo "[Unit]
Description=Soccer bots
After=multi-user.target

[Service]
Type=idle
ExecStart=/home/pi/startServer.sh

[Install]
WantedBy=multi-user.target" | sudo tee /lib/systemd/system/soccerbots.service

sudo chmod 644 /lib/systemd/system/soccerbots.service
sudo systemctl daemon-reload
sudo systemctl enable soccerbots.service


echo -n "Enter Team Name? "
read name < /dev/tty
echo "[Main]
TeamName = $name" > /home/pi/Documents/yunServerSoftware/src/pi/config.ini
sudo raspi-config nonint do_hostname $name

echo "Rebooting"
sudo reboot
