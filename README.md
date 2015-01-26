midi-transform
============

Transform MIDI files using Python. Uses [python-midi](https://github.com/vishnubob/python-midi) to handle midi files.


Download
===========

* [Windows build](https://docs.google.com/file/d/0B3A4M1pvdmsGRDB3NVBmbTR5WEE)
* [Linux build](https://drive.google.com/file/d/0B3A4M1pvdmsGZEFOT21mTVpveUE/view?usp=sharing)
* [Android APK](https://drive.google.com/file/d/0B3A4M1pvdmsGSHdTTXQzVkxwclk/view?usp=sharing)


Showcase
===========

Examples of the files produced by the script.

* [Inverse Brahms Symphony No. 3 in F major, Op. 90. Mov. I](https://www.youtube.com/watch?v=kfrJyiVtBUI)
* [Reverse Chopin Ballade No. 1 in G minor, Op. 23](https://www.youtube.com/watch?v=8sbFRNm7dDo)


Instructions
===========
```
Usage: python2 miditransform.py [input file] [output file]
Options:
  -l      , --log=<arg>                Write log to files.
  -i      , --invert                   Invert notes on pentagram.
  -r      , --reverse                  Reverse midi file (play backward).
  -c <arg>, --change_pitch=<arg>       Change pitch of midi file. The argument is the pitch change. E.g: -c 2.
  -t      , --test                     Test similarity of files after transformations.
  -h        --help                     Print usage and exit.
```

A Qt GUI is provided in "miditransform-gui.pyw". It can also be compiled for android using Kivy and Buildozer.

Requires
===========

* [Python](http://www.python.org/download/) (2.6 or 2.7)
* [PySide](http://qt-project.org/wiki/PySide) For the Qt GUI version.
* [PyGame](http://pygame.org) For the Qt GUI version.
* [Kivy](http://kivy.org) For Android version.

License
===========
midi-transform is released into the public domain by the copyright holders.