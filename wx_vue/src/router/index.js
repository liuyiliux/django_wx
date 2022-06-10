import { createRouter, createWebHashHistory } from 'vue-router'
import LoginView from '../views/LoginView.vue'
const routes = [
  {
    path: '/',
    name: 'login',
    component: LoginView,
	meta: {
	title: '登录'
	}
  }, {
    path: '/home',
    component: () => import('../views/HomeView.vue'),
	meta: {
	title: '用户信息'
	}
  }, {
    path: '/register',
    component: () => import('../views/RegisterView.vue'),
	meta: {
	title: '注册'
	}
  }
]
const router = createRouter({
  history: createWebHashHistory(),
  routes
})
export default router
router.beforeEach((to, from, next) => {
//beforeEach是router的钩函数，在进路由前执
if (to.meta.title) {
//判断是否有标题
// console.log(to.meta.title)
document.title = to.meta.title
} else {
document.title = '测试开发真货'
}
next()
})
