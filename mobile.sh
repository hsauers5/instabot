sudo apt update
sudo apt install -y openjdk-8-jdk

sudo wget https://dl.google.com/android/repository/sdk-tools-linux-4333796.zip
sudo unzip sdk-tools-linux-4333796.zip -d android-sdk
sudo mv android-sdk /opt/
export ANDROID_SDK_ROOT=/opt/android-sdk
sudo echo "export ANDROID_SDK_ROOT=/opt/android-sdk" >> ~/.bashrc
sudo echo "export PATH=$PATH:$ANDROID_SDK_ROOT/tools" >> ~/.bashrc

cd /opt/android-sdk/tools/bin
/opt/android-sdk/tools/bin/sdkmanager --update
/opt/android-sdk/tools/bin/sdkmanager --licenses
/opt/android-sdk/tools/bin/sdkmanager "system-images;android-25;google_apis;armeabi-v7a"

/opt/android-sdk/tools/bin/sdkmanager "emulator"
/opt/android-sdk/tools/bin/sdkmanager "platform-tools"
touch /home/ubuntu/.android/repositories.cfg
mkdir /opt/android-sdk/platforms
/opt/android-sdk/tools/bin/avdmanager -v create avd -f -n MyAVD -k "system-images;android-25;google_apis;armeabi-v7a" -p "/opt/android-sdk/avd"
