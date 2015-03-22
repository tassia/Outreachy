import sys, os
from PyQt4 import QtCore, QtGui 
import paramiko

"""
A Qt client application to upload files via SSH.
Author: Tassia Camoes Araujo
License: GPLv3

Inspirated by:
http://stackoverflow.com/questions/25269608/pyqt-pushbutton-to-upload-file
http://www.blog.pythonlibrary.org/2012/10/26/python-101-how-to-move-files-between-servers/
"""

class SSHConnection(object):
    """
    Connect and transfer files over SSH using paramiko library
    """

    def __init__(self, host, username, password, port=22):
        """
        Initialize and setup connection
        """
        self.ssh = None
        self.isOpen = False
        self.transport = paramiko.Transport((host, port))
        self.transport.connect(username=username, password=password)

    def _openConnection(self):
        """
        Open a connection if not already open
        """
        if not self.isOpen:
            self.ssh = paramiko.SFTPClient.from_transport(self.transport)
            self.isOpen = True

    def push(self, local_path, remote_path = None):
        """
        Copie a file from the local host to the remote host user directory
        """
        self._openConnection()
        if not remote_path:
            remote_path = os.path.expanduser("~") +'/'+ os.path.basename(unicode(local_path))
        print 'Local path:', local_path
        print 'Remote path: ', remote_path
        self.ssh.put(local_path, remote_path)

    def close(self):
        """
        Close SSH connection
        """
        if self.isOpen:
            self.ssh.close()
            self.isOpen = False
        self.transport.close()


class UploadWindow(QtGui.QWidget):
    """
    Main application window
    """

    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.initLayout()
        self.initSignal()

    def initLayout(self):
        self.setGeometry(350, 300, 300, 300)
        self.setWindowTitle('Upload via SSH')

        self.serverLabel = QtGui.QLabel("Server:")
        self.serverEdit = QtGui.QLineEdit(self)

        self.userLabel = QtGui.QLabel("User:")
        self.userEdit = QtGui.QLineEdit(self)

        self.passwordLabel = QtGui.QLabel("Password:")
        self.passwordEdit = QtGui.QLineEdit(self)
        self.passwordEdit.setEchoMode(2)

        self.fileLabel = QtGui.QLabel("File:")
        self.fileEdit = QtGui.QLineEdit(self)

        self.fileButton = QtGui.QPushButton('Select', self)
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
        self.connect(self.quitButton, QtCore.SIGNAL('clicked()'), QtGui.qApp, QtCore.SLOT('quit()'))

    def selectFile(self):
        selectedFile = QtGui.QFileDialog.getOpenFileName(self, 'Select File', os.path.expanduser("~"))
        self.fileEdit.setText(selectedFilename)
        print 'Selected file'

    def upload (self):
        try: 
            ssh = SSHConnection(str(self.serverEdit.text()), str(self.userEdit.text()), str(self.passwordEdit.text()))
            ssh.push(self.fileEdit.text())
            print 'Uploaded file'
            ssh.close()
        except:
            print "Unexpected error: ", sys.exc_info()[1]

def main():
    app = QtGui.QApplication(sys.argv)
    mw = UploadWindow()
    mw.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
