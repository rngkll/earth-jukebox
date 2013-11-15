#!/usr/bin/env python
#coding: utf-8

import xmmsclient
from xmmsclient import collections as cx
import os

class Controller(object):
    """A simple wrapper class of XMMSSync."""

    def __init__(self, options):
        
        self.c = xmmsclient.XMMSSync('Rokola')
        
        try:
            self.c.connect()
            
        except IOError:
            os.system('xmms2-launcher')
            self.c.connect()

        self.options = options
        
    def is_playing(self):
        return self.c.playback_status() == xmmsclient.PLAYBACK_STATUS_PLAY

    def play(self, pos):
        self.c.playlist_set_next(pos)
        self.c.playback_start()
        
    def play_start(self):
        self.c.playback_start()
        
    def add_idtopls(self,id):
        self.c.playlist_add_id(id)
    

    def delete(self, pos):
        """Remove a song from playlist.
	#cambiar esto porque no se puede parar la musica
        If the song to be removed is playing now, we first stop it.
        """
        if self.is_playing():
            if self.current_position() == pos:
                self.c.playback_stop()
        self.c.playlist_remove_entry(pos)

    def stop(self):
        self.c.playback_stop()

    def load(self, name):
        self.c.playlist_load(name)
        
    def clear(self):
        #self.c.playback_stop()
        self.c.playlist_clear()

    def current_position(self):
        print self.c.playlist_current_pos()
        """Return current position in the playlist."""

        # It is an error to call playlist_current_pos when there are
        # no entries in the playlist.
        try:
            return self.c.playlist_current_pos()
        except xmmsclient.XMMSError:
            return None

    def playlist(self):
        """Format the playlist.
        
        First we try to get imformation from id3v2, if it fails,
        then try id3, else we just display the file name.
        """
        def iconv(s):
            encoding = self.options["id3_encoding"]
            if encoding:
                return s.encode('latin1').decode(encoding).encode('utf-8')
            else:
                return s.encode('latin1')

        lst = []
        for id in self.c.playlist_list_entries():
            song = self.c.medialib_get_info(id)
            try:
                artist = iconv(song[('plugin/id3v2', 'artist')])
            except KeyError:
                try:
                    artist = iconv(song[('plugin/mad', 'artist')])
                except KeyError:
                    artist = ''
            try:
                title = iconv(song[('plugin/id3v2', 'title')])
            except KeyError:
                try:
                    title = iconv(song[('plugin/mad', 'title')])
                except KeyError:
                    title = ''
            if artist == "" and title == "":
                name = os.path.split(song[('server', 'url')])[1]
                name = os.path.splitext(name)[0]
                name = urllib.unquote(name.decode('utf-8').encode('latin1'))
                name = name.replace("+", " ")
                lst.append('  ' + name)
            else:
                lst.append('  %s - %s' % (artist.ljust(6), title))

        return lst

        
    def get_coll_ids(self, collection):
        res = self.c.coll_query_ids(collection)
        return res
        
    def get_current_mode(self):
        res = self.c.playback_status()
        return res

    def get_coll_values(self, collection, fields):
        res = self.c.coll_query_infos(collection, fields)
        return res

    def get_av_artist_list(self):
        #res = self.c.coll_query_infos(coll=xmmsclient.xmmsapi.Universe(), fields=['artist'] )
        res = self.c.coll_query_infos(coll=cx.Universe(), fields=['artist'], groupby=['artist'])
        return res

# retrive bindata for given hash key
    def get_bindata(self, hash):
        res = self.c.bindata_retrive(hash)
        return res.get_bin()

# create a collection that contains tracks of artist and album
    def create_a_coll(self, artist):
        print '------------- funcion create_a_coll-----------------'
         
        m = cx.Match(field="artist", value=artist)
        print m
        ids =  self.c.coll_query_ids(m)
        print ids
        
        infor = self.c.coll_query_infos(m, ["id","artist", "title" ])
        print infor
        
        return infor
        
        
