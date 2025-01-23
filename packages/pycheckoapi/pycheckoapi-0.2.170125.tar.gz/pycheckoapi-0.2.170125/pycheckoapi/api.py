from requests import get
from pycheckoapi.exceptions import MessageException
from json import dump


    
def save(json,filename): 
    with open(f"{filename}.json",'w',encoding="utf-8") as json_file:
        dump(json,json_file,ensure_ascii=False)

def parse(func):
    def wrapper():
        request = func()
        for i in request:
            print(f"> | {i}:{request[i]}")
    return wrapper

def is_connection_secure(connection): 
    if connection or connection is None:
        return "https"
    else:
        return "http"
             
def message(meta):  
    try:
        if not meta['message']:
            return True
        else:
            raise MessageException(msg=meta['message'])
    except KeyError:
        pass
          
class Checko:
    def __init__(self, method:str, api_key:str, parameters:str,
                 id:str, secure_connect = None): 
        
        self.secure_connect = is_connection_secure(connection=secure_connect)
        self.method = method
        self.api_key = api_key
        self.parameters = parameters
        self.id = id
        self.URL = f"{self.secure_connect}://api.checko.ru/v2/{self.method}?key={self.api_key}&{self.parameters}={self.id}&source=true"
        self.request = get(self.URL)
        self.msg = message(self.request.json()["meta"])

    def json(self,request):
        return request.json()
        
    def data(self,request):
        return request.json()['data']
    
    def source(self,request):
        return request.json()["source_data"]

    def meta(self,request):
        return request.json()['meta']
    
    def get_request_count(self,request):
        return request.json()['meta']['today_request_count']
    
    def get_balance(self,request):
        return request.json()['meta']['balance']

    def status_code(self,request):
        return request.status_code
    

class Search:
    def __init__(self,api_key,by:str,obj:str,query,region = None,okved = None, opf = None,
                 active = None, limit = None, page = None,secure_connect = None):
        
        self.secure_connect = is_connection_secure(connection=secure_connect)
        self.api_key = api_key
        self.by = by
        self.obj = obj
        self.query = query
        self.region = region
        self.okved = okved
        self.opf = opf
        self.active = active
        self.limit = limit
        self.page = page

        self.URL = get(f"{self.secure_connect}://api.checko.ru/v2/search?key={self.api_key}&by={self.by}&obj={self.obj}&query={self.query}")

        if region is not None: self.URL = self.URL + f"&region={self.region}"
        if okved is not None and by != "okved": self.URL = self.URL + f"&okved={self.okved}"
        if opf is not None and by != "name" and obj != "ent": self.URL = self.URL + f"&opf={self.opf}"
        if active is not None: self.URL = self.URL + f"&active={self.active}"
        if limit is not None: self.URL = self.URL + f"&limit={self.limit}"
        if page is not None: self.URL = self.URL + f"&page={self.page}"
        
        self.request = get(self.URL)
        
    def default_parse(self,request):
        js = request.json()
        m = js["meta"]
        if self.b.message(meta=m):
            d = js["data"]
            for i in d:
                print(f"> | {i}:{d[i]}")

class Person:
    def __init__(self,api_key,inn,secure_connect = None):
        self.api_key = api_key
        self.inn = inn
        self.secure_connect = is_connection_secure(connection=secure_connect)
        self.URL = f"{self.secure_connect}://api.checko.ru/v2/person?key={self.api_key}&inn={self.inn}"
        self.request = get(self.URL)

    def json(self,request):
        return request.json()

    def data(self,request):
        return request.json()["data"]

    def ceo(self,request):
        for i in request.json()['data']["Учред"]:
            return i

        
class Finances:
    """ TODO:
    возможность выбора года отчётности
    """
    def __init__(self,api_key,parameter,id,extended = None,secure_connect = None):
        self.secure_connect = is_connection_secure(connection=secure_connect)
        self.api_key = api_key
        self.parameter = parameter
        self.id = id 
        self.extended = extended
        self.URL = f"{self.secure_connect}://api.checko.ru/v2/finances?key={self.api_key}&{self.parameter}={self.id}"
        if self.extended is True: self.URL = self.URL + "&extended=true"
        self.request = get(self.URL)


    def json(self,request):
        return request.json()
    
    def company(self,request):
        return request.json()["company"]
    
    def links(self,request):
        return request.json()["bo.nalog.ru"]["Отчет"]
    
    def meta(self,request):
        return request.json()["meta"]

    def data(self,request):
        return request.json()["data"]

