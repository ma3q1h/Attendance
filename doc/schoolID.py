#!/usr/bin/env python
# -*- coding: utf-8 -*-
import nfc

def read_kucard(tag):
    servc = 0x1A8B
    service_code = [nfc.tag.tt3.ServiceCode(servc >> 6, servc & 0x3F)]

    tag.dump() # これがないと何故かうまくいかなかった

    bc_id = [nfc.tag.tt3.BlockCode(0)] #blockcodeの指定番号
    bd_id = tag.read_without_encryption(service_code, bc_id)
    #student_id = int(bd_id[2:10].decode("utf-8"))
    student_id = int(bd_id[2:10])

    bc_name = [nfc.tag.tt3.BlockCode(1)]
    student_name = (
        tag.read_without_encryption(service_code, bc_name)
        .decode("shift-jis")
        .rstrip("\x00")
    )

    print(student_id)
    print(student_name)
    return student_id, student_name

# タッチ時のハンドラを設定して待機する
clf = nfc.ContactlessFrontend('usb')
clf.connect(rdwr={'on-connect': read_kucard})