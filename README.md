# CEEOEngineering: SPIKE Backpacks
![](https://github.com/Chenlu-Wu/CEEOEngineering--SPIKE-Backpacks/raw/master/webpic/getstart.png) 

Welcome to __MicroPython__ - a subset of python for small microprocessors. <br>
*please note - this site is for Tufts students only - and is not necessarily accurate, nor supported by the LEGO Group in any way.<br>

To get started, download the latest code versions:<br>


[![](https://github.com/Chenlu-Wu/CEEOEngineering--SPIKE-Backpacks/raw/master/webpic/Codeversions.png)  ](https://drive.google.com/drive/folders/15DpZ5mj2ZChWe8YYptyO587tFtHo1Eoi "![](https://github.com/Chenlu-Wu/CEEOEngineering--SPIKE-Backpacks/raw/master/webpic/Codeversions.png)  ")      [![](https://github.com/Chenlu-Wu/CEEOEngineering--SPIKE-Backpacks/raw/master/webpic/LabviewStandalones.png)](https://drive.google.com/drive/folders/166k8Vc7ZjFBHzkrO7dHIHEkHC7gKq4Na "![](https://github.com/Chenlu-Wu/CEEOEngineering--SPIKE-Backpacks/raw/master/webpic/LabviewStandalones.png)")

### Step 1:
Plug in your SPIKE Prime.

### Step 2:
Choose one of the three options to program SPIKE Prime.
1.  Any terminal emulator
2.  Python code
3.  My IDE (written in LabVIEW)

#### OPTION #1: TERMINAL IDE

> 1. Grab a terminal emulator
>
>		1). CoolTerm works on all platforms, including Pi<br>
>		2). Putty is good on windows<br>
>		3). screen command in Terminal on a unix operating system<br>
>
>2. Find your port
>
>		1). on mac, type ls /dev/tty.usbmodem<br>
>		2). on a pc, look in your device manager under serial to see what serial ports you have connected<br>
>		3). on pi, it will be something like ttyAMC0 - check in your /dev/ folder<br>
>3. Connect up to the right port at 115200 baud (no parity, 8 data bits, and 1 stop bit)
>		1).in Terminal - screen /dev/my_port_name 115200<br>
>		2). in software - hit connect (after setting up the settings in settings)
>
>4. you should get: 
>```
>MicroPython v1.9.3-1767-g1a6b45250 on 2019-05-23; LEGO Technic Large Hub with STM32F413xx
>Type "help()" for more information.
>>>>
>```

#### OPTION 2 PYTHON IDE

>Make sure you are running python 3.X. <br>
>Type python3 in your Terminal or Console - you should get something like<br>
>```
>function helloWorld(str) {
>	document.open();
>	document.write(str);
>	document.close();
>}
>
>helloWorld('<h1>Hello, World!</h1>');
>```
>and then use the exit() command to get back to the terminal prompt.
>
>Make sure that pySerial is installed by typing in the terminal prompt:
>```
>fredsComputer$ pip3 install pySerial
>```
>
>Select a serial port and hit 'Connect'. If the Spike is not listed in the ports, make sure it is on and connected.
>![](https://github.com/Chenlu-Wu/CEEOEngineering--SPIKE-Backpacks/raw/master/webpic/spiketerminal.png)
>
>Now you are ready to go, just follow the directions.
>
>![](https://github.com/Chenlu-Wu/CEEOEngineering--SPIKE-Backpacks/raw/master/webpic/spiketerminal2.png)
>
#### OPTION #3: LABVIEW IDE
>For this, you will need to download both the executable (Mac or PC only) and the >runtime engine (try running the  executable and it will walk you through what to do).<br>
>
>Unfortunately you will also have to tell Windows or Mac that you trust this software as >well.<br>
1. >		1. download uPython.zip
1. >		2. unzip the folder and drag the unzipped folder wherever you want to keep the app.
1. >		3. run uPython (app or .exe) and you should get something like the image below:
>				1. 1).First select the COM port in the upper left.
>				1. 2).click on the help button on the upper right and select your processor and look at all the examples - copy one
>				1. 3). click the green RUN button on the bottom of the screen
>				4). for more control, click on the REPL button and go to town.
>				5). The final button saves the file to your SPIKE Prime using the name in the upper left (uPythonX in this case)
