#!/bin/bash
cd ~
if [ -d socios/VirtualBoxVMs ]; then
        rm -rf socios/VirtualBoxVMs
fi

mkdir -p socios/VirtualBoxVMs

#Updating the folder permission
chmod -R 755 socios/VirtualBoxVMs

# Destination to save the VDI File 
DESTINATION=~/socios/VirtualBoxVMs
ISO=~/socios/image

target_disk=$(diskutil list | awk '/Apple_APFS/ {print $7}')

echo "$target_disk"
default_disk=$target_disk
parent_identifier="$(diskutil info /dev/$default_disk | grep "Part of Whole" | awk '{print $4}')"
whole_disk=/dev/"$parent_identifier"

# List available Guest OS on MAC Machine
echo "Available Guest OS on MAC Machine "
VBoxManage list ostypes | grep -i Fedora

echo "Enter the VM name: "
read name
MACHINENAME=Inception

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

diskutil list $whole_disk | grep -E "Linux Swap" | awk '{print $2$3$7}'
read -p "Please provide the last number you see in the Linux Swap identifier(eg:3 for $whole_disk"s3") :  " first

diskutil list $whole_disk | grep -E "Bios Boot Partition" | awk '{print $3$4$8}'
read -p "Please provide the last number you see in the Boot partition identifier(eg:4 for $whole_disk"s4") :  " sec

diskutil list $whole_disk | grep -E "Linux Filesystem" | awk '{print $2$3$7}'
read -p "Please provide the last number you see in the first Linux filesystem identifier(eg:5 for $whole_disk"s5") :  " third
read -p "Please provide the last number you see in the seconnd Linux filesystem identifier(eg:6 for $whole_disk"s6") :  " fourth

#diskutil umount /dev/$disk_id
sudo  chmod  go+rw  $whole_disk"s"$first
sudo  chmod  go+rw  $whole_disk"s"$sec
sudo  chmod  go+rw  $whole_disk"s"$third
sudo  chmod  go+rw  $whole_disk"s"$fourth
sudo  chmod  go+rw  $whole_disk

read -p "Enter the name of your mac user:  " USER

#sudo chown $USER $whole_disk"s"$first
#sudo chown $USER $whole_disk"s"$sec
#sudo chown $USER $whole_disk"s"$third
#sudo chown $USER $whole_disk"s"$fourth


#Create Disk and connect Debian Iso
echo "Creating Virtual Hard Disk"
vboxmanage  internalcommands  createrawvmdk  -filename  $DESTINATION/$MACHINENAME/$MACHINENAME.vmdk -rawdisk  $whole_disk -partitions $first,$sec,$third,$fourth

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
VBoxManage setextradata "$MACHINENAME" GUI/ScaleFactor 1.0

echo "ISO image booted in Virtualbox.... Start setup process"
