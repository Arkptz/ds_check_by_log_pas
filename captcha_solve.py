import imp
import discord
from loguru import logger
from time import sleep
import requests
import aiohttp
class CaptchaSolver(discord.CaptchaHandler):
    async def fetch_token(self, data: dict, proxy: str, proxy_auth: aiohttp.BasicAuth, token, tries, location:str=None) -> str:
        dop_info = f'при {location}' if location else ''
        logger.debug(f'{proxy} - Решение капчи {dop_info}... попытка №{int(tries) +1}')
        logger.info(f'Решение капчи {dop_info}... попытка №{int(tries) +1}')
        #print(data)
        #rq = data['captcha_rqtoken']
        proxy = proxy.replace('http://', '').replace('https://', '')
        params = {
            'key': 'ac6655347ad8d033e3e5f2f5fd74e846',
            'method': 'hcaptcha',
            'sitekey': data['captcha_sitekey'],
            'pageurl':'https://discord.com/app/@me',
            # 'proxy':f'{proxy_auth.login}:{proxy_auth.password}@{proxy}',
            # 'proxytype':'HTTP'
            }
        if 'captcha_rqdata' in data.keys():
            params['data'] = data['captcha_rqdata']
            params['invisible'] =  1
        gg = True
        key = ''
        while gg == True:
            try:
                async with aiohttp.request('GET', 'http://rucaptcha.com/in.php', params=params) as resp:
                    id = await resp.text()
            except:continue
            id = id.split('|')[1]
            logger.debug(f'{proxy} - Решение капчи {dop_info}... id - {id}')
            while True:
                params_2 = {
                    'key': 'ac6655347ad8d033e3e5f2f5fd74e846',
                    'action': 'get',
                    'id': id
                }
                try:
                    async with aiohttp.request('GET', 'http://rucaptcha.com/res.php', params=params_2) as resp:
                        txt = await resp.text()
                except:continue
                sleep(3)
                #print(txt)
                logger.debug(f'{proxy} - Ответ по капче - {txt}')
                if txt != 'CAPCHA_NOT_READY':
                    try:
                        key = txt.split('|')[1]
                    except:
                        break
                    gg = False
                    break
        return key