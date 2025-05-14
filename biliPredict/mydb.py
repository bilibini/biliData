import pymysql
import time
from config import config

conn=pymysql.connect(host=config['mysql_host'],
                     user=config['mysql_user'],
                     passwd=config['mysql_pw'],
                     database=config['mysql_db'],
                     port=config['mysql_port'],
                     charset='utf8',
                     cursorclass=pymysql.cursors.DictCursor)

class Mydb:
    def create_table_user(self):
        """创建用户数据表"""
        cursor=conn.cursor()
        sqlstr="""
        CREATE TABLE user (
            mid varchar(20) not null comment '用户mid',
            name varchar(30) comment '用户昵称',
            sex varchar(4) comment '性别',
            sign varchar(400) comment '用户签名',
            rank smallint unsigned comment '用户权限等级',
            level tinyint(1) comment '用户等级：0-6',
            silence boolean comment '封禁状态,0：正常,1：被封',
            fans_badge boolean comment '是否具有粉丝勋章,false：无,true：有',
            vip tinyint(1) comment '会员信息，0：无，1：月大会员，2：年度及以上大会员',
            birthday varchar(5) comment '生日,MM-DD,如设置隐私为空',
            school varchar(40) comment '学校',
            is_senior_member boolean comment '是否为硬核会员,0：否,1：是',
            official tinyint comment '认证类型,-1：无,0：个人认证,1：机构认证',
            official_title varchar(500) comment '认证信息',
            is_fans_medal boolean comment '是否佩戴粉丝勋章',
            following smallint unsigned comment '关注数',
            follower int unsigned comment '粉丝数',
            video mediumint unsigned comment '投稿视频数',
            bangumi smallint unsigned comment '追番数',
            cinema smallint unsigned comment '追电影数',
            channel smallint unsigned comment '关注频道数',
            favourite smallint unsigned comment '收藏夹数数',
            tag smallint unsigned comment '关注TAG数',
            article smallint unsigned comment '投稿专栏数',
            album smallint unsigned comment '投稿相簿数',
            audio smallint unsigned comment '投稿音频数',
            pugv smallint unsigned comment '投稿课程数',
            water tinyint(1) comment '是否为水军，0：不是，1：是',
            upsqldate date comment '上传数据库时间，YYYY-MM-DD'
        )
        """
        cursor.execute(sqlstr)
        cursor.close()
        print('[数据库操作]用户数据表创建完毕')

    def create_table_medal(self):
        """创建粉丝勋章数据表"""
        cursor=conn.cursor()
        sqlstr="""
        CREATE TABLE medal (
            medal_id varchar(18) comment '粉丝勋章id',
            target_id varchar(20) comment '粉丝勋章所属UP的mid',
            medal_name varchar(20) comment '粉丝勋章名字',
            medal_color mediumint unsigned comment '粉丝勋章颜色,十进制数',
            uid varchar(20) comment '拥有用户的mid',
            medal_level tinyint unsigned comment '粉丝勋章等级',
            upsqldate date comment '上传数据库时间，YYYY-MM-DD'
        )
        """
        cursor.execute(sqlstr)
        cursor.close()
        print('[数据库操作]粉丝勋章数据表创建完毕')

    def create_table_video(self):
        """创建视频数据表"""
        cursor=conn.cursor()
        sqlstr="""
        CREATE TABLE video (
            aid varchar(20) not null comment '视频aid',
            bvid varchar(20) comment '视频bvid',
            videos tinyint unsigned comment '包含视频数量',
            tid tinyint unsigned comment '分区id',
            tname varchar(20) comment '分区名字',
            copyright tinyint(1) comment '版权标志',
            title varchar(100) comment '视频标题',
            pubdate int unsigned comment '发布时间',
            ctime int unsigned comment '创建时间',
            videodesc varchar(500) comment '视频简介',
            duration smallint unsigned comment '视频时长',
            mid varchar(20) comment 'up主mid',
            name varchar(30) comment 'up主名字',
            view int unsigned comment '视频观看量',
            danmaku int unsigned comment '视频弹幕量',
            reply int unsigned comment '视频评论量',
            favorite int unsigned comment '视频收藏量',
            coin int unsigned comment '视频投币量',
            share int unsigned comment '视频分享量',
            videolike int unsigned comment '视频点赞量',
            width smallint unsigned comment '视频宽度',
            height smallint unsigned comment '视频高度',
            cid varchar(20) comment '视频弹幕cid',
            replyemo float(5,4) comment '评论总情绪：0~1，越大越正向',
            danmakuemo float(5,4) comment '弹幕总情绪：0~1，越大越正向',
            upsqldate date comment '上传数据库时间，YYYY-MM-DD'
        )
        """
        cursor.execute(sqlstr)
        cursor.close()
        print('[数据库操作]视频数据表创建完毕')

    def create_view_videos_group(self):
        """创建视频分组数据视图"""
        cursor=conn.cursor()
        sqlstr="""
        CREATE VIEW view_videos_group AS
        SELECT * FROM video GROUP BY aid
        """
        cursor.execute(sqlstr)
        cursor.close()
        print('[数据库操作]视频分组数据视图创建完毕')

    def create_view_videos(self):
        """创建视频综合数据视图"""
        cursor=conn.cursor()
        sqlstr="""
        CREATE VIEW view_videos AS
        select 
        avg(b.duration) AS duration_avg,
        avg(b.view) AS view_avg,
        avg(b.danmaku) AS danmaku_avg,
        avg(b.reply) AS reply_avg,
        avg(b.favorite) AS favorite_avg,
        avg(b.coin) AS coin_avg,
        avg(b.share) AS share_avg,
        avg(b.videolike) AS videolike_avg,
        floor(avg(b.width)) AS width_avg,
        floor(avg(b.height)) AS height_avg,
        (select (count(*)/(select count(*) from view_videos_group)) from view_videos_group where (view_videos_group.width >= view_videos_group.height)) AS LandscapeVideo_scale,
        (select (count(*)/(select count(*) from view_videos_group)) from view_videos_group where (view_videos_group.duration >= 480)) AS LongVideo_scale
        from view_videos_group b
        """
        cursor.execute(sqlstr)
        cursor.close()
        print('[数据库操作]视频综合数据视图创建完毕')

    def create_table_up(self):
        """创建up主数据表"""
        cursor=conn.cursor()
        sqlstr="""
        CREATE TABLE up (
            mid varchar(20) not null comment '用户mid',
            name varchar(30) comment '用户昵称',
            sex varchar(4) comment '性别',
            sign varchar(400) comment '用户签名',
            rank smallint unsigned comment '用户权限等级',
            level tinyint(1) comment '用户等级：0-6',
            silence boolean comment '封禁状态,0：正常,1：被封',
            fans_badge boolean comment '是否具有粉丝勋章,false：无,true：有',
            vip tinyint(1) comment '会员信息，0：无，1：月大会员，2：年度及以上大会员',
            birthday varchar(5) comment '生日,MM-DD,如设置隐私为空',
            school varchar(40) comment '学校',
            is_senior_member boolean comment '是否为硬核会员,0：否,1：是',
            official tinyint comment '认证类型,-1：无,0：个人认证,1：机构认证',
            official_title varchar(500) comment '认证信息',
            following smallint unsigned comment '关注数',
            follower int unsigned comment '粉丝数',
            video mediumint unsigned comment '投稿视频数',
            bangumi smallint unsigned comment '追番数',
            cinema smallint unsigned comment '追电影数',
            channel smallint unsigned comment '关注频道数',
            favourite smallint unsigned comment '收藏夹数数',
            tag smallint unsigned comment '关注TAG数',
            article smallint unsigned comment '投稿专栏数',
            album smallint unsigned comment '投稿相簿数',
            audio smallint unsigned comment '投稿音频数',
            pugv smallint unsigned comment '投稿课程数',
            replyemo float(5,4) comment '评论总情绪：0~1，越大越正向',
            danmakuemo float(5,4) comment '弹幕总情绪：0~1，越大越正向',
            updaterate float comment '最近视频更新频率，单位小时',
            avg_duration float unsigned comment '投稿视频平均时长，单位分钟',
            tlist varchar(1024) comment '投稿视频分区统计',
            upsqldate date comment '上传数据库时间，YYYY-MM-DD'
        )
        """
        cursor.execute(sqlstr)
        cursor.close()
        print('[数据库操作]up主数据表创建完毕')

    def create_table_uptask(self):
        """创建up主任务数据表"""
        cursor=conn.cursor()
        sqlstr="""
        CREATE TABLE uptask(
            mid varchar(18) not null comment '用户mid'
        )
        """
        cursor.execute(sqlstr)
        cursor.close()
        print('[数据库操作]up主任务数据表创建完毕')

    def create_table_videotask(self):
        """创建视频任务数据表"""
        cursor=conn.cursor()
        sqlstr="""
        CREATE TABLE videotask(
            aid varchar(18) not null comment '视频aid'
        )
        """
        cursor.execute(sqlstr)
        cursor.close()
        print('[数据库操作]视频任务数据表创建完毕')


    def insert_into(self,tab_name:str,data_dict:dict):
        """表插入数据"""
        sqlstr=""
        data_key=[]
        data_val=[]
        for key,val in  data_dict.items():
            data_key.append(key)
            data_val.append(val)
        str_key=','.join(data_key)
        str_val='%s,'*(len(data_key)-1)+'%s'
        sqlstr=f"insert into {tab_name}({str_key},upsqldate) values({str_val},'{time.strftime('%Y-%m-%d',time.localtime())}')"
        while True:
            try:
                cursor=conn.cursor()
                print(sqlstr)
                try:
                    cursor.execute(sqlstr,data_val)
                except:
                    conn.ping()
                    cursor=conn.cursor()
                    cursor.execute(sqlstr,data_val)
                conn.commit()
                cursor.close()
                break
            except Exception as error:
                conn.ping(True)
                print(f'数据库插入数据错误{error}')
        print(f'[数据库操作]{tab_name}表数据写入完毕')

    def select_table(self,tab_name:str,data_dict:dict={})->list:
        """查询表数据，返回结果为列表包裹的字典类型"""
        sqlstr=""
        data_val=[]
        data_list=[]
        for key,val in  data_dict.items():
            data_val.append(val)
            data_list.append(f'{key}=%s')
        str_list=' and '.join(data_list)
        sqlstr=f"select * from {tab_name} {'where' if str_list!='' else '' } {str_list}"
        cursor=conn.cursor()
        print(sqlstr)
        try:
            cursor.execute(sqlstr,data_val)
        except:
            conn.ping()
            cursor=conn.cursor()
            cursor.execute(sqlstr,data_val)
        res=cursor.fetchall()
        cursor.close()
        print(res)
        print(f'[数据库操作]{tab_name}表查询完毕,查询到{len(res)}条数据')
        return res
        
    def get_where_is(self,tab_name:str,data_dict:dict={})->bool:
        """判断表中是否存在该条数据，有：True，无：False"""
        res=self.select_table(tab_name,data_dict)
        if len(res)>0:
            return True
        else:
            return False

    def get_query(self,sqlstr:str)->list:
        cursor=conn.cursor()
        print(sqlstr)
        try:
            cursor.execute(sqlstr)
        except:
            conn.ping()
            cursor=conn.cursor()
            cursor.execute(sqlstr)
        res=cursor.fetchall()
        cursor.close()
        # print(res)
        print(f'[数据库操作]执行sql语句完毕,查询到{len(res)}条数据')
        return res

mydb=Mydb()
# mydb.create_view_videos()
# mydb.create_view_videos_group()
# mydb.create_table_videotask()
# mydb.create_table_uptask()
# mydb.create_table_user()
# mydb.create_table_up()
# mydb.create_table_video()
# mydb.create_table_medal()