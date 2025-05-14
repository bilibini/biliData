<template>
  <el-row>
    <el-card class="input-card">
      <!-- <el-row> -->
        请输入视频AID：
        <el-input v-model="aid" placeholder="aid" clearable type="number" >
        </el-input>
        <el-button @click="cilikId()" type="primary" plain>确定</el-button>
      <!-- </el-row> -->
      <!-- <el-row>
        请输入视频BVID：
        <el-input v-model="bvid" placeholder="bvid" clearable type="string" >
        </el-input>
        <el-button @click="cilikId()" type="primary" plain>确定</el-button>
      </el-row> -->
    </el-card>
  </el-row>
  <el-row>
    <el-card class="input-card" style="margin-top: 20px;">
      <el-descriptions  :column="4" size="large" direction="horizontal" border>
        <el-descriptions-item span="2">
          <template #label>
            <div class="cell-item">
              视频标题
            </div>
          </template>
          <a  target="_blank" :href="'https://www.bilibili.com/video/'+videoData.bvid" class="alink">{{videoData.title}}</a>
        </el-descriptions-item>
        <el-descriptions-item>
          <template #label>
            <div class="cell-item">
              aid
            </div>
          </template>
          {{videoData.aid}}
        </el-descriptions-item>
        <el-descriptions-item>
          <template #label>
            <div class="cell-item">
              bvid
            </div>
          </template>
          {{videoData.bvid}}
        </el-descriptions-item>
        <!--  -->
        <el-descriptions-item span="2">
          <template #label>
            <div class="cell-item">
              up主
            </div>
          </template>
          <a class="alink" target="_blank" :href="'https://space.bilibili.com/'+videoData.owner.mid">
          <div class="u-avatar-name" >
            <el-avatar class="u-avatar" shape="square" size="default" loading="lazy" fit="cover" :src="videoData.owner.face" />
            <span class="u-name">{{videoData.owner.name}}</span>
          </div>
          </a>
        </el-descriptions-item>
        <el-descriptions-item span="2">
          <template #label>
            <div class="cell-item">
              视频封面
            </div>
          </template>
          <img style="height: 200px;" :src="videoData.pic" alt="">
          <!-- <el-image   :src="videoData.pic" lazy /> -->
        </el-descriptions-item>
        <!--  -->
        <el-descriptions-item span="4">
          <template #label>
            <div class="cell-item">
              视频简介
            </div>
          </template>
          {{videoData.desc}}
        </el-descriptions-item>
        <!--  -->
        <el-descriptions-item>
          <template #label>
            <div class="cell-item">
              播放量
            </div>
          </template>
          {{videoData.stat.view}}
        </el-descriptions-item>
        <el-descriptions-item>
          <template #label>
            <div class="cell-item">
              点赞量
            </div>
          </template>
          {{videoData.stat.like}}
        </el-descriptions-item>
        <el-descriptions-item>
          <template #label>
            <div class="cell-item">
              投币量
            </div>
          </template>
          {{videoData.stat.coin}}
        </el-descriptions-item>
        <el-descriptions-item>
          <template #label>
            <div class="cell-item">
              收藏量
            </div>
          </template>
          {{videoData.stat.favorite}}
        </el-descriptions-item>
        <!--  -->
        <el-descriptions-item>
          <template #label>
            <div class="cell-item">
              评论量
            </div>
          </template>
          {{videoData.stat.reply}}
        </el-descriptions-item>
        <el-descriptions-item>
          <template #label>
            <div class="cell-item">
              弹幕量
            </div>
          </template>
          {{videoData.stat.danmaku}}
        </el-descriptions-item>
        <el-descriptions-item>
          <template #label>
            <div class="cell-item">
              分享量
            </div>
          </template>
          {{videoData.stat.share}}
        </el-descriptions-item>
        <el-descriptions-item>
          <template #label>
            <div class="cell-item">
              历史最高排名
            </div>
          </template>
          {{videoData.stat.his_rank}}
        </el-descriptions-item>
        <!--  -->
      </el-descriptions>
    </el-card>
  </el-row>
  <el-row v-if="userName!=''">
    <el-card class="input-card">
      <div ref="videos_predic" class="echarts-contentbox"></div>
    </el-card>
  </el-row>
</template>

<script>
  import store from '../store'
  import router from '../router'
  import { useRoute } from 'vue-router'
  import * as echarts from 'echarts'
  export default{
    data(){
      return{
        userName:'',
        aid:"",
        bvid:"",
        videoData:{
          aid:"",
          bvid:"",
          desc:"",
          width:0,
          height:0,
          duration:0,
          owner:{
            face:"",
            mid:0,
            name:""
          },
          pic:"",
          pubdate:0,
          stat:{},
          title:"",
          tname:""
        }
      }
    },
    mounted(){
      this.userName=store.getters.getUserName
      let id=(useRoute().params).id
      if(parseInt(id)!=0){
        this.aid=id
        this.getVideo()
      }
      
    },
    methods:{
      async getVideo(){
        let videoData={}
        await store.dispatch("tourists/getVideoInfo",this.aid,this.bvid)
        .then(res=>videoData=res)
        .catch(err=>videoData=err)
        console.log(videoData)
        this.videoData=videoData
        if(this.userName!=''){
          this.set_predic(videoData)
        }
      },
      cilikId(){
        console.log(this.uid)
        this.getVideo()
      },
      set_predic(videoData){
        let chart = this.$refs.videos_predic
        let myChart = echarts.init(chart)
        
        let coef=[41.14111591,-1.36481389,28.62751738,13.0184178,2.31496991,-4.74428634,3.12123164,10.20081329]
        let intercept=46116.78311216127
        
        let day=Math.round(((new Date().getTime()/1000)-parseInt(videoData.pubdate))/86400)
        let duration=parseInt(videoData.duration)
        let danmaku=parseInt(videoData.stat.danmaku)
        let reply=parseInt(videoData.stat.reply)
        let favorite=parseInt(videoData.stat.favorite)
        let coin=parseInt(videoData.stat.coin)
        let share=parseInt(videoData.stat.share)
        let like=parseInt(videoData.stat.like)
        
        let bl=[0,duration,danmaku,reply,favorite,coin,share,like]
        
        let jieguo=0
        let tianshu=day+3
        for(var j = 1; j < coef.length; j++){
          jieguo=jieguo+bl[j]*coef[j]
        }
        jieguo=jieguo+coef[0]*tianshu+intercept
        let zj=bl.map(x=>((x/(videoData.stat.view))*jieguo)-x)
        for(var j = 2; j < coef.length; j++){
          jieguo=jieguo+zj[j]*coef[j]
        }
        jieguo=parseInt(jieguo)
        let option = {
          title: {
            text: '3日后播放量预测'
          },
          tooltip: {},
          legend: {
            data: ['播放量']
          },
          xAxis: {
            data: ['当前播放量', '预测播放量']
          },
          yAxis: {},
          series: [{
              name: '播放量',
              type: 'bar',
              data: [videoData.stat.view, jieguo]
          }]
        }
        myChart.setOption(option)
      }
    }
  }
</script>

<style lang="less">
  .input-card{
    width: 100%;
    // height: 150px;
    .el-input{
      width: 230px;
      /* 在Chrome浏览器下 */
      input::-webkit-outer-spin-button,
      input::-webkit-inner-spin-button {
          -webkit-appearance: none;
      }
      /* 在Firefox浏览器下 */
      input[type="number"]{
          -moz-appearance: textfield;
      }
    }
  }
  .u-avatar-name{
    display: inline-flex;
    flex-direction: row;
    align-items: center;
    background: aliceblue;
    padding: 10px;
    border-radius: 30px;
    .u-avatar{
      display: flex;
      border-radius: 50%;
    }
    .u-name{
      display: flex;
      line-height: 30px;
      padding-left: 14px;
      padding-right: 20px;
    }
  }
  .echarts-contentbox{
    height: 400px;
    width: 100%;
  }
  .alink{
    text-decoration:none;
    color:#000
  }
</style>