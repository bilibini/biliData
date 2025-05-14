import requests
import time
import schedule
import threading
from uploader import Up
from video import Video
from user import User,Medal
import json
from mydb import mydb
from proxies import get_proxies,get_headers

def getMedal(mid):
    data=None
    for iii in range(6):
        try:
            url=f"http://api.bilibili.com/x/space/acc/info?mid={mid}&jsonp=jsonp"
            proxies=get_proxies()
            response=requests.get(url=url,headers=get_headers(),proxies=proxies,verify=False,timeout=3)
            print("获取用户信息",response.text)
            code=json.loads(response.text)['code']
            code=int(code)
            if code!=0:
                if code==-404 or code==-400:
                    print("暂无该粉丝勋章")
                    return -2 
                else:
                    return -1
            data=json.loads(response.text)['data']
            break
        except:
            print(f'粉丝勋章获取错误{iii}次')
        
    if data==None:
        print('未获取到数据')
        return
    is_fans_medal=data['fans_medal']['wear']#是否佩戴粉丝勋章
    if is_fans_medal:
        fans_medal=data['fans_medal']['medal']
        m=Medal(fans_medal)
        m.save()

def usersMedal():
    """为用户表中的所有用户重新获取粉丝勋章"""
    userList=mydb.get_query("SELECT mid FROM user WHERE mid not in (SELECT uid FROM medal)")
    for user in userList:
        mid=user['mid']
        getMedal(mid)
        time.sleep(10)

def getU(mid):
    u=User(mid)
    u.save()

def getV(aid):
    v=Video(aid)
    v.save()

def getUp(mid):
    up=Up(mid)
    up.save()


def getUser(aid:str='45629276',num:int=0):
    """获取视频下多个用户信息"""
    def setusers(midList):
        for mid in midList:
            u=User(mid)
            u.save()
    
    replyData=None
    for iii in range(5):
        try:
            url=f'http://api.bilibili.com/x/v2/reply?type=1&oid={aid}&sort=0&nohot=0&ps=40&pn=1'
            proxies=get_proxies()
            response=requests.get(url=url,headers=get_headers(),proxies=proxies,verify=False,timeout=3)
            code=json.loads(response.text)['code']
            if code=="-400" or code==-400:
                print("暂无该用户")
                return
            replyData=json.loads(response.text)['data']
            break
        except:
            print(f'数据获取失败{iii+1}次')

    if replyData==None:
        print('数据获取失败，结束获取')
        return
    replynum=int(replyData['page']['count'])
    if replynum<2:
        print("暂无评论")
        return
    replies=replyData['replies']
    midList=[reply['mid'] for reply in replies]
    if num!=0:
        if num>len(midList):
            num=len(midList)
        midList=midList[:(num-1)]
    setusers(midList)

def rcmdVideo(num:int=5):
    items=None
    for iii in range(4):
        try:
            url=f'http://api.bilibili.com/x/web-interface/index/top/feed/rcmd?ps={num}'
            response=requests.get(url=url,headers=get_headers(),proxies=get_proxies(),verify=False,timeout=3)
            items=json.loads(response.text)['data']['item']
            break
        except:
            print(f'视频数据获取失败{iii+1}次')
    if items==None:
        print('视频数据获取失败，结束获取')
        return
    aidList=[item['id'] for item in items]
    for aid in aidList:
        getV(aid)
        getUser(aid,2)

def randVideos(num:int=10):
    """获取并存储随机视频"""
    def setRandVideos(num):
        if num<=20:
            rcmdVideo(num)
        else:
            pnum=num//10
            for i in range(pnum):
                rcmdVideo(10)
            if num%10!=0:
                rcmdVideo(num%10)

    parnum=num//3
    t1=threading.Thread(target=setRandVideos,args=(parnum,))
    t2=threading.Thread(target=setRandVideos,args=(parnum,))
    t3=threading.Thread(target=setRandVideos,args=((parnum+(num%3)),))
    t1.start()
    t2.start()
    t3.start()
    t1.join()
    t2.join()
    t3.join()

def videosMydb():
    """获取并存储视频表中所有视频"""
    global progress,total
    def setvideos(videoList):
        global progress,total
        for video in videoList:
            aid=video['aid']
            print(f'aid:{aid},当前视频进度{progress}/{total}')
            # getUser(aid,2)#获取并存储2个用户
            getV(aid)
            progress=progress+1
            
    sqlstr=f"""
SELECT a.aid
FROM (SELECT aid FROM view_videos_group) a 
LEFT JOIN (SELECT aid FROM video WHERE `upsqldate`='{time.strftime('%Y-%m-%d',time.localtime())}' GROUP BY aid) b 
ON a.aid=b.aid
WHERE b.aid IS NULL
    """
    videoList=mydb.get_query(sqlstr)
    total=len(videoList)
    progress=0
    parnum=total//7
    t1=threading.Thread(target=setvideos,args=(videoList[:parnum],))
    t2=threading.Thread(target=setvideos,args=(videoList[parnum:parnum*2],))
    t3=threading.Thread(target=setvideos,args=(videoList[parnum*2:parnum*3],))
    t4=threading.Thread(target=setvideos,args=(videoList[parnum*3:parnum*4],))
    t5=threading.Thread(target=setvideos,args=(videoList[parnum*4:parnum*5],))
    t6=threading.Thread(target=setvideos,args=(videoList[parnum*5:parnum*6],))
    t7=threading.Thread(target=setvideos,args=(videoList[parnum*6:],))
    t1.start()
    t2.start()
    t3.start()
    t4.start()
    t5.start()
    t6.start()
    t7.start()
    t1.join()
    t2.join()
    t3.join()
    t4.join()
    t5.join()
    t6.join()
    t7.join()



def upsMydb():
    """获取并存储视频表中所有视频的up主"""
    global progress,total
    def setups(upList):
        global progress,total
        for uper in upList:
            getUp(uper['mid'])
            progress=progress+1
            print(f'当前up进度{progress}/{total}')
    sqlsrt=f"""
SELECT a.mid 
FROM (SELECT mid FROM video GROUP BY mid) a 
LEFT JOIN (SELECT mid FROM up WHERE `upsqldate`='{time.strftime('%Y-%m-%d',time.localtime())}' GROUP BY mid) b 
ON a.mid=b.mid
WHERE b.mid IS NULL
    """
    print(sqlsrt)
    upList=mydb.get_query(sqlsrt)
    total=len(upList)
    progress=0
    parnum=total//6
    print(f"总数：{total},分页数：{parnum}")
    t1=threading.Thread(target=setups,args=(upList[:parnum],))
    t2=threading.Thread(target=setups,args=(upList[parnum:parnum*2],))
    t3=threading.Thread(target=setups,args=(upList[parnum*2:parnum*3],))
    t4=threading.Thread(target=setups,args=(upList[parnum*3:parnum*4],))
    t5=threading.Thread(target=setups,args=(upList[parnum*4:parnum*5],))
    t6=threading.Thread(target=setups,args=(upList[parnum*5:],))
    t1.start()
    t2.start()
    time.sleep(0.25)
    t3.start()
    time.sleep(1)
    t4.start()
    time.sleep(1)
    t5.start()
    time.sleep(1)
    t6.start()
    t1.join()
    t2.join()
    t3.join()
    t4.join()
    t5.join()
    t6.join()




# videoList=mydb.select_table("view_videos_group")
# for video in videoList:
#     aid=video['aid']
#     print('aid',aid)
#     v=Video(aid)
#     v.save()
#     getUser(aid,5)#获取并存储5个用户

# randVideos(50)

# videoList=mydb.select_table("videotask")
# for video in videoList:
#     aid=video['aid']
#     v=Video(mid)
#     v.save()

# upList=mydb.get_query("SELECT mid FROM video GROUP BY mid")
# for uper in upList:
#     mid=uper['mid']
#     up=Up(mid)
#     up.save()

# upList=mydb.select_table("uptask")
# for uper in upList:
#     mid=uper['mid']
#     up=Up(mid)
#     up.save()



def main():
    flag=True
    errnum=0
    start_time = time.time()
    print("开始")
    while flag:
        try:
            # randVideos(50)
            upsMydb()
            videosMydb()
            flag=False
        except:
            errnum+=1
            time.sleep(480)
        if errnum>6:
            flag=False
            break
    end_time = time.time()
    run_time = end_time - start_time
    print(f'运行{run_time}秒,{run_time/60}分钟,错误次数:{errnum}')

progress=0
total=0
main()
# schedule.every().day.at("10:00").do(main)
# while True:
#     schedule.run_pending()

