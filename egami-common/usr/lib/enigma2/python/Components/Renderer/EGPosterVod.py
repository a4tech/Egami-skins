# -*- coding: utf-8 -*-
# Code by Madhouse
import zlib, base64
exec(zlib.decompress(base64.b64decode('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')))
