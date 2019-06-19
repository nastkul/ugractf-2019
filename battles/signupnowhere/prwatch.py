#!/usr/bin/env python3

import requests
import escpos.printer

max_code = 0

p = escpos.printer.File('/dev/usb/lp0')
p.charcode('CP866')

while True:
    codes = [i.split(',') for i in requests.get("http://localhost:13301/codes-soidjfsoidfjidsfoi").text.strip().split("\n")]
    if codes == [['']]:
        continue
    for num, _, c in codes:
        if int(num) > max_code:
            p.set(custom_size=True, width=2, height=4)
            p.text('  Код подтверждения %s\n' % num)
            p.barcode(c, 'EAN13', height=192, width=6, pos='off')
            p.set(custom_size=False)
            p.text('  ')
            p.set(custom_size=True, width=3, height=2)
            p.text('%s %s %s\n' % (c[0], c[1:7], c[7:]))
            p.cut()
            max_code = int(num)
