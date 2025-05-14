import requests
import json
import re
import copy
import time
from proxies import get_proxies,get_headers
from mydb import mydb

class Medal:
    """粉丝勋章"""
    def __init__(self,fans_medal:dict) -> None:
        self.target_id=""#粉丝勋章所属UP的mid
        self.medal_id=""#粉丝勋章id
        self.medal_name=""#粉丝勋章名字
        self.medal_color=0#粉丝勋章颜色,十进制数
        self.uid=""#此用户mid
        self.medal_level=0#粉丝勋章等级
        
        self.medal_id=fans_medal['medal_id']#粉丝勋章id
        self.target_id=fans_medal['target_id']#粉丝勋章所属UP的mid
        self.medal_name=fans_medal['medal_name']#粉丝勋章名字
        self.medal_level=fans_medal['level']#粉丝勋章等级
        self.medal_color=fans_medal['medal_color']#粉丝勋章颜色,十进制数
        self.uid=fans_medal['uid']#此用户uid

    def save(self):
        if mydb.get_where_is('medal',{
            'medal_id':self.medal_id,
            'uid':self.uid
        }):
            print('该粉丝勋章已存在数据库中')
            return None
        data_dict=self.__dict__
        mydb.insert_into('medal',data_dict)
        

class User:
    """用户类"""
    def __init__(self,mid:str="-1") -> None:
        self.mid=mid#用户mid
        self.name=""#姓名
        self.sex=""#性别
        self.sign=""#签名，最长60个字符
        self.rank=""#用户权限等级
        self.level=0#用户等级,0-6
        self.silence=0#封禁状态,0：正常,1：被封
        self.fans_badge=False#是否具有粉丝勋章,false：无,true：有
        self.vip=""#会员信息，0：无，1：月大会员，2：年度及以上大会员//1：月度大会员,3：年度大会员,7：十年大会员,15：百年大会员
        self.birthday=""#生日,MM-DD,如设置隐私为空
        self.school=""#学校
        self.is_senior_member=""#是否为硬核会员,0：否,1：是
        self.official=""#认证类型,-1：无,0：个人认证,1：机构认证
        self.official_title=""#认证信息
        self.is_fans_medal=False#是否佩戴粉丝勋章
        self.fans_medal=None#粉丝勋章信息
        
        self.following=0#关注数
        self.follower=0#粉丝数
        
        self.video=0#投稿视频数
        self.bangumi=0#追番数
        self.cinema=0#追电影数
        self.channel=0#关注频道数
        self.favourite=0#收藏夹数数
        self.tag=0#关注TAG数
        self.article=0#投稿专栏数
        self.album=0#投稿相簿数
        self.audio=0#投稿音频数
        self.pugv=0#投稿课程数
        
        self.water=0#是否为水军，0：不是，1：是
        
        if self.inis():
            print('该用户已存在数据库中')
            self.mid=="-2"
            return None
        self.get_info()
        if self.mid=="-1" or self.mid=="-2":
            print("未获取到该用户")
            return None
        self.get_follow()
        if self.mid=="-1" or self.mid=="-2":
            print("未获取到该用户")
            return None
        self.get_stat()
        # self.get_water()
        
    def get_info(self):
        """初始化用户基本信息"""
        def get_data(mid):
            data=None
            try:
                url=f"http://api.bilibili.com/x/space/acc/info?mid={mid}&jsonp=jsonp"
                response=requests.get(url=url,headers=get_headers(),proxies=get_proxies(),verify=False,timeout=3)
                print("获取用户信息",response.text)
                code=json.loads(response.text)['code']
                code=int(code)
                if code!=0:
                    if code==-404 or code==-400:
                        print("暂无该用户")
                        self.mid="-1"
                        return -2
                    else:
                        return -1
                data=json.loads(response.text)['data']
            except:
                return -1
            return data
            
        mid=self.mid
        data=get_data(mid)
        for iii in range(6):
            if data!=-1:
                break
            data=get_data(mid)
        
        if type(data)==type(1):
            self.mid="-1"
        
        if self.mid=="-1":
            return None
        
        self.name=data['name']
        self.sex=data['sex']
        self.sign=data['sign']
        self.rank=data['rank']#用户权限等级
        self.level=data['level']#用户等级
        self.silence=data['silence']#封禁状态
        self.fans_badge=data['fans_badge']#是否具有粉丝勋章
        self.vip=data['vip']['role']#会员信息，0：无，1：月大会员，2：年度及以上大会员,1：月度大会员,3：年度大会员,7：十年大会员,15：百年大会员
        self.birthday=data['birthday']#生日,MM-DD,如设置隐私为空
        if data['school']=="" or data['school']==None:
            self.school=""#学校
        else:
            self.school=data['school']['name']#学校
        self.is_senior_member=data['is_senior_member']#是否为硬核会员,0：否,1：是
        self.official=data['official']['type']#认证类型,-1：无,0：个人认证,1：机构认证
        self.official_title=data['official']['title']#认证信息
        self.is_fans_medal=data['fans_medal']['wear']#是否佩戴粉丝勋章
        if self.is_fans_medal:
            fans_medal=data['fans_medal']['medal']
            self.fans_medal=Medal(fans_medal)
        else:
            self.fans_medal=None#粉丝勋章
    
    def get_follow(self):
        """初始化用户关注数与粉丝数"""
        def get_data(mid):
            try:
                url=f"http://api.bilibili.com/x/relation/stat?vmid={mid}&jsonp=jsonp"
                response=requests.get(url=url,headers=get_headers(),proxies=get_proxies(),verify=False,timeout=3)
                data=json.loads(response.text)['data']
                return data
            except:
                return -1
        
        mid=self.mid
        data=get_data(mid)
        for iii in range(6):
            if data!=-1:
                break
            data=get_data(mid)
        
        if data==-1:
            self.mid=="-1"
            return None
        
        if not data:
            self.mid=="-1"
            return None

        self.following=data['following']#关注数
        self.follower=data['follower']#粉丝数
    
    def get_stat(self):
        """初始化用户追番，投稿状态"""
        def get_data(mid):
            try:
                url=f"http://api.bilibili.com/x/space/navnum?mid={mid}"
                response=requests.get(url=url,headers=get_headers(),proxies=get_proxies(),verify=False,timeout=3)
                data=json.loads(response.text)['data']
                return data
            except:
                return -1
        
        mid=self.mid
        data=get_data(mid)
        for iii in range(6):
            if data!=-1:
                break
            data=get_data(mid)
        
        if data==-1:
            self.mid=="-1"
            return None
        self.video=data['video']#投稿视频数
        self.bangumi=data['bangumi']#追番数
        self.cinema=data['cinema']#追电影数
        self.channel=data['channel']['master']#关注频道数
        self.favourite=data['favourite']['master']#收藏夹数数
        self.tag=data['tag']#关注TAG数
        self.article=data['article']#投稿专栏数
        self.album=data['album']#投稿相簿数
        self.audio=data['audio']#投稿音频数
        self.pugv=data['pugv']#投稿课程数

    def get_water(self):
        """初始化用户是否为水军/潜水"""
        if int(self.is_senior_member)==1 or self.fans_badge or int(self.rank)>10000 or int(self.official)>=0 or self.is_fans_medal:
            self.water=0
            return None
        
        if self.bangumi+self.cinema+self.channel+self.favourite+self.tag+self.article+self.album+self.audio+self.pugv<3:
            self.water=1
    
    def inis(self):
        return mydb.get_where_is('user',{
            'mid':self.mid
        })

    def save(self):
        """将类转为字典存储于数据库中"""
        if self.mid=="-1":
            print('该数据为空')
            return None
        if self.mid=="-2":
            print('该用户已保存在数据库中')
            return None
        if self.inis():
            print('该用户已存在数据库中')
            return None
        if self.is_fans_medal:
            self.fans_medal.save()
        if self.sex=="":
            print('该数据为空')
            return None
        data_dict=copy.copy(self.__dict__)
        del data_dict['fans_medal']
        mydb.insert_into('user',data_dict)
        





# for i in range(1000,1100):
#     user=User(f'{i}')
#     if user.mid=="-1":
#         print(f'{i},用户不存在')
#     elif user.mid=="-2":
#         print(f'{i},访问出错稍后再试')
#     else:
#         print(f'{i},用户名:{user.name}')
#         user.save()


        