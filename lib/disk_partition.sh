#!/bin/bash
#Automated script for create ing partition from APFS to Linux.
#Default we are created for 30 Gb for New virtualbox VM.
echo "Available disk partitions in mac machine"
diskutil list

echo "Recommended swap space for disk partition is minimum 4GB, It will allocate automatically from the current disk space"

echo "checking the Apple_Apfs disk"
target_disk=$(diskutil list | awk '/Apple_APFS/ {print $7}')

echo "$target_disk"
default_disk=$target_disk
default_size=50

read -p "Enter Yes to use the default disk for the partition, No to select custom disk (Yes\No):" choice

case "$choice" in
      Yes|yes|y|Y|YES|"") Input=1;;
      No|no|n|N|NO|"") Input=0;;
      * ) { echo "Invalid option. Please select the correct option."; exit 1; };;
      No|no) Input=0;;
esac

if [ $Input == 1 ]
then
    echo "Resizing the APFS container for partition named New_volume $default_disk $default_size"
    total_space="$(diskutil info /dev/$default_disk | grep "Disk Size" | awk '{print $3}')"
    crct_default_space="$(echo $total_space - $default_size | bc)"
    sudo diskutil apfs resizeContainer "$default_disk" "$crct_default_space""g"
else
    diskutil list
    echo "Provide the disk space want to use for the above list."
  total_space="$(diskutil info /dev/$default_disk | grep "Disk Size" | awk '{print $3}')"
    read -p "Provide the disk space want to allocate for Linux OS in numerals(e.g:30 for 30GB):  " size_input
  if [[ $size_input -le 20 ]]; then
    read -p "Please Provide the disk space more than 20(e.g:30):  " size_input
    crct_space="$(echo $total_space - $size_input | bc)"
    diskutil apfs resizeContainer "$default_disk" "$crct_space""g"
  else
    crct_space="$(echo $total_space - $size_input | bc)"
    diskutil apfs resizeContainer "$default_disk" "$crct_space""g"
  fi
fi


#diskutil info /dev/disk1s2 | grep "Part of Whole" | awk '{print $4}'
disk_identifier="$(diskutil info /dev/$default_disk | grep "Part of Whole" | awk '{print $4}')"
whole_disk=/dev/"$disk_identifier"

echo "Installing SGdisk"
brew install gptfdisk

echo "SGDisk installation completed"

ram=$(system_profiler SPHardwareDataType | grep "Memory:" | awk '{print $2}')

if [[ $ram -le 12 ]]
then
    let ram=ram
  sum=$(expr $ram + 4)
  extra_ram="+""$sum""G"
  echo "Swap space of $sum"GB" is created for Socios"
  sudo sgdisk -n 0:0:$extra_ram -c 0:"SWAP" -t 0:0700 "$whole_disk"
else
    let ram=12
  sum=$(expr $ram + 4)
  extra_ram="+""$sum""G"
  echo "Swap space of $sum"GB" is created for Socios"
  sudo sgdisk -n 0:0:$extra_ram -c 0:"SWAP" -t 0:0700 "$whole_disk"
fi

echo "Rest of the space is allotted for the Socios Storage and booting process"
ENDSECTOR=$(sudo sgdisk -E "$whole_disk")
sudo sgdisk -n 0:0:"$ENDSECTOR" -c 0:"FEDORA" -t 0:0700 "$whole_disk"
sudo sgdisk -p "$whole_disk"

diskutil list
