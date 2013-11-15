import pygtk
pygtk.require('2.0')
import gtk


class Caja_lista:

    def __init__(self, store, Nombre_columna):
        
        self.sw = gtk.ScrolledWindow()
        self.sw.set_shadow_type(gtk.SHADOW_ETCHED_IN)
        self.sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)        
        
        self.tV = gtk.TreeView(store)
        #self.tV.connect("row-activated", self.on_activated)
        self.tV.set_rules_hint(True)
        self.sw.add(self.tV)
        
        self.create_columns(self.tV, Nombre_columna)
        
        
    def create_columns(self, treeView, Nombre_columna):
    
        rendererText = gtk.CellRendererText()
        column = gtk.TreeViewColumn(Nombre_columna, rendererText, text=0)
        column.set_sort_column_id(0)    
        treeView.append_column(column)
        
        
        
		
		
