#!/bin/bash
#Automated script for create ing partition from APFS to Linux.
#Default we are created for 30 Gb for New virtualbox VM.

target_disk=$(diskutil list | awk '/Apple_APFS/ {print $7}')

echo "$target_disk"
default_disk=$target_disk
default_size='40g'

read -p "Click Yes to use the default disk for the partition, No to select custom disk (Yes\No):" choice

case "$choice" in
	Yes|yes|"") Input=1;;
	No|no) Input=0;;
	* ) { echo "Invalid option. Plesase select the correct option."; exit 1; };;
esac

if [ $Input == 1 ]
then
    echo "Resizing the APFS container for partition $default_disk $default_size"
    diskutil apfs resizeContainer $default_disk $default_size
else
    diskutil list
    echo "Provide the disk space want to use for the above list."
    read -p "Provide the disk space want to use for Linux OS:  " disk_input
    read -p "Provide the disk space want to allocate for Linux OS in GB(e.g:30g):  " size_input
    diskutil apfs resizeContainer "$disk_input" "$size_input"
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
