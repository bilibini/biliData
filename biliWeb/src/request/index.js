import axios from 'axios'
import { ElMessage } from 'element-plus'
import store from '../store'
import router from '../router'

function sendMessage(error){
  switch(error.response.status){
    case 400:
      ElMessage({
        message:'数据错误，请重新申请',
        duration:2000,
        type:'error',
        showClose:true
      })
      break
    case 401:
      ElMessage({
        message:'登录失败，请重新登录',
        duration:1500,
        type:'warning'
      })
      router.replace({
        path:'/login'
      })
      break
    case 403:
      ElMessage({
        message:'登录过期，请重新登录',
        duration:1500,
        type:'warning'
      })
      store.commit('delToken')
      router.replace({
        path:'/login'
      })
      break
    case 404:
      ElMessage({
        message:'网络请求失败，请检查网络',
        duration:2000,
        type:'error',
        showClose:true
      })
      break
    default:
      ElMessage({
        message:`请求错误:${error.response.statusText}`,
        duration:2000,
        type:'error',
        showClose:true
      })
  }
}

axios.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded'

const tourists = axios.create({
  baseURL:'http://localhost.com/open',
  timeout:20000,
})

const login=axios.create({
  baseURL:'http://localhost.com/auth',
  timeout:20000,
})

const logged=axios.create({
  baseURL:'http://localhost.com/user',
  timeout:25000,
})



// 用户请求拦截器
logged.interceptors.request.use(response=>{
  if(response.status==200){
    return Promise.resolve(response)
  }else{
    return Promise.reject(response)
  }
},error=>{
  return Promise.reject(error)
})
// logged.interceptors.request.use(config=>{
//   const token=store.getters.getToken
//   if(token){
//     config.headers.Authorization=`Bearer ${token}`
//   }
//   return config
// },response=>{
//   if(response.status==200){
//     return Promise.resolve(response)
//   }else{
//     return Promise.reject(response)
//   }
// },error=>{
//   return Promise.reject(error)
// })

// 访客响应拦截器
tourists.interceptors.response.use(response=>{
  if(response.status==200){
    return Promise.resolve(response)
  }else{
    return Promise.reject(response)
  }
},error=>{
  sendMessage(error)
  return Promise.reject(error.response)
})

// 登录响应拦截器
login.interceptors.response.use(response=>{
  if(response.status==200){
    return Promise.resolve(response)
  }else{
    return Promise.reject(response)
  }
},error=>{
  sendMessage(error)
  return Promise.reject(error.response)
})

// 用户响应拦截器
logged.interceptors.response.use(response=>{
  if(response.status==200){
    return Promise.resolve(response)
  }else{
    return Promise.reject(response)
  }
},error=>{
  sendMessage(error)
  return Promise.reject(error.response)
})

// 访客get请求
export function get(url,params){
  return new Promise((resolve,reject)=>{
    tourists.get(url,{params})
    .then(res=>resolve(res.data))
    .catch(err=>reject(err.data))
  })
}
// 访客post请求
export function post(url,data){
  return new Promise((resolve,reject)=>{
    tourists.post(url,data)
    .then(res=>resolve(res.data))
    .catch(err=>reject(err.data))
  })
}

// 登录get请求
export function loginGet(url,params){
  return new Promise((resolve,reject)=>{
    login.get(url,{params})
    .then(res=>resolve(res.data))
    .catch(err=>reject(err.data))
  })
}
// 登录post请求
export function loginPost(url,data){
  return new Promise((resolve,reject)=>{
    login.post(url,data)
    .then(res=>resolve(res.data))
    .catch(err=>reject(err.data))
  })
}

// 用户get请求
export function loggedGet(url,params){
  return new Promise((resolve,reject)=>{
    logged.get(url,{params})
    .then(res=>resolve(res.data))
    .catch(err=>reject(err.data))
  })
}
// 用户post请求
export function loggedPost(url,data){
  return new Promise((resolve,reject)=>{
    logged.post(url,data)
    .then(res=>resolve(res.data))
    .catch(err=>reject(err.data))
  })
}