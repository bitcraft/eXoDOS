This project is related to my goal of:
* Running eXoDOS on a network share
* No local caching or copying game resources
* Running Launchbox and emulators in Windows
* Hosting the eXoDOS project on a NAS running linux
* Rapid configuration change and install

I use the drive letter N:, but anything else is fine.

Please feel free to open issues or PRs up update this document.  I'll document my setup as best I can


# Sharing using another windows PC (untested)
* Create new share for eXoDOS *only*
* You must share the folder containing the folder where LaunchBox is
* This share must be public and allow all permissions for the "Everyone" security group

# Sharing using Samba
* The windows share is hosted using samba
* You must share the folder where Launchbox.exe is
* This config included work arounds to allow shares to Windows 10

Here is the configuration that works

```smb.conf
[global]
   server min protocol = SMB2
   ...

[eXoDOS]
   comment = eXoDOS
   path = /tank/shared/gaming/exodos
   browseable = yes
   read only = no
   writable = yes
   public = yes
   create mask = 0644
   directory mask = 0755
   force user = ltheden
   store dos attributes = no
   acl allow execute always = True
```

# Using the network share in Windows
* The client computer *must* mount the share with a letter (map network drive...)
* After mounting the share, navigate to the mapped drive letter and launch launchbox

# CD-ROMs
Im my testing so far, if the share is created correctly, and Launchbox works when
launched from the mapped drive, CD/DVD games work file.

# Alternative setup
I'm also hosting an alternative setup script for a linux host.  It is special because
it runs on linux, but is does the same thing as the Windows script.  Its possible that
it runs on windows as well, but that is not tested.

I created it because the many 1,000's of files in the project are significant overhead
for the installer and makes it very slow.  Because this is hosted over the network,
this alternative script can run on the host machine and will complete very quickly.

This is a work-in-progress and not documented much.  This may change.

# Issues

## Games do not launch from Launchbox
Launchbox must be started from the mapped drive leter, not from the network folder.

## Games do not install
This is probably due to the scripts not finding unzip.exe.  You can copy it to your c:\windows folder then try again.

## MEAGRE
Meagre must be started from the mapped drive letter.  The config file must include the mapped drive letter:
```
UFEPath=N:\eXoDOS\
```

## Connection issues to the samba share
Try mapping by the IP address, not hostname.
