from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.cluster import KMeans
from collections import Counter
from mydb import mydb
import time
import datetime
import pickle
import tensorflow as tf
from tensorflow.keras import layers
import numpy as np
import pandas as pd
# X_train = [[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12]]
# y_train = [5, 8, 11, 14]
# # 创建线性回归模型
# model = LinearRegression()
# # 拟合模型
# model.fit(X_train, y_train)
# print(model.__dict__)
# # 使用模型进行预测
# y_predict = model.predict([[13, 14, 15]])
# # 输出预测结果
# print(y_predict)

def video_predict():
    # strsql="""
    # SELECT b.*,a.* FROM 
    # (select mid,follower,videolike as up_like,upsqldate from up) a 
    # INNER JOIN 
    # (select mid,pubdate,duration,danmaku,reply,favorite,coin,share,videolike,view,upsqldate from video) b 
    # on a.mid=b.mid and a.upsqldate=b.upsqldate
    # """
    strsql="select pubdate,duration,danmaku,reply,favorite,coin,share,videolike,view,upsqldate from video"
    trains=mydb.get_query(strsql)
    x_trains=[]
    y_trains=[]
    for train in trains:
        x=[]
        t1=datetime.date.fromtimestamp(time.mktime(time.localtime(train['pubdate'])))
        t2=train['upsqldate']
        delta=t2-t1
        x.append(delta.days)#视频已发布时间
        # x.append(train['copyright'])#版权
        x.append(train['duration'])#视频时长
        x.append(train['danmaku'])#弹幕量
        x.append(train['reply'])#评论量
        x.append(train['favorite'])#收藏量
        x.append(train['coin'])#投币量
        x.append(train['share'])#分享量
        x.append(train['videolike'])#点赞量
        # x.append(train['follower'])#up主粉丝数
        # x.append(train['up_like'])#up主总获赞数
        # x.append(train['danmakuemo'])#弹幕情感
        # x.append(train['replyemo'])#评论情感
        x_trains.append(x)
        y_trains.append(train['view'])


    model = LinearRegression()
    parnum=(len(x_trains)//3)*2

    x_test=x_trains[:parnum]
    y_test=y_trains[:parnum]

    x_verify=x_trains[parnum:]
    y_verify=y_trains[parnum:]
    model.fit(x_test,y_test)
    print(model.__dict__)
    y_predict = model.predict(x_verify)

    mean=mean_squared_error(y_verify,y_predict)#均方误差
    score=r2_score(y_verify,y_predict)#解释方差分数:1是完美的预测
    print(f'{sum(y_predict)}/{sum(y_verify)}:{sum(y_predict)/sum(y_verify)}')
    print(mean,score)


def up_predict():
    trains=mydb.get_query("SELECT * FROM up WHERE videolike>0")
    x_trains=[]
    y_trains=[]
    for train in trains:
        x=[]
        x.append(train['video'])#视频投稿数
        x.append(train['videolike'])#视频总点赞量
        # x.append(train['updaterate'])#视频更新频率
        # x.append(train['avg_duration'])#视频平均时长
        x_trains.append(x)
        y_trains.append(train['follower'])#粉丝数


    model = LinearRegression()
    parnum=(len(x_trains)//5)*4

    x_test=x_trains[:parnum]
    y_test=y_trains[:parnum]

    x_verify=x_trains[parnum:]
    y_verify=y_trains[parnum:]
    model.fit(x_test,y_test)
    print(model.__dict__)
    y_predict = model.predict(x_verify)

    mean=mean_squared_error(y_verify,y_predict)#均方误差
    score=r2_score(y_verify,y_predict)#解释方差分数:1是完美的预测
    print(f'{sum(y_predict)}/{sum(y_verify)}:{sum(y_predict)/sum(y_verify)}')
    print(mean,score)

def up_cluster():
    x=[[a['follower'],a['videolike']] for a in mydb.get_query("SELECT follower,videolike FROM view_ups_group WHERE videolike>0")]
    kmeans = KMeans(n_clusters=3,max_iter=600)
    kmeans.fit(x)

    unique_labels = Counter(kmeans.labels_) # 获得所有不同的簇标号
    c_c=kmeans.cluster_centers_.tolist() #将numpy转list
    x_cluster=[]
    for index,c in enumerate(c_c):
        coordinate={
            'index':-1,
            'name':'',
            'center':c,
            'count':unique_labels[index]
        }
        print(index,c)
        print(type(c))
        print(min(c_c),type(min(c_c)))
        if c==min(c_c):
            coordinate['name']='up主'
            coordinate['index']=0
        elif c==max(c_c):
            coordinate['name']='大大up主'
            coordinate['index']=2
        else:
            coordinate['name']='大up主'
            coordinate['index']=1
        x_cluster.append(coordinate)
    x_cluster=sorted(x_cluster, key=lambda x: x['index'], reverse=False)

    print(x_cluster)

    

# up_predict()
# video_predict()
# up_cluster()

def video_predict2():
    strsql="select pubdate,duration,danmaku,reply,favorite,coin,share,videolike,view,upsqldate from video"
    trains=mydb.get_query(strsql)
    x_trains=[]
    y_trains=[]
    for train in trains:
        x=[]
        t1=datetime.date.fromtimestamp(time.mktime(time.localtime(train['pubdate'])))
        t2=train['upsqldate']
        delta=t2-t1
        x.append(delta.days)#视频已发布时间
        x.append(train['duration'])#视频时长
        x.append(train['danmaku'])#弹幕量
        x.append(train['reply'])#评论量
        x.append(train['favorite'])#收藏量
        x.append(train['coin'])#投币量
        x.append(train['share'])#分享量
        x.append(train['videolike'])#点赞量
        x_trains.append(x)
        y_trains.append(train['view'])

    parnum=(len(x_trains)//5)*4
    #训练集
    x_test=x_trains[:parnum]
    y_test=y_trains[:parnum]
    #测试集
    x_verify=x_trains[parnum:]
    y_verify=y_trains[parnum:]
    model = LinearRegression()
    model.fit(x_test,y_test)#训练
    y_predict = model.predict(x_verify)#预测

    mean=mean_squared_error(y_verify,y_predict)#均方误差
    score=r2_score(y_verify,y_predict)#解释方差分数:1是完美的预测
    with open('videomodel.pkl', 'wb') as f:
        pickle.dump(model, f)
    print(f'训练数据:{len(x_test)}条\n测试数据:{len(x_verify)}条\n均方误差:{mean}\n解释方差分数:{score}\n多元系数:{model.coef_}\n常量:{model.intercept_}')



def up_predict2():
    trains=mydb.get_query("SELECT * FROM up WHERE videolike>0")
    x_trains=[]
    y_trains=[]
    for train in trains:
        x=[]
        x.append(train['video'])#视频投稿数
        x.append(train['videolike'])#视频总点赞量
        x_trains.append(x)
        y_trains.append(train['follower'])#粉丝数

    parnum=(len(x_trains)//5)*4
    #训练集
    x_test=x_trains[:parnum]
    y_test=y_trains[:parnum]
    #测试集
    x_verify=x_trains[parnum:]
    y_verify=y_trains[parnum:]
    model = LinearRegression()
    model.fit(x_test,y_test)#训练
    y_predict = model.predict(x_verify)#预测

    mean=mean_squared_error(y_verify,y_predict)#均方误差
    score=r2_score(y_verify,y_predict)#解释方差分数
    print(f'训练数据:{len(x_test)}条\n测试数据:{len(x_verify)}条\n均方误差:{mean}\n解释方差分数:{score}\n多元系数:{model.coef_}\n常量:{model.intercept_}')

def video_predict3():
    strsql="select pubdate,duration,danmaku,reply,favorite,coin,share,videolike,view,upsqldate from video"
    trains=mydb.get_query(strsql)
    x_trains=[]
    y_trains=[]
    for train in trains:
        x=[]
        t1=datetime.date.fromtimestamp(time.mktime(time.localtime(train['pubdate'])))
        t2=train['upsqldate']
        delta=t2-t1
        x.append(delta.days)#视频已发布时间
        x.append(train['duration'])#视频时长
        x.append(train['danmaku'])#弹幕量
        x.append(train['reply'])#评论量
        x.append(train['favorite'])#收藏量
        x.append(train['coin'])#投币量
        x.append(train['share'])#分享量
        x.append(train['videolike'])#点赞量
        x_trains.append(x)
        y_trains.append(train['view'])

    parnum=(len(x_trains)//5)*4
    #训练集
    x_test=x_trains[:parnum]
    y_test=y_trains[:parnum]
    #测试集
    x_verify=x_trains[parnum:]
    y_verify=y_trains[parnum:]
    # 模型参数
    W = tf.Variable(tf.random.normal([7, 1]))
    b = tf.Variable(tf.random.normal([1]))
    # 构建模型
    model = tf.matmul(x_test, W) + b
    # 损失函数和优化器
    cost = tf.reduce_sum(tf.pow(model-y_test, 2)) / (len(x_test))
    optimizer = tf.train.GradientDescentOptimizer(learning_rate=0.5).minimize(cost)
    # 初始化变量
    init = tf.global_variables_initializer()
    # 启动session
    sess = tf.Session()
    sess.run(init)
    # 拟合平面
    for step in range(4):
        sess.run(optimizer)
        if step % 1 == 0:
            print(step, sess.run(cost))
    # 保存模型
    saver = tf.train.Saver()
    saver.save(sess, "videomodel.ckpt")
    sess.close()
    # 测试集上预测结果
    pred = sess.run(pred, feed_dict={x_test: x_verify})

    # 计算RMSE
    rmse = np.sqrt(np.mean(np.square(pred - y_verify)))
    print("Test RMSE: %.3f" % rmse)
    sess.close()


def video_predict4():
    strsql="select pubdate,duration,danmaku,reply,favorite,coin,share,videolike,view,upsqldate from video"
    trains=mydb.get_query(strsql)
    x_trains=[]
    y_trains=[]
    for train in trains:
        x=[]
        t1=datetime.date.fromtimestamp(time.mktime(time.localtime(train['pubdate'])))
        t2=train['upsqldate']
        delta=t2-t1
        x.append(delta.days)#视频已发布时间
        x.append(train['duration'])#视频时长
        x.append(train['danmaku'])#弹幕量
        x.append(train['reply'])#评论量
        x.append(train['favorite'])#收藏量
        x.append(train['coin'])#投币量
        x.append(train['share'])#分享量
        x.append(train['videolike'])#点赞量
        x_trains.append(x)
        y_trains.append(train['view'])
    
    x_trains=np.array(x_trains)
    y_trains=np.array(y_trains)
    #数据归一化
    for i in range(8):
        x_trains[:,i] = x_trains[:,i] / (np.max(x_trains[:,i]) - np.min(x_trains[:,i]))
    x_train, x_test, y_train, y_test = train_test_split(x_trains, y_trains, test_size=0.1)

    # 构建网络结构 
    model = tf.keras.models.Sequential([
    layers.Dense(512, activation='relu'),
    layers.Dense(10, activation='softmax')
    ])
    # 编译网络 
    model.compile(optimizer='adam', 
                loss=tf.keras.losses.SparseCategoricalCrossentropy(),
                metrics=['accuracy'])
    # 训练网络
    model.fit(x_train, y_train, epochs=8, batch_size=32)
    # 评估网络
    model.evaluate(x_test, y_test, batch_size=32)
    # 进行预测
    y_pred = model.predict(x_test)
    print(y_pred)

video_predict()
up_predict()






