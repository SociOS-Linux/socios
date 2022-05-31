# Socios

This repository contains scripts connected with the SociOS Linux Homebrew installer which can be installed witht he following:
brew tap SociOS-Linux/socios-setup
brew install socios


## Socios Package

- Socios package contains the below files and directory
    1. ***socios*** – root bin command file.
    2. ***lib*** – directory contains with below script files
    3. ***install_virtualbox.scpt*** – this script file will be run by calling the check function
    4. ***image.sh*** – this script file is included in the above file as source
    5. ***create_vm.sh*** – this file will be run by calling the build function
    6. ***csrutil_status.sh*** – this file detect the SIP status and run it accordingly
    7. ***Disk_partition.sh*** -  this file will help to create the partation in disk space

## Socios bin command file
- This file contains the functions and arguments of socios such as build, check, help, and version. Currently, we have added 4 functions to this file.

***Install_virtualbox.scpt***
- This file helps us to check whether the virtual box is installed or not and prompts the question to the user to install the virtual box. Based on the user input the source script files will be run.

***Image.sh***
- This script helps us download the Socios image from the remote repositorysitory to the local directory `/tmp/socios` next to the installation of the VirtualBox. Currently, we have added google drive for testing purposes. In the future, we need to add the launchpad repositorysitory instead of Google cloud.

***create_vm.sh***
- We can able to create a virtual machine to boot our socios image in the physical partition. Temporarily we used default disk space of 30 GB and ubuntu image. We need to alter the script file once the Socios image

***csrutil_status.sh*** 
- This script file helps us to detect the SIP protection status in the current Mac OS and run based on results accordingly.
    Generally, SIP security protection technology has been implemented in El captain and later versions. 

    Some older version Mac OS’s does not have SIP – continue the next script
    SIP available and status is disabled – continue the next script
    SIP available and status is enabled – exit and shows the message to disable it with reference link

***Disk_partition.sh***
- The below script commands have been created to convert the APFS to a Linux partition. 
- This script can be run after disabling the SIP protection. We will add this script with the socios package once testing is completed. 
- In the script there are two methods avalable for doing the disk partition;
    1. Using the default disk space utility Like selecting the default disk "disk0s2" and the default size of 40GB will be used on disk partition.
    2. Other method is getting the disk input from the user by listing the available disk on the particular machine and get the custom disk sapce from the user input
