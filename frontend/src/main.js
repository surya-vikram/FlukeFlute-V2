import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'

import 'bootstrap'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-icons/font/bootstrap-icons.css'
import 'bootswatch/dist/slate/bootstrap.css'
import './assets/main.css'

import VuexPersistedstate from 'vuex-plugin-persistedstate/dist/index.js';

createApp(App).use(store).use(router).use(VuexPersistedstate).mount('#app')

