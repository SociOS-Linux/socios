#!/bin/bash
#Automated script for create ing partition from APFS to Linux.
#Default we are created for 30 Gb for New virtualbox VM.

target_disk=$(diskutil list | awk '/Apple_APFS/ {print $7}')

echo "$target_disk"
default_disk=$target_disk
default_size=40

read -p "Click Yes to use the default disk for the partition, No to select custom disk (Yes\No):" choice

case "$choice" in
	Yes|yes|"") Input=1;;
	* ) { echo "Invalid option. Plesase select the correct option."; exit 1; };;
esac

  No|no) Input=0;;
if [ $Input == 1 ]
then
    echo "Resizing the APFS container for partition named New_volume $default_disk $default_size"
    read -p "Provide the total space you find on the left side of the $target_disk in numerals(eg:100 for 100GB):  " total_space
    crct_default_space="$(echo $total_space - $default_size | bc)"
    diskutil apfs resizeContainer "$default_disk" "$crct_default_space""g" jhfs+ New_volume "$default_size""g"
else
    diskutil list
    echo "Provide the disk space want to use for the above list."
    read -p "Provide the APFS container identifier you want to use for Linux OS(e.g:disk0s2):  " disk_input
    read -p "Provide the total space you find on the left side of the provided identifier in numerals(eg:100 for 100GB):  " total_space
    read -p "Provide a name for the volume of your wish:  " name
    read -p "Provide the disk space want to allocate for Linux OS in numerals(e.g:30 for 30GB):  " size_input
    crct_space="$(echo $total_space - $size_input | bc)"
    diskutil apfs resizeContainer "$disk_input" "$crct_space""g" jhfs+ "$name" "$size_input""g"
fi

disk=$(/dev/"$disk_input")

sudo umount "$disk"

sed -e 's/\s*\([\+0-9a-zA-Z]*\).*/\1/' << EOF | gdisk $disk
  n # new partition
    # default partition to end of disk
    # default - start at beginning of disk 
$target_disk# GB boot parttion
8300# for converting HFS to Linux type
  p # print the in-memory partition table
  w # write the partition table
  q # and we're done
EOF