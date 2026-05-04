import { createRouter, createWebHistory } from 'vue-router'
import Home from './views/Home.vue'
import Admin from './views/Admin.vue'
import Login from './views/Login.vue'
import MenuDetail from './views/MenuDetail.vue'

const routes = [
  { path: '/', component: Home },
  { path: '/admin', component: Admin },
  { path: '/login', component: Login },
  { path: '/menu/:id', component: MenuDetail },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router