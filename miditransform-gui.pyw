#!/usr/bin/env python
#Encoding: utf-8

#========================================================================================
# title           : midi-reverse-gui.pyw
# description     : Graphical interface for miditransform.py
# author          : CMRM.
# usage           : Open midi file and apply transformation.
# python_version  : 2.7
# license         : Public domain.
#========================================================================================

import sys
import pygame
import threading
import tempfile
import os
from miditransform import *
from PySide import QtCore, QtGui

# UI generated code.
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(284, 226)
        self.central_widget = QtGui.QWidget(MainWindow)
        self.central_widget.setObjectName("central_widget")
        self.verticalLayout_8 = QtGui.QVBoxLayout(self.central_widget)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.groups_layout = QtGui.QVBoxLayout()
        self.groups_layout.setObjectName("groups_layout")
        self.transform_pitch_layout = QtGui.QHBoxLayout()
        self.transform_pitch_layout.setObjectName("transform_pitch_layout")
        self.transform_group = QtGui.QGroupBox(self.central_widget)
        self.transform_group.setObjectName("transform_group")
        self.verticalLayout_5 = QtGui.QVBoxLayout(self.transform_group)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.none_radio = QtGui.QRadioButton(self.transform_group)
        self.none_radio.setChecked(True)
        self.none_radio.setObjectName("none_radio")
        self.verticalLayout_5.addWidget(self.none_radio)
        self.invert_radio = QtGui.QRadioButton(self.transform_group)
        self.invert_radio.setObjectName("invert_radio")
        self.verticalLayout_5.addWidget(self.invert_radio)
        self.revert_radio = QtGui.QRadioButton(self.transform_group)
        self.revert_radio.setObjectName("revert_radio")
        self.verticalLayout_5.addWidget(self.revert_radio)
        self.transform_pitch_layout.addWidget(self.transform_group)
        self.pitch_group = QtGui.QGroupBox(self.central_widget)
        self.pitch_group.setObjectName("pitch_group")
        self.verticalLayout_6 = QtGui.QVBoxLayout(self.pitch_group)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.change_pitch_box = QtGui.QCheckBox(self.pitch_group)
        self.change_pitch_box.setObjectName("change_pitch_box")
        self.verticalLayout_6.addWidget(self.change_pitch_box)
        self.pitch_value_spin = QtGui.QSpinBox(self.pitch_group)
        self.pitch_value_spin.setObjectName("pitch_value_spin")
        self.verticalLayout_6.addWidget(self.pitch_value_spin)
        self.transform_pitch_layout.addWidget(self.pitch_group)
        self.groups_layout.addLayout(self.transform_pitch_layout)
        self.preview_group = QtGui.QGroupBox(self.central_widget)
        self.preview_group.setObjectName("preview_group")
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.preview_group)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.play_button = QtGui.QPushButton(self.preview_group)
        self.play_button.setObjectName("play_button")
        self.horizontalLayout_2.addWidget(self.play_button)
        self.time_label = QtGui.QLabel(self.preview_group)
        self.time_label.setObjectName("time_label")
        self.horizontalLayout_2.addWidget(self.time_label)
        self.groups_layout.addWidget(self.preview_group)
        self.verticalLayout_8.addLayout(self.groups_layout)
        MainWindow.setCentralWidget(self.central_widget)
        self.menu_bar = QtGui.QMenuBar(MainWindow)
        self.menu_bar.setGeometry(QtCore.QRect(0, 0, 284, 21))
        self.menu_bar.setObjectName("menu_bar")
        self.menu_file = QtGui.QMenu(self.menu_bar)
        self.menu_file.setObjectName("menu_file")
        self.menu_help = QtGui.QMenu(self.menu_bar)
        self.menu_help.setObjectName("menu_help")
        MainWindow.setMenuBar(self.menu_bar)
        self.action_open = QtGui.QAction(MainWindow)
        self.action_open.setObjectName("action_open")
        self.action_save = QtGui.QAction(MainWindow)
        self.action_save.setObjectName("action_save")
        self.action_exit = QtGui.QAction(MainWindow)
        self.action_exit.setObjectName("action_exit")
        self.action_about = QtGui.QAction(MainWindow)
        self.action_about.setObjectName("action_about")
        self.menu_file.addAction(self.action_open)
        self.menu_file.addAction(self.action_save)
        self.menu_file.addAction(self.action_exit)
        self.menu_help.addAction(self.action_about)
        self.menu_bar.addAction(self.menu_file.menuAction())
        self.menu_bar.addAction(self.menu_help.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Midi-Transform", None, QtGui.QApplication.UnicodeUTF8))
        self.transform_group.setTitle(QtGui.QApplication.translate("MainWindow", "Transform", None, QtGui.QApplication.UnicodeUTF8))
        self.none_radio.setToolTip(QtGui.QApplication.translate("MainWindow", "No transform.", None, QtGui.QApplication.UnicodeUTF8))
        self.none_radio.setText(QtGui.QApplication.translate("MainWindow", "None", None, QtGui.QApplication.UnicodeUTF8))
        self.invert_radio.setToolTip(QtGui.QApplication.translate("MainWindow", "Mirror notes upside down.", None, QtGui.QApplication.UnicodeUTF8))
        self.invert_radio.setText(QtGui.QApplication.translate("MainWindow", "Invert", None, QtGui.QApplication.UnicodeUTF8))
        self.revert_radio.setToolTip(QtGui.QApplication.translate("MainWindow", "Revert notes to play backwards.", None, QtGui.QApplication.UnicodeUTF8))
        self.revert_radio.setText(QtGui.QApplication.translate("MainWindow", "Revert", None, QtGui.QApplication.UnicodeUTF8))
        self.pitch_group.setTitle(QtGui.QApplication.translate("MainWindow", "Pitch", None, QtGui.QApplication.UnicodeUTF8))
        self.change_pitch_box.setToolTip(QtGui.QApplication.translate("MainWindow", "Raise or lower all the notes.", None, QtGui.QApplication.UnicodeUTF8))
        self.change_pitch_box.setText(QtGui.QApplication.translate("MainWindow", "Change Pitch", None, QtGui.QApplication.UnicodeUTF8))
        self.pitch_value_spin.setToolTip(QtGui.QApplication.translate("MainWindow", "Values can be positive for higher pitch or negative for lower pitch.", None, QtGui.QApplication.UnicodeUTF8))
        self.preview_group.setTitle(QtGui.QApplication.translate("MainWindow", "Preview", None, QtGui.QApplication.UnicodeUTF8))
        self.play_button.setText(QtGui.QApplication.translate("MainWindow", "Play", None, QtGui.QApplication.UnicodeUTF8))
        self.time_label.setText(QtGui.QApplication.translate("MainWindow", "00:00", None, QtGui.QApplication.UnicodeUTF8))
        self.menu_file.setTitle(QtGui.QApplication.translate("MainWindow", "File", None, QtGui.QApplication.UnicodeUTF8))
        self.menu_help.setTitle(QtGui.QApplication.translate("MainWindow", "Help", None, QtGui.QApplication.UnicodeUTF8))
        self.action_open.setText(QtGui.QApplication.translate("MainWindow", "Open", None, QtGui.QApplication.UnicodeUTF8))
        self.action_save.setText(QtGui.QApplication.translate("MainWindow", "Save", None, QtGui.QApplication.UnicodeUTF8))
        self.action_exit.setText(QtGui.QApplication.translate("MainWindow", "Exit", None, QtGui.QApplication.UnicodeUTF8))
        self.action_about.setText(QtGui.QApplication.translate("MainWindow", "About", None, QtGui.QApplication.UnicodeUTF8))


class ControlMainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(ControlMainWindow, self).__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.registerEvents()
        self.fopen = ""

        # Start audio mixer.
        freq = 44100
        bitsize = -16
        channels = 2
        buffer = 1024
        pygame.mixer.init(freq, bitsize, channels, buffer)

        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        # Manual adjustments.
        self.setWindowIcon(QtGui.QIcon(os.path.join(base_path, 'resources', 'midi-transform-icon.png')))
        self.setMaximumSize(310, 310)
        self.ui.action_open.setShortcut("Ctrl+O")
        self.ui.action_save.setShortcut("Ctrl+S")
        self.ui.pitch_value_spin.setRange(-127, 127)
        self.play_icon = QtGui.QIcon(os.path.join(base_path, "resources", "play.png"))
        self.stop_icon = QtGui.QIcon(os.path.join(base_path, "resources", "stop.png"))
        self.ui.play_button.setIcon(self.play_icon)

    def transform(self, in_file, out_file):
        # Apply transformation to midi file.
        a = MidiFile()
        a.open(in_file)

        if self.ui.invert_radio.isChecked():
            a.invert()
        elif self.ui.revert_radio.isChecked():
            a.revert()

        if self.ui.change_pitch_box.isChecked():
            change = self.ui.pitch_value_spin.value()
            a.change_pitch(change)

        a.save(out_file)

    def playMusic(self, music_file):
        # Set slider.
        clock = pygame.time.Clock()
        try:
            pygame.mixer.music.load(music_file)
        except pygame.error:
            print "File %s not found! (%s)" % (music_file, pygame.get_error())
            return

        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            # Check if playback has finished.
            clock.tick(10)
            time = pygame.mixer.music.get_pos()/1000
            m, s = divmod(time, 60)
            self.ui.time_label.setText("%02d:%02d" % (m, s))

        # When finished.
        self.ui.time_label.setText("00:00")
        self.ui.play_button.setText("Play")
        self.ui.play_button.setIcon(self.play_icon)
        self.activateGui()

    def registerEvents(self):
        self.ui.action_open.triggered.connect(self.onOpen)
        self.ui.action_save.triggered.connect(self.onSave)
        self.ui.action_exit.triggered.connect(self.onExit)
        self.ui.action_about.triggered.connect(self.onAbout)
        self.ui.play_button.clicked.connect(self.onPlay)

    def deactivateGui(self):
        self.ui.none_radio.setDisabled(True)
        self.ui.invert_radio.setDisabled(True)
        self.ui.revert_radio.setDisabled(True)
        self.ui.change_pitch_box.setDisabled(True)
        self.ui.pitch_value_spin.setDisabled(True)

    def activateGui(self):
        self.ui.none_radio.setEnabled(True)
        self.ui.invert_radio.setEnabled(True)
        self.ui.revert_radio.setEnabled(True)
        self.ui.change_pitch_box.setEnabled(True)
        self.ui.pitch_value_spin.setEnabled(True)

    def onOpen(self):
        self.fopen, _ = QtGui.QFileDialog.getOpenFileName(self, "Open Midi file", "", "Midi File (*.mid)")
        if pygame.mixer.music.get_busy():
            self.stopPlay()

    def onSave(self):
        self.fsave, _ = QtGui.QFileDialog.getSaveFileName(self, "Save Midi file", "", "Midi File (*.mid)")
        self.transform(self.fopen, self.fsave)

    def onExit(self):
        self.close()

    def closeEvent(self, event):
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()
        event.accept()

    def onAbout(self):
        msgBox = QtGui.QMessageBox()
        msgBox.setWindowTitle("midi-transform")
        msgBox.setText("midi-transform Qt-Gui")
        msgBox.setInformativeText("Author: cmrm\n\nWeb: https://github.com/cmrm/midi-transform")
        msgBox.exec_()

    def startPlay(self):
        # Transform to temp file and play.
        temp_file = os.path.join(tempfile.gettempdir(), "temp.mid")
        self.transform(self.fopen, temp_file)
        t = threading.Thread(target=self.playMusic, args = (temp_file,))
        t.start()
        self.ui.play_button.setText("Stop")
        self.ui.play_button.setIcon(self.stop_icon)
        self.deactivateGui()

    def stopPlay(self):
        pygame.mixer.music.stop()
        self.ui.play_button.setText("Play")
        self.ui.play_button.setIcon(self.play_icon)
        self.activateGui()

    def onPlay(self):
        # Play preview.
        if self.fopen:
            if not pygame.mixer.music.get_busy():
                self.startPlay()
            else:
                self.stopPlay()
        else:
            msgBox = QtGui.QMessageBox()
            msgBox.setText("Open a file first.")
            msgBox.exec_()
   
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    mySW = ControlMainWindow()
    mySW.show()
    sys.exit(app.exec_())