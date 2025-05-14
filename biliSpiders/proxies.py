import requests
import random
import json
import re
from fake_useragent import UserAgent
from config import config

ua = UserAgent()
def get_headers()->dict:
    """获取随机headers"""
    headers={
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Cookie":config['cookie'],
        "User-Agent":ua.random,
    }
    return headers

def post_httpips()->str:
    """获取代理ip池"""
    print("[代理ip池]正在初始化代理ip池……")
    ips=[]
    url="http://代理ip池api"
    response=requests.get(url=url,headers=get_headers(),verify=False,timeout=10)
    result = json.loads(response.text)['ips']
    print(result)
    for index,ht in enumerate(result):
        try:
            proxies={
                'http':f'http://{ht}',
            }
            response=requests.get(url='http://httpbin.org/ip',proxies=proxies,verify=False,timeout=2)
            origin=json.loads(response.text)["origin"]
            ips.append(ht)
        except:
            print(f"[代理ip池]进度:{index+1}/{len(result)}")
    print(f"[代理ip池]共获取{len(ips)}可使用ip")
    url="http://服务器地址/proxies/addip.php"
    response=requests.post(url=url,data={"ips":'||'.join(ips)},verify=False,timeout=10)
    if response.text=="2333" or response.text=="":
        print(f"[代理ip池]上传ip失败,{response.text}")
    return '||'.join(ips)


def verify_httpips()->None:
    """验证代理ip池"""
    ips=[]
    url="http://服务器地址/proxies/getip.php"
    response=requests.get(url=url,verify=False,timeout=10)
    tmp_ips=response.text

    try:
        ips=tmp_ips.split('||')
    except:
        ips=[]

    for index,ht in enumerate(ips):
        try:
            proxies={
                'http':f'http://{ht}',
            }
            response=requests.get(url='http://httpbin.org/ip',proxies=proxies,verify=False,timeout=2)
            origin=json.loads(response.text)["origin"]
            print(ht)
        except:
            print(f"[代理ip池]进度:{index+1}/{len(ips)}")
    print(f"[代理ip池]共获取{len(ips)}可使用ip")

def get_httpips()->list:
    """获取代理ip池"""
    ips=[]
    url="http://服务器地址/proxies/getip.php"
    response=requests.get(url=url,verify=False,timeout=10)
    tmp_ips=response.text

    if tmp_ips=="" or tmp_ips==None:
        try:
            tmp_ips=post_httpips()
        except Exception as e:
            print(f"[代理ip池]获取异常,{e}")
            tmp_ips=""
    
    try:
        ips=tmp_ips.split('||')
    except:
        ips=[]
    
    if ips=="":
        ips=[]
    print(f"[代理ip池]ip数量:{len(ips)}")
    return ips
    

httpips=get_httpips()

def get_proxies()->dict:
    """获取随机proxies"""
    if len(httpips)==0 :
        return {}
    if httpips[0]=="" or httpips[0]==None:
        return {}
    
    httpip=random.choice(httpips)
    proxies={
        'http':f'http://{httpip}',
        'https':f'https://{httpip}'
    }
    return proxies
