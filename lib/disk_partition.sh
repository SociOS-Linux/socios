#Automated script for create ing partition from APFS to Linux.
#Default we are created for 30 Gb for New virtualbox VM.

target_disk=$(diskutil list | awk '/Apple_APFS/ {print $7}')

read -P "Provide the disk space want to allocate for Linux OS in GB(e.g:30g):" $size

diskutil apfs resizeContainer $target_disk $size

disk=$(/dev/disk0)

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
