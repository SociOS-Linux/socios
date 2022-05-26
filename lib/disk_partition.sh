#!/bin/bash
#Automated script for create ing partition from APFS to Linux.
#Default we are created for 30 Gb for New virtualbox VM.

target_disk=$(diskutil list | awk '/Apple_APFS/ {print $7}')

echo "$target_disk"
default_disk=$target_disk
default_size=50

read -p "Click Yes to use the default disk space for the partition, No to select custom disk space (Yes\No):" choice

case "$choice" in
	Yes|yes|"") Input=1;;
	No|no) Input=0;;
	* ) { echo "Invalid option. Plesase select the correct option."; exit 1; };;
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
sudo sgdisk -n 0:0:"$ENDSECTOR" -c 0:"UBUNTU" -t 0:0700 "$whole_disk"
sudo sgdisk -p "$whole_disk"

diskutil list




#!/bin/bash
cd ~
if [ -d ~/socios ]; then
        rm -rf ~/socios
fi
mkdir -p ~/socios
chmod -R 755 ~/socios

echo "Copying the ISO Image to Root Path"

cp /tmp/socios/ubuntu.iso ~/socios

# Destination to save the VDI File 
DESTINATION=~/socios/VirtualBoxVMs
ISO=~/socios

# List available Guest OS on MAC Machine
echo "Available Guest OS on MAC Machine "
VBoxManage list ostypes | grep -i Fedora

echo "Enter the VM name: "
read name
MACHINENAME=$name-$(date +%d-%m-%Y_%H-%M-%S)

#Creating virtual machine
echo "Creating a $MACHINENAME virtual machine"
vboxmanage createvm --name $MACHINENAME --ostype "Fedora_64" --register --basefolder $DESTINATION

#Set memory and network
echo "Setting up the memory and network for created $MACHINENAME virtual machine"
VBoxManage modifyvm $MACHINENAME --ioapic on
VBoxManage modifyvm $MACHINENAME --memory 4096
vboxmanage modifyvm $MACHINENAME --vram 128
VBoxManage modifyvm $MACHINENAME --nic1 nat
vboxmanage modifyvm $MACHINENAME --cpus 4
vboxmanage modifyvm $MACHINENAME --graphicscontroller VMSVGA

diskutil list

space_available=$(diskutil info / | grep "Container Free Space" | awk '{print $4$5}')
echo "You have $space_available of free space in your Mac machine"

diskutil list | grep "Microsoft Basic Data"
read -p "Please mention the identifier of the largest partition which is alloted for storage (Eg:$default_disk"s2", $default_disk"s3" ) :  " disk_id

diskutil umount /dev/$disk_id
sudo  chmod  go+rw  /dev/$disk_id

#Create Disk and connect Debian Iso
echo "Creating Virtual Hard Disk"
vboxmanage  internalcommands  createrawvmdk  -filename  $DESTINATION/$MACHINENAME/$MACHINENAME.vmdk  -rawdisk  /dev/$disk_id
read -p "Enter the name of your mac user:  " USER

#providing permission for vmdk file
sudo  chown  $USER  $DESTINATION/$MACHINENAME/$MACHINENAME*.vmdk

#Add Storage Controller to Virtual Machine
VBoxManage storagectl $MACHINENAME --name "SATA Controller" --add sata --bootable on --hostiocache on

#Attach Virtual Hard Disk to Virtual Storage Controller
VBoxManage storageattach $MACHINENAME --storagectl "SATA Controller" --port 0 --device 0 --type hdd --medium $DESTINATION/$MACHINENAME/$MACHINENAME.vmdk

#Add IDE Controller to Virtual Machine (To Later Connect ISO/CD/DVD)
VBoxManage storagectl $MACHINENAME --name "IDE Controller" --add ide --controller PIIX4

#Resize virtual machine (VDI and VHD)
#VBoxManage modifyhd "$DESTINATION/$MACHINENAME/$MACHINENAME.vdi" −−resize 40000
#This changes the size of the virtual hard drive to 40000 MB

#Attach ISO_image
VBoxManage storageattach $MACHINENAME --storagectl "IDE Controller" --port 1 --device 0 --type dvddrive --medium $ISO/Fedora.iso

#Start the Virtual Machine in Headless Mode
VBoxManage startvm $MACHINENAME

#Resize the Virtualbox in VM
VBoxManage setextradata "$MACHINENAME" GUI/ScaleFactor 2.0

echo "ISO image booted in Virtualbox.... Start setup process"
