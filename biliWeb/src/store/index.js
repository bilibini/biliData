import { createStore } from 'vuex'
import { ElMessage } from 'element-plus'
import router from '../router'
import {get,post,loginGet,loginPost,loggedGet,loggedPost} from '../request'

const tourists={
  namespaced:true,
  state:{
    userInfo:{
      uid:"",
      name:"",
      sex:"",
      face:"",
      fans:"",
      sign:"",
      friend:"",
      level:"",
      vip:"",
      like_num:"",
      video:"",
      archive_count:"",
      bangumi:"",
      cinema:"",
      up:"",
      scale:0
    },
    usersInfo:{
      fans_badge:0,
      favourite:0,
      follower:0,
      following:0,
      silence:0,
      unsign:0,
      up:0,
      video:0,
      level:[],
      sex:[],
      vip:[],
      movies:{},
    },
    videoInfo:{
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
    },
    videosInfo:{
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
    },
    upsInfo:{
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
  },
  mutations:{
    deltouristsInfo(state){
      localStorage.removeItem('usersInfo')
      localStorage.removeItem('videosInfo')
    },
    setUsersInfo(state,usersInfo){
      state.usersInfo=usersInfo
      localStorage.setItem('usersInfo',JSON.stringify(usersInfo))
    },
    setVideosInfo(state,videosInfo){
      state.videosInfo=videosInfo
      localStorage.setItem('videosInfo',JSON.stringify(videosInfo))
    },
    setUpsInfo(state,upsInfo){
      state.upsInfo=upsInfo
      localStorage.setItem('upsInfo',JSON.stringify(upsInfo))
    },
  },
  actions:{
    async getUsersInfo(context){
      async function getUsersData(){
        let response={}
        await get('/user/users.php').then(res=>{response=res})
        return response
      }
      let usersInfo=context.state.usersInfo
      try{
        if(!usersInfo.up){
          usersInfo=JSON.parse(localStorage.getItem('usersInfo'))
          if(!usersInfo.up){
            usersInfo=await getUsersData()
          }
        }else{
          return Promise.resolve(usersInfo)
        }
      }catch(e){
        usersInfo=await getUsersData()
      }
      if(!usersInfo.up){
        return Promise.reject(context.state.usersInfo)
      }else{
        context.commit('setUsersInfo',usersInfo)
        return Promise.resolve(usersInfo)
      }
    },
    async getUserInfo(context,uid){
      function vipname(vip){
        vip=''+vip
        let ch_vip=''
        switch(vip){
          case '0':
            ch_vip='无会员'
            break;
          case '1':
            ch_vip='月度大会员'
            break;
          case '3':
            ch_vip='年度大会员'
            break;
          case '7':
            ch_vip='十年大会员'
            break;
          case '15':
            ch_vip='百年大会员'
            break;
          default:
            ch_vip='其他'
        }
        return ch_vip
      }
      if(!uid){
        return {}
      }
      let params={uid}
      let response={}
      await get('/user/card.php',params).then(res=>{response=res})
      context.state.userInfo.uid=uid
      if(response.code!=0){
        if(response.code==404){
          ElMessage({
            showClose: true,
            message: '暂无此用户哟~',
            type: 'warning',
          })
        }else{
          ElMessage({
            showClose: true,
            message: '用户UID错误，请核对后重新输入',
            type: 'error',
          })
        }
        return Promise.reject(context.state.userInfo)
      }
      response=response.data
      context.state.userInfo.name=response.card.name
      context.state.userInfo.face='https://image.baidu.com/search/down?tn=download&word=download&ie=utf8&fr=detail&url='+response.card.face
      context.state.userInfo.sex=response.card.sex
      context.state.userInfo.sign=response.card.sign
      let vip_id=response.card.vip.role
      context.state.userInfo.vip=vipname(vip_id)
      context.state.userInfo.fans=response.card.fans
      context.state.userInfo.friend=response.card.friend
      context.state.userInfo.level=response.card.level_info.current_level
      context.state.userInfo.like_num=response.like_num
      context.state.userInfo.archive_count=response.archive_count
      
      await get('/user/navnum.php',params).then(res=>{response=res.data})
      let videoNum=parseInt(response.video)
      context.state.userInfo.up=videoNum>0?"up主":"观看者"
      context.state.userInfo.bangumi=parseInt(response.bangumi)>0?"追番":"不追番"
      context.state.userInfo.cinema=parseInt(response.cinema)>0?"追电影":"不追电影"
      
      await context.dispatch('getUsersInfo').then(res=>{response=res})
      let dengji=parseFloat(response.level[parseInt(context.state.userInfo.level)-1].value)
      let zuifan=parseFloat(response.movies.bangumi)
      if(context.state.userInfo.bangumi<=0){zuifan=1-zuifan}
      let dianying=parseFloat(response.movies.cinema)
      if(context.state.userInfo.cinema<=0){dianying=1-dianying}
      let xingbie=parseFloat(response.sex.filter(x=>x.name==context.state.userInfo.sex)[0].value)/100
      let vip=parseFloat(response.vip.filter(x=>x.name==vip_id)[0].value)/100
      let isup=parseFloat(response.up)
      if(videoNum<=0){isup=1-isup}
      let unsign=parseFloat(response.unsign)
      if(context.state.userInfo.sign){unsign=1-unsign}
      
      let scale=1*dengji*zuifan*dianying*xingbie*vip*isup*unsign
      context.state.userInfo.scale=scale
      return Promise.resolve(context.state.userInfo)
    },
    async getVideosInfo(context){
      let videosData=JSON.parse(localStorage.getItem('videosInfo'))
      if(videosData){
        return Promise.resolve(videosData)
      }
      
      await get('/video/videos.php')
      .then((response) => {
        console.log(response)
        videosData=response
      }).catch((error)=>{
        console.log(error)
      })
      context.state.videosInfo.view_avg=(Number(videosData.view_avg)/1000).toFixed(2)
      context.state.videosInfo.danmaku_avg=(Number(videosData.danmaku_avg)/1000).toFixed(2)
      context.state.videosInfo.reply_avg=(Number(videosData.reply_avg)/1000).toFixed(2)
      context.state.videosInfo.favorite_avg=(Number(videosData.favorite_avg)/1000).toFixed(2)
      context.state.videosInfo.coin_avg=(Number(videosData.coin_avg)/1000).toFixed(2)
      context.state.videosInfo.share_avg=(Number(videosData.share_avg)/1000).toFixed(2)
      context.state.videosInfo.videolike_avg=(Number(videosData.videolike_avg)/1000).toFixed(2)
      context.state.videosInfo.duration_avg=(Number(videosData.duration_avg)/60).toFixed(1)
      context.state.videosInfo.width_avg=Number(videosData.width_avg)
      context.state.videosInfo.height_avg=Number(videosData.height_avg)
      context.state.videosInfo.LandscapeVideo_scale=Number(videosData.LandscapeVideo_scale)
      context.state.videosInfo.LongVideo_scale=Number(videosData.LongVideo_scale)
      context.commit('setVideosInfo',context.state.videosInfo)
      return Promise.resolve(context.state.videosInfo)
    },
    async getVideoInfo(context,aid,bvid){
      let videoData=null;
      let params={aid,bvid}
      await get('/video/video.php',params)
      .then((response) => {
        console.log(response)
        videoData=response
      }).catch((error)=>{
        console.log(error)
      })
      //错误检测
      if(videoData.code!=0){
        if(videoData.code==-404){
          ElMessage({
            showClose: true,
            message: '暂无此视频哟~',
            type: 'warning',
          })
        }else{
          ElMessage({
            showClose: true,
            message: '信息错误错误，请核对后重新输入',
            type: 'error',
          })
        }
        return Promise.reject({})
      }
      videoData=videoData.data
      aid=videoData.aid
      bvid=videoData.bvid
      let {desc,dimension,duration,owner,pic,pubdate,stat,title,tname}=videoData
      context.state.videoInfo.aid=aid
      context.state.videoInfo.bvid=bvid
      context.state.videoInfo.desc=desc
      context.state.videoInfo.width=dimension.width
      context.state.videoInfo.height=dimension.height
      context.state.videoInfo.duration=duration
      context.state.videoInfo.owner=owner
      context.state.videoInfo.pic=pic
      context.state.videoInfo.pubdate=pubdate
      context.state.videoInfo.stat=stat
      context.state.videoInfo.title=title
      context.state.videoInfo.tname=tname
      context.state.videoInfo.owner.face="https://image.baidu.com/search/down?tn=download&word=download&ie=utf8&fr=detail&url="+context.state.videoInfo.owner.face
      context.state.videoInfo.pic="https://image.baidu.com/search/down?tn=download&word=download&ie=utf8&fr=detail&url="+pic
      return Promise.resolve(context.state.videoInfo)
    },
    async getUpsInfo(context){
      let upsData=JSON.parse(localStorage.getItem('upsInfo'))
      if(upsData){
        return Promise.resolve(upsData)
      }
      let upsInfo={
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
      await get('/up/ups.php')
      .then((response) => {
        console.log(response)
        upsData=response
      }).catch((error)=>{
        console.log(error)
      })
      upsInfo.following=Number((Number(upsData.following)).toFixed(2))//平均关注数
      upsInfo.follower=Number((Number(upsData.follower)).toFixed(2))//平均粉丝数
      upsInfo.video=Number((Number(upsData.following)).toFixed(2))//平均投稿数
      upsInfo.videolike=Number((Number(upsData.videolike)).toFixed(2))//平均视频点赞数
      upsInfo.updaterate=Number((Number(upsData.updaterate)).toFixed(2))//平均视频更新频率（小时）
      upsInfo.duration=Number((Number(upsData.duration)).toFixed(2))//平均视频时长（分钟）
      upsInfo.avg_bangumi=Number(Number(upsData.avg_bangumi).toFixed(2))//平均追番数
      upsInfo.avg_cinema=Number(Number(upsData.avg_cinema).toFixed(2))//平均看电影数
      upsInfo.bangumi=(Number(upsData.bangumi))//占比
      upsInfo.bangumiandcinema=(Number(upsData.bangumiandcinema))//占比
      upsInfo.cinema=(Number(upsData.cinema))//占比
      upsInfo.senior_member=(Number(upsData.senior_member))//硬核会员占比
      upsInfo.longvideo=(Number(upsData.longvideo))//长视频up主占比
      upsInfo.official=(Number(upsData.official))//无认证up主占比
      upsInfo.level=upsData.level
      upsInfo.sex=upsData.sex
      upsInfo.vip=upsData.vip
      
      context.state.upsInfo=upsInfo
      context.commit('setUpsInfo',context.state.upsInfo)
      return Promise.resolve(context.state.upsInfo)
    },
  }
}

const store=createStore({
  state:{
    token:"",
    userName:"",
    id:"",
    mid:"",
    rank:0,
  },
  getters:{
    getToken(state){
      if(state.token||localStorage.getItem('token')){
        return state.token||localStorage.getItem('token')
      }else{
        // ElMessage({
        //   message:'未登录，请登录后操作',
        //   duration:1500,
        //   type:'error'
        // })
        // // state.commit('delLogin')
        // store.commit('delLogin')
        // router.replace({
        //   path:'/login'
        // })
        return ""
      }
    },
    getUserName(state){
      if(state.userName){
        return state.userName
      }else if(localStorage.getItem('userName')){
        state.userName=localStorage.getItem('userName')
        return state.userName
      }else{
        return ""
      }
    },
    getInfo(state){
      let info=localStorage.getItem('info')
      if(!info){
        ElMessage({
          message:'未登录，请登录后操作',
          duration:1500,
          type:'error'
        })
        store.commit('delLogin')
        router.replace({
          path:'/login'
        })
        return false
      }
      return JSON.parse(info)
    }
  },
  mutations:{
    delLogin(state){
      console.log("2333333")
      state.token=""
      localStorage.removeItem('token')
      state.userName=""
      localStorage.removeItem('userName')
      localStorage.removeItem('info')
      ElMessage({
        message:'已成功退出登录~',
        duration:1500,
        type:'success'
      })
    },
    setToken(state,token){
      state.token=token
      localStorage.setItem('token',token)
    },
    setUserName(state,userName){
      state.userName=userName
      localStorage.setItem('userName',userName)
    },
    setInfo(state,info){
      let {id,mid,rank,token,username}=info
      state.id=id
      state.mid=mid
      state.rank=parseInt(rank)
      state.token=token
      state.userName=username
      localStorage.setItem('token',token)
      localStorage.setItem('userName',username)
      localStorage.setItem('info',JSON.stringify(info))
    }
  },
  actions:{
    
  },
  modules:{
    tourists
  }
})

export default store