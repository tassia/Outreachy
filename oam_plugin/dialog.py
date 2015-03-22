from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *

import sys, os
from PyQt4 import QtCore, QtGui
from connection import SSHConnection

class OAMDialog(QtGui.QDialog):
    """
    Main OAM plugin dialog
    """

    def __init__(self,parent,iface):
        QtGui.QDialog.__init__(self, parent) 
        
        self.iface = iface 
        self.parent = parent
        self.dlgBase = None

        self.initLayout()
        self.initSignal()

    def initLayout(self):
        self.setGeometry(350, 300, 300, 300)
        self.setWindowTitle('Upload via SSH')

        self.serverLabel = QtGui.QLabel('Server:')
        self.serverEdit = QtGui.QLineEdit(self)

        self.userLabel = QtGui.QLabel('User:')
        self.userEdit = QtGui.QLineEdit(self)

        self.passwordLabel = QtGui.QLabel('Password:')
        self.passwordEdit = QtGui.QLineEdit(self)
        self.passwordEdit.setEchoMode(2)

        self.fileLabel = QtGui.QLabel('Current layer:')
        self.fileEdit = QtGui.QLineEdit(self)
        try:
            layer_path = self.iface.activeLayer().dataProvider().dataSourceUri()
            self.fileEdit.setText(layer_path)
        except:
            print 'Failed to get layer path: ', sys.exc_info()[1] 

        self.fileButton = QtGui.QPushButton('Select another', self)
        self.uploadButton = QtGui.QPushButton('Upload', self)
        self.quitButton = QtGui.QPushButton('Quit', self)

        vBoxLayout = QtGui.QVBoxLayout()
        vBoxLayout.addWidget(self.serverLabel)
        vBoxLayout.addWidget(self.serverEdit)
        vBoxLayout.addWidget(self.userLabel)
        vBoxLayout.addWidget(self.userEdit)
        vBoxLayout.addWidget(self.passwordLabel)
        vBoxLayout.addWidget(self.passwordEdit)
        vBoxLayout.addWidget(self.fileLabel)
        vBoxLayout.addWidget(self.fileEdit)
        vBoxLayout.addWidget(self.fileButton)
        vBoxLayout.addWidget(self.uploadButton)
        vBoxLayout.addWidget(self.quitButton)

        self.setLayout(vBoxLayout)

    def initSignal(self):
        self.connect(self.fileButton, QtCore.SIGNAL('clicked()'), self.selectFile)
        self.connect(self.uploadButton, QtCore.SIGNAL('clicked()'), self.upload)
        self.connect(self.quitButton, QtCore.SIGNAL('clicked()'), self.closeDialog)

    def closeDialog(self):
        self.close()

    def selectFile(self):
        selectedFile = QtGui.QFileDialog.getOpenFileName(self, 'Select File', os.path.expanduser("~"))
        self.fileEdit.setText(selectedFile)
        print 'Selected file'

    def upload (self):
        try:
            ssh = SSHConnection(str(self.serverEdit.text()), str(self.userEdit.text()), str(self.passwordEdit.text()))
            ssh.push(self.fileEdit.text())
            print 'Uploaded file'
            ssh.close()
            self.fileEdit.setText('')
        except:
            print 'Unexpected error: ', sys.exc_info()[1]
