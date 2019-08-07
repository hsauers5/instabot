sudo apt update
sudo apt install -y xvfb
sudo apt install -y python3
sudo apt install -y python3-pip
sudo pip3 install selenium
sudo pip3 install xvfbwrapper
sudo apt install -y firefox
sudo wget https://github.com/mozilla/geckodriver/releases/download/v0.24.0/geckodriver-v0.24.0-linux64.tar.gz
sudo tar xzf geckodriver-v0.24.0-linux64.tar.gz
sudo chmod +x geckodriver
sudo mv geckodriver /usr/local/bin/geckodriver
sudo fallocate -l 1.5G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
sudo sh -c 'echo "/swapfile swap swap defaults 0 0" >> /etc/fstab'
