<template>
  <el-row>
    <el-col :span="12">
      <div ref="users_level" class="echarts-contentbox" ></div>
    </el-col>
    <el-col :span="12">
      <div ref="users_avg" style="height: 290px;"></div>
      <el-card shadow="hover" class="echarts-cardbox">
        <el-row>
          <el-col :span="6"><el-statistic title="平均关注数" :value="usersData.following"/></el-col>
          <el-col :span="6"><el-statistic title="平均粉丝数" :value="usersData.follower"></el-statistic></el-col>
          <el-col :span="6"><el-statistic title="平均发布视频数" :value="usersData.video"></el-statistic></el-col>
          <el-col :span="6"><el-statistic title="平均收藏夹数" :value="usersData.favourite"></el-statistic></el-col>
        </el-row>
      </el-card>
    </el-col>
  </el-row>
  <el-row>
    <el-col :span="12">
      <div ref="users_scale" class="echarts-contentbox" ></div>
    </el-col>
    <el-col :span="12">
      <div ref="users_vip" class="echarts-contentbox" ></div>
    </el-col>
  </el-row>
  <el-row>
    <el-col :span="12">
      <div ref="users_sex" class="echarts-contentbox" ></div>
    </el-col>
    <el-col :span="12">
      <div ref="users_movies" class="echarts-contentbox" ></div>
      <el-card shadow="hover" class="echarts-cardbox movies-card" >
        <el-row ><el-statistic title="平均追番数" :value="usersData.movies.avg_bangumi"/></el-row>
        <el-row ><el-statistic title="平均追电影数" :value="usersData.movies.avg_cinema"/></el-row>
      </el-card>
    </el-col>
  </el-row>
  
</template>

<script>
  import * as echarts from 'echarts'
  import axios from 'axios'
  export default{
    data(){
      return{
        usersData:{
          following:0,
          follower:0,
          favourite:0,
          video:0,
          up:0,
          unsign:0,
          silence:0,
          fans_badge:0,
          movies:{
            avg_bangumi:0,
            avg_cinema:0,
          }
        }
      }
    },
    async mounted(){
      await this.getUsers()
      this.getEchartData()
    },
    methods:{
      async getUsers(){
        let usersData={}
        await axios.get("http://服务器地址/display/users/users.php")
        .then((response) => {
          console.log(response.data)
          usersData=response.data
        }).catch((error)=>{
          console.log(error)
        })
        this.usersData=usersData
        console.log(this.usersData.level[0])
      },
      getEchartData(){
        const thisf=this
        function setLevel(){//等级分布可视化
          let level=thisf.usersData.level
          let chart = thisf.$refs.users_level
          let myChart = echarts.init(chart)
          let option = {
            title: {
              text: '活跃用户等级分布'
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
          let avgs=[thisf.usersData.following,thisf.usersData.follower,thisf.usersData.video,thisf.usersData.favourite]
          let following=parseFloat(thisf.usersData.following)
          let follower=parseFloat(thisf.usersData.follower)
          let scale_following=(following/(following+follower))
          let chart = thisf.$refs.users_avg
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
          let chart = thisf.$refs.users_scale
          let myChart = echarts.init(chart)
          let option = {
            tooltip:{
              trigger:'item'
            },
            legend: {
              show:true,
              orient :'vertical',
              left:0,
              top:'25%',
            },
            series:[
              {
                type:'pie',
                name:'up主比例',
                right:'40%',
                bottom:'45%',
                left:'15%',
                label:{
                  show:true,
                  position:'inner',
                  formatter:'{b}: {d}%'
                },
                data:[{
                  name:'up主',
                  value:thisf.usersData.up
                },{
                  name:'普通用户',
                  value:1-thisf.usersData.up
                }],
                
              },
              {
                type:'pie',
                name:'封禁比例',
                left:'50%',
                bottom:'45%',
                label:{
                  show:true,
                  position:'inner',
                  formatter:'{b}: {d}%'
                },
                data:[
                  {
                    name:'封禁用户',
                    value:thisf.usersData.silence,
                  },{
                    name:'正常用户',
                    value:1-thisf.usersData.silence
                  }
                ]
              },
              {
                type:'pie',
                name:'拥有粉丝勋章比例',
                right:'40%',
                top:'45%',
                left:'15%',
                label:{
                  show:true,
                  position:'inner',
                  formatter:'{b}: {d}%'
                },
                data:[
                  {
                    name:'有粉丝勋章',
                    value:thisf.usersData.fans_badge,
                  },{
                    name:'无粉丝勋章',
                    value:1-thisf.usersData.fans_badge
                  }
                ]
              },
              {
                type:'pie',
                name:'个人签名比例',
                left:'50%',
                top:'45%',
                label:{
                  show:true,
                  position:'inner',
                  formatter:'{b}: {d}%'
                },
                data:[
                  {
                    name:'无个人签名',
                    value:thisf.usersData.unsign,
                  },{
                    name:'有个人签名',
                    value:1-thisf.usersData.unsign
                  }
                ]
              }
            ]
          }
          myChart.setOption(option)
        }
        function setVip(){//vip分布可视化
          let vips=thisf.usersData.vip
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
          let chart = thisf.$refs.users_vip
          let myChart = echarts.init(chart)
          let option = {
            title: {
              text: '活跃用户VIP分布'
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
          let sex=thisf.usersData.sex
          let chart = thisf.$refs.users_sex
          let myChart = echarts.init(chart)
          let option = {
            title: {
              text: '活跃用户性别分布'
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
          let movies=thisf.usersData.movies
          let binge=parseFloat(movies.bangumi)+parseFloat(movies.cinema)-parseFloat(movies.bangumiandcinema)
          let chart = thisf.$refs.users_movies
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
      margin: -240px 0px 0px 320px;
    }
  }
</style>