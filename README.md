# airofile

host the selected folder on the localhost or the local network currently works only on linux

hosting_modes:
1 (the default) for local host , 127.0.0.1
2 for local network 

usermodes:
user (the default) only view files
admin view files , delete files and folders , create folders , run commands , open urls in the default browser 

syntax:
python3 App.py -p <path> -s <hosting_mode> -m <usermode>

 example:
 \npyhton3 App.py -p /home/bob/ -s 2 -m admin
