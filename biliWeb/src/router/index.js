import * as VueRouter from 'vue-router'
import store from '../store'

import HelloWorld from '../components/HelloWorld.vue'
import Users from '../pages/Users.vue'
import UsersPage from '../pages/users/UsersPage.vue'
import Us1 from '../pages/users/us1.vue'
import Us2 from '../pages/users/us2.vue'
import Us3 from '../pages/users/us3.vue'
import User from '../pages/User.vue'
import Videos from '../pages/Videos.vue'
import Video from '../pages/Video.vue'
import Ups from '../pages/Ups.vue'
import Admin from '../pages/Admin.vue'
import Login from '../pages/Login.vue'
import Signup from '../pages/Signup.vue'
// 316568752

const routes = [{
    path: '/',
    name: 'Users',
    component: Users,
  },
  {
    path: '/users',
    name: 'Users',
    component: Users
  },
  {
    path: '/userspage',
    name: 'UsersPage',
    component: UsersPage,
    children: [{
        path: '1',
        component: Us1,
      },
      {
        path: '2',
        component: Us2,
      },
      {
        path: '3',
        component: Us3,
      },
    ]
  },
  {
    path: '/user',
    name: 'User',
    component: User
  },
  {
    path: '/videos',
    name: 'Videos',
    component: Videos
  },
  {
    path: '/video/:id',
    name: 'Video',
    component: Video
  },
  {
    path: '/ups',
    name: 'Ups',
    component: Ups
  },
  {
    path: '/admin',
    name: 'Admin',
    component: Admin,
    beforeEnter: (to, from, next) => {
      if (store.getters.getToken) {
        next()
      }else{
        next('/login')
      }
      
    }
  },
  {
    path: '/login',
    name: 'Login',
    component: Login,
  },
  {
    path: '/signup',
    name: 'Signup',
    component: Signup,
  },
]

const router = VueRouter.createRouter({
  routes,
  history: VueRouter.createWebHistory()
})

export default router
