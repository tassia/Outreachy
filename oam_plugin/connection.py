import os, paramiko

class SSHConnection(object):
    """
    Connect and transfer files over SSH using paramiko library
    Based on http://www.blog.pythonlibrary.org/2012/10/26/python-101-how-to-move-files-between-servers/
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
