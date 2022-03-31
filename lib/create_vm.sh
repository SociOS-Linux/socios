#!/bin/bash
Server_name="socios_vm"
Disk_location="/tmp/socios/$Server_name.vdi"
Image_file="/tmp/socios/ubuntu.iso"

# Download debian.iso
if [ ! -f ./debian.iso ]; then
    wget https://cdimage.debian.org/debian-cd/current/amd64/iso-cd/debian-9.9.0-amd64-netinst.iso -O debian.iso
fi

#Creating virtual machine
vboxmanage createvm --name $Server_name --ostype "Ubuntu_64" --register --basefolder `pwd`

#Set memory and network
VBoxManage modifyvm $MACHINENAME --ioapic on
VBoxManage modifyvm $MACHINENAME --memory 4096
vboxmanage modifyvm $Server_name --vram 128
VBoxManage modifyvm $MACHINENAME --nic1 nat
vboxmanage modifyvm $Server_name --cpus 4
vboxmanage modifyvm $Server_name --graphicscontroller VMSVGA

#Create Disk and connect Debian Iso
VBoxManage createhd --filename `pwd`/$MACHINENAME/$MACHINENAME.vdi --size 40000 --format VDI
VBoxManage modifyvm $MACHINENAME --boot1 dvd --boot2 disk --boot3 none

#Configuration of virtual hard_disk
VBoxManage storagectl $MACHINENAME --name "SATA Controller" --add sata --controller IntelAhci
VBoxManage storageattach $MACHINENAME --storagectl "SATA Controller" --port 0 --device 0 --type hdd --medium  `pwd`/$MACHINENAME/$MACHINENAME_DISK.vdi

#Configuration of ISO_image
VBoxManage storagectl $MACHINENAME --name "IDE Controller" --add ide --controller PIIX4
VBoxManage storageattach $MACHINENAME --storagectl "IDE Controller" --port 1 --device 0 --type dvddrive --medium `pwd`/debian.iso

#Enable RDP
VBoxManage modifyvm $MACHINENAME --vrde on
VBoxManage modifyvm $MACHINENAME --vrdemulticon on --vrdeport 10001

#Start the VM
VBoxHeadless --startvm $MACHINENAME
