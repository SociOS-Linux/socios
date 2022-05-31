# Disk partition - script explanation

1. The script first creates a free space with default size of 50 gb if the user's choice is to stick to default settings by giving a "Yes/yes". 

```
default_size=50
```

2. The user can also deny the default settings and can give a "No/no" which lets them decide how much space they need for SociOS.Either choice will create a free space for the sgdisk to do the rest.

```
read -p "Click Yes to use the default disk space for the partition, No to select custom disk space (Yes\No):" choice

case "$choice" in
	Yes|yes|"") Input=1;;
	No|no) Input=0;;
	* ) { echo "Invalid option. Please select the correct option."; exit 1; };;
esac
```

3. The below code creates the free space of desired size for Example if 40 is given in the disk0s2 disk having a total space of 250gb

```
$ diskutil apfs resizeContainer disk0s2 210g
```
by doing this we are allocating 210gb for disk0s2, so rest of it becomes the free space

4. The information about the free available space is given to user for them to conviniently choose the disk space from their Mac machine. 

```
$ space_available=$(diskutil info / | grep "Container Free Space" | awk '{print $4$5}')
```

5. After the free space is created, the sgdisk kicks in and creates 4 volumes
	
	a. Swap space - 2gb Larger than the Mac machine RAM size, Swap space is limited to 16gb even if the Mac machine possess larger memory.
	
	b. Boot partition space is 1mb.
	
	c. Two Linux Filesystem partition one with the size of 3 gb and other with the remaining space from the free space.
	
	d. Mac machine user password is needed to proceed with sgdisk for which user is asked for.
	
The sgdisk code explaination is given below:

```	
$ sudo sgdisk -n 0:0:$extra_ram -c 0:"SWAP" -t 0:8200 "$whole_disk"
$ sudo sgdisk -n 0:0:+2M -c 0:"Boot partition" -t 0:ef02  "$whole_disk"
$ sudo sgdisk -n 0:0:+3G -c 0:"Linux FS" -t 0:8300 "$whole_disk"
$ sudo sgdisk -n 0:0:"$ENDSECTOR" -c 0:"Linux FS" -t 0:8300 "$whole_disk"
```
**sudo**  - need root permission to access sgdisk
**-n**    - New partition
**0:0:+5G** - Partition number (adding 0 will select the default):First sector(adding 0 will select the default):how much memory you want from the free space (for 5 gb ----> +5G (G indicated gb))

**-c**	  - naming the partition, 0 indicates the default partition number and SWAP is the name of the partition

**0:8200** - partition format hexa code for default partition number (0), 8200 is the hex code for Swap partition format  
**whole disk** - its the whole disk disk0, disk1
**ef02** - is the hex code for Boot partition format
**8300** - is the hex code for Linux filesystem partition format

```
ENDSECTOR = $ sudo sgdisk -E "$whole_disk"
```

**-E**    - its the end of the largest available sector, so that every other free space gets allotted to FEDORA storage
```
$ sudo sgdisk -p "$whole_disk"
```
**-p**     - prints the partition of the whole disk i.e.(disk0)
	
