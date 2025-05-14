<template>
  <el-card class="cardbox">
    <template #header>
      <div class="card-header">
        <el-text>账号注册</el-text>
      </div>
    </template>
    <el-form class="card-form" ref="signupform" :rules="rules" :model="signupform" label-width="80px">
      <el-form-item label="用户名" prop="username">
        <el-input v-model="signupform.username"></el-input>
      </el-form-item>
      <el-form-item label="B站mid" prop="mid">
        <el-input v-model="signupform.mid"></el-input>
      </el-form-item>
      <el-form-item label="密码" prop="password">
        <el-input type="password" v-model="signupform.password"></el-input>
      </el-form-item>
      <el-form-item label="重复密码" prop="confirmPassword">
        <el-input type="password" v-model="signupform.confirmPassword"></el-input>
      </el-form-item>
      <el-row>
        <el-button type="primary" @click="signup">注册</el-button>
        <el-button @click="resetForm">重置</el-button>
      </el-row>
    </el-form>
    <router-link  to="/login"><el-link type="primary">登录</el-link></router-link>
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
        signupform: {
          username: '',
          mid:'',
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
        } else if (value !== this.signupform.password) {
          callback(new Error('两次输入的密码不一致'))
        } else {
          callback()
        }
      },
      async signup(){
        await this.$refs.signupform.validate(async valid => {
          if (valid) {
            let password=CryptoJS.MD5(this.signupform.password).toString()
            let mid=this.signupform.mid
            let username=this.signupform.username
            await loginPost('/signup.php',{username,mid,password}).then(res=>{
              ElNotification({
                message:'账号注册成功,欢迎您的加入~',
                type: 'success',
              })
              router.replace({
                path:'/login'
              })
            }).catch(err=>{
              ElNotification({
                message:err.data.message,
                type: 'error',
              })
            })
            console.log(password,username);
          }
        })
      },
      resetForm() {
        this.$refs.signupform.resetFields();
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
    }
    .el-input{
      width:80%;
    }
    .el-button{
      width: 150px;
    }
  }
</style>