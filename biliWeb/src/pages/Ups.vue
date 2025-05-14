<template>
  <el-row>
    <el-col :span="12">
      <div ref="ups_level" class="echarts-contentbox" ></div>
    </el-col>
    <el-col :span="12">
      <div ref="ups_avg" style="height: 290px;"></div>
      <el-card shadow="hover" class="echarts-cardbox">
        <el-row>
          <el-col :span="6"><el-statistic title="平均关注数" :value="upsData.following"></el-statistic></el-col>
          <el-col :span="6"><el-statistic title="平均粉丝数" :value="upsData.follower/1000"><template #suffix>K</template></el-statistic></el-col>
          <el-col :span="6"><el-statistic title="平均发布视频数" :value="upsData.video"></el-statistic></el-col>
          <el-col :span="6"><el-statistic title="平均获赞数" :value="upsData.videolike/1000"><template #suffix>K</template></el-statistic></el-col>
        </el-row>
      </el-card>
    </el-col>
  </el-row>
  <el-row>
    <el-col :span="12">
      <div ref="ups_scale" class="echarts-contentbox" ></div>
    </el-col>
    <el-col :span="12">
      <div ref="ups_vip" class="echarts-contentbox" ></div>
    </el-col>
  </el-row>
  <el-row>
    <el-col :span="12">
      <div ref="ups_sex" class="echarts-contentbox" ></div>
    </el-col>
    <el-col :span="12">
      <div ref="ups_movies" class="echarts-contentbox" ></div>
      <el-card shadow="hover" class="echarts-cardbox movies-card" >
        <el-row ><el-statistic title="平均追番数" :value="upsData.avg_bangumi"/></el-row>
        <el-row ><el-statistic title="平均追电影数" :value="upsData.avg_cinema"/></el-row>
      </el-card>
    </el-col>
  </el-row>
</template>

<script>
  import * as echarts from 'echarts'
  import store from '../store'
  export default{
    data(){
      return{
        upsData:{
          following:0,
          follower:0,
          video:0,
          videolike:0,
          avg_bangumi:0,
          avg_cinema:0,
          bangumi:0,
          bangumiandcinema:0,
          cinema:0,
          updaterate:0,
          duration:0,
          senior_member:0,
          longvideo:0,
          official:0,
          level:[],
          sex:[],
          vip:[]
        }
      }
    },
    async mounted(){
      await this.getUps()
      this.getEchartData()
    },
    methods:{
      async getUps(){
        let upsData={}
        await store.dispatch('tourists/getUpsInfo')
        .then((response) => {
          console.log(response)
          upsData=response
        }).catch((error)=>{
          console.log(error)
        })
        this.upsData=upsData
        console.log(this.upsData.level[0])
      },
      getEchartData(){
        const thisf=this
        function setLevel(){//等级分布可视化
          let level=thisf.upsData.level
          let chart = thisf.$refs.ups_level
          let myChart = echarts.init(chart)
          let option = {
            title: {
              text: 'up主等级分布'
            },
            tooltip:{
              trigger:'item'
            },
            legend:{
              left :0,
              top:30,
              orient:'vertical'
            },
            series:[
              {
                type:'pie',
                data:level
              }
            ]
          }
          myChart.setOption(option)
        }
        function setAvg(){//平均数据可视化
          let avgs=[thisf.upsData.following,thisf.upsData.follower,thisf.upsData.video,thisf.upsData.favourite]
          let following=parseFloat(thisf.upsData.following)
          let follower=parseFloat(thisf.upsData.follower)
          let scale_following=(following/(following+follower))
          let chart = thisf.$refs.ups_avg
          let myChart = echarts.init(chart)
          let option = {
            dataset:{
              source:[
                ['product','关注/粉丝数','关注/粉丝比例'],
                ['关注',following,scale_following*100],
                ['粉丝',follower,(1-scale_following)*100]
              ]
            },
            tooltip:{
              trigger:'item'
            },
            xAxis:{type: 'category'},
            yAxis:{},
            grid: [{ right: '50%' }, { left: '50%' }],
            series:[
              {
                type:'bar',
                name:'关注/粉丝数',
                label:{
                  show:true,
                  distance:5
                },
                tooltip:{
                  trigger:'item'
                },
              },
              {
                type:'pie',
                name:'关注/粉丝比例',
                left:'55%',
                label:{
                  show:true,
                  position:'inner',
                  formatter:'{b}: {d}%'
                },
                tooltip:{
                  trigger:'item',
                  formatter:'{a}<br/><span style="background-color: #95d475;display: inline-block; width: 8px;height: 8px; border-radius: 50%;margin-right: 4px;line-height: 12px"></span>{b}:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{d}%'
                }
              }
            ]
          }
          myChart.setOption(option)
        }
        function setScale(){//比例数据可视化
          let chart = thisf.$refs.ups_scale
          let myChart = echarts.init(chart)
          let option = {
            tooltip:{
              trigger:'item'
            },
            title: {
              text: '长短视与有无认证up主'
            },
            legend: {
              show:true,
              // orient :'vertical',
              left:0,
              // top:'15%',
              bottom:'15%',
            },
            series:[
              {
                type:'pie',
                name:'长短视频比例',
                right:'50%',
                // left:'15%',
                label:{
                  show:true,
                  position:'inner',
                  formatter:'{b}: {d}%'
                },
                data:[{
                  name:'长视频up主',
                  value:thisf.upsData.longvideo
                },{
                  name:'短视频up主',
                  value:1-thisf.upsData.longvideo
                }],
                
              },
              {
                type:'pie',
                name:'有无认证比例',
                left:'50%',
                label:{
                  show:true,
                  position:'inner',
                  formatter:'{b}: {d}%'
                },
                data:[
                  {
                    name:'无认证up主',
                    value:thisf.upsData.official,
                  },{
                    name:'有认证up主',
                    value:1-thisf.upsData.official
                  }
                ]
              }
            ]
          }
          myChart.setOption(option)
        }
        function setVip(){//vip分布可视化
          let vips=thisf.upsData.vip
          vips=vips.map((vip)=>{
            let ch_vip={
              name:'',
              value:vip.value
            }
            switch(vip.name){
              case '0':
                ch_vip.name='无会员'
                break;
              case '1':
                ch_vip.name='月度大会员'
                break;
              case '3':
                ch_vip.name='年度大会员'
                break;
              case '7':
                ch_vip.name='十年大会员'
                break;
              case '15':
                ch_vip.name='百年大会员'
                break;
              default:
                ch_vip.name='其他'
            }
            return ch_vip
          })
          let chart = thisf.$refs.ups_vip
          let myChart = echarts.init(chart)
          let option = {
            title: {
              text: 'up主VIP分布'
            },
            tooltip:{
              trigger:'item'
            },
            legend:{
              right :0,
              top:30,
              orient:'vertical'
            },
            series:[
              {
                type:'pie',
                data:vips
              }
            ]
          }
          myChart.setOption(option)
          console.log(vips)
        }
        function setSex(){//性别分布可视化
          let sex=thisf.upsData.sex
          let chart = thisf.$refs.ups_sex
          let myChart = echarts.init(chart)
          let option = {
            title: {
              text: 'up主性别分布'
            },
            tooltip:{
              trigger:'item'
            },
            legend:{
              left :0,
              bottom:'10%',
              orient:'vertical'
            },
            series:[
              {
                type:'pie',
                data:sex
              }
            ]
          }
          myChart.setOption(option)
        }
        function setMovies(){//比例数据可视化
          let movies=thisf.upsData
          let binge=parseFloat(movies.bangumi)+parseFloat(movies.cinema)-parseFloat(movies.bangumiandcinema)
          let chart = thisf.$refs.ups_movies
          let myChart = echarts.init(chart)
          let option = {
            tooltip:{
              trigger:'item'
            },
            xAxis:{type: 'category'},
            yAxis:{},
            legend: {
              show:true,
              // orient :'vertical',
              left:0,
              bottom:0,
            },
            grid: [{ right: '45%',top:'40%'}],
            series:[
              {
                type:'pie',
                name:'追剧比例',
                right:'60%',
                bottom:'60%',
                label:{
                  show:true,
                  position:'inner',
                  formatter:'{b}: {d}%'
                },
                data:[{
                  name:'追剧',
                  value:binge
                },{
                  name:'不追剧',
                  value:1-binge
                }],
                
              },
              {
                type:'pie',
                name:'追番比例',
                left:'2%',
                bottom:'60%',
                label:{
                  show:true,
                  position:'inner',
                  formatter:'{b}: {d}%'
                },
                data:[
                  {
                    name:'追番',
                    value:movies.bangumi,
                  },{
                    name:'不追番',
                    value:1-movies.bangumi
                  }
                ]
              },
              {
                type:'pie',
                name:'追电影比例',
                left:'60%',
                bottom:'60%',
                label:{
                  show:true,
                  position:'inner',
                  formatter:'{b}: {d}%'
                },
                data:[
                  {
                    name:'追电影',
                    value:movies.cinema,
                  },{
                    name:'不追电影',
                    value:1-movies.cinema
                  }
                ]
              },
              {
                type:'bar',
                name:'所有追剧比例',
                label:{
                  show:true,
                  position:'inner',
                  formatter:'{b}'
                },
                data:[
                  {
                    name:'追番',
                    value:movies.bangumi,
                  },{
                    name:'追电影',
                    value:movies.cinema
                  },{
                    name:'追番、追电影',
                    value:movies.bangumiandcinema
                  }
                ]
              }
            ]
          }
          myChart.setOption(option)
        }
        setLevel()
        setAvg()
        setVip()
        setScale()
        setSex()
        setMovies()
      }
    }
  }
</script>

<style lang="less">
  .echarts-contentbox{
    height: 400px;
  }
  .echarts-cardbox{
    // height: 110px;
    text-align: center;
    margin-top: -30px;
    background-color: rgba(0, 0, 0, 0);
    .el-statistic{
      text-align: center;
      line-height: 40px;
    }
    &.movies-card{
      width: 125px;
      margin: -240px 55px 0px auto;
    }
  }
</style>