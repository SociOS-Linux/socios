# Socios
### Homebrew formula
The Homebrew tap/formula process is the combination of two Git hub repos. The first git hub repo contains the functionality package (socios) and the second repo has the homebrew formula with the ruby file (homebrew-socios).
### Homebrew Directory list
The homebrew package uses the below folder path to configuration.  
**Formula** – The package definition uses the path
`/usr/local/Homebrew/Library/Taps/homebrew/homebrew-core/Formula/socios.rb`

**Keg** - The installation prefix of a Formula uses the path 
`/usr/local/Cellar/Socios/v1.0.0`

**Cellar** - All Kegs are installed in path 
`/usr/local/Cellar`

**Tap** - A Git repository of Formulae and/or commands uses the path `/usr/local/Homebrew/Library/Taps/homebrew/homebrew-core`

### creating the Homebrew tap/formula
- git clone https://github.com/repo-url
- Switch into that cloned repo and place the script packages in that repo and start the upload it in git using the below commands in terminal

        git add .
        git commit -am "first commit"
        git push -u origin main
        git tag v1.0.0
        git push origin v1.0.0

- Create the second repository for the ruby formula file in git called “homebrew-socios”. Then clone that repo in the local computer using the git clone command.
- Switch into that new repo to create the formula 
- Then, we need to copy the compressed tar.gz file link from the git hub release and create the ruby file formula by running the below command in terminal

        brew create http://github.com/repo.tar.gz

- The above command will generate the default formula file in a ruby format for our socios packages (No need to edit this default formula).
- Copy the default formula to the new repository and open it with VI editor to add the below lines in it as shown in the picture.
    1. bin.install "socios"
    2. prefix.install Dir["lib"]
    3. 
- Then upload this file into the new git hub repository using the below commands

        git add .
        git commit -am "formula"
        git push -u origin main
- Once completed the above procedures, we can able to download and use our socios packages by using the below commands.

        brew tap Socios-linux/socios
        brew install Socios
- Then we can check the functions of Socios using the below commands

        socios --help
        socios --version

## Socios Package
- Socios package contains the below files and directory
    1. ***Socios*** – root bin command file.
    2. ***Lib*** – directory contains with below script files
    3. ***Install_virtualbox.scpt*** – this script file will be run by calling the check function
    4. ***Image.sh*** – this script file is included in the above file as source
    5. ***Create_vm.sh*** – this file will be run by calling the build function
    6. ***Csrutil_status.sh*** – this file detect the SIP status and run it accordingly

## Socios bin command file
- This file contains the functions and arguments of socios such as build, check, help, and version. Currently, we have added 4 functions to this file.

***Install_virtualbox.scpt***
- This file helps us to check whether the virtual box is installed or not and prompts the question to the user to install the virtual box. Based on the user input the source script files will be run.

***Image.sh***
- This script helps us download the Socios image from the remote repository to the local directory `/tmp/socios` next to the installation of the VirtualBox. Currently, we have added google drive for testing purposes. In the future, we need to add the launchpad repository instead of Google cloud.

***create_vm.sh***
- We can able to create a virtual machine to boot our socios image in the physical partition. Temporarily we used default disk space of 30 GB and ubuntu image. We need to alter the script file once the Socios image

***csrutil_status.sh*** 
- This script file helps us to detect the SIP protection status in the current Mac OS and run based on results accordingly.
    Generally, SIP security protection technology has been implemented in El captain and later versions. 

    Some older version Mac OS’s does not have SIP – continue the next script
    SIP available and status is disabled – continue the next script
    SIP available and status is enabled – exit and shows the message to disable it with reference link
    

   

