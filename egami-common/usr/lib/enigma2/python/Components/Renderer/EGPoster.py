# -*- coding: utf-8 -*-
from Components.Renderer.Renderer import Renderer
from enigma import iPlayableServicePtr, eServiceReference
from enigma import ePixmap, ePicLoad, eTimer
from Components.AVSwitch import AVSwitch
from Components.Pixmap import Pixmap
try:
    from urllib.request import urlopen, quote
    from _thread import start_new_thread
except ImportError:
    from urllib2 import urlopen, quote
    from thread import start_new_thread
import json
import re
from os import path
from Components.config import config
leng = config.osd.language.value
leng = leng.replace('_', '-')

folder_path = "/tmp/odposter/"

api_key = 'f23c2bd91113daf777dcba03990aea77'

class EGPoster(Renderer):
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
        try:
            refer = self.source.serviceref.toString()
            if refer.startswith('4097'):
                if what[0] == self.CHANGED_CLEAR:
                    self.instance.hide()
                if what[0] != self.CHANGED_CLEAR:
                    self.timer.start(10, True)
            else:
                if refer.startswith('5002'):
                    if what[0] == self.CHANGED_CLEAR:
                        self.instance.hide()
                    if what[0] != self.CHANGED_CLEAR:
                        self.timer.start(10, True)
                else:
                    pass
        except:
            pass

    def showPoster(self):
        service = self.source.service
        info = None
        if isinstance(service, iPlayableServicePtr):
            info = service and service.info()
            service = None
        if not info:
            return ''
        name = service and info.getName(service)
        if name is None:
            name = info.getName()
        name = name.replace('\xc2\x86', '').replace('\xc2\x87', '')
        rep_name = ["sd", "hd", "fhd", "uhd", "4k", "vod", "1080p", "720p", "blueray", "x264", "aac", "ozlem", "hindi", "hdrip", "(cache)", "(kids)", "[3d-en]", "[iran-dubbed]", "imdb", "top250", "multi-audio",
                     "multi-subs", "multi-sub", "[audio-pt]", "[nordic-subbed]", "[nordic-subbeb]",
                     "ae:", "al:", "ar:", "at:", "ba:", "be:", "bg:", "br:", "cg:", "ch:", "cz:", "da:", "de:", "dk:", "ee:", "en:", "es:", "ex-yu:", "fi:", "fr:", "gr:", "hr:", "hu:", "in:", "ir:", "it:", "lt:", "mk:",
                     "mx:", "nl:", "no:", "pl:", "pt:", "ro:", "rs:", "ru:", "se:", "si:", "sk:", "tr:", "uk:", "us:", "yu:",
                     "[ae]", "[al]", "[ar]", "[at]", "[ba]", "[be]", "[bg]", "[br]", "[cg]", "[ch]", "[cz]", "[da]", "[de]", "[dk]", "[ee]", "[en]", "[es]", "[ex-yu]", "[fi]", "[fr]", "[gr]", "[hr]", "[hu]", "[in]", "[ir]", "[it]", "[lt]", "[mk]",
                     "[mx]", "[nl]", "[no]", "[pl]", "[pt]", "[ro]", "[rs]", "[ru]", "[se]", "[si]", "[sk]", "[tr]", "[uk]", "[us]", "[yu]",
                     "-ae-", "-al-", "-ar-", "-at-", "-ba-", "-be-", "-bg-", "-br-", "-cg-", "-ch-", "-cz-", "-da-", "-de-", "-dk-", "-ee-", "-en-", "-es-", "-ex-yu-", "-fi-", "-fr-", "-gr-", "-hr-", "-hu-", "-in-", "-ir-", "-it-", "-lt-", "-mk-",
                     "-mx-", "-nl-", "-no-", "-pl-", "-pt-", "-ro-", "-rs-", "-ru-", "-se-", "-si-", "-sk-", "-tr-", "-uk-", "-us-", "-yu-",
                     "|ae|", "|al|", "|ar|", "|at|", "|ba|", "|be|", "|bg|", "|br|", "|cg|", "|ch|", "|cz|", "|da|", "|de|", "|dk|", "|ee|", "|en|", "|es|", "|ex-yu|", "|fi|", "|fr|", "|gr|", "|hr|", "|hu|", "|in|", "|ir|", "|it|", "|lt|", "|mk|",
                     "|mx|", "|nl|", "|no|", "|pl|", "|pt|", "|ro|", "|rs|", "|ru|", "|se|", "|si|", "|sk|", "|tr|", "|uk|", "|us|", "|yu|",
                     "(", ")", "[", "]", "u-", "3d", "-", "'", " S01 ", " S02 ", " S03 ", " S04 ", " S05 ", " S06 ", " S07 ", " S08 ", " S09 ", " S10 ", " S11 ", " S12 ", " S13 ", " S14 ",
                     " S15 ", " S16 ", "E01", "E02", "E03", "E04", "E05", "E06", "E07", "E08", "E09", "E10", "E11", "E12", "E13", "E14",  "E15", "E16", "E17", "E18", "E19", "E20", "E21", "E22", "E23", "E24", "E25", ]
        for j in range (1900, 2025):
            rep_name.append(str(j))
        for i in rep_name:
            name = name.replace(i, '')
        if service or info:
            evntNm = re.sub("([\(\[]).*?([\)\]])|(: odc.\d+)|(\d+: odc.\d+)|(\d+ odc.\d+)|(:)|( -(.*?).*)|(,)|!|/.*|\|\s[0-9]+\+|[0-9]+\+|\s\d{4}\Z|([\(\[\|].*?[\)\]\|])|(\"|\"\.|\"\,|\.)\s.+|\"|:|Премьера\.\s|(х|Х|м|М|т|Т|д|Д)/ф\s|(х|Х|м|М|т|Т|д|Д)/с\s|\s(с|С)(езон|ерия|-н|-я)\s.+|\s\d{1,3}\s(ч|ч\.|с\.|с)\s.+|\.\s\d{1,3}\s(ч|ч\.|с\.|с)\s.+|\s(ч|ч\.|с\.|с)\s\d{1,3}.+|\d{1,3}(-я|-й|\sс-н).+|", "", str(name)).rstrip()
            pstrNm = folder_path + "{}.jpg".format(evntNm)
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
        service = self.source.service
        info = None
        if isinstance(service, iPlayableServicePtr):
            info = service and service.info()
            service = None
        if not info:
            return ''
        name = service and info.getName(service)
        if name is None:
            name = info.getName()
        name = name.replace('\xc2\x86', '').replace('\xc2\x87', '')
        rep_name = ["sd", "hd", "fhd", "uhd", "4k", "vod", "1080p", "720p", "blueray", "x264", "aac", "ozlem", "hindi", "hdrip", "(cache)", "(kids)", "[3d-en]", "[iran-dubbed]", "imdb", "top250", "multi-audio",
                     "multi-subs", "multi-sub", "[audio-pt]", "[nordic-subbed]", "[nordic-subbeb]",
                     "ae:", "al:", "ar:", "at:", "ba:", "be:", "bg:", "br:", "cg:", "ch:", "cz:", "da:", "de:", "dk:", "ee:", "en:", "es:", "ex-yu:", "fi:", "fr:", "gr:", "hr:", "hu:", "in:", "ir:", "it:", "lt:", "mk:",
                     "mx:", "nl:", "no:", "pl:", "pt:", "ro:", "rs:", "ru:", "se:", "si:", "sk:", "tr:", "uk:", "us:", "yu:",
                     "[ae]", "[al]", "[ar]", "[at]", "[ba]", "[be]", "[bg]", "[br]", "[cg]", "[ch]", "[cz]", "[da]", "[de]", "[dk]", "[ee]", "[en]", "[es]", "[ex-yu]", "[fi]", "[fr]", "[gr]", "[hr]", "[hu]", "[in]", "[ir]", "[it]", "[lt]", "[mk]",
                     "[mx]", "[nl]", "[no]", "[pl]", "[pt]", "[ro]", "[rs]", "[ru]", "[se]", "[si]", "[sk]", "[tr]", "[uk]", "[us]", "[yu]",
                     "-ae-", "-al-", "-ar-", "-at-", "-ba-", "-be-", "-bg-", "-br-", "-cg-", "-ch-", "-cz-", "-da-", "-de-", "-dk-", "-ee-", "-en-", "-es-", "-ex-yu-", "-fi-", "-fr-", "-gr-", "-hr-", "-hu-", "-in-", "-ir-", "-it-", "-lt-", "-mk-",
                     "-mx-", "-nl-", "-no-", "-pl-", "-pt-", "-ro-", "-rs-", "-ru-", "-se-", "-si-", "-sk-", "-tr-", "-uk-", "-us-", "-yu-",
                     "|ae|", "|al|", "|ar|", "|at|", "|ba|", "|be|", "|bg|", "|br|", "|cg|", "|ch|", "|cz|", "|da|", "|de|", "|dk|", "|ee|", "|en|", "|es|", "|ex-yu|", "|fi|", "|fr|", "|gr|", "|hr|", "|hu|", "|in|", "|ir|", "|it|", "|lt|", "|mk|",
                     "|mx|", "|nl|", "|no|", "|pl|", "|pt|", "|ro|", "|rs|", "|ru|", "|se|", "|si|", "|sk|", "|tr|", "|uk|", "|us|", "|yu|",
                     "(", ")", "[", "]", "u-", "3d", "-", "'", " S01 ", " S02 ", " S03 ", " S04 ", " S05 ", " S06 ", " S07 ", " S08 ", " S09 ", " S10 ", " S11 ", " S12 ", " S13 ", " S14 ",
                     " S15 ", " S16 ", "E01", "E02", "E03", "E04", "E05", "E06", "E07", "E08", "E09", "E10", "E11", "E12", "E13", "E14",  "E15", "E16", "E17", "E18", "E19", "E20", "E21", "E22", "E23", "E24", "E25", ]
        for j in range (1900, 2025):
            rep_name.append(str(j))
        for i in rep_name:
            name = name.replace(i, '')
        if service or info:
            evntNm = re.sub("([\(\[]).*?([\)\]])|(: odc.\d+)|(\d+: odc.\d+)|(\d+ odc.\d+)|(:)|( -(.*?).*)|(,)|!|/.*|\|\s[0-9]+\+|[0-9]+\+|\s\d{4}\Z|([\(\[\|].*?[\)\]\|])|(\"|\"\.|\"\,|\.)\s.+|\"|:|Премьера\.\s|(х|Х|м|М|т|Т|д|Д)/ф\s|(х|Х|м|М|т|Т|д|Д)/с\s|\s(с|С)(езон|ерия|-н|-я)\s.+|\s\d{1,3}\s(ч|ч\.|с\.|с)\s.+|\.\s\d{1,3}\s(ч|ч\.|с\.|с)\s.+|\s(ч|ч\.|с\.|с)\s\d{1,3}.+|\d{1,3}(-я|-й|\sс-н).+|", "", str(name)).rstrip()
            pstrNm = folder_path + "{}.jpg".format(evntNm)
            try:
                self.instance.hide()
                url = 'http://api.themoviedb.org/3/search/tv?api_key={}&query={}'.format(api_key,quote(evntNm))
                jurl = json.loads(urlopen(url).read().decode('utf-8'))
                if 'results' in jurl:
                    if 'id' in jurl['results'][0]:
                        ids = jurl['results'][0]['id']
                url_2 = 'http://api.themoviedb.org/3/tv/' + str(ids) + '?api_key={}&language={}'.format(api_key,str(leng))
                data2 = json.loads(urlopen(url_2).read().decode('utf-8'))
                poster = data2['poster_path']
                url_poster = "http://image.tmdb.org/t/p/w185{}".format(poster)
                with open(pstrNm,'wb') as f:
                    f.write(urlopen(url_poster).read())
                    self.timer.start(10, True)
            except:
                try:
                    url = 'http://api.themoviedb.org/3/search/movie?api_key={}&query={}'.format(api_key,quote(evntNm))
                    jurl = json.loads(urlopen(url).read().decode('utf-8'))
                    if 'results' in jurl:
                        if 'id' in jurl['results'][0]:
                            ids = jurl['results'][0]['id']
                    url_2 = 'http://api.themoviedb.org/3/movie/' + str(ids) + '?api_key={}&language={}'.format(api_key,str(leng))
                    data2 = json.loads(urlopen(url_2).read().decode('utf-8'))
                    poster = data2['poster_path']
                    url_poster = "http://image.tmdb.org/t/p/w185{}".format(poster)
                    with open(pstrNm,'wb') as f:
                        f.write(urlopen(url_poster).read())
                        self.timer.start(10, True)
                except:
                    pass
