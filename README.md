# RunScriptAtStart
Instructions for making a python script to autostart a boot (for raspberry pi)


# Step 1 - Your Python Script 

My example script was stored in the /home/cristian/CristiCode directory and named “scripty.py”. Obviously your script can be called something 
else but keep an eye on where it is referenced in the commands and text below.

# Step 2 - Create A Unit File

Next we will create a configuration file (aka a unit file) that tells systemd what we want it to do and when :Next we will create a 
configuration file (aka a unit file) that tells systemd what we want it to do and when :

 `sudo nano /lib/systemd/system/myscript.service`

 Add in the following text :

 `[Unit]
Description=My Script Service
After=multi-user.target

[Service]
Type=idle
ExecStart=/usr/bin/python /home/pi/myscript.py

[Install]
WantedBy=multi-user.target`
