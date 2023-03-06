from data_class import data_cl
import traceback
import discord
import asyncio
from discord.http import HTTPClient
from imap import imap
from loguru import logger
class methods:
    result:dict
    servers:list
    guilds:list[discord.Guild]
    data:data_cl
    user:discord.User
    http:HTTPClient
    avatars_q:asyncio.Queue
    homeDir:str
    close:discord.Client.close
    async def check_servers(self,ns:bool=False):
        if ns:return ''
        if self.servers:
            counter_server = 1
            for id in self.servers:
                id = int(id)
                suc = False
                for i in self.guilds:
                    if int(i.id) == id:
                        self.result[f'Server{counter_server}'] = 'Подписан'
                        suc = True
                        break
                if not suc: self.result[f'Server{counter_server}'] = ('Не подписан')
                counter_server +=1
    async def change_pass(self,ns:bool=False):
        if ns:
            self.result['Пароль'] = 'Не изменён'
            return ''
        if self.data.dis_new_pass and not('принудительный пароль' in self.result.keys()):
            answer = await self.http.change_password(old_password=self.data.dis_pass, new_password=self.data.dis_new_pass)
            self.http.token = answer['token']
            self.result['Пароль'] = 'Изменён'

    async def change_avatar(self,ns:bool=False):
        if ns:return ''
        if not self.user.avatar:
            if not self.avatars_q.empty():
                avatar = await self.avatars_q.get()
                with open(f'{self.homeDir}\\avatars\\{avatar}', 'rb') as file:
                    img = file.read()
                img = discord.utils._bytes_to_base64_data(img)
                res = await self.http.change_avatar(base64_image=img)
                self.result['Avatar'] = 'Проставлен' if self.user.avatar else 'Не проставлен'
            else:self.result['Avatar'] = 'Закончились'
    async def clear_sessions(self, ns:bool=False):
        if ns:self.result['Удаление старых сессий'] = 'Не успешно'
        if self.data.clear_sessions and self.data.dis_pass and not('принудительный пароль' in self.result.keys()):
                ans = await self.http.remove_all_sessions(password=self.data.dis_pass)
                self.result['Удаление старых сессий'] = 'удалены '
                
    async def fetch_user_m(self,ns:bool=False):
        if ns:return ''
        if 'Повторный вериф почты' in self.result.keys():
            if self.result['Повторный вериф почты'] == 'Почта' and self.data.email_pass and self.data.verif_mail:
                raise
            else: return ''
        await self.fetch_user_profile(self.user.id)
    async def mail_verif(self,ns:bool=False):
        if ns:
            return ''
        if 'Повторный вериф почты' in self.result.keys():
            val = self.result['Повторный вериф почты']
            if val == 'повторный вериф тел':
                return 'Snos'
            resp = None
            if val == 'Почта' and self.data.verif_mail:
                msgs = await imap(login_rambler=self.data.login, password_rambler=self.data.email_pass, msg_count=True)
                await self.http.resend_verify()
                url = await imap(login_rambler=self.data.login, password_rambler=self.data.email_pass, messages=msgs)
                
                resp = await self.http.mail_verify(url, v2=True)
                self.result['Повторный вериф почты'] = 'Пройден'
            elif val == 'Почта' and not self.data.verif_mail:
                for i in self.result.keys():
                    self.result[i] = val
                return 'Snos'