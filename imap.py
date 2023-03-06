# -*- coding: utf-8 -*-
import imaplib
import email
from time import time
import asyncio
from bs4 import BeautifulSoup
async def msg_get(mail):
    status, msg = mail.select("inbox")
    status, msg2 = mail.select("Spam")
    return msg, msg2
async def imap(login_rambler, password_rambler, msg_count = False, messages = None):
    try:mail = imaplib.IMAP4_SSL('imap.rambler.ru')
    except:mail = imaplib.IMAP4_SSL('imap.rambler.ru')
    #print(f'{login_rambler} --- {password_rambler}')
    mail.login(user = login_rambler, password = password_rambler)
    mail.list()
    if msg_count:
        status, messages = mail.select('inbox')
        status, messages2 = mail.select('Spam')
        return [messages, messages2]
    
    if messages != None:
        c = time()
        msg, msg2 = await msg_get(mail)
        while msg[0] == messages[0][0] and msg2[0] == messages[1][0]:
            if time() - c > 60:
                raise
            msg, msg2 = await msg_get(mail)
        if not msg[0] == messages[0][0]:
            numOfMessages = int(msg[0])  
            status, msg = mail.select("inbox")       # get number of messages
        else:
            numOfMessages = int(msg2[0])
            status, msg = mail.select("Spam")  
        res,msg = mail.fetch(str(numOfMessages), "(RFC822)")  # fetches email using ID
        for response in msg:
            if isinstance(response, tuple):
                #print(response)
                msg = email.message_from_bytes(response[1])
                #sp_view = BeautifulSoup(msg, 'html.parser')
                #print(str(msg))
                return str(msg).split('''bgcolor=3D"#5865f2"><a href=3D"''')[1].split('"')[0].replace('=\n', '').replace('upn=3D', 'upn=')
# msgs = imap(*'3gpf02dxrv@rambler.ru:16!u@o@7@32PPCuxR@wM'.split(':'),msg_count=True)
# print(msgs)
# mails = '''Andersonqcd@rambler.ru:herRUV214
# Martinx2k@rambler.ru:ybmBCP94!
# Parkerieq@rambler.ru:bviVUL72!
# Lopezn9j@rambler.ru:gsmSAH331
# Williams1rs@rambler.ru:oloMPD378
# Kingyme@rambler.ru:hseCEI598
# Lopez54o@rambler.ru:zxtQGK582
# Millerxmm@rambler.ru:pfuAVD37!
# Mitchell1zv@rambler.ru:lfbLOP727
# Taylor78q@rambler.ru:qbjSAC955
# Harris52l@rambler.ru:akpGLP939
# Robinsoni4v@rambler.ru:fodZIT6!5
# Youngkuv@rambler.ru:ptmVVO778
# Millerhku@rambler.ru:uatZSW893
# Davis6um@rambler.ru:aroAJN274
# Gonzalezys9@rambler.ru:grnSAM614
# Leewa2@rambler.ru:aglYHS962
# Martinezqv7@rambler.ru:xzcDQI866
# Martinez4yd@rambler.ru:vnbCPC279
# Parkerop7@rambler.ru:mryAWT951'''
# for mail in mails.split('\n'):
#     try:
#         asyncio.run(imap(*mail.split(':'), msg_count=True))
#         print(mail)
#     except:pass