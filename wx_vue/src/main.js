import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import installElementPlus from './plugins/element'
import VueCookies from 'vue-cookies'
import store from './store'
import config from './config/index'
import axios from 'axios'
axios.defaults.baseURL = config.baseApi
// 因为导出的是一个对象，结构赋值
const app = createApp(App).use(store).use(VueCookies).use(router)
installElementPlus(app)
app.mount('#app')
app.config.globalProperties.$config = config