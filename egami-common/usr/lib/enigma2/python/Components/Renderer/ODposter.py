# -*- coding: utf-8 -*-
# Code by Madhouse
# <widget source="session.Event_Now" render="ODposter" position="1620,505" size="300,438" alphatest="blend" zPosition="9" />
# <widget source="session.Event_Next" render="ODposter" position="1620,505" size="300,438" alphatest="blend" zPosition="9" />
from Components.Renderer.Renderer import Renderer
from enigma import ePixmap, ePicLoad, eTimer
from Components.AVSwitch import AVSwitch
try:
    from urllib.request import urlopen, quote
except ImportError:
    from urllib2 import urlopen, quote
import json, re, os, socket, shutil

# Dir Poster Download
folder_path = "/tmp/odposter/"
apikey = "f23c2bd91113daf777dcba03990aea77"

try:
    folder_size=sum([sum(map(lambda fname: os.path.getsize(os.path.join(folder_path, fname)), files)) for folder_path, folders, files in os.walk(folder_path)])
    odposter = "%0.f" % (folder_size/(1024*1024.0))
    if odposter >= "5": # Elimino al raggiungimento di 5mb
        shutil.rmtree(folder_path)
except:
    pass

# Recupero lingua sistema
leng = os.popen("cat /etc/enigma2/settings | grep config.osd.language|sed '/^config.osd.language=/!d'").read().replace('config.osd.language=', '').replace('_', '-').replace('\n', '')

class ODposter(Renderer):
    def __init__(self):
        Renderer.__init__(self)
        self.timer10 = eTimer()
        self.intCheck()
    # Verifico presenza internet
    def intCheck(self):
        try:
            socket.setdefaulttimeout(0.5)
            socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect(("8.8.8.8", 53))
            return True
        except:
            return False

    GUI_WIDGET = ePixmap
    def changed(self, what):
        if not self.instance:
            return
        if what[0] == self.CHANGED_CLEAR:
            self.instance.hide()
        if what[0] != self.CHANGED_CLEAR:
            self.delay()

    def info(self):
        if self.downloading:
            return
        self.downloading = True
        self.event = self.source.event
        if self.event:
            evnts = self.event.getEventName()
            evnt = evnts.replace('FILM ', '').replace('FILM - ', '').replace('film - ', '').replace('TELEFILM ', '').replace('TELEFILM - ', '').replace('telefilm - ', '')
            evntN = re.sub("([\(\[]).*?([\)\]])|(: odc.\d+)|(\d+: odc.\d+)|(\d+ odc.\d+)|(:)|( -(.*?).*)|(,)|!", "", evnt).rstrip()
            self.evntNm = evntN
            self.pstrNm = "/tmp/odposter/{}.jpg".format(self.evntNm)
            try:
                url = 'http://api.themoviedb.org/3/search/tv?api_key={}&query={}'.format(apikey,quote(self.evntNm))
                url2 = urlopen(url).read().decode('utf-8')
                jurl = json.loads(url2)
                if 'results' in jurl:
                    if 'id' in jurl['results'][0]:
                        ids = jurl['results'][0]['id']
                url_2 = 'http://api.themoviedb.org/3/tv/' + str(ids) + '?api_key={}&language={}'.format(apikey,str(leng))
                url_3 = urlopen(url_2).read().decode('utf-8')
                data2 = json.loads(url_3)
                poster = data2['poster_path']
                if poster:
                    self.url_poster = "http://image.tmdb.org/t/p/w185{}".format(poster) #w185 risoluzione poster
                    self.savePoster()
                self.timer10.stop()
            except:
                try:
                    url = 'http://api.themoviedb.org/3/search/movie?api_key={}&query={}'.format(apikey,quote(self.evntNm))
                    url2 = urlopen(url).read().decode('utf-8')
                    jurl = json.loads(url2)
                    if 'results' in jurl:
                        if 'id' in jurl['results'][0]:
                            ids = jurl['results'][0]['id']
                    url_2 = 'http://api.themoviedb.org/3/movie/' + str(ids) + '?api_key={}&language={}'.format(apikey,str(leng))
                    url_3 = urlopen(url_2).read().decode('utf-8')
                    data2 = json.loads(url_3)
                    poster = data2['poster_path']
                    if poster:
                        self.url_poster = "http://image.tmdb.org/t/p/w185{}".format(poster) #w185 risoluzione poster
                        self.savePoster()
                    self.timer10.stop()
                except:
                    self.timer10.stop()
                    pass
        else:
            self.instance.hide()
            self.timer10.stop()

    def delay(self):
        self.downloading = False
        self.event = self.source.event
        if self.event:
            evnts = self.event.getEventName()
            evnt = evnts.replace('FILM ', '').replace('FILM - ', '').replace('film - ', '').replace('TELEFILM ', '').replace('TELEFILM - ', '').replace('telefilm - ', '')
            evntN = re.sub("([\(\[]).*?([\)\]])|(: odc.\d+)|(\d+: odc.\d+)|(\d+ odc.\d+)|(:)|( -(.*?).*)|(,)|!", "", evnt).rstrip()
            self.evntNm = evntN
            self.pstrNm = "/tmp/odposter/{}.jpg".format(self.evntNm)
            if os.path.exists(self.pstrNm):
                self.showPoster()
            else:
                self.instance.hide()
                try:
                    self.timer10.callback.append(self.info)
                except:
                    self.timer10_conn = self.timer10.timeout.connect(self.info)
                self.timer10.start(450, False) # Timer avvio Download Poster
        else:
            self.instance.hide()

    def showPoster(self):
        if os.path.exists(self.pstrNm):
            size = self.instance.size()
            self.picload = ePicLoad()
            sc = AVSwitch().getFramebufferScale()
            if self.picload:
                self.picload.setPara([size.width(), size.height(), sc[0], sc[1], False, 1, '#00000000'])
                if os.path.exists('/var/lib/dpkg/status'):
                    self.picload.startDecode(self.pstrNm, False)
                else:
                    self.picload.startDecode(self.pstrNm, 0, 0, False)
            ptr = self.picload.getData()
            if ptr != None:
                self.instance.setPixmap(ptr)
                self.instance.show()
            else:
                self.instance.hide()
    # Download Poster
    def savePoster(self):
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        pic_image = urlopen(self.url_poster).read()
        try:
            with open(self.pstrNm, "wb") as f:
                f.write(pic_image)
            self.showPoster()
        except:
            pass
