
# Socios Documentation

### Socio Formula

Socios formula is a package definition written in Ruby.

It can be created with brew create <URL> where <URL> is zip or tarball. 

```bash
$ brew create https://github.com/SociOS-Linux/socios/archive/refs/tags/v1.3.6.tar.gz
```

Installed with brew install <formula>command  & debugged with brew install --debug.

```bash
$ brew install package-name

$ brew install package --debug
```

### Socios terminology

| Terms  | Description | Example |
| ------------- | ------------- | ------- |
| Formula  | Package definition uses the path  | /usr/local/Homebrew/Library/Taps/homebrew/homebrew-core/Formula/socios.rb | 
| Keg  | Installation prefix of a Formula  | /usr/local/Cellar/Socios/v1.3.6 |
| Cellar  | All Kegs are installed in path  | /usr/local/Cellar | 
| Tap  | Git repository of Formulae and/or commands  | /usr/local/Homebrew/Library/Taps/homebrew/homebrew-core |
| Bottle  | Pre-built Keg used instead of building from source  | qt-4.8.4.catalina.bottle.tar.gz | 

### An Introduction

Homebrew uses Git for downloading updates and contributing to the project.

Homebrew installs to the Cellar and then symlinks some of the installations into /usr/local 

Packages are installed according to their formulae, which live in 

/usr/local/Homebrew/Library/Taps/homebrew/homebrew-core/Formula/socios.rb

### Basic Instructions

Before we can start need to update the Repository. This turns our Homebrew installation into a Git repository.

Before submitting a new formula make sure our package

Check All our Acceptable Formula requirements.

Passes all brew audit --new-formula <formula> tests

Reference URL:  https://docs.google.com/document/d/1VOfEAn4aYBdE7l_Kc9hk-EsGQXKLoJiCCtY7q3skwwQ/edit?usp=sharing

In the above documentation, we have mentioned all Tag, version, Release, and formulas in detail.

### Install the formula

Open MAC machine terminal. Now we need to set a socios repository name with brew tap repo.

The brew tap command adds more repositories to the list of formulas that Homebrew tracks, updates, and installs from. Run the following command in the terminal.

```bash
$ brew tap SociOS-Linux/socios
```

<img src="https://i.ibb.co/fGSgKG4/image-0.png" width="700px">

Above command is initializing our package with the brew repository. Once the brew tap execution is completed.

We need to install the socios formula in the MAC machine using the below command.

```bash
$ brew install socios
```

<img src="https://i.ibb.co/bgR71xg/image-1.png" width="700px">

The Socios installation is completed. We can able to use the “socios” command in the MAC machine also we can check the version of our package using the below command.

```bash
$ socios –version
```

<img src="https://i.ibb.co/NxtzbdC/image-2.png" width="700px">
      
### Step1:  Install virtual box in MAC machine with the latest version

Once we verified with Socios version. We can start to install Virtual Box and Download the Ubuntu ISO image on the MAC machine.

In this function, we have added the Virtualbox installation commands and ISO image downloading command in the script file.
```bash
$ socios init
```

Drive details: We have created a separate drive for the Ubuntu iso image and updated the ImageID and ISO ImageURL in the Image script file 

Mail ID:      socios.setup@gmail.com
Password: Arya143$

<img src="https://i.ibb.co/fYJ2fzy/image-3.png" width="700px">

Reference Documentation: https://docs.google.com/document/d/1PQFOSeFuEH0rISVxM-Hw60s8AGVopTlQEdAWVg_IkFA/edit?usp=sharing

### Step2:  Create Virtual Machine in Virtual Box & Booting the ISO image in Virtual box

We can able to check the VirtualBox image in Launchpad

<img src="https://i.ibb.co/C2bkFQq/image-4.png" width="700px">

Open the Terminal, Now we need to run the below command to create a Virtual machine and Booting the ISO image file 

```bash
$ socios build
```

<img src="https://i.ibb.co/37Mcf8p/image-5.png" width="700px">

Once we execute the above command in the terminal we need to give some user inputs

Enter the VM Name: Socios-VM

Then press enter, here we can able to view the Disk space from the hard disk.

<img src="https://i.ibb.co/G74VQZr/image-6.png" width="700px">

Now we need to enter the Storage size in GB  Example: 10, After the size is given in GB, the script will convert the value into MB and proceed for the next command

Once the Virtual disk is created. We have associated the SATA Controller & IDE controller with the Virtual Machine

Then the ISO image is booted in VM and starts launching the Virtual machine in the virtual box

<img src="https://i.ibb.co/MgtKw21/image-7.png" width="700px">

Once the VirtualBox popup box will appear. We need to configure the Linux machine in a Virtual box.

<img src="https://i.ibb.co/pjbpHyp/image-8.png" width="600px">

Select the language option “ English” and click on “Install Ubuntu”

Click on Continue 
       
<img src="https://i.ibb.co/8BTzdbB/image-9.png" width="600px">	   

Click on Install Now

<img src="https://i.ibb.co/tM3P6PG/image-11.png" width="600px">

Popup screen will appear. Then click on continue.

<img src="https://i.ibb.co/BstRkyc/image-12.png" width="600px">

Follow the installation procedure and fill the Who are you Screen.

<img src="https://i.ibb.co/cJBkKnZ/image-13.png" width="600px">        

Once done with instruction - Click on continue

<img src="https://i.ibb.co/C2DVt2j/image-14.png" width="600px">  

<img src="https://i.ibb.co/yXDn3ty/image-15.png" width="600px">         

Click on Restart - Once restart will done.

<img src="https://i.ibb.co/17LfxGw/image-16.png" width="600px"> 
