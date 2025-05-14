import requests
import json
import copy
import time
from video import Video
from proxies import get_proxies,get_headers
from mydb import mydb

class Up():
    """up主类"""
    def __init__(self,mid:str="0") -> None:
        self.mid=mid
        self.name=""#姓名
        self.sex=""#性别
        self.sign=""#签名，最长60个字符
        self.rank=""#用户权限等级
        self.level=0#用户等级,0-6
        self.silence=0#封禁状态,0：正常,1：被封
        self.fans_badge=False#是否具有粉丝勋章
        self.vip=""#会员信息，0：无，1：月大会员，2：年度及以上大会员
        self.birthday=""#生日,MM-DD,如设置隐私为空
        self.school=""#学校
        self.is_senior_member=""#是否为硬核会员,0：否,1：是
        self.official=""#认证类型,-1：无,0：个人认证,1：机构认证
        self.official_title=""#认证信息
        
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
        
        self.videolike=0#视频总获赞数量

        self.replyemo=0#评论情感
        self.danmakuemo=0#弹幕情感
        self.updaterate=0#视频投稿频率，单位小时
        self.avg_duration=0#视频平均长度，单位分钟
        self.tlist=[]#投稿视频分区统计,dict,存数据库转json
        self.videolist=[]#视频列表（10以内）
        
        
        if self.inis():
            print('该up已存在数据库中')
            self.mid="-2"
            return None
        self.get_info()
        if self.mid=="-1" or self.mid=="-2":
            print("未获取到该up")
            return None
        self.get_stat()
        if self.mid=="-1" or self.mid=="-2":
            print("未获取到该up")
            return None
        self.get_videolike()
        self.get_follow()
        self.get_videolist()
        # self.save_videolist()
         
    def get_info(self):
        """初始化up主基本信息"""
        def get_data(mid):
            data=None
            try:
                url=f"http://api.bilibili.com/x/space/acc/info?mid={mid}&jsonp=jsonp"
                response=requests.get(url=url,headers=get_headers(),proxies=get_proxies(),verify=False,timeout=3)
                # print("获取用户信息",response.text)
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
        for iii in range(5):
            if data!=-1:
                break
            data=get_data(mid)
        
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
    
    def get_follow(self):
        """初始化up主关注数与粉丝数"""
        def get_data(mid):#容错处理
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
            #获取失败，继续获取，最多获取6次
            if data!=-1:
                break
            data=get_data(mid)
        self.following=data['following']#关注数
        self.follower=data['follower']#粉丝数
    
    def get_stat(self):
        """初始化up主追番，投稿状态"""
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
            #如果获取失败，则继续获取，最多获取6次
            if data!=-1:
                break
            data=get_data(mid)
        self.video=data['video']#投稿视频数
        if int(self.video)<1:
            self.mid="-1"
            print("该用户不是up主")
            return None
        self.bangumi=data['bangumi']#追番数
        self.cinema=data['cinema']#追电影数
        self.channel=data['channel']['master']#关注频道数
        self.favourite=data['favourite']['master']#收藏夹数数
        self.tag=data['tag']#关注TAG数
        self.article=data['article']#投稿专栏数
        self.album=data['album']#投稿相簿数
        self.audio=data['audio']#投稿音频数
        self.pugv=data['pugv']#投稿课程数
    
    def get_videolike(self):
        def get_like_num(mid):
            try:
                url=f"http://api.bilibili.com/x/web-interface/card?mid={mid}&jsonp=jsonp"
                response=requests.get(url=url,headers=get_headers(),proxies=get_proxies(),verify=False,timeout=3)
                like_num=json.loads(response.text)['data']['like_num']
                return like_num
            except:
                return -1
        mid=self.mid
        like_num=get_like_num(mid)
        for iii in range(6):
            if like_num!=-1:
                break
            like_num=get_like_num(mid)
        self.videolike=like_num

    def save_videolist(self):
        """初始化up主视频列表"""
        def get_videodata(mid,videonum):
            datalist=None
            try:
                url=f"http://api.bilibili.com/x/space/wbi/arc/search?mid={mid}&pn=1&ps={videonum}&order=pubdate&tid=0&"
                response=requests.get(url=url,headers=get_headers(),proxies=get_proxies(),verify=False,timeout=3)
                datalist=json.loads(response.text)['data']['list']
                if len(datalist['vlist'])==0:
                    return None#没有投稿视频
            except:
                return -1#数据获取失败
            return datalist
            
        mid=self.mid
        videonum=self.video#视频数量
        if videonum<1:
            self.mid="-1"
            print("该用户不是up主")
            return None
        if videonum>6:#限制到最近6个视频
            videonum=6
        
        datalist=[]
        for iii in range(6):
            #如果没得到数据就一直循环到读到数据为止(为了防止死循环，循环5次结束)
            datalist=get_videodata(mid,videonum)
            if datalist==None:
                return -2#空数据
            if datalist!=-1:
                break
        
        if type(datalist)==type(1):
            self.mid="-1"
            print("未获取到该up数据")
            return None
        
        vlist=datalist['vlist']
        tlist=datalist['tlist']
        
        self.tlist=[val for key,val in tlist.items()]
        aidlist=[val['aid'] for val in vlist]
        
        for aid in aidlist:
            v=Video(aid,get=True)
            for iii in range(3):
                #如果没得到数据就一直循环到读到数据为止(为了防止死循环，循环5次结束)
                if v.aid!="-1":
                    break
                v=Video(aid,get=True)
            if v.aid=="-1":
                continue
            v.save()

    def get_videolist(self):
        """初始化up主视频列表"""
        def get_videodata(mid,videonum):
            datalist=None
            try:
                url=f"http://api.bilibili.com/x/space/wbi/arc/search?mid={mid}&pn=1&ps={videonum}&order=pubdate&tid=0&"
                response=requests.get(url=url,headers=get_headers(),proxies=get_proxies(),verify=False,timeout=3)
                datalist=json.loads(response.text)['data']['list']
                if len(datalist['vlist'])==0:
                    return None#没有投稿视频
            except:
                return -1#数据获取失败
            return datalist
            
        mid=self.mid
        videonum=self.video#视频数量
        if videonum<1:
            self.mid="-1"
            print("该用户不是up主")
            return None
        if videonum>6:#限制到最近6个视频
            videonum=6
        
        datalist=[]
        for iii in range(6):
            #如果没得到数据就一直循环到读到数据为止(为了防止死循环，循环5次结束)
            datalist=get_videodata(mid,videonum)
            if datalist==None:
                return -2#空数据
            if datalist!=-1:
                break
        
        if type(datalist)==type(1):
            self.mid="-1"
            print("未获取到该up数据")
            return None
        
        vlist=datalist['vlist']
        tlist=datalist['tlist']
        
        self.tlist=[val for key,val in tlist.items()]
        aidlist=[val['aid'] for val in vlist]
        
        for aid in aidlist:
            v=Video(aid,get=True)
            for iii in range(3):
                #如果没得到数据就一直循环到读到数据为止(为了防止死循环，循环5次结束)
                if v.aid!="-1":
                    break
                v=Video(aid,get=True)
            if v.aid=="-1":
                continue
            # video_dict=copy.copy(v.__dict__)#将视频数据字典化
            # self.videolist.append(video_dict)#将视频数据添加到视频列表中
            self.videolist.append(v)#将视频对象添加到列表
            v.save()
            # print(video_dict)
        
        updatelist=[]
        durationlist=[]
        
        if len(self.videolist)<1:
            self.mid="-1"
            print("获取视频列表失败，该用户不是up主")
            return None

        for v in self.videolist:
            updatelist.append(int(v.pubdate))
            durationlist.append(int(v.duration))
        
        self.avg_duration=0
        updatetimelist=[]
        updatetimelist.append(int(time.time())-updatelist[0])
        if len(updatelist)>1:
            for i in range(len(updatelist)-1):
                updatetime=updatelist[i]-updatelist[i+1]
                updatetimelist.append(updatetime)
            

        if len(updatetimelist)>3:
            self.avg_duration=(sum(durationlist)-min(durationlist)-max(durationlist))/(len(durationlist)-2)/60
            self.updaterate=(sum(updatetimelist)-min(updatetimelist)-max(updatetimelist))/(len(updatetimelist)-2)/3600
        else:
            self.avg_duration=(sum(durationlist)/len(durationlist))/60
            self.updaterate=(sum(updatetimelist)/len(updatetimelist))/3600
        self.updaterate=int(self.updaterate*10000)/10000
        self.avg_duration=int(self.avg_duration*10000)/10000
        if self.updaterate >347905:#2009-09-09 09:09:09大于b站发布的第一个视频
            self.updaterate=0
        
        # 获取视频所有情感
        # replyemo_zero=0
        # danmakuemo_zero=0
        # for v in self.videolist:
        #     if v.replyemo==0:
        #         replyemo_zero+=1
        #     if v.danmakuemo==0:
        #         danmakuemo_zero+=1
        #     self.replyemo+=v.replyemo#叠加评论总值
        #     self.danmakuemo+=v.danmakuemo#叠加弹幕总值
        #     updatelist.append(int(v.pubdate))
        #     durationlist.append(int(v.duration))
        # if self.replyemo!=0:
        #     #标准化，且保留到小点后4位
        #     self.replyemo=(self.replyemo/(len(self.videolist)-replyemo_zero)*10000)//1/10000
        # if self.danmakuemo!=0:
        #     #标准化，且保留到小点后4位
        #     self.danmakuemo=(self.danmakuemo/(len(self.videolist)-danmakuemo_zero)*10000)//1/10000

    def inis(self):
        return mydb.get_where_is('up',{
            'mid':self.mid,
            'upsqldate':time.strftime('%Y-%m-%d',time.localtime())
        })
            
    def save(self):
        # for v in self.videolist:
        #     v.save()
        if self.mid=="-1":
            print('该数据为空')
            return None
        if self.mid=="-2":
            print('该up已保存在数据库中')
            return None
        if self.inis():
            print('该up已存在数据库中')
            return None
        
        self.videolist=[]
        data_dict=self.__dict__
        del data_dict['videolist']
        data_dict['tlist']=json.dumps(data_dict['tlist'])
        print(data_dict)
        mydb.insert_into('up',data_dict)


# up=Up('378851290')
# up.save()

# print(json.dumps(up.__dict__))
