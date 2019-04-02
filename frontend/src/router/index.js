import Vue from 'vue'
import Router from 'vue-router'
import JellyChat from '@/components/JellyChat'
import AuthenticationForm from '@/components/AuthenticationForm'

Vue.use(Router)

const router = new Router({
  routes: [
    {
      path: '/chats/:uri?',
      name: 'JellyChat',
      component: JellyChat
    },
    {
      path: '/auth',
      name: 'AuthenticationForm',
      component: AuthenticationForm
    }
  ]
})

router.beforeEach((to, from, next) => {
  if (sessionStorage.getItem('authToken') !== null || to.path === '/auth') {
    next()
  } else {
    next('/auth')
  }
})

export default router
