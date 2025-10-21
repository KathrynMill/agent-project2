import { createRouter, createWebHashHistory } from 'vue-router'
import MainWindow from '../views/MainWindow.vue'
import Settings from '../views/Settings.vue'

const routes = [
  {
    path: '/',
    name: 'MainWindow',
    component: MainWindow
  },
  {
    path: '/settings',
    name: 'Settings',
    component: Settings
  }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

export default router



