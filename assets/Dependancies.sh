sudo apt-get update

sudo apt-get install python3.6

python3 -m pip install mutagen

pip3 install moviepy
pip3 install asset

pip3 install --upgrade google-api-python-client
pip3 install --upgrade google-auth-oauthlib google-auth-httplib2

pip3 install boto3
pip3 install botocore

pip3 install PyYAML
pip3 install 2to3
pip3 install oauth2client

pip3 install fonttools


if [[ "$OSTYPE" == "linux-gnu" ]]; then
  # identify -version [MKAE BASH FILE]
  # Linux
  sudo apt-get install ttf-mscorefonts-insta

  sudo apt install --reinstall man

  apt install wget
  sudo apt-get --purge remove imagemagick
  sudo apt autoremove

  sudo apt-get install build-essential
  sudo apt-get install checkinstall
  sudo apt-get install libgs-dev
  sudo apt-get install ghostscript

  mkdir ~/src
  cd ~/src

  wget http://www.imagemagick.org/download/releases/ImageMagick-6.7.7-10.tar.xz

  tar xf ImageMagick-6.7.7-10.tar.xz
  cd ImageMagick-6.7.7-10/

  sudo ./configure --with-gslib=yes
  sudo make
  sudo checkinstall
  sudo ldconfig

  identify -version

elif [[ "$OSTYPE" == "darwin"* ]]; then
  #Mac
  brew install imagemagick
  brew install ghostscript

else
  echo "Cant Detect OS"

fi

# Sorry wasnt sure about Win32 you Nerds
