<template>
  <el-row>
    <el-card class="input-card">
      请输入用户UID：
      <el-input v-model="uid" placeholder="UID" clearable type="number" >
        <!-- <template #prepend>
          <el-icon><UserFilled /></el-icon>
        </template> -->
        <!-- <template #append>
          <el-button @click="cilikUid()" type="primary">确定</el-button>
        </template> -->
      </el-input>
      <el-button @click="cilikUid()" type="primary" plain>确定</el-button>
    </el-card>
  </el-row>
  <el-row>
    <el-card class="input-card" style="margin-top: 20px;">
      <el-descriptions  :column="3" size="large" direction="horizontal" border>
        <el-descriptions-item span="1">
          <template #label>
            <div class="cell-item">
              <el-icon>
                <user />
              </el-icon>
              用户头像
            </div>
          </template>
          <el-avatar shape="square" size="default" loading="lazy" fit="cover" :src="userData.face" />
          <!-- <img src="https://image.baidu.com/search/down?tn=download&word=download&ie=utf8&fr=detail&url=http://i2.hdslb.com/bfs/face/fde8917f71229586e48b1ae482c6d1744915b858.jpg"/> -->
        </el-descriptions-item>
        <el-descriptions-item>
          <template #label>
            <div class="cell-item">
              <el-icon><user /></el-icon>
              用户名
            </div>
          </template>
          {{userData.name}}
        </el-descriptions-item>
        <el-descriptions-item>
          <template #label>
            <div class="cell-item">
              <el-icon><user /></el-icon>
              性别
            </div>
          </template>
          {{userData.sex}}
        </el-descriptions-item>
        <el-descriptions-item span="3">
          <template #label>
            <div class="cell-item">
              <el-icon><user /></el-icon>
              个性签名
            </div>
          </template>
          {{userData.sign}}
        </el-descriptions-item>
        <el-descriptions-item>
          <template #label>
            <div class="cell-item">
              <el-icon><user /></el-icon>
              账号等级
            </div>
          </template>
          {{userData.level}}
        </el-descriptions-item>
        <el-descriptions-item>
          <template #label>
            <div class="cell-item">
              <el-icon><user /></el-icon>
              VIP情况
            </div>
          </template>
          {{userData.vip}}
        </el-descriptions-item>
        <el-descriptions-item>
          <template #label>
            <div class="cell-item">
              <el-icon><user /></el-icon>
              投稿数
            </div>
          </template>
          {{userData.archive_count}}
        </el-descriptions-item>
        <el-descriptions-item>
          <template #label>
            <div class="cell-item">
              <el-icon><user /></el-icon>
              粉丝数
            </div>
          </template>
          {{userData.fans}}
        </el-descriptions-item>
        <el-descriptions-item>
          <template #label>
            <div class="cell-item">
              <el-icon><user /></el-icon>
              关注数
            </div>
          </template>
          {{userData.friend}}
        </el-descriptions-item>
        
        <el-descriptions-item>
          <template #label>
            <div class="cell-item">
              <el-icon><user /></el-icon>
              总获赞量
            </div>
          </template>
          {{userData.like_num}}
        </el-descriptions-item>
        <el-descriptions-item span="1.5">
          <template #label>
            <div class="cell-item">
              <el-icon><user /></el-icon>
              目前状况
            </div>
          </template>
          <div v-if="userData.uid">
            <el-tag>{{userData.up}}</el-tag>
            <el-tag>{{userData.bangumi}}</el-tag>
            <el-tag>{{userData.cinema}}</el-tag>
          </div>
        </el-descriptions-item>
        <el-descriptions-item >
          <template #label>
            <div class="cell-item">
              <el-icon><user /></el-icon>
              人群比例
            </div>
          </template>
          {{userData.scale}}
        </el-descriptions-item>
      </el-descriptions>
    </el-card>
  </el-row>
</template>

<script>
  import { Calendar, Search } from '@element-plus/icons-vue'
  import store from '../store'
  
  export default{
    data(){
      return{
        uid:"",
        userData:{
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
        }
      }
    },
    async mounted(){
      
    },
    methods:{
      async getUser(){
        let userData={}
        await store.dispatch("tourists/getUserInfo",this.uid)
        .then(res=>userData=res)
        .catch(err=>userData=res)
        console.log(userData)
        try{
          this.userData=userData
        }catch(e){
          console.log("单用户数据错误")
          return null
        }
      },
      cilikUid(){
        console.log(this.uid)
        this.getUser()
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
</style>