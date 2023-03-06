from dataclasses import dataclass
from loguru import logger
import sys
import base64
class data_cl:
    string:str=None
    login:str=None
    dis_pass:str=None
    dis_new_pass:str=None
    user_agent:str=None
    email_pass:str=None
    token:str=None
    clear_sessions:bool=False
    verif_mail:bool=False
    servers:list=None
    def __init__(self, string:str) -> None:
        self.string = string
        if string.count('|') ==2:
            self.user_agent, string_n, self.servers = string.split('|')[0], string.split('|')[1:]
        elif string.count('|') ==1:
            self.user_agent, string_n = string.split('|')[0], string.split('|')[1]
        else:string_n = string
        spl_string = string_n.split(':')
        count_true_false = ctf=  string.count('true') + string.count('false')
        lenght = ln = len(spl_string)
        if ln == 1 +ctf:
            self.token = spl_string[0]
        elif ln == 3 +ctf:
            self.login, self.dis_pass,self.email_pass  = spl_string[:-ctf] if ctf >0 else spl_string
        elif ln == 4 +ctf:
            self.login, self.dis_pass,self.email_pass, self.dis_new_pass  = spl_string[:-ctf] if ctf >0 else spl_string
            try:
                check_token = base64.b64decode(self.dis_new_pass.split('.')[0].encode('utf-8')[:-2])
                int(check_token)
                self.token = self.dis_new_pass
                self.dis_new_pass = None
            except:pass
        elif ln == 5 +ctf:
            self.login, self.dis_pass,self.email_pass, self.dis_new_pass,self.token  = spl_string[:-ctf] if ctf >0 else spl_string
        else:
            logger.error(f'Ошибка ввода данных: {string}')
            sys.exit()
        self.get_params(spl_string, ctf)
        if self.verif_mail and not self.email_pass:
            logger.error(f'Указано подтверждение почты, но не указан пароль от почты.\n{string}')
            sys.exit()
        if self.clear_sessions and not self.dis_pass:
            logger.error(f'Указана чистка сессий, но не указан пароль от дса.\n{string}')
            sys.exit()
    def get_params(self, spl_string:str, ctf:int) ->None:
        if ctf ==1:
            self.clear_sessions = spl_string[-1].lower() == 'true'
            self.verif_mail = False
        elif ctf ==0:
            self.clear_sessions = False
        else:
            self.clear_sessions = spl_string[-2].lower() == 'true'
            self.verif_mail = spl_string[-1].lower() == 'true'