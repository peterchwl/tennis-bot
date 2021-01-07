import secrets
from datetime import datetime, timedelta

class gettoken:
    # the token will expire in {expire} datetime object
    # self.expire is the numebr of hours
    def __init__(self, expire="24"):
        # self.__ogtime = datetime.now()
        # self.__status = True
        # self.expire = expire
        self.gettoken = secrets.token_hex(4)
    # returns boolean if the token is valid or not
    # true == valid
    # false == not valid
    # def status(self):
    #     if self.expire:
    #         self.__status = datetime.now() < self.__ogtime + timedelta(hours = float(self.expire))
    #     return self.__status
    # # blacklists the token 
    # def blacklist(self):
    #     self.expire = ""
    #     self.__status = False
    # 
    # def printtoken(self):
    #     return self.gettoken

# print(datetime.now() < datetime.now() + timedelta(hours = float("0.0001")))
# global counter
# def
#     counter = 0
#     token{counter} = token(expire='1')
#     counter+=1
# print(token.token)
# print(token.status())
# token.blacklist()
# print(token.status())
