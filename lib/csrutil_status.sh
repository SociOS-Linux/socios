#!/bin/bash

osvers_major=$(sw_vers -productVersion | awk -F. '{print $1}')
osvers_minor=$(sw_vers -productVersion | awk -F. '{print $2}')

if [[ ${osvers_major} -ne 10 ]]; then
  echo "Unknown Version of Mac OS X"
  source $Cellar/*/lib/install_virtualbox.scpt
fi

# Checks to see if the OS on the Mac is 10.11.x or higher.
# If it is not, the following message is displayed without quotes:

if [[ ${osvers_major} -eq 10 ]] && [[ ${osvers_minor} -lt 11 ]]; then
  echo "System Integrity Protection Not Available For `sw_vers -productVersion`"
  source $Cellar/*/lib/install_virtualbox.scpt
fi


if [[ ${osvers_major} -eq 10 ]] && [[ ${osvers_minor} -ge 11 ]]; then

# Checks System Integrity Protection status on Macs
# running 10.11.x or higher

  SIP_status=`/usr/bin/csrutil status | awk '/status/ {print $5}' | sed 's/\.$//'`


  if [ $SIP_status = "disabled" ]; then
      result=Disabled
      source $Cellar/*/lib/install_virtualbox.scpt
  elif [ $SIP_status = "enabled" ]; then
      result=Active
  fi
   echo "SIP status is $result. visit the link to disable it. https://developer.apple.com/documentation/security/disabling_and_enabling_system_integrity_protection" && exit 1
fi
