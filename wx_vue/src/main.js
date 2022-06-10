import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import installElementPlus from './plugins/element'
import VueCookies from 'vue-cookies'
import store from './store'

const app = createApp(App).use(store).use(VueCookies).use(router)
installElementPlus(app)
app.mount('#app')