<template>
  <el-menu mode="horizontal" >
    <el-menu-item>bilibili数据挖掘</el-menu-item>
    <div v-if="userName==''" class="top-left">
      <router-link class="alink" to="/login">
        登录
      </router-link>|
      <router-link class="alink" to="/signup">
        注册
      </router-link>
    </div>
    <div v-else class="top-left" @click="goout()">
      <el-link >
        欢迎回来,{{userName}}|退出登录
      </el-link>
    </div>
    
  </el-menu>
</template>

<script setup>
  import store from '../store'
  import router from '../router'
  import { getCurrentInstance,reactive,toRefs,ref } from 'vue'
  let userName=ref(store.getters.getUserName)
  function goout(){
    store.commit('delLogin')
    router.go(0)
  }
</script>

<style>
  .top-left{
    position: absolute;
    right: 10px;
  }
</style>