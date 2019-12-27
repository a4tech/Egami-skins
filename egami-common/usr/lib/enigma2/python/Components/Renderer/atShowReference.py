from Renderer import Renderer
from enigma import eLabel
from Components.VariableText import VariableText
from enigma import eServiceReference

class atShowReference(VariableText, Renderer):

    def __init__(self):
        Renderer.__init__(self)
        VariableText.__init__(self)

    GUI_WIDGET = eLabel

    def connect(self, source):
        Renderer.connect(self, source)
        self.changed((self.CHANGED_DEFAULT,))

    def changed(self, what):
        if self.instance:
            self.text = 'Reference: X:X:X:XXXX:XXX:X:XXXXXX:X:X:X'
            if what[0] != self.CHANGED_CLEAR:
                service = self.source.service
                marker = service.flags & eServiceReference.isMarker == eServiceReference.isMarker
                bouquet = service.flags & eServiceReference.flagDirectory == eServiceReference.flagDirectory
                sname = service.toString()
                if not marker and not bouquet and sname is not None and sname != '':
                    if sname[-1] != ':' and ('http' in sname or '//' in sname):
                        self.text = sname.replace(':', '_').replace(' ', '_').replace('%', '_').replace('/', '')
                    else:
                        pos = sname.rfind(':')
                        if pos != -1:
                            sname = sname[:pos].rstrip(':')
                            if '::' not in sname:
                                self.text = 'Reference: ' + sname
        return
