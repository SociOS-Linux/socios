# Fix VirtualBox’s “Kernel Driver Not Installed” Error on a Mac


### ERROR:
 
<img src="https://i.ibb.co/rp7b41J/image-0.png" width="700px">

Solution:

-	Whether we are trying to set up a Linux VM the error is appearing because this is our Mac’s first time installing any Oracle products (like VirtualBox). You’ll need to give the piece of software explicit permission to access the computer. For this Error, we have found a solution kernel issue.


### Step 1: Updating the Security policy in MAC Machine

-	First, navigate to System Preferences by clicking the Apple icon on the top menu bar

<img src="https://i.ibb.co/wzw2Hkn/image-1.png" width="700px">

-	Select the “System Preferences” button. 

<img src="https://i.ibb.co/BnByDw6/image-2.png" width="700px">

-	From there, click the “Security and Privacy” option.

-	Under the “General” tab, there should be text near the bottom that says, “System Software from Developer ‘Oracle America, Inc.’ Was Blocked from Loading.”


<img src="https://i.ibb.co/Qj9XmxL/image-3.png" width="700px">

-	The installation will now complete successfully

<img src="https://i.ibb.co/nD2Cdzk/image-4.png" width="700px">
