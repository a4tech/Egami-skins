#!/usr/bin/env python
import zlib, base64
from base64 import b64encode, b64decode
from EGActive import egcrypt
app = '11087&23128'
exec(b64decode(egcrypt('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', b64encode(app.encode('utf-8')).decode('utf-8'))))
