# Booting a VM using MAC Physical Disk:

1. After all the partitions are done the Virtual Machine is created from the Virtual Box, the user is prompted for the Virtual machine name of their choice. The VM name is created with the date and time information, so even if they provide similar name by mistake a separate VM will get created.

```
cd ~
if [ -d socios/VirtualBoxVMs ]; then
        rm -rf socios/VirtualBoxVMs
fi

mkdir -p socios/VirtualBoxVMs
```
- At first, the script check for the required folder in the root. If not present, it created it and provides the permission along with it.

2. The user is prompted for the disk identifier which was created for storage just then. The ask has been simplified at its finest so that a user cannot get too confused which one to enter.

```
Please provide the last number you see in the Linux Swap identifier(eg:3 for $whole_disk"s3") 
```
-Mention the last number in the identifier, if an identifier "disk0s4" is shown give the number 4 and if "disk0s5" is given give 5

3. After the partition numbers are entered in, all the partitions are pointed to the vmdk file that is created for the virtual machine. The Mac physical disk is converted to storage space,swap and boot for Virtual Machine.

```
sudo  vboxmanage  internalcommands  createrawvmdk  -filename  "/User/username/vmname/linux.vmdk"  -rawdisk  /dev/disk0  -partitions  4,5,6,7
```

4. The Mac username is asked from the user for providing necessary permission to the VMDK file and all the partition.

5. The ISO image is loaded from the iso destination folder, and both the VMDK file and the ISO is attached to the Virtual Machine to Boot.

6. The Virtual Machine boots with Fedora Linux having the physical storage space and the Fedora ISO image 
