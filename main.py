# -*- coding: utf-8 -*-
from discord import Client
import discord
from captcha_solve import CaptchaSolver
from loguru import logger as lg
import asyncio
import os
import sys
import pandas as pd
from colorama import Fore, init, Back, Style
import aiohttp
import traceback
from proxy import Proxy_Class
import warnings
from dataclasses import dataclass
from fake_useragent import UserAgent
import base64
from imap import imap
from time import time
import imaplib
from methods import methods
import multiprocessing
from data_class import data_cl
warnings.filterwarnings("ignore")
if getattr(sys, 'frozen', False):
    homeDir = os.path.dirname(sys.executable)
elif __file__:
    homeDir = os.path.dirname(__file__)


@dataclass(repr=True, init=False)
class status_working:
    osn = None
    verif_mail = None
    servers = None
    fetch_user = None
    sessons = None
    replace_avatar = None
    passw = None
    itog = None


class MyClient(Client, methods):
    def __init__(self, data: data_cl, servers, my_pr: Proxy_Class, *args, **kwargs):
        self.data = data
        self.my_pr = my_pr
        self.servers = servers
        self.result = {}
        self.status_working = []
        self.osn = False
        self.avatars_q = avatars_q
        self.homeDir = homeDir
        super().__init__(_ua=data.user_agent, *args, **kwargs)

    async def on_required_action_update(self, *args, **kwargs):
        # print(args[0], type(args[0]))
        # print('verify_email' in str(args[0]))
        # print('verify_phone' in str(args[0]))
        if 'verify_email' in str(args[0]):
            self.result['Повторный вериф почты'] = "Почта"
            if self.mail_verif in self.status_working:
                self.status_working.remove(self.mail_verif)
        if 'verify_phone' in str(args[0]):
            self.result['Повторный вериф почты'] = "повторный вериф тел"
            self.status_working.append(True)
            await self.close()

    async def on_ready(self):
        if not self.osn:
            self.result.update({'Nick': self.user, 'Phone': str(self.user.phone), 'Email': self.user.email,
                                'Avatar': 'есть' if self.user.avatar else 'нету'})
            self.osn = True
        logger.debug(f'{self.data.string} - Запуск цикла')
        if not self.mail_verif in self.status_working and self.data.email_pass:
            for i in range(3):
                try:
                    if await self.mail_verif() == 'Snos':
                        self.status_working.append(True)
                        return self.close()
                    self.status_working.append(self.mail_verif)
                    break
                except:
                    logger.debug(traceback.format_exc())
                    if i == 2:
                        return await self.close()
        elif not self.mail_verif in self.status_working:
            self.status_working.append(self.mail_verif)
        for func in [self.check_servers, self.fetch_user_m, self.clear_sessions, self.change_avatar, self.change_pass]:
            if (not func in self.status_working) and not (True in self.status_working):
                try:
                    if (await func()) == 'Snos':
                        self.status_working.append(True)
                    self.status_working.append(func)
                    logger.debug(
                        f'{self.data.string} -- {func.__name__} -- Успешно')
                except:
                    logger.debug(
                        f'{self.data.string} -- {func.__name__} - Ошибка в цикле')
                    try:
                        logger.debug(traceback.format_exc())
                    except:
                        pass
                    await func(ns=True)
        if len(self.status_working) == 6:
            logger.debug(f'{self.data.string} - Конец цикла')
            self.status_working.append(True)
        await self.close()
        # await self.accept_invite("mcsol")


async def dis_client(proxy: Proxy_Class, data: data_cl, ip: str):
    global excel_file
    global csv_file

    need_reset = False
    servers = data.servers
    if type_proxy == 'mobile':
        client = cl = MyClient(captcha_handler=CaptchaSolver(), data=data, servers=servers, my_pr=proxy,
                               proxy=f'http://{proxy.ip}:{proxy.port}', proxy_auth=aiohttp.BasicAuth(proxy.login, proxy.password))  # proxy = self.proxys, proxy_auth = self.proxy_auth)
    else:
        client = cl = MyClient(captcha_handler=CaptchaSolver(), data=data, servers=servers, my_pr=proxy,
                               proxy=f'http://{proxy.url_proxy}',)

    async def restore_password():
        msgs = await imap(login_rambler=data.login, password_rambler=data.email_pass, msg_count=True)
        await cl.http.reset_pas(data.login)
        url = await imap(login_rambler=data.login, password_rambler=data.email_pass, messages=msgs)
        new_pass = data.dis_new_pass if data.dis_new_pass else data.dis_pass
        resp = await client.http.mail_verify(url, v3=True, new_pass=new_pass)
        cl.result['принудительный пароль'] = new_pass
        data.dis_pass = cl.data.dis_pass = new_pass
        cl.status_working.append(cl.clear_sessions)
        cl.status_working.append(cl.change_pass)

    suc = False
    data_token = data.token
    token = data.token
    # print(token)
    for i in range(10):
        try:
            if need_reset:
                await restore_password()
                await asyncio.sleep(20)
                need_reset = False
            if not token and data.dis_pass:
                # print(f'{log} --- {pas}')
                msgs = await imap(login_rambler=data.login, password_rambler=data.email_pass, msg_count=True)
                psw = data.dis_pass if not 'принудительный пароль' in cl.result.keys(
                ) else cl.result['принудительный пароль']
                res = await client.login_by_login(login=data.login, password=psw)
                if res == 'ACCOUNT_LOGIN_VERIFICATION_EMAIL':
                    url = await imap(login_rambler=data.login, password_rambler=data.email_pass, messages=msgs)
                    # print(url)
                    resp = await client.http.mail_verify(url)
                    token = resp
                    res = await client.login_by_login(login=data.login, password=psw)
                try:
                    token = res['token']
                except:
                    # print(res)
                    token = None
                    raise
                if not data.token:
                    data_token = res['token']
                else:
                    cl.result['Принудительный токен'] = res['token']
            # await asyncio.sleep(10000)
            if data.verif_mail:
                msgs = await imap(login_rambler=data.login, password_rambler=data.email_pass, msg_count=True)
            await client.login(token=token)
            await client.connect()
            try:
                await client.close()
            except:
                pass
            if True in cl.status_working:
                logger.success(
                    f'{Fore.YELLOW}{cl.http.token}{Fore.RESET}{Fore.MAGENTA}|{proxy.port}|{Fore.RED}{ip}{Fore.RESET}|{Fore.CYAN}{cl.http.user_agent}{Fore.GREEN}|Успешно')
                end_res = 'Успешно'
            else:
                _str = ''
                for c in cl.status_working:
                    if type(c) != bool:
                        _str += c.__name__ + ' '
                logger.debug(f'Список выполненных функций: {_str}')
                raise
        except discord.errors.LoginFailure:
            # logger.error(f'{token} - невалид')
            end = f'{Fore.BLUE}|Конечный результат{Fore.RESET}' if i == 9 else ''
            logger.error(f'{Fore.YELLOW}{token}{Fore.RESET}{Fore.MAGENTA}|{proxy.port}|{Fore.RED}{ip}{Fore.RESET}|{Fore.CYAN}{cl.http.user_agent}{Fore.RED}|Попытка войти по лог\пас (если они есть){end}')
            end_res = 'невалидный токен'
            if data.dis_pass:
                token = False
                continue
            break
        except imaplib.IMAP4.error:
            end_res = 'отключён imap/неверный пас почта'
            logger.error(f'{Fore.YELLOW}{token}{Fore.RESET}{Fore.MAGENTA}|{proxy.port}|{Fore.RED}{ip}{Fore.RESET}|{Fore.CYAN}{cl.http.user_agent}{Fore.RED}|{end_res}{Fore.BLUE}|Конечный результат{Fore.RESET}')
            break
        except:
            await asyncio.sleep(5)
            tr = str(traceback.format_exc())
            if 'Login or password is invalid.' in tr:
                end_res = f'{Fore.GREEN}Смена пароля дс{Fore.RESET}' if i != 9 else f'Неверный пас дс{Fore.BLUE}|Конечный результат{Fore.RESET}'
                logger.error(
                    f'{Fore.YELLOW}{token}{Fore.RESET}{Fore.MAGENTA}|{proxy.port}|{Fore.RED}{ip}{Fore.RESET}|{Fore.CYAN}{cl.http.user_agent}{Fore.RED}|{end_res}')
                need_reset = True
                continue
                break
            elif 'Your account has been disabled.' in tr:
                end_res = 'Бан'
                logger.error(
                    f'{Fore.YELLOW}{token}{Fore.RESET}{Fore.MAGENTA}|{proxy.port}|{Fore.RED}{ip}{Fore.RESET}|{Fore.CYAN}{cl.http.user_agent}{Fore.RED}|{end_res}')
                break
            try:
                logger.debug(tr)
            except:
                pass
            if i == 9:
                logger.error(
                    f'{Fore.YELLOW}{token}{Fore.RESET}{Fore.MAGENTA}|{proxy.port}|{Fore.RED}{ip}{Fore.RESET}|{Fore.CYAN}{cl.http.user_agent}{Fore.RED}|Ошибка прокси')
                end_res = 'Ошибка прокси'
                break
            continue
        break
    cl.result['data'], cl.result['Токен'] = data.string, cl.http.token
    cop = cl.result.copy()
    errors = ['отключён imap/неверный пас почта', 'невалидный токен',
              'неверный пас дс', 'повторный вериф тел', 'Бан']
    for i in cop.values():
        if (i in errors) or (end_res in errors):
            for b in excel_file.columns.to_list():
                if b != 'data':
                    cl.result[b] = i if i in errors else end_res
            break
    if 'Принудительный токен' in cl.result.keys():
        if cl.result['Принудительный токен'] == data_token:
            del cl.result['Принудительный токен']
        elif not cl.result['Принудительный токен'] in errors:
            cl.result['data'] = cl.result['data'].replace(
                data_token, cl.result['Принудительный токен'])
    # for b in excel_file.columns.to_list():
    #     if not b in cl.result.keys():
    #         cl.result[b] = '-'
    cl.result['Итог'] = end_res
    excel_file = excel_file.append(cl.result, ignore_index=True)
    cols = excel_file.columns.to_list()
    cols.remove('Итог')
    cols.append('Итог')
    excel_file = excel_file.reindex(columns=cols)
    excel_file.to_excel(f'{homeDir}\\result.xlsx', engine='xlsxwriter')
    csv_file = csv_file.append({'data': data.string}, ignore_index=True)
    csv_file.to_csv(f'{homeDir}\\csv\\tokens_use.csv')


async def proxy_manage(proxy: Proxy_Class):
    global workers
    global thread_count
    global type_proxy
    while not tokens_queue.empty():
        counter = 0
        last_ip = '0'
        while True:
            if tokens_queue.empty():
                return ''
            try:
                ip = await proxy.check_connection(type_proxx=type_proxy)
                if ip:
                    break
            except:
                pass
        if ip == last_ip:
            counter += 1
        else:
            counter = 0
        if counter >= 3:
            break
        last_ip = ip
        with open(f'{homeDir}\\stop.txt', 'r') as file:
            if 'true' in file.read():
                break
        if workers < thread_count:
            workers += 1
            await title()
            if not tokens_queue.empty():
                token = await tokens_queue.get()
            else:
                return ''
            st_t = time()
            logger.debug(f'Запуск потока {token}')
            await dis_client(proxy, data_cl(token), ip)
            workers -= 1
            await title()
            if type_proxy == 'mobile':
                await asyncio.sleep(70-(time()-st_t))
                logger.success(await proxy.change_ip())
            await asyncio.sleep(10)


async def main():
    tasks = []
    while not proxy_queue.empty():
        tasks.append(proxy_manage(await proxy_queue.get()))
    await asyncio.gather(*tasks)


async def title():
    os.system(f'title "Кол-во потоков: {workers}|{thread_count}"')
with open(f'{homeDir}\\stop.txt', 'w') as file:
    pass
try:
    df = pd.read_excel(f'{homeDir}\\result.xlsx', index_col=0)
except:
    df = pd.DataFrame(columns=['data', 'Токен', 'Nick',
                      'Phone', 'Email', 'Avatar', 'Итог'])
    df.to_excel(f'{homeDir}\\result.xlsx')
excel_file = df
csv_file = pd.read_csv(f'{homeDir}\\csv\\tokens_use.csv', index_col=0)
tokens_queue = asyncio.Queue()
avatars_q = asyncio.Queue()
with open(f'{homeDir}/txt/tokens.txt', 'r') as file:
    df = pd.read_csv(f'{homeDir}/csv/tokens_use.csv',
                     index_col=0)['data'].to_list()
    tokens = file.readlines()
    for i in tokens:
        i = i.replace('\n', '')
        if i == '':
            continue
        if not i in df:
            tokens_queue.put_nowait(i)
df = pd.read_csv(f'{homeDir}/csv/avatar_use.csv',
                 index_col=0)['avatar'].to_list()
for i in os.listdir(f'{homeDir}\\avatars'):
    if not i in df:
        avatars_q.put_nowait(i)
workers = 0
proxy_queue = asyncio.Queue()
type_proxy = None
with open(f'{homeDir}/txt/proxy.txt', 'r') as file:
    proxys = file.readlines()
    proxy_list = [Proxy_Class(i) for i in proxys if i != '']
    type_proxy = 'mobile' if proxy_list[0].proxy_link else 'data'
    for i in proxy_list:
        proxy_queue.put_nowait(i)
# thread_count = int(input('Кол-во потоков: '))
# print(asyncio.run(proxy_queue.get_nowait().check_connection()))
if __name__ == "__main__":
    logger = lg
    logger.remove()
    logger.add(f'{homeDir}\\logs\\log_1.log', level='DEBUG', rotation='100MB')
    logger.add(sys.stderr, level='INFO')
    thread_count = int(input('Кол-во потоков: '))
    asyncio.run(main())
