# Booting a VM using MAC Physical Disk:

1. The script first searches for the folder VirtualBox/socios, it removes the folder if present, it creates the folder if not. This process occurs in root folder of every mac machine. After all the partitions are done the Virtual Machine is created from the Virtual Box, the VM name is fixed to "Inception".

```
cd ~
if [ -d VirtualBoxVMs/socios ]; then
        rm -rf VirtualBoxVMs/socios
fi

mkdir -p VirtualBoxVMs/socios
```
- At first, the script check for the required folder in the root. If not present, it created it and provides the permission along with it.

2. The user is prompted for the disk identifier which was created for storage just then. The ask has been simplified at its finest so that a user cannot get too confused which one to enter.

```
Please provide the last number you see in the Linux Swap identifier(eg:3 for $whole_disk"s3") 
```
-Mention the last number in the identifier, if an identifier "disk0s4" is shown give the number 4 and if "disk0s5" is given give 5
-The user is asked for the identifier for all the volumes

3. After the partition numbers are entered in, all the partitions are pointed to the vmdk file that is created for the virtual machine. The Mac physical disk is converted to storage space,swap and boot for Virtual Machine.

```
sudo  vboxmanage  internalcommands  createrawvmdk  -filename  "/User/username/Inception/Inception.vmdk"  -rawdisk  /dev/disk0  -partitions  4,5,6,7
```

4. The Mac username is asked from the user for providing necessary permission to the VMDK file and all the partition.

5. The ISO image is loaded from the iso destination folder, and both the VMDK file and the ISO is attached to the Virtual Machine to Boot.

6. The Virtual Machine boots with Fedora Linux having the physical storage space and the Fedora ISO image 
