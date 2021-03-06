Midi-Transform
============

Ever wondered how some musical piece would sound if played backwards? What would happen if you would play that piece with your sheet upside down? Midi-Transform lets you make this transformations to MIDI files. 

The transformations available are: Revert, Invert and Change pitch.


Download
===========

These are builds with graphical user interface. To use it by command line clone the repository.

* [Windows build](https://github.com/CarlosManuelRodr/Midi-Transform/releases/download/v1.0.2/miditransform-gui_v1.0.2.exe)
* [Linux build](https://github.com/CarlosManuelRodr/Midi-Transform/releases/download/v1.0.2/miditransform-gui_v1.0.2.tar.gz)
* [Android APK](https://github.com/CarlosManuelRodr/Midi-Transform/releases/download/v1.0.2/MidiTransform-1.0.2.apk)

Screenshots
===========
![Windows](extra/qt_screenshot.png?raw=true "Windows") 
![Linux](extra/qt_linux_screenshot.png?raw=true "Linux") 

![Android](extra/android_screenshot.png?raw=true "Android")


Transformations
===============
#### Revert
Revert note order. This transform the MIDI to play backwards.

![Revert example](extra/RevertTransform.png?raw=true "Revert example")

#### Invert
Invert the notes like in a mirror. In MIDI every note has a numerical value. For example, C5, G4, B4 and E5 have numeric values of 72, 67, 71 and 76 respectively. MIDI files can have note values ranging from 0 to 127, so the inversion is done by changing the values to: note_value = 127 - note_value. The new values will be 55, 60, 56 and 51 which correspond to G3, C4, G#3 and D#3. This transformation has the proporty that alters the chord structure from major to minor and viceversa.

![Invert example](extra/InvertTransform.png?raw=true "Invert example")

#### Pitch change
Change pitch of every note. Works by adding or sustracting the pitch change to the note values.

![Pitch change example](extra/PitchTransform.png?raw=true "Pitch change example")

Showcase
===========

Examples of the files produced by the script.

* [Inverse Brahms Symphony No. 3 in F major, Op. 90. Mov. I](https://www.youtube.com/watch?v=IyzKsCrA1ak)
* [Reverse Chopin Ballade No. 1 in G minor, Op. 23](https://www.youtube.com/watch?v=j0EiAq5D0MI)


Instructions
===========
To use it by command line.
```
Usage: python2 miditransform.py [input file] [output file]
Options:
  -l      , --log                      Write log to files.
  -i      , --invert                   Invert notes on pentagram.
  -r      , --revert                   Revert midi file (play backward).
  -c <arg>, --change_pitch=<arg>       Change pitch of midi file. The argument is the pitch change. E.g: -c 2.
  -t      , --test                     Test similarity of files after transformations.
  -h        --help                     Print usage and exit.
```

A Qt GUI is provided in "miditransform-gui.pyw". It can also be compiled for Android using Kivy and Buildozer.

Requires
===========

* [Python](http://www.python.org/download/) (2.6 or 2.7)
* [PySide](http://qt-project.org/wiki/PySide) For the Qt GUI version.
* [PyGame](http://pygame.org) For the Qt GUI version.
* [Kivy](http://kivy.org) For Android version.

License
===========
Midi-Transform is released into the public domain by the copyright holders.
