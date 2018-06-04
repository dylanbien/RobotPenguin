# RobotPenguinPi

This project is a game designed to teach the basics of computer programming to a young audience. It is meant to be ported to two Raspberry Pis. It is written in Kivy and Python. The control screen and display communicate with a server which mediates them and sends commands from the control screen to the display.

main.py and display.py both work as clients which communicate with the simpleserver.py; simpleserver.py works on localhost, so both display.py and main.py run on the same local machine. main.py and hardware.py are clients for hardwareserver.py as well. Hardware integration is still spotty. The UI can also be improved. main.py could use some graphical work, and display.py's methods which determine the enemy's movement need work as well. surfacedev is the most recent branch, and should be referred to for the hardware code.

I would recommend connecting the Raspberry Pi to a Surface by ethernet using a USB to ethernet adapter. The Raspberry Pi cannot run the UI code without significant slowdowns. I recommend a crossover cable to get it working.
