#!/bin/bash
MACHINENAME="socios_vm_test"
#Disk_location="/tmp/socios/$Server_name.vdi"
#Image_file="/tmp/socios/ubuntu.iso"

#Creating virtual machine
echo "Creating a $MACHINENAME virtual machine"
vboxmanage createvm --name $MACHINENAME --ostype "Ubuntu_64" --register --basefolder `pwd`

#Set memory and network
echo "Setting up the memory and network for created $MACHINENAME virtual machine"
VBoxManage modifyvm $MACHINENAME --ioapic on
VBoxManage modifyvm $MACHINENAME --memory 4096
vboxmanage modifyvm $MACHINENAME --vram 128
VBoxManage modifyvm $MACHINENAME --nic1 nat
vboxmanage modifyvm $MACHINENAME --cpus 4
vboxmanage modifyvm $MACHINENAME --graphicscontroller VMSVGA

diskutil list
echo "Select the partition disk to install the OS"

read -p "Provide the disk space want to use for Linux OS:  " disk_input

disk=$(/dev/"$disk_input")

#Create Disk and connect Debian Iso
# VBoxManage createhd --filename `pwd`/$MACHINENAME/$MACHINENAME.vdi --size 40000 --format VDI
VBoxManage internalcommands createrawvmdk -filename `pwd`/"$MACHINENAME"/$MACHINENAME.vmdk -rawdisk disk
VBoxManage modifyvm "$MACHINENAME" --boot1 dvd --boot2 disk --boot3 none

#Configuration of virtual hard_disk
VBoxManage storagectl "$MACHINENAME" --name "SATA Controller" --add sata --controller IntelAhci
VBoxManage storageattach $MACHINENAME --storagectl "SATA Controller" --port 0 --device 0 --type hdd --medium  `pwd`/$MACHINENAME/$MACHINENAME_DISK.vdi

#Configuration of ISO_image
VBoxManage storagectl $MACHINENAME --name "IDE Controller" --add ide --controller PIIX4
VBoxManage storageattach $MACHINENAME --storagectl "IDE Controller" --port 1 --device 0 --type dvddrive --medium `pwd`/ubuntu.iso

#Enable RDP
VBoxManage modifyvm $MACHINENAME --vrde on
VBoxManage modifyvm $MACHINENAME --vrdemulticon on --vrdeport 10001

#Start the VM
VBoxHeadless --startvm $MACHINENAME
