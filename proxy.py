import requests
from dataclasses import dataclass
from requests.auth import HTTPProxyAuth
from time import sleep
from loguru import logger
import ssl
import traceback
import aiohttp
@dataclass(repr=True)
class Proxy_Class:
    ip:str
    port:str
    login:str
    password:str
    proxy_link:str
    def __init__(self, proxy:str, logging:str=False) -> None:
        self.ip, self.port, self.login, self.password, self.proxy_link = self.proxy_reorganize(proxy)
        self.list_data = [self.ip, self.port, self.login, self.password, self.proxy_link]
        self.proxy_default_format = f'{self.ip}:{self.port}:{self.login}:{self.password}'
        self.proxy_default_format_with_url = f'{self.ip}:{self.port}:{self.login}:{self.password}|{self.proxy_link}'
        self.url_proxy = f'{self.login}:{self.password}@{self.ip}:{self.port}' if self.password else f'{self.ip}:{self.port}'
        self.logging =logging
    def proxy_reorganize(self, proxy:str)->list[str] or None:
        if proxy == None:
            return None, None,None,None,None
        if '|' in proxy:
            proxy, proxy_link = proxy.split('|')
            proxy_link = proxy_link.replace('http://', '').replace('https://', '')
        else:proxy_link=None
        if "http" in proxy:
            proxy = proxy.split('://')[1]
        if '@' in proxy:
            log_pas, ip_port = proxy.split('@')
            login, password = log_pas.split(':')
            ip, port = ip_port.split(':')
        else:
            if len(proxy.split(':')) ==2:
                ip, port, login, password =*proxy.split(':'), None, None
            else:
                ip, port, login, password = proxy.split(':')
        return ip, port, login, password, proxy_link
    async def change_ip(self,proxy_refresh_limit=60):
        for i in range(3):
            try:
                async with aiohttp.request('GET','http://'+ self.proxy_link) as resp:
                    return await resp.text()
            except: 
                if i ==2: return False
                await asyncio.sleep(5)
    async def check_connection(self, att = 20, type_proxx='mobile'):
        for cycle_index in range(att):
            if cycle_index == att-1:
                return False
            try:
                if type_proxx =='mobile': kw ={'proxy':f'http://{self.ip}:{self.port}', 'proxy_auth':aiohttp.BasicAuth(self.login, self.password)}
                else: kw = {'proxy':f'http://{self.url_proxy}'}
                async with aiohttp.request('GET', 'http://httpbin.org/ip', **kw) as response:
                    if response.status != 200:
                        raise
                    ans =await response.json()
                    return ans['origin']
            except:
                #print(traceback.format_exc())
                await asyncio.sleep(5)
                #logger.error(f'{self.url_proxy} не отвечает...')
import asyncio
# p = Proxy_Class('91.247.170.62:57387:ta5Y27Ss:gp4VGF9D')
# print(asyncio.run(p.check_connection()))