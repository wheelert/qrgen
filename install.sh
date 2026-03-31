#!/bin/bash
#
# Check for prereqs
#


# zenity
if ! command -v zenity &> /dev/null; then
    echo -e "\e[33m you must install zenity (pacman -S zenity or apt install zenity) \e[0m"
	exit
fi

# python-qrcode
if ! command -v python -c "import qrcode" &> /dev/null; then
	echo -e "\e[33m python module (qrcode) needed \e[0m"
	echo -e "\e[33m install: pacman -S python-qrcode or apt install python-qrcode\e[0m"
	echo -e "\e[33m \tor via pip install qrcode\e[0m"
	exit
fi

# python-pillow
if ! command -v python -c "import pillow" &> /dev/null; then
	echo -e "\e[33m python module (pillow) needed\e[0m"
	echo -e "\e[33m install: pacman -S python-pillow or apt install python-pillow\e[0m"
	echo -e "\e[33m \tor via pip install pillow\e[0m"
	exit
fi



if zenity --question --text="Install QRGen?"; then


APPDIR=$HOME/.local/share/QRGen

(
	echo "10"
	echo "#Checking for previous versions"
	sleep 2
	if [ -d "$APPDIR" ]; then
	echo "20"
	echo "#removing older version files"
	    rm -rf $APPDIR
	    rm $HOME/.local/share/applications/QRGen.desktop
	fi
	  sleep 2
	 echo "50"
	 echo "#Installing QRGen"
	mkdir $APPDIR
	cp qrgen.py $APPDIR
	cp qrcode.ui $APPDIR
    cp default.png $APPDIR

	cp QRGen.desktop $HOME/.local/share/applications/
	  sleep 2
	 echo "100"
	 echo "# Done!"
) | zenity --progress \
  --title="Installing QRGen" \
  --text="installing..." \
  --percentage=0 \
  --auto-close
  
 

else
    exit 1
fi