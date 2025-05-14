<template>
  <div class="PersonTop">
    <div class="PersonTop_img">
      <img :src="info.face" />
    </div>
    <div class="PersonTop_text">
      <div class="user_text">
        <div class="user_name">
          <span> {{ userName }} </span>
        </div>
        <div class="user-v" v-if="rank == 6">
          <!-- <img src="@/assets/img/V.png" class="user-v-img" /> -->
          <span class="user-v-font">管理员</span>
        </div>
        <div class="user-v" v-else>
          <!-- <img src="@/assets/img/V.png" class="user-v-img" /> -->
          <span class="user-v-font">普通用户</span>
        </div>
        <div class="user_qianming">
          <span> b站用户名：<a target="_blank" :href="'https://space.bilibili.com/'+mid">{{ info.name }}</a></span>
        </div>
        <div class="user_qianming">
          <span>{{ info.sign }}</span>
        </div>
      </div>
      <div class="user_num">
        <div style="cursor: pointer" >
          <div class="num_number">{{ info.fans }}</div>
          <span class="num_text">粉丝</span>
        </div>
        <div style="cursor: pointer" >
          <div class="num_number">{{ info.friend }}</div>
          <span class="num_text">关注</span>
        </div>
        <div>
          <div class="num_number">{{ info.like_num }}</div>
          <span class="num_text">获赞</span>
        </div>
      </div>
    </div>
  </div>
  <el-card shadow="never">
    <!-- <template #header>
      <div class="card-header">
        <span>Card name</span>
      </div>
    </template> -->
    <div ref="sates" class="echarts-contentbox"></div>
  </el-card>
  <el-card shadow="never">
    <template #header>
      <div class="card-header">
        <span>最近视频</span>
      </div>
    </template>
    <el-scrollbar class="vlist-box">
      <div class="scrollbar-flex-content">
      <div v-for="item in info.vlist" :key="item.mid" class="video-card">
        <img :src="imgurla+item.pic" class="image"/>
        <div class="card-text">
          <span class="card-title">{{item.title}}</span>
          <div class="card-s">
            <span>播放量:{{item.play}}</span>
            <span>评论量:{{item.video_review}}</span>
            <span>弹幕量:{{item.comment}}</span>
            <span>时长:{{item.length}}</span>
            <el-button class="go" type="primary" @click="gotovideo(item.aid)" >
              数据预测<el-icon class="el-icon--right"><ArrowRight /></el-icon>
            </el-button>
          </div>
        </div>
      </div>
      </div>
    </el-scrollbar>
  </el-card>
  <el-card shadow="never" v-if="rank == 6">
    <template #header>
      <div class="card-header">
        <span>数据库情况</span>
      </div>
    </template>
    <el-row >
      <el-col :span="6"><el-statistic title="平台用户数量" :value="sqlinfo.u"><template #suffix>个</template></el-statistic></el-col>
      <el-col :span="6"><el-statistic title="采集视频数量" :value="sqlinfo.video"><template #suffix>条</template></el-statistic></el-col>
      <el-col :span="6"><el-statistic title="采集up数量" :value="sqlinfo.up"><template #suffix>条</template></el-statistic></el-col>
      <el-col :span="6"><el-statistic title="采集用户数量" :value="sqlinfo.user"><template #suffix>条</template></el-statistic></el-col>
    </el-row>
  </el-card>
  <el-card shadow="never" v-if="rank == 6">
    <template #header>
      <div class="card-header">
        <span>平台用户注册情况</span>
      </div>
    </template>
    <el-table border stripe  :data="sqlinfo.userinfo" :key="sqlinfo.userinfo" style="width: 100%">
      <el-table-column prop="id" label="id" width="180" />
      <el-table-column prop="mid" label="B站mid" width="180" />
      <el-table-column prop="role" label="权限值" width="180" />
      <el-table-column prop="username" label="用户名" />
    </el-table>
  </el-card>
  <el-card shadow="never" v-if="rank == 6">
    <template #header>
      <div class="card-header">
        <span>服务器情况</span>
      </div>
    </template>
    <iframe width="100%" height="500px" src="http://localhost.com/user/server.php" frameborder="0" seamless></iframe>
  </el-card>
</template>

<script setup>
  import { getCurrentInstance,reactive,toRefs,ref } from 'vue'
  import router from '../router'
  import * as echarts from 'echarts'
  import store from '../store'
  import {loggedGet} from '../request'
  import axios from 'axios'
  const thisf= getCurrentInstance().ctx
  const imgurla="https://image.baidu.com/search/down?url="
  let userName=store.getters.getUserName
  let mid=store.getters.getInfo.mid
  let rank=parseInt(store.getters.getInfo.rank)
  let info=reactive({
    sates: [],
    vlist:[],
    face: imgurla+"http://i0.hdslb.com/bfs/face/member/noface.jpg",
    name: "未知",
    sex: "男",
    sign: "无",
    fans: 200,
    friend: 2,
    like_num: 100
  })
  let sqlinfo=reactive({
    u:0,
    up:0,
    user:0,
    video:0,
    userinfo:[]
  })
  if(rank == 6){
    get_sqlinfo()
  }
  
  function get_sqlinfo(){
    axios.get("http://localhost.com/user/sqlinfo.php").then(response=>{
      let data=response.data
      sqlinfo.userinfo=data.userinfo
      sqlinfo.u=data.userinfo.length
      sqlinfo.up=data.sqlinfo.up
      sqlinfo.user=data.sqlinfo.user
      sqlinfo.video=data.sqlinfo.video
    })
  }
  
  function gotovideo(id){
    router.push({name: 'Video',params:{ id:id}});
  }
  
  function set_sates(sateslist){
    let chart = thisf.$refs.sates
    let myChart = echarts.init(chart)
    let xAxis=[]
    let video=[]
    let videolike=[]
    let follower=[]
    let duration=[]//视频平均长度（分
    let updaterate=[]//更新频率（小时
    sateslist.reverse()
    let video0=parseInt(sateslist[0].video)
    let videolike0=parseInt(sateslist[0].videolike)
    let duration0=parseFloat(sateslist[0].duration)
    let updaterate0=parseFloat(sateslist[0].updaterate)
    let follower0=parseInt(sateslist[0].follower)
    sateslist.forEach((sate)=>{
      xAxis.push(sate.upsqldate)
      video.push(parseInt(sate.video)-video0)
      videolike.push(parseInt(sate.videolike)-videolike0)
      duration.push(parseFloat((parseFloat(sate.duration)-duration0).toFixed(3)))
      updaterate.push(parseFloat((parseFloat(sate.updaterate)-updaterate0).toFixed(3)))
      follower.push(parseInt(sate.follower)-follower0)
    })
    console.log(xAxis,video,videolike,duration,updaterate)
    let option = {
      title: {
        text: '最近状态'
      },
      tooltip: {
        trigger: 'axis'
      },
      legend: {
        data: ['投稿数', '点赞数', '粉丝数', '视频时长', '更新频率']
      },
      grid: {
        left: '3%',
        right: '4%',
        bottom: '3%',
        containLabel: true
      },
      toolbox: {
        feature: {
          saveAsImage: {}
        }
      },
      xAxis: {
        type: 'category',
        boundaryGap: false,
        data: xAxis
      },
      yAxis: {
        type: 'value'
      },
      series: [
        {
          name: '投稿数',
          type: 'line',
          stack: 'Total',
          data: video
        },
        {
          name: '视频时长',
          type: 'line',
          stack: 'Total',
          data: duration
        },
        {
          name: '更新频率',
          type: 'line',
          stack: 'Total',
          data: updaterate
        },
        {
          name: '粉丝数',
          type: 'line',
          stack: 'Total',
          data: follower
        },
        {
          name: '点赞数',
          type: 'line',
          stack: 'Total',
          data: videolike
        }
      ]
    }
    myChart.setOption(option)
  }
  
  
  console.log(mid)
  axios.get("http://localhost.com/user/info.php?uid="+mid).then(response=>{
    info.sates=response.data.sates
    info.vlist=response.data.vlist
    info.name=response.data.name
    info.sex=response.data.sex
    info.sign=response.data.sign
    info.fans=response.data.fans
    info.friend=response.data.friend
    info.like_num=response.data.like_num
    info.face=imgurla+response.data.face
    set_sates(info.sates)
  })
  // loggedGet('/info.php',mid).then(res=>console.log(res)).catch(err=>console.log(err))
  console.log("介绍")
</script>

<style lang="less">
.PersonTop {
  height: 140px;
  padding-top: 20px;
  background-color: white;
  display: flex;
  border-radius: 5px;
  // box-shadow: var(--el-box-shadow-light);
}

.PersonTop_img {
  width: 120px;
  height: 120px;
  background-color: #8c939d;
  margin-right: 24px;
  margin-left: 20px;
  overflow: hidden;
  border-radius: 20px;
}

.PersonTop_img img {
  width: 100%;
  height: 100%;
  border-radius: 20px;
}

.PersonTop_text {
  height: 120px;
  width: 880px;
  display: flex;
}

.user_text {
  width: 60%;
  height: 100%;
  line-height: 30px;
}

.user_name {
  font-weight: bold;
  display: flex;
  
}
.user-v {
  margin-bottom: -5px;
  display: flex;
}
.user-v-img {
  width: 15px;
  height: 15px;
}
.user-v-font {
  font-size: 15px;
  color: #00c3ff;
}
.user_qianming {
  font-size: 14px;
  color: #999;
  display: flex;
}
.user_qianming a{
  text-decoration: none; /* 去除默认的下划线 */
  color: #999;
}
.user_qianming a:hover{
  color: #00aaff;
}

.user_num {
  width: 40%;
  height: 100%;
  display: flex;
  align-items: center;
}

.user_num > div {
  text-align: center;
  /* border-right: 1px dotted #999; */
  box-sizing: border-box;
  width: 115px;
  height: 40px;
  line-height: 20px;
}

.num_text {
  color: #999;
}

.num_number {
  font-size: 20px;
  color: #333;
}
.el-menu-item>span {
  font-size: 16px;
  color: #999;
}

.el-card{
  line-height:20px;
  margin-top: 20px;
  .card-header{
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  .echarts-contentbox{
    height: 400px;
    width: 100%;
  }
}
.scrollbar-flex-content {
  display: flex;
}
.vlist-box{
  .video-card{
    background: #aaffff;
    width: 250px;
    height: 140px;
    position:relative;
    display: inline-block;
    box-sizing: border-box;
    margin-bottom: 10px;
    margin-left: 10px;
    img{
      display: inline-block;
      width: 250px;
      height: 140px;
      background: #233 repeat fixed center;
      box-sizing: border-box;
    }
  }
  .card-text{
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    text-align: left;
    position: absolute;
    top: 0;
    background: #00000085;
    color: #fff;
    padding: 10px;
    width: 230px;
    height: 120px;
    text-shadow: -2px -1px 13px #44ceedbf;
    backdrop-filter: blur(1px);
    .card-title{
      line-height: 28px;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }
    .card-s{
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      flex-flow: column;
      margin-top: 5px;
      margin-left: 10px;
      .go{
        position: absolute;
        right: 10px;
        bottom: 10px;
      }
    }
  }
}
// .alink-b{
//   text-decoration:none;
//   color:#fff
// }

</style>