# Enable & Disable System Integrity Protection (SIP) on Mac

### Step1:  Turn off System Integrity Protection (SIP) on Mac.

Click on the “Apple Icon” - Click on “about this MAC” then Click on “System reports”

Now click on the Software section we can able to the SIP status

<img src="https://i.ibb.co/rwYXYwM/image-0.png" width="700px">

Turn off the MAC machine or device

<img src="https://i.ibb.co/n6852fH/image-1.png" width="700px">

Now we need to enter recovery mode to edit system settings and disable System Integrity Protection on Mac. 

Hold down Command-R and press the Power button. Keep holding Command-R until the Apple logo appears.

<img src="https://i.ibb.co/nMtwsCW/image-2.png" width="700px">

Select the User and enter the password - Click on continue 

 Wait for OS X to boot into the OS X Utilities window.
      
<img src="https://i.ibb.co/7VD3vVb/image-3.png" width="700px">	  

Click on Utilities then select the terminal option. Now open Terminal and enter the  Below Command in terminal 

```bash
$ csrutil status
```

Check the status on SIP in MAC Machine if it is enabled - We need to Disable the SIP option on the Mac machine

```bash
$  csrutil disable
```       
	   
<img src="https://i.ibb.co/092mzBn/image-4.png" width="700px">

Now Click on the Quit terminal. Now we need to restart the Mac machine.

<img src="https://i.ibb.co/Jn5qQpY/image-5.png" width="700px">        

Once restart done. 


Open the terminal and check the status of the SIP option.

```bash
$ csrutil status
```

<img src="https://i.ibb.co/wr7qXyP/image-6.png" width="700px">

### Step2:  Turn on System Integrity Protection (SIP) on Mac.

Click on the “Apple Icon” - Click on “about this MAC” then Click on “System reports”

Now click on the Software section we can able to the SIP status

<img src="https://i.ibb.co/RDDTLc6/image-7.png" width="700px">

Turn off the MAC machine or device

<img src="https://i.ibb.co/n6852fH/image-1.png" width="700px">

Now we need to enter recovery mode to edit system settings and Enable System Integrity Protection on Mac. 

Hold down Command-R and press the Power button. Keep holding Command-R until the Apple logo appears.

<img src="https://i.ibb.co/nMtwsCW/image-2.png" width="700px">

Select the User and enter the password - Click on continue 

Wait for OS X to boot into the OS X Utilities window.
   
<img src="https://i.ibb.co/7VD3vVb/image-3.png" width="700px">   

Click on Utilities then select the terminal option. Now open Terminal and enter the  Below Command in terminal 

```bash
$ csrutil status
```

Check the status on SIP in MAC Machine if it is Disable - We need to Enable the SIP option on the Mac machine

```bash
$  csrutil Enable
```
   
<img src="https://i.ibb.co/092mzBn/image-4.png" width="700px">

Now Click on the Quit terminal. Now we need to restart the Mac machine.

<img src="https://i.ibb.co/Jn5qQpY/image-5.png" width="700px">         

Once restart Done. 

<img src="https://i.ibb.co/rGwrzrf/image-13.png" width="700px"> 

Open the terminal and check the status of the SIP option.

```bash
$ csrutil status
```
