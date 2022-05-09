#!/bin/bash

echo "Do you want Uninstall VirtualBox & GDisk"

read -p "Click Yes to uninstall the Virtualbox & Gdisk, No to exist from the option (Yes\No):" choice

case "$choice" in
	Yes|yes|"") Input=1;;
	No|no) Input=0;;
	* ) { echo "Invalid option. Plesase select the correct option."; exit 1; };;
esac

if [ $Input == 1 ]
then
    echo "Uninstalling VirtualBox & GDisk"
    brew uninstall --cask virtualbox
	brew uninstall --cask gdisk
else
    echo "VirtualBox & GDisk are Available in Destination"
    exit
fi