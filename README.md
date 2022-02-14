# AiroFile

host the selected folder on the localhost or the local network 

hosting_modes:

[1] (the default) for local host , 127.0.0.1

[2] for local network 

usermodes:

[user] (the default) only view files

[admin] view files , delete files and folders , create folders , run commands , open urls in the default browser 

syntax:

python3 App.py -p <path> -s <hosting_mode> -m <usermode>

example:
  
pyhton3 App.py -p / -s 2 -m admin
  

![screenshot](https://github.com/IceShell101/airofile/blob/main/screenshots/Screenshot%20from%202022-02-13%2021-42-47.png)

