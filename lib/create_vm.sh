#!/bin/bash
cd ~

if [ -d socios/VirtualBoxVMs ]; then
        rm -rf socios/VirtualBoxVMs
fi

mkdir -p socios/VirtualBoxVMs

#Updating the folder permission 
chmod -R 755 socios/VirtualBoxVMs

# Destination to save the VDI File 
DESTINATION=socios/VirtualBoxVMs
ISO=socios/image

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
read -p "Enter the storage space for your virtual machine in GB in numerals:" gb
size=`expr $gb \* 1024`

#Create Disk and connect Debian Iso
echo "Creating Virtual Hard Disk"
VBoxManage createhd --filename $DESTINATION/$MACHINENAME/$MACHINENAME.vdi --size $size --format VDI --variant Standard

#Add Storage Controller to Virtual Machine
VBoxManage storagectl $MACHINENAME --name "SATA Controller" --add sata --bootable on

#Attach Virtual Hard Disk to Virtual Storage Controller
VBoxManage storageattach $MACHINENAME --storagectl "SATA Controller" --port 0 --device 0 --type hdd --medium $DESTINATION/$MACHINENAME/$MACHINENAME.vdi

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