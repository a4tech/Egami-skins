# -*- coding: utf-8 -*-
# Code by Madhouse
from Components.Renderer.Renderer import Renderer
from enigma import ePixmap, ePicLoad, eTimer
from Components.AVSwitch import AVSwitch
try:
    from urllib.request import urlopen, quote
    from _thread import start_new_thread
except ImportError:
    from urllib2 import urlopen, quote
    from thread import start_new_thread
import json
import re
from os import path, walk, popen, makedirs
import socket
from shutil import rmtree
from Components.config import config
leng = config.osd.language.value
leng = leng.replace('_', '-')

# Dir Poster Download
folder_path = "/tmp/odposter/"
apikey = "f23c2bd91113daf777dcba03990aea77"

try:
    folder_size=sum([sum(map(lambda fname: path.getsize(path.join(folder_path, fname)), files)) for folder_path, folders, files in walk(folder_path)])
    odposter = "%0.f" % (folder_size/(1024*1024.0))
    if odposter >= "5":
        rmtree(folder_path)
except:
    pass

class ODposter(Renderer):
    def __init__(self):
        Renderer.__init__(self)
        self.intCheck()
        self.timer = eTimer()
        self.timer.callback.append(self.showPoster)

    def intCheck(self):
        try:
            socket.setdefaulttimeout(1)
            socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect(("8.8.8.8", 53))
            return True
        except:
            return

    GUI_WIDGET = ePixmap
    def changed(self, what):
        if not self.instance:
            return
        if what[0] == self.CHANGED_CLEAR:
            self.instance.hide()
        if what[0] != self.CHANGED_CLEAR:
            self.timer.start(10, True)

    def showPoster(self):
        if not path.isdir(folder_path):
            makedirs(folder_path)
        self.instance.hide()
        self.event = self.source.event
        if self.event is None:
            self.instance.hide()
            return
        evnts = self.event.getEventName()
        evntNm = re.sub("([\(\[]).*?([\)\]])|(: odc.\d+)|(\d+: odc.\d+)|(\d+ odc.\d+)|(:)|( -(.*?).*)|(,)|!|/.*|\|\s[0-9]+\+|[0-9]+\+|\s\d{4}\Z|([\(\[\|].*?[\)\]\|])|(\"|\"\.|\"\,|\.)\s.+|\"|:|Премьера\.\s|(х|Х|м|М|т|Т|д|Д)/ф\s|(х|Х|м|М|т|Т|д|Д)/с\s|\s(с|С)(езон|ерия|-н|-я)\s.+|\s\d{1,3}\s(ч|ч\.|с\.|с)\s.+|\.\s\d{1,3}\s(ч|ч\.|с\.|с)\s.+|\s(ч|ч\.|с\.|с)\s\d{1,3}.+|\d{1,3}(-я|-й|\sс-н).+|", "", evnts).rstrip()
        evntNm = evntNm.replace('\xc2\x86', '').replace('\xc2\x87', '')
        pstrNm = folder_path + "{}.jpg".format(evntNm)
        if self.event:
            if path.exists(pstrNm):
                size = self.instance.size()
                self.picload = ePicLoad()
                sc = AVSwitch().getFramebufferScale()
                if self.picload:
                    self.picload.setPara([size.width(), size.height(), sc[0], sc[1], False, 1, '#00000000'])
                    self.picload.startDecode(pstrNm, 0, 0, False)
                ptr = self.picload.getData()
                if ptr != None:
                    self.instance.setPixmap(ptr)
                    self.instance.show()
                else:
                    self.instance.hide()
            else:
                start_new_thread(self.info, ())
        else:
            self.instance.hide()
            return

    def info(self):
        self.event = self.source.event
        evnts = self.event.getEventName()
        evntNm = re.sub("([\(\[]).*?([\)\]])|(: odc.\d+)|(\d+: odc.\d+)|(\d+ odc.\d+)|(:)|( -(.*?).*)|(,)|!|/.*|\|\s[0-9]+\+|[0-9]+\+|\s\d{4}\Z|([\(\[\|].*?[\)\]\|])|(\"|\"\.|\"\,|\.)\s.+|\"|:|Премьера\.\s|(х|Х|м|М|т|Т|д|Д)/ф\s|(х|Х|м|М|т|Т|д|Д)/с\s|\s(с|С)(езон|ерия|-н|-я)\s.+|\s\d{1,3}\s(ч|ч\.|с\.|с)\s.+|\.\s\d{1,3}\s(ч|ч\.|с\.|с)\s.+|\s(ч|ч\.|с\.|с)\s\d{1,3}.+|\d{1,3}(-я|-й|\sс-н).+|", "", evnts).rstrip()
        evntNm = evntNm.replace('\xc2\x86', '').replace('\xc2\x87', '')
        pic_image = folder_path + "{}.jpg".format(evntNm)
        try:
            url = 'http://api.themoviedb.org/3/search/tv?api_key={}&query={}'.format(apikey,quote(evntNm))
            jurl = json.loads(urlopen(url).read().decode('utf-8'))
            if 'results' in jurl:
                if 'id' in jurl['results'][0]:
                    ids = jurl['results'][0]['id']
            url_2 = 'http://api.themoviedb.org/3/tv/' + str(ids) + '?api_key={}&language={}'.format(apikey,str(leng))
            data2 = json.loads(urlopen(url_2).read().decode('utf-8'))
            poster = data2['poster_path']
            url_poster = "http://image.tmdb.org/t/p/w185{}".format(poster)
            with open(pic_image,'wb') as f:
                f.write(urlopen(url_poster).read())
                self.timer.start(10, True)
        except:
            try:
                url = 'http://api.themoviedb.org/3/search/movie?api_key={}&query={}'.format(apikey,quote(evntNm))
                jurl = json.loads(urlopen(url).read().decode('utf-8'))
                if 'results' in jurl:
                    if 'id' in jurl['results'][0]:
                        ids = jurl['results'][0]['id']
                url_2 = 'http://api.themoviedb.org/3/movie/' + str(ids) + '?api_key={}&language={}'.format(apikey,str(leng))
                data2 = json.loads(urlopen(url_2).read().decode('utf-8'))
                poster = data2['poster_path']
                url_poster = "http://image.tmdb.org/t/p/w185{}".format(poster)
                with open(pic_image,'wb') as f:
                    f.write(urlopen(url_poster).read())
                    self.timer.start(10, True)
            except:
                pass
