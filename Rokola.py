#!/usr/bin/env python

# example helloworld2.py

import pygtk
pygtk.require('2.0')
import gtk
import xmmsclient
import os
import Controller
import Caja_paraLista
import serial
import time


class PrimeraRokola:

    def __init__(self):
        
        # -------------Ventana y Propiedades-----------------
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.fullscreen()
        self.window.set_title("Rokola")
        self.window.connect("delete_event", self.delete_event)
        self.window.set_border_width(50)

        self.box_grande = gtk.HBox(False, 0)
        self.window.add(self.box_grande)
        #-----------------------------------------------------
        #-------------Ventana para Bloqueo--------------------
        self.muro = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.muro.fullscreen()
        self.muro.set_title("MURO")
        self.muro.set_border_width(50)
        image = gtk.Image()
        image.set_from_file("Pantalla.gif")
        image.show()
        self.muro.add(image)

        
        #------------------------------------------------------
        

        self.player = Controller.Controller({})
        self.player.stop()
        self.player.clear()
        
        self.id_agregar = None
        self.tam_pls = 0
        
        self.store_1 = self.create_model()
        self.store_2 = None
        self.store_3 = None
        
        self.lista_Izq = Caja_paraLista.Caja_lista(self.store_1, "Inicial")
        self.lista_Cen = Caja_paraLista.Caja_lista(self.store_2, "Artista")
        self.lista_Der = Caja_paraLista.Caja_lista(self.store_3, "Cancion")
        
   
        #agregar las cajas para lista al BOX
        self.box_grande.pack_start(self.lista_Izq.sw, True, True, 0)
        self.box_grande.pack_start(self.lista_Cen.sw, True, True, 0)
        self.box_grande.pack_start(self.lista_Der.sw, True, True, 0)
        
        # Creates a new button with the label "Button 1".
        self.button1 = gtk.Button("Agregar")
        # Now when the button is clicked, we call the "callback" method
        # with a pointer to "button 1" as its argument
        self.button1.connect("clicked", self.play_callback, "button agregar")
        
        self.lista_Izq.tV.connect("row-activated", self.artistas)
        self.lista_Cen.tV.connect("row-activated", self.canciones)
        self.lista_Der.tV.connect("row-activated", self.accion)
        self.box_grande.pack_start(self.button1, True, True, 0)
        
        self.window.show_all()
        
    def play_callback(self, widget, data):
        if self.id_agregar:
            if self.player.is_playing():
                self.player.add_idtopls(self.id_agregar)
            else:
                self.player.clear()
                self.player.add_idtopls(self.id_agregar)
                self.player.play_start()
                #self.player.play(self.tam_pls)     # el cero es el numero de la cacion
        
            self.tam_pls = self.tam_pls + 1
            print self.tam_pls
            print "Hello again - %s was pressed" % data
            self.id_agregar = None
            self.bloqueo()
            
        
    def delete_event(self, widget, event, data=None):
        gtk.main_quit()
        return False
        
    def create_model(self):
		
	Inicial = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", 
    "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M","N",
     "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
        
        store = gtk.ListStore(str)

        for Ini in Inicial:
            store.append([Ini])

        return store
    
        
    def artistas(self, widget = None, row = None, col = None):
        if widget != None:
            model = widget.get_model()
            text = model[row][0]
        else:
            text = None
		
        store = gtk.ListStore(str)
        store.clear()
        artist = self.player.get_av_artist_list()
        print "Buscando artistas con Inicial = %s " % text
        
        for art in artist:
            U = art["artist"]
            if U != None:
                if U[0] == text:
                    store.append([U])
                    
        self.lista_Cen.tV.set_model(store)
        
    def canciones(self, widget = None, row = None, col = None):
        if widget != None:
            model = widget.get_model()
            text = model[row][0]
        else:
            text = None
        
        store = gtk.ListStore(str, int)
        store.clear()
        artistmatch = self.player.create_a_coll(text)
            
        print artistmatch
        
        for art in artistmatch:
            U = art["title"]
            X = art["id"]
            print U
            print X
            if U != None:
                    store.append([U, X])
        
        self.lista_Der.tV.set_model(store)
        
    def accion(self, widget = None, row = None, col = None):
        print '----------acciones----------'
        if widget != None:
            model = widget.get_model()
            text = model[row][0]
            ids = model[row][1]
        else:
            text = None
        
        print text
        print ids
        
        self.id_agregar = ids
        
        
    def bloqueo(self):
        print '-----------para bloquear pantalla ------------'
        
        bit = 'B'
        self.muro.show_all()
        while gtk.events_pending():
            gtk.main_iteration(False)

        
        #limpiar la columnas despues de desbloqueo
        self.lista_Cen.tV.set_model(None)
        self.lista_Der.tV.set_model(None)
        
        #se define la entrada serial
        usbport = '/dev/ttyUSB0'
        ser = serial.Serial(usbport, 9600, timeout=1)
        
        
        cont = 0
        while bit != 'h':
            
            bit = ser.read(1)
            print cont
            cont =  cont + 1
        
        self.muro.hide_all()
        while gtk.events_pending():
            gtk.main_iteration(False)
        

        


def main():
    gtk.main()
    return 0

if __name__ == "__main__":
    rokola = PrimeraRokola()
    main()
