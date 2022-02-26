#!/bin/bash
Server_name="socios_vm"
Disk_location="/tmp/socios/$Server_name.vdi"
Image_file="/tmp/socios/ubuntu.iso"

#Creating virtual machine
vboxmanage createvm --name $Server_name --ostype Ubuntu_64 --register
vboxmanage createhd --filename $Disk_location  --size 32000 --format VDI

#Memory & CPU configuration
vboxmanage modifyvm $Server_name --memory 4096
vboxmanage modifyvm $Server_name --vram 16
vboxmanage modifyvm $Server_name --graphicscontroller VMSVGA
vboxmanage modifyvm $Server_name --cpus 2

#Configuration of virtual hard_disk
vboxmanage storagectl $Server_name --name "SATA Controller" --add sata --controller IntelAhci
vboxmanage storageattach $Server_name --storagectl "SATA Controller" --port 0 --device 0 --type hdd --medium $Disk_location

#Configuration of ISO_image
vboxmanage storagectl $Server_name --name "IDE Controller" --add ide --controller PIIX4
vboxmanage storageattach $Server_name --storagectl "IDE Controller" --port 1 --device 0 --type dvddrive --medium $Image_file
