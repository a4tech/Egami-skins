from Components.Converter.Converter import Converter
from Components.Element import cached
from Components.Converter.Poll import Poll
from enigma import eConsoleAppContainer
import os
from os import system, path, popen
from boxbranding import getMachineBuild

class EGTemp(Poll, Converter):
    TEMPERATURE = 0
    HDDTEMP = 1
    CPULOAD = 2
    CPUSPEED = 3
    FANINFO = 4
    UPTIME = 5

    def __init__(self, type):
        Converter.__init__(self, type)
        Poll.__init__(self)
        self.container = eConsoleAppContainer()
        type = type.split(',')
        self.short_list = True
        self.list = []
        self.shortFormat = 'Short' in type
        if 'CPULoad' in type:
            self.type = self.CPULOAD
        elif 'CPUSpeed' in type:
            self.type = self.CPUSPEED
        elif 'Temperature' in type:
            self.type = self.TEMPERATURE
        elif 'Uptime' in type:
            self.type = self.UPTIME
        elif 'HDDTemp' in type:
            self.type = self.HDDTEMP
            self.hddtemp_output = ''
            self.hddtemp = 'Waiting for HDD Temp Data...'
            self.container.appClosed.append(self.runFinished)
            self.container.dataAvail.append(self.dataAvail)
            self.container.execute('hddtemp -n -q /dev/sda')
        elif 'FanInfo' in type:
            self.type = self.FANINFO
        if 'HDDTemp' in type:
            self.poll_interval = 500
        else:
            self.poll_interval = 7000
        self.poll_enabled = True

    def dataAvail(self, strData):
        self.hddtemp_output = self.hddtemp_output.encode('utf-8', 'ignore') + strData

    def runFinished(self, retval):
        temp = self.hddtemp_output.decode('utf-8', 'ignore')
        if 'No such file or directory' in temp or 'not found' in temp:
            self.hddtemp = 'HDD Temp: N/A'
        else:
            temp = int(temp)
            if temp > 0:
                temp = str(temp)
                self.hddtemp = 'HDD Temp: %s\xc2\xb0C' % temp
            else:
                self.hddtemp = 'HDD idle or N/A'

    @cached
    def getText(self):
        if self.type == self.CPULOAD:
            cpuload = ''
            if os.path.exists('/proc/loadavg'):
                try:
                    with open('/proc/loadavg', 'r') as (l):
                        load = l.readline(4)
                except:
                    load = ''

                cpuload = load.replace('\n', '').replace(' ', '')
                return 'CPU Load: %s' % cpuload
        else:
            if self.type == self.TEMPERATURE:
                tempinfo = ''
                if path.exists('/proc/stb/sensors/temp0/value'):
                    f = open('/proc/stb/sensors/temp0/value', 'r')
                    tempinfo = f.read()
                    f.close()
                elif path.exists('/proc/stb/fp/temp_sensor'):
                    f = open('/proc/stb/fp/temp_sensor', 'r')
                    tempinfo = f.read()
                    f.close()
                elif path.exists('/proc/stb/sensors/temp/value'):
                    f = open('/proc/stb/sensors/temp/value', 'r')
                    tempinfo = f.read()
                    f.close()
                if tempinfo and int(tempinfo.replace('\n', '')) > 0:
                    mark = str('\xc2\xb0')
                    AboutText = _('%s') % tempinfo.replace('\n', '').replace(' ', '') + mark + 'C\n'
                tempinfo = ''
                if path.exists('/proc/stb/fp/temp_sensor_avs'):
                    f = open('/proc/stb/fp/temp_sensor_avs', 'r')
                    tempinfo = f.read()
                    f.close()
                elif path.exists('/proc/stb/power/avs'):
                    f = open('/proc/stb/power/avs', 'r')
                    tempinfo = f.read()
                    f.close()
                elif path.exists('/sys/devices/virtual/thermal/thermal_zone0/temp'):
                    try:
                        f = open('/sys/devices/virtual/thermal/thermal_zone0/temp', 'r')
                        tempinfo = f.read()
                        tempinfo = tempinfo[:-4]
                        f.close()
                    except:
                        tempinfo = ''

                elif path.exists('/proc/hisi/msp/pm_cpu'):
                    try:
                        for line in open('/proc/hisi/msp/pm_cpu').readlines():
                            line = [ x.strip() for x in line.strip().split(':') ]
                            if line[0] in 'Tsensor':
                                temp = line[1].split('=')
                                temp = line[1].split(' ')
                                tempinfo = temp[2]
                                if getMachineBuild() in ('u41', 'u42', 'u43'):
                                    tempinfo = str(int(tempinfo) - 15)

                    except:
                        tempinfo = ''

                if tempinfo and int(tempinfo.replace('\n', '')) > 0:
                    mark = str('\xc2\xb0')
                    AboutText = _('%s') % tempinfo.replace('\n', '').replace(' ', '') + mark + 'C\n'
                return AboutText
            if self.type == self.HDDTEMP:
                return self.hddtemp
        if self.type == self.CPUSPEED:
            try:
                cpuspeed = 0
                for line in open('/proc/cpuinfo').readlines():
                    line = [ x.strip() for x in line.strip().split(':') ]
                    if line[0] == 'cpu MHz':
                        cpuspeed = '%1.0f' % float(line[1])

                if not cpuspeed:
                    try:
                        import binascii
                        cpuspeed = int(int(binascii.hexlify(open('/sys/firmware/devicetree/base/cpus/cpu@0/clock-frequency', 'rb').read()), 16) / 100000000) * 100
                    except:
                        try:
                            cpuspeed = int(open('/sys/devices/system/cpu/cpu0/cpufreq/cpuinfo_max_freq').read()) / 1000
                        except:
                            cpuspeed = '-'

                return 'CPU Speed: %s MHz' % cpuspeed
            except:
                return ''

        if self.type == self.FANINFO:
            fs = ''
            fv = ''
            fp = ''
            try:
                if os.path.exists('/proc/stb/fp/fan_speed'):
                    with open('/proc/stb/fp/fan_speed', 'r') as (fs):
                        fs = str(fs.readline().strip())
                if os.path.exists('/proc/stb/fp/fan_vlt'):
                    with open('/proc/stb/fp/fan_vlt', 'r') as (fv):
                        fv = str(int(fv.readline().strip(), 16))
                if os.path.exists('/proc/stb/fp/fan_pwm'):
                    with open('/proc/stb/fp/fan_pwm', 'r') as (fp):
                        fp = str(int(fp.readline().strip(), 16))
            except:
                pass

            if fs == '':
                return 'Fan Info: N/A'
            if self.shortFormat:
                return '%s - %sV - P:%s' % (fs, fv, fp)
            return 'Speed: %s V: %s PWM: %s' % (fs, fv, fp)
        elif self.type == self.UPTIME:
            try:
                with open('/proc/uptime', 'r') as (up):
                    uptime_info = up.read().split()
            except:
                return 'Uptime: N/A'
                uptime_info = None

            if uptime_info is not None:
                total_seconds = float(uptime_info[0])
                MINUTE = 60
                HOUR = MINUTE * 60
                DAY = HOUR * 24
                days = str(int(total_seconds / DAY))
                hours = str(int(total_seconds % DAY / HOUR))
                minutes = str(int(total_seconds % HOUR / MINUTE))
                seconds = str(int(total_seconds % MINUTE))
                uptime = ''
                if self.shortFormat:
                    uptime = '%sd %sh %sm %ss' % (days, hours, minutes, seconds)
                else:
                    if days > '0':
                        uptime += days + ' ' + (days == '1' and 'day' or 'days') + ', '
                    if len(uptime) > 0 or hours > '0':
                        uptime += hours + ' ' + (hours == '1' and 'hr' or 'hrs') + ', '
                    if len(uptime) > 0 or minutes > '0':
                        uptime += minutes + ' ' + (minutes == '1' and 'min' or 'mins')
                return 'Uptime: %s' % uptime
        return text

    text = property(getText)

    def changed(self, what):
        if what[0] == self.CHANGED_POLL:
            self.downstream_elements.changed(what)
