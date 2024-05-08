import requests



class Cybersafeapi:
    def __init__(self,username=None,password=None) -> None:
        self.url = "https://store.cyber-safe.pro/"
        self.username = username 
        self.password = password
        self.User_Agent = "Bot_disfree_autolike_cybersafe"
        
    def Login(self):
        return requests.post(self.url + "api/login",json={
            "username":self.username,
            "password":self.password
        },
        headers={"User-Agent":self.User_Agent})
        
    def Me(self,Token=None):
        return requests.get(self.url + "api/me",headers={"x-token" : Token,"User-Agent":self.User_Agent})
        
    def Dtlike(self):
        return requests.get(self.url + "api/get_detali_like",headers={"User-Agent":self.User_Agent})
        
    def Buylike(self,Token,link,amount,idlike):
        return requests.post(self.url + "api/like",
            json={
                    "amount":amount,
                    "link":link,
                    "idlike":idlike
            },
            headers={"x-token" : Token,"User-Agent":self.User_Agent})
        
    def Angpao(self,Token,link):
        return requests.post(self.url + "api/topup/truemoney/angpao",
            json={
                    "link":link
            },
            headers={"x-token" : Token,"User-Agent":self.User_Agent})
        