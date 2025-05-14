<template>
  <el-row style="margin-top: 30px;">
    <el-col :span="12">
      <el-card shadow="hover" class="echarts-cardbox">
        <el-row >
          <el-col :span="6"><el-statistic title="平均播放量" :value="view_avg"><template #suffix>K</template></el-statistic></el-col>
          <el-col :span="6"><el-statistic title="平均弹幕量" :value="danmaku_avg"><template #suffix>K</template></el-statistic></el-col>
          <el-col :span="6"><el-statistic title="平均评论量" :value="reply_avg"><template #suffix>K</template></el-statistic></el-col>
          <el-col :span="6"><el-statistic title="平均视频时长" :value="duration_avg"><template #suffix>分钟</template></el-statistic></el-col>
        </el-row>
        <el-row>
          <el-col :span="6"><el-statistic title="平均点赞量" :value="videolike_avg"><template #suffix>K</template></el-statistic></el-col>
          <el-col :span="6"><el-statistic title="平均投币量" :value="coin_avg"><template #suffix>K</template></el-statistic></el-col>
          <el-col :span="6"><el-statistic title="平均收藏量" :value="favorite_avg"><template #suffix>K</template></el-statistic></el-col>
          <el-col :span="6"><el-statistic title="平均分享量" :value="share_avg"><template #suffix>K</template></el-statistic></el-col>
        </el-row>
      </el-card>
    </el-col>
    <el-col :span="12">
      <el-card shadow="hover" class="echarts-cardbox">
        <el-row >
          <canvas ref="video_scale" width="400" height="250" style="width: 220px;height: 138px;" />
          <div class="video-wh">
            <p>平均宽度:{{width_avg}}</p>
            <p>平均高度:{{height_avg}}</p>
            <p>宽高比:{{(width_avg/height_avg).toFixed(2)}}</p>
          </div>
        </el-row >
      </el-card>
    </el-col>
  </el-row>
  <el-row><div ref="videos_avg" class="echarts-contentbox" ></div></el-row>
  <el-row><div ref="videos_scale" class="echarts-contentbox" ></div></el-row>
</template>

<script>
  import * as echarts from 'echarts'
  import store from '../store'
  export default{
    data(){
      return{
        view_avg:0,
        danmaku_avg:0,
        reply_avg:0,
        favorite_avg:0,
        coin_avg:0,
        share_avg:0,
        videolike_avg:0,
        duration_avg:0,
        width_avg:1,
        height_avg:1,
        LandscapeVideo_scale:0,
        LongVideo_scale:0
      }
    },
    async mounted(){
      await this.getVideos()
      this.setVideoScale2d(this.width_avg,this.height_avg)
      this.getEchartData()
    },
    methods:{
      async getVideos(){
        let videosData={}
        await store.dispatch('tourists/getVideosInfo')
        .then((response) => {
          console.log(response)
          videosData=response
        })
        let {view_avg,danmaku_avg,reply_avg,favorite_avg,coin_avg,share_avg,videolike_avg,duration_avg,width_avg,height_avg,LandscapeVideo_scale,LongVideo_scale}=videosData
        this.view_avg=view_avg
        this.danmaku_avg=danmaku_avg
        this.reply_avg=reply_avg
        this.favorite_avg=favorite_avg
        this.coin_avg=coin_avg
        this.share_avg=share_avg
        this.videolike_avg=videolike_avg
        this.duration_avg=duration_avg
        this.width_avg=width_avg
        this.height_avg=height_avg
        this.LandscapeVideo_scale=LandscapeVideo_scale
        this.LongVideo_scale=LongVideo_scale
      },
      setVideoScale2d(width,height){
        let wh_scale=(width/height).toFixed(2)
        height=200
        width=wh_scale*200
        let videoScale=this.$refs.video_scale
        let videoScale2d=videoScale.getContext("2d")
        videoScale2d.fillStyle = "#cfe2f3"; // 设置填充颜色为淡蓝色
        videoScale2d.fillRect(0, 0, width, height); // 绘制长 200 高 160 的矩形，左上角坐标为 (100, 100)
        videoScale2d.strokeStyle = "#1E90FF"; // 设置线条颜色为深蓝色
        videoScale2d.lineWidth = 1; // 设置线条宽度为 2
        videoScale2d.beginPath(); // 开始一条新路径
        videoScale2d.moveTo(0, 0); // 将画笔移动到矩形左上角
        videoScale2d.lineTo(width, height); // 绘制到矩形右下角
        videoScale2d.stroke(); // 绘制线条
        var angle = Math.atan2(height, width); // 计算斜线的倾角
        videoScale2d.save(); // 保存当前画布状态
        videoScale2d.translate(width/2, height/2); // 将画布原点移到斜线的中点
        videoScale2d.rotate(angle); // 旋转画布，使斜线与 x 轴重合
        videoScale2d.fillStyle = "#007FFF"; // 设置文本颜色为深蓝色
        videoScale2d.font = "bold 18px Arial"; // 设置文本样式
        videoScale2d.textAlign = "center"; // 设置文本水平对齐方式为居中
        videoScale2d.textBaseline = "middle"; // 设置文本垂直对齐方式为居中
        videoScale2d.fillText(wh_scale, 0, 10); // 在画布原点绘制文本
        videoScale2d.restore(); // 恢复画布状态
      },
      getEchartData(){
        const thisf=this
        function setVideosAvg(){
          let chart = thisf.$refs.videos_avg
          let myChart = echarts.init(chart)
          let option = {
            xAxis:{type: 'value'},
            yAxis:{
              type: 'category',
              data: ['播放量', '弹幕量', '评论量', '点赞量', '投币量', '收藏量', '分享量']
            },
            series:[
              {
                data: [thisf.view_avg, thisf.danmaku_avg, thisf.reply_avg, thisf.videolike_avg, thisf.coin_avg, thisf.favorite_avg, thisf.share_avg],
                type:'bar',
                name:'视频数据',
                label:{
                  show:true,
                  position:'inner',
                  formatter:'{c}K'
                },
              },
            ]
          }
          myChart.setOption(option)
        }
        function setVideosScale(){
          let chart = thisf.$refs.videos_scale
          let myChart = echarts.init(chart)
          let option = {
            legend: {
              show:true,
              right:0,
              bottom:0,
            },
            series:[
              {
                type:'pie',
                name:'视频横竖比例',
                right:'50%',
                label:{
                  show:true,
                  position:'inner',
                  formatter:'{b}: {d}%'
                },
                data:[{
                  name:'横向视频',
                  value:thisf.LandscapeVideo_scale*100
                },{
                  name:'竖向视频',
                  value:100-(thisf.LandscapeVideo_scale*100)
                }],
                
              },
              {
                type:'pie',
                name:'长短视频比例',
                left:'50%',
                label:{
                  show:true,
                  position:'inner',
                  formatter:'{b}: {d}%'
                },
                data:[
                  {
                    name:'长视频',
                    value:thisf.LongVideo_scale*100,
                  },{
                    name:'短视频',
                    value:100-(thisf.LongVideo_scale*100)
                  }
                ]
              },
            ]
          }
          myChart.setOption(option)
        }
        setVideosAvg()
        setVideosScale()
      }
    }
  }
</script>

<style lang="less">
  .echarts-cardbox{
    .el-statistic{
      text-align: center;
      line-height: 40px;
    }
    .el-row:not(:first-child){
      margin-top: 10px;
    }
  }
  .video-wh{
    p{
      height: 20px;
      line-height: 20px;
    }
  }
  .echarts-contentbox{
    height: 400px;
    width: 100%;
  }
</style>