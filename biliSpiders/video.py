import requests
import time
from snownlp import SnowNLP
import json
from bs4 import BeautifulSoup
from proxies import get_proxies,get_headers
from mydb import mydb

class Video:
    """视频类"""
    def __init__(self,aid:str="-1",bvid:str="",get:bool=False) -> None:
        self.aid=aid#视频avid
        self.bvid=bvid#视频bvid
        self.videos=0#包含视频数量
        self.tid=0#分区id
        self.tname=""#分区名字
        self.copyright=0#版权标志
        self.title=""#视频标题
        self.pubdate=0#发布时间
        self.ctime=0#创建时间
        self.videodesc=""#视频简介
        self.duration=0#视频简介
        
        self.mid=0#up主mid
        # self.name=""#up主名字
        
        self.view=0#视频观看量
        self.danmaku=0#视频弹幕量
        self.reply=0#视频评论量
        self.favorite=0#视频收藏量
        self.coin=0#视频投币量
        self.share=0#视频分享量
        self.videolike=0#视频点赞量
        self.width=0#视频宽度
        self.height=0#视频高度
        
        self.cid=0#视频弹幕cid
        
        # self.danmakuemo={#弹幕情绪
        #     "positive":0,#正面
        #     "negative":0,#负面
        #     "neutral":0,#中立
        #     "sum":0#情绪总值
        # }
        # self.replyemo={#评论情绪
        #     "positive":0,#正面
        #     "negative":0,#负面
        #     "neutral":0,#中立
        #     "sum":0#情绪总值
        # }
        self.danmakuemo=0
        self.replyemo=0

        if self.inis():
            print('该视频已存在数据库中')
            if get:
                print('获取数据库中视频数据')
                info=self.get()
                self.pubdate=info['pubdate']
                self.duration=info['duration']
            self.aid="-2"
            return None
        try:
            self.get_info()
        except:
            self.aid="-1"
            print("未获取到该视频")
            return None
        # self.get_danmakuemo()
        # self.get_replyemo()
        
    def get_info(self):
        def get_data(aid,bvid):
            try:
                url=f"http://api.bilibili.com/x/web-interface/view?aid={aid}&bvid={bvid}"
                response=requests.get(url=url,headers=get_headers(),proxies=get_proxies(),verify=False,timeout=3)
                # print('视频信息',response.text)
                data=json.loads(response.text)['data']
                return data
            except:
                return -1

        aid=self.aid
        bvid=self.bvid
        if aid=="-1" and bvid=="":
            return None
        data=get_data(aid,bvid)
        for iii in range(6):
            if data!=-1:
                break
            data=get_data(aid,bvid)
        
        if data==-1:
            self.aid="-1"
            return None

        self.aid=data['aid']#视频avid
        self.bvid=data['bvid']#视频bvid
        self.cid=data['cid']#视频弹幕cid
        self.videos=data['videos']#包含视频数量
        self.tid=data['tid']#分区id
        self.tname=data['tname']#分区名字
        self.copyright=data['copyright']#版权标志
        self.title=data['title']#视频标题
        self.pubdate=data['pubdate']#发布时间
        self.ctime=data['ctime']#创建时间
        self.videodesc=data['desc']#视频简介
        self.duration=data['duration']#视频简介
        
        self.mid=data['owner']['mid']#up主mid
        # self.name=data['owner']['name']#up主名字
        
        self.view=data['stat']['view']#视频观看量
        self.danmaku=data['stat']['danmaku']#视频弹幕量
        self.reply=data['stat']['reply']#视频评论量
        self.favorite=data['stat']['favorite']#视频收藏量
        self.coin=data['stat']['coin']#视频投币量
        self.share=data['stat']['share']#视频分享量
        self.videolike=data['stat']['like']#视频点赞量
        
        self.width=data['dimension']['width']#视频宽度
        self.height=data['dimension']['height']#视频高度
        
        
    def get_replyemo(self):
        """初始化评论情绪"""
        def get_replylist(aid,pagenum:int)->list:
            #获取指定页数评论
            replies=[]
            try:
                url=f"http://api.bilibili.com/x/v2/reply?type=1&oid={aid}&sort=1&nohot=0&ps=40&pn={pagenum}"
                response=requests.get(url=url,headers=get_headers(),proxies=get_proxies(),verify=False,timeout=3)
                replies=json.loads(response.text)['data']['replies']
                replies=[reply['content']['message'] for reply in replies]
                #文本清理[doge]
            except:
                replies=[]
            return replies
        
        def get_replynum(aid)->int:
            #获取所有评论数量
            replynum=-1
            try:
                url=f"http://api.bilibili.com/x/v2/reply?type=1&oid={aid}"
                response=requests.get(url=url,headers=get_headers(),proxies=get_proxies(),verify=False,timeout=3)
                replyData=json.loads(response.text)['data']
                code=json.loads(response.text)['code']
                if int(code)==12002:
                    return -2
                replynum=int(replyData['page']['count'])
                size=int(replyData['page']['size'])
                if replynum==0:
                    return -2
                rnum=len(replyData['replies'])
                if rnum<2:
                    return -2
                if size>rnum:
                    replynum=rnum
            except:
                replynum=-1
            return replynum
        
        # self.replyemo={
        #     "positive":0,#正面
        #     "negative":0,#负面
        #     "neutral":0,#中立
        #     "sum":0#情绪总值
        # }
        
        aid=self.aid

        replynum=-1
        replylist=[]
        for iii in range(6):
            #如果没得到数据就一直循环到读到数据为止(为了防止死循环，循环10次结束)
            replynum=get_replynum(aid)
            print(replynum)
            if replynum==-2:
                print("暂无评论")
                return -2
            if replynum!=-1:
                break
            
        
        if replynum>400:
            for pagenum in range(1,6):
                tmp_replylist=get_replylist(aid,pagenum)
                if type(tmp_replylist)=='number':
                    print("暂无评论")
                    return None
                for iii in range(5):
                    #如果没得到数据就一直循环到读到数据为止(为了防止死循环，循环10次结束)
                    if len(tmp_replylist)!=0:
                        break
                    tmp_replylist=get_replylist(aid,pagenum)
                replylist+=tmp_replylist
            for pagenum in range((replynum//40)-4,(replynum//40)+1):
                tmp_replylist=get_replylist(aid,pagenum)
                for iii in range(5):
                    #如果没得到数据就一直循环到读到数据为止(为了防止死循环，循环10次结束)
                    if len(tmp_replylist)!=0:
                        break
                    tmp_replylist=get_replylist(aid,pagenum)
                replylist+=tmp_replylist
        else:
            for pagenum in range((replynum//40)+1):
                tmp_replylist=get_replylist(aid,pagenum)
                for iii in range(5):
                    #如果没得到数据就一直循环到读到数据为止(为了防止死循环，循环10次结束)
                    if len(tmp_replylist)!=0:
                        break
                    tmp_replylist=get_replylist(aid,pagenum)
                replylist+=tmp_replylist
        print(replylist)
        if len(replylist)==0:
            print('暂无评论')
            return
        emolist=[SnowNLP(yuan).sentiments for yuan in replylist]
        # for emol in emolist:
        #     self.replyemo['sum']+=emol
        #     if emol >= 0.75:
        #         self.replyemo['positive']+=1
        #     elif 0.45 <= emol < 0.75:
        #         self.replyemo['neutral']+=1
        #     else:
        #         self.replyemo['negative']+=1
        # if self.replyemo['sum'] != 0:
        #     #标准化，且保留到小点后4位
        #     self.replyemo['sum']=(self.replyemo['sum']/len(emolist)*10000)//1/10000
        self.replyemo=(sum(emolist)/len(emolist)*10000)//1/10000
        print('[视频类]评论情绪处理完毕')
        
    def get_danmakuemo(self):
        def get_danmakulist(cid)->list:
            #获取指定视频弹幕
            danmakulist=[]
            try:
                url=f"http://api.bilibili.com/x/v1/dm/list.so?oid={cid}"
                response=requests.get(url=url,headers=get_headers(),proxies=get_proxies(),verify=False,timeout=6)
                response.encoding = 'utf-8'
                # print("弹幕信息",response.text)
                bs=BeautifulSoup(response.text,features="xml")
                source=bs.select_one('source')
                chatid=bs.select_one('chatid')
                if source==None and chatid!=None:
                    return -2
                elif source.text =="k-v":
                    danmakus=bs.select('d')
                    danmakulist=[danmaku.text for danmaku in danmakus]
                    if len(danmakulist)>400:
                        danmakulist=danmakulist[0:401]
                else:
                    return -2
            except:
                return -1
            return danmakulist
        cid = self.cid
        # self.danmakuemo={
        #     "positive":0,#正面
        #     "negative":0,#负面
        #     "neutral":0,#中立
        #     "sum":0#情绪总值
        # }
        
        danmakulist=[]
        for iii in range(6):
            #如果没得到数据就一直循环到读到数据为止(为了防止死循环，循环3次结束)
            danmakulist=get_danmakulist(cid)
            if danmakulist==-2:
                print('暂无弹幕')
                return
            if danmakulist!=-1:
                break
            
        print(danmakulist)
        if len(danmakulist)==0:
            print('暂无弹幕')
            return
        emolist=[SnowNLP(yuan).sentiments for yuan in danmakulist]
        # for emol in emolist:
        #     self.danmakuemo['sum']+=emol
        #     if emol >= 0.75:
        #         self.danmakuemo['positive']+=1
        #     elif 0.45 <= emol < 0.75:
        #         self.danmakuemo['neutral']+=1
        #     else:
        #         self.danmakuemo['negative']+=1
        # if self.danmakuemo['sum'] !=0:
        #     #标准化，且保留到小点后4位
        #     self.danmakuemo['sum']=(self.danmakuemo['sum']/len(emolist)*10000)//1/10000
        self.danmakuemo=(sum(emolist)/len(emolist)*10000)//1/10000
        print('[视频类]弹幕情绪处理完毕')
        
    def inis(self):
        return mydb.get_where_is('video',{
            'aid':self.aid,
            'upsqldate':time.strftime('%Y-%m-%d',time.localtime())
        })

    def get(self):
        return mydb.select_table("video",{
            'aid':self.aid,
            'upsqldate':time.strftime('%Y-%m-%d',time.localtime())
        })[0]

    def save(self):
        if self.aid=="-1":
            print('该数据为空')
            return None
        if self.aid=="-2":
            print('该视频已保存在数据库中')
            return None
        if self.inis():
            print('该视频已存在数据库中')
            return None
        # self.replyemo=json.dumps(self.replyemo)
        # self.danmakuemo=json.dumps(self.danmakuemo)
        data_dict=self.__dict__
        mydb.insert_into('video',data_dict)
    

# v=Video('483039191')
# v.cid='1445418'
# v.get_danmakuemo()
# v.get_replyemo()
# print(v.__dict__)
