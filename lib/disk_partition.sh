#!/bin/bash
#Automated script for create ing partition from APFS to Linux.
echo "Checking the Apple_Apfs disk identifier from the Mac Machine"
target_disk=$(diskutil list | awk '/Apple_APFS/ {print $7}')

echo "Available disk partitions in your mac machine"
diskutil list

echo "The default disk for resizing is the standard Apple_APFS Container disk1 is $target_disk"
default_disk=$target_disk
default_size=150

read -p "Ready to proceed with Re-Partitioning of default disk? (Yes\No):" choice

case "$choice" in
      Yes|yes|y|Y|YES|"") Input=0;;
      No|no|n|N|NO|"") Input=1;;
      * ) { echo "Invalid option. Please select the correct option."; exit 1; };;
      No|no) Input=0;;
esac

if [ $Input == 1 ]
then
    exit
   # echo "Resizing the APFS container for partition named New_volume $default_disk $default_size"
   #total_space="$(diskutil info /dev/$default_disk | grep "Disk Size" | awk '{print $3}')"
   # crct_default_space="$(echo $total_space - $default_size | bc)"
   # sudo diskutil apfs resizeContainer "$default_disk" "$crct_default_space""g"
else
    diskutil list
    space_available=$(diskutil info / | grep "Container Free Space" | awk '{print $4$5}')
    echo "You have $space_available of free space in your Mac machine"
    echo "Provide the disk space want to use from the above list."
    total_space="$(diskutil info /dev/$default_disk | grep "Disk Size" | awk '{print $3}')"
        read -p "Provide the disk space want to allocate for Linux OS in numerals(e.g:40 for 40GB):  " size_input
	if [[ $size_input -le 30 ]]; then
		read -p "Please Provide the disk space more than 30(e.g:40):  " size_input
		crct_space="$(echo $total_space - $size_input | bc)"
		diskutil apfs resizeContainer "$default_disk" "$crct_space""g"
	else
		crct_space="$(echo $total_space - $size_input | bc)"
		diskutil apfs resizeContainer "$default_disk" "$crct_space""g"
	fi
fi

brew install gptfdisk

#diskutil info /dev/disk1s2 | grep "Part of Whole" | awk '{print $4}'
parent_identifier="$(diskutil info /dev/$default_disk | grep "Part of Whole" | awk '{print $4}')"
whole_disk=/dev/"$parent_identifier"

ram=$(system_profiler SPHardwareDataType | grep "Memory:" | awk '{print $2}')

if [[ $ram -le 12 ]]
then
    let ram=ram
	sum=$(expr $ram + 2)
	extra_ram="+""$sum""G"
	echo "Swap space of $sum"GB" is created for Socios"
	sudo sgdisk -n 0:0:$extra_ram -c 0:"SWAP" -t 0:8200 "$whole_disk"
else
    let ram=12
	sum=$(expr $ram + 2)
	extra_ram="+""$sum""G"
	echo "Swap space of $sum"GB" is created for Socios"
	sudo sgdisk -n 0:0:$extra_ram -c 0:"SWAP" -t 0:8200 "$whole_disk"
fi

sudo sgdisk -n 0:0:+2M -c 0:"Boot partition" -t 0:ef02  "$whole_disk"

sudo sgdisk -n 0:0:+3G -c 0:"Linux FS" -t 0:8300 "$whole_disk"

echo "Rest of the space is allotted for the Socios Storage and booting process"
ENDSECTOR=$(sudo sgdisk -E "$whole_disk")
sudo sgdisk -n 0:0:"$ENDSECTOR" -c 0:"Linux FS" -t 0:8300 "$whole_disk"
sudo sgdisk -p "$whole_disk"

diskutil list
