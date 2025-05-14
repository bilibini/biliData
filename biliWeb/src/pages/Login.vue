<template>
  <el-card class="cardbox">
    <template #header>
      <div class="card-header">
        <el-text>账号登录</el-text>
      </div>
    </template>
    <el-form class="card-form" ref="loginform" :rules="rules" :model="loginform" label-width="80px">
      <el-form-item label="用户名" prop="username">
        <el-input v-model="loginform.username"></el-input>
      </el-form-item>
      <el-form-item label="密码" prop="password">
        <el-input type="password" v-model="loginform.password"></el-input>
      </el-form-item>
      <el-row>
        <el-button type="primary" @click="login">登录</el-button>
        <el-button @click="resetForm">重置</el-button>
      </el-row>
    </el-form>
    <router-link  to="/signup"><el-link type="primary">注册</el-link></router-link>
  </el-card>
  
</template>
<script>
  import CryptoJS from 'crypto-js'
  import {loginGet,loginPost} from '../request'
  import { ElNotification  } from 'element-plus'
  import store from '../store'
  import router from '../router'
  export default {
    data() {
      return {
        loginform: {
          username: '',
          password: ''
        },
        ragisterform: {
          username: '',
          password: '',
          confirmPassword:''
        },
        rules: {
          username: [
            { required: true, message: '请输入用户名', trigger: 'blur' },
            { min: 3, max: 10, message: "长度在 3 到 10个字符", trigger: "blur" },
            { pattern: /^[a-zA-Z0-9@？！，。.,]+$/, message: '请输入正确格式的用户名', trigger: 'blur' }
          ],
          password: [
            { required: true, message: '请输入密码', trigger: 'blur' },
            { min: 6, max: 18, message: "长度在 6 到 18 个字符", trigger: "blur" },
            { pattern: /^[a-zA-Z0-9@?!.,]+$/, message: '请输入正确格式的密码', trigger: 'blur' }
          ],
          confirmPassword: [
            { required: true, message: '请再次输入密码', trigger: 'blur' },
            { min: 6, max: 18, message: "长度在 6 到 18 个字符", trigger: "blur" },
            { pattern: /^[a-zA-Z0-9@?!.,]+$/, message: '请输入正确格式的密码', trigger: 'blur' },
            { validator: this.checkPassword, trigger: 'blur' }
          ]
        }
      };
    },
    mounted(){
      if(store.getters.getToken){
        ElNotification({
          message:'你已登录了哟~',
          type: 'info',
        })
        router.replace({
          path:'/admin'
        })
      }
    },
    methods: {
      checkPassword(rule, value, callback){
        if (value === '') {
          callback(new Error('请再次输入密码'))
        } else if (value !== this.ragisterform.password) {
          callback(new Error('两次输入的密码不一致'))
        } else {
          callback()
        }
      },
      async login() {
        await this.$refs.loginform.validate(async valid => {
          if (valid) {
            let password=CryptoJS.MD5(this.loginform.password).toString()
            let username=this.loginform.username
            await loginPost('/login.php',{username,password}).then(res=>{
              ElNotification({
                message:'登录成功,欢迎回来~',
                type: 'success',
              })
              store.commit("setInfo",res.data)
              router.replace({
                path:'/admin'
              })
            }).catch(err=>{
              ElNotification({
                message:err.data.message,
                type: 'error',
              })
            })
            
          }
        })
      },
      resetForm() {
        this.$refs.loginform.resetFields();
      }
    }
  };
</script>

<style lang="less">
  .cardbox{
    display: flex;
    flex-direction:column;
    justify-content:center;
    align-items: center;
    padding-bottom: 50px;
    .card-header{
      height: 90px;
    }
    .card-form{
      width: 400px;
      display: flex;
      flex-direction:column;
      // justify-content:center;
    }
    .el-row{
      display: flex;
      flex-direction:row;
      flex-wrap:nowrap;
      justify-content: center;
    }
    .el-input{
      width:80%;
    }
    .el-button{
      width: 150px;
    }
  }
</style>