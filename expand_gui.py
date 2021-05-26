#!/bin/python3
from PIL import Image
import math
import sys

from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QListWidget, QFileDialog, QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot

from functools import partial

def say_hi():
    print("hi")

def addFiles(listWidget):
    fileDiag = QFileDialog()
    fileDiag.setFileMode(QFileDialog.AnyFile)

    filenames = fileDiag.getOpenFileNames(None, "Select your gifs!", "", "GIF Files (*.gif)")
    print(filenames)
    for f in filenames[0]:
        listWidget.addItem(f)
    
def remFiles(listWidget):
    listItems = listWidget.selectedItems()
    for item in listItems:
        listWidget.takeItem(listWidget.row(item))

def convert(listWidget):
    for i in range(0, listWidget.count()):
        filename = listWidget.item(i).text()
        print("Converting " + filename)
        origGif = Image.open(filename) # open it
        frames = origGif.n_frames
        origWidth, origHeight = origGif.size
        newHeight = origHeight * math.ceil(frames/2)
        newWidth = origWidth*2

        # Create new png with right dimensions
        output = Image.new("RGB", (newWidth, newHeight), color=0)
        # go through each frame and add it to output
        yCoord = 0 # start at top
        xCoord = 0
        for i in range(0, frames):
            origGif.seek(i)
            output.paste(origGif, (xCoord, yCoord))
            if((i % 2) == 1): yCoord += origHeight # go to next one
            xCoord += (origWidth)
            xCoord %= newWidth
        # save this one with _expand.png
        print("Saved in " + filename.split('.')[0] + "_expand" + ".png")
        output.save(filename.split('.')[0] + "_expand" + ".png", "png")
    # Once that is done
    message = QMessageBox()
    message.setIcon(QMessageBox.Information)
    message.setText("Expansion is done!\nYou can find your new gifs in the same folder as the old ones.")
    message.setWindowTitle("Good News!")
    message.setStandardButtons(QMessageBox.Ok)
    message.exec()
    

def window():
    app = QApplication(sys.argv)
    widget = QWidget()

    textLabel = QLabel(widget)
    textLabel.setText("GIFS to expand:")

    mainVbox = QVBoxLayout()
    numFiles = 0
    fileList = QListWidget()

    mainVbox.addWidget(textLabel)
    mainVbox.addWidget(fileList)

    buttonHbox = QHBoxLayout()
    addFile = QPushButton("Add Files")
    addFile.clicked.connect(partial(addFiles, fileList))
    
    removeFile = QPushButton("Remove Selected")
    removeFile.clicked.connect(partial(remFiles, fileList))

    
    buttonHbox.addWidget(addFile)
    buttonHbox.addWidget(removeFile)

    mainVbox.addLayout(buttonHbox)

    convertButton = QPushButton("Expand!")
    convertButton.clicked.connect(partial(convert, fileList))
    
    mainVbox.addWidget(convertButton)
    
    widget.setLayout(mainVbox)
    widget.setGeometry(50, 50, 320, 200)
    widget.setWindowTitle("Will's GIF Expander")
    widget.show()
    #addFile(fileList)
    sys.exit(app.exec_())

if __name__ == '__main__':
    window()
