def name(): 
  return "OAM Plugin" 

def description():
  return "Tiles local aerial image dataset and upload them to OAM"

def version(): 
  return "Version 0.1" 

def qgisMinimumVersion():
  return "1.0"

def icon():
    return "icon.png"

def authorName():
  return "Tassia Camoes Araujo"

def classFactory(iface):
  from mainplugin import OAMPlugin
  return OAMPlugin(iface)
