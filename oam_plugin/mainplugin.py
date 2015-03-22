from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *

from dialog import OAMDialog

# initialize Qt resources from file resources.py
import resources

class OAMPlugin:

  def __init__(self, iface):
    # save reference to the QGIS interface
    self.iface = iface

  def initGui(self):
    # create action that will start plugin configuration
    self.action = QAction(QIcon(":/plugins/oamplug/icon.png"), "OAM plugin", self.iface.mainWindow())
    self.action.setObjectName("Action")
    self.action.setWhatsThis("Configuration for OAM plugin")
    self.action.setStatusTip("This is status tip")
    QObject.connect(self.action, SIGNAL("triggered()"), self.run)

    # add toolbar button and menu item
    self.iface.addToolBarIcon(self.action)
    self.iface.addPluginToMenu("&OAM plugins", self.action)

    # connect to signal renderComplete which is emitted when canvas
    # rendering is done
    QObject.connect(self.iface.mapCanvas(), SIGNAL("renderComplete(QPainter *)"), self.renderOAM)

  def unload(self):
    # remove the plugin menu item and icon
    self.iface.removePluginMenu("&OAM plugins", self.action)
    self.iface.removeToolBarIcon(self.action)

    # disconnect form signal of the canvas
    QObject.disconnect(self.iface.mapCanvas(), SIGNAL("renderComplete(QPainter *)"), self.renderOAM)

  def run(self):
    # create and show a configuration dialog or something similar
    print "OAMPlugin: run called!"
    dlg = OAMDialog(self.iface.mainWindow(), self.iface) 
    dlg.exec_()

  def renderOAM(self, painter):
    # use painter for drawing to map canvas
    print "OAMPlugin: renderOAM called!"
