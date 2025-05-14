<template>
  
  <el-menu
    default-active="/"
    class="el-menu-vertical-demo"
   @open="handleOpen"
    @close="handleClose"
    :router="true"
  >
    <el-menu-item index="/" >
      <el-icon></el-icon>
      <span>bilibili数据挖掘</span>
    </el-menu-item>
    <el-sub-menu index="/users">
      <template #title>
        <el-icon><User /></el-icon>
        <span>用户分析</span>
      </template>
        <!-- <el-sub-menu index="/users">
          <template #title>
            <span>活跃用户数据</span>
          </template>
          <el-menu-item index="/userspage/1">等级、粉丝</el-menu-item>
          <el-menu-item index="/userspage/2">VIP、UP</el-menu-item>
          <el-menu-item index="/userspage/3">性别、追剧</el-menu-item>
        </el-sub-menu> -->
        <el-menu-item index="/users">所有用户数据</el-menu-item>
        <el-menu-item index="/user">单用户数据</el-menu-item>
    </el-sub-menu>
    <el-sub-menu  index="/videos">
      <template #title>
        <el-icon><VideoCamera /></el-icon>
        <span>视频分析</span>
      </template>
      <el-menu-item index="/videos">所有视频数据</el-menu-item>
      <el-menu-item index="/video/0">单视频数据</el-menu-item>
    </el-sub-menu>
    <el-menu-item index="/ups" ><!-- disabled -->
      <el-icon><Avatar /></el-icon>
      <span>up主分析</span>
    </el-menu-item>
    <el-menu-item index="/admin" >
      <el-icon><setting /></el-icon>
      <span>设置</span>
    </el-menu-item>
  </el-menu>
</template>

<script>
  
</script>

<style>
  .el-menu-vertical-demo:not(.el-menu--collapse) {
    width: 200px;
    min-height: 400px;
  }
</style>