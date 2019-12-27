from Components.Converter.Converter import Converter
from Components.Element import cached
from Tools.Directories import fileExists
from Poll import Poll
import time
import os

weather_city = '711665'
time_update = 20
time_update_ms = 30000

class YWeather(Poll, Converter, object):
    city = 0
    country = 1
    direction = 2
    speed = 3
    humidity = 4
    visibility = 5
    pressure = 6
    pressurenm = 7
    wtext = 8
    temp = 9
    picon = 10

    def __init__(self, type):
        Converter.__init__(self, type)
        Poll.__init__(self)
        if type == "city":
            self.type = self.city
        elif type == "country":
            self.type = self.country
        elif type == "direction":
            self.type = self.direction
        elif type == "speed":
            self.type = self.speed
        elif type == "humidity":
            self.type = self.humidity
        elif type == "visibility":
            self.type = self.visibility
        elif type == "pressure":
            self.type = self.pressure
        elif type == "pressurenm":
            self.type = self.pressurenm
        elif type == "text":
            self.type = self.wtext
        elif type == "temp":
            self.type = self.temp
        elif type == "picon":
            self.type = self.picon
        self.poll_interval = time_update_ms
        self.poll_enabled = True
                    
    @cached
    def getText(self):
        xweather = {'ycity':"city", 'ycountry':"code", 'ydirection':"361", 'yspeed':"spd", 'yhumidity':"hmd", 'yvisibility':"vis", 'ypressure':"bar", 'ytext':"...", 'ytemp':"tmp", 'ypicon':"3200"}
        direct = 0
        info = ""
        if fileExists("/usr/lib/enigma2/python/Plugins/Extensions/Weather/Config/Location_id"):
            weather_city = open("/usr/lib/enigma2/python/Plugins/Extensions/Weather/Config/Location_id").read()
        else:
            weather_city = 715693
        try:
            if fileExists("/tmp/yweather.xml"):
                if int((time.time() - os.stat("/tmp/yweather.xml").st_mtime)/60) >= time_update:
                    os.system("rm /tmp/yweather.xml")
                    os.system("wget -P /tmp -T2 'http://weather.yahooapis.com/forecastrss?w=%s&u=c' -O /tmp/yweather.xml" % weather_city)
            else:
                os.system("wget -P /tmp -T2 'http://weather.yahooapis.com/forecastrss?w=%s&u=c' -O /tmp/yweather.xml" % weather_city)
        except:
		pass
        if not fileExists("/tmp/yweather.xml"):
            os.system("echo -e 'None' >> /tmp/yweather.xml")
        for line in open("/tmp/yweather.xml"):
            if line.find("<yweather:location") > -1:
                xweather['ycity'] = line.split('city')[1].split('"')[1]
                xweather['ycountry'] = line.split('country')[1].split('"')[1]
            elif line.find("<yweather:wind") > -1:
                xweather['ydirection'] = line.split('direction')[1].split('"')[1]
                print "xweather['ydirection']================================",line.split('direction')[1].split('"')[1]
                xweather['yspeed'] = line.split('speed')[1].split('"')[1]
            elif line.find("<yweather:atmosphere") > -1:
                xweather['yhumidity'] = line.split('humidity')[1].split('"')[1]
                xweather['yvisibility'] = line.split('visibility')[1].split('"')[1]
                xweather['ypressure'] = line.split('pressure')[1].split('"')[1]
            elif line.find("<yweather:condition") > -1:
                xweather['ytext'] = line.split('text')[1].split('"')[1]
                xweather['ypicon'] = line.split('code')[1].split('"')[1]
                xweather['ytemp'] = line.split('temp')[1].split('"')[1]
                                        
        if self.type == self.city:
            info = xweather['ycity']
        elif self.type == self.country:
            info = xweather['ycountry']
        elif self.type == self.direction:
            direct = int(xweather['ydirection'])
            if direct >= 0 and direct <= 20:
                info = _('N')
            elif direct >= 21 and direct <= 35:
                info = _('Nne')
            elif direct >= 36 and direct <= 55:
                info = _('Ne')
            elif direct >= 56 and direct <= 70:
                info = _('Ene')
            elif direct >= 71 and direct <= 110:
                info = _('E')
            elif direct >= 111 and direct <= 125:
                info = _('Nse')
            elif direct >= 126 and direct <= 145:
                info = _('Se')
            elif direct >= 146 and direct <= 160:
                info = _('Sse')
            elif direct >= 161 and direct <= 200:
                info = _('S')
            elif direct >= 201 and direct <= 215:
                info = _('Ssw')
            elif direct >= 216 and direct <= 235:
                info = _('Sw')
            elif direct >= 236 and direct <= 250:
                info = _('Wsw')
            elif direct >= 251 and direct <= 290:
                info = _('W')
            elif direct >= 291 and direct <= 305:
                info = _('Wnw')
            elif direct >= 306 and direct <= 325:
                info = _('Nw')
            elif direct >= 326 and direct <= 340:
                info = _('Nnw')
            elif direct >= 341 and direct <= 360:
                info = _('N')
            elif direct == 361 :
                info = _(' ')								
                                        
        elif self.type == self.speed:
            info = xweather['yspeed'] + ' km/h'
        elif self.type == self.humidity:
            info = xweather['yhumidity'] + ' mb'
        elif self.type == self.visibility:
            info = xweather['yvisibility'] + ' km'
        elif self.type == self.pressure:
            info = xweather['ypressure'] + ' mb'
        elif self.type == self.pressurenm:
            if xweather['ypressure'] != " ":
                info = "%d mmHg" % round(float(xweather['ypressure']) * 0.75)
            else:
                info = " "
        elif self.type == self.wtext:
                        info = xweather['ytext']
        elif self.type == self.temp:
            if info != " ":
                if xweather['ytemp'][0] != '-' and xweather['ytemp'][0] != '0':
                    info = '+' + xweather['ytemp'] + '%s' % unichr(176).encode("latin-1")
                else:
                    info = xweather['ytemp'] + '%s' % unichr(176).encode("latin-1")
            else:
                info = xweather['ytemp']
        elif self.type == self.picon:
            info = xweather['ypicon']
        return info

    text = property(getText)

    def changed(self, what):
        Converter.changed(self, (self.CHANGED_POLL,))
