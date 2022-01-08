import Vue from 'vue'
import App from './App.vue'

import io from 'socket.io-client';
import VueApexCharts from 'vue-apexcharts'

const socket =  io.connect('http://localhost:8081', { transports: ['websocket'] });

Vue.prototype.$socket = socket;

Vue.use(VueApexCharts)

Vue.component('apexchart', VueApexCharts)

import { BootstrapVue, IconsPlugin } from 'bootstrap-vue'

// Import Bootstrap an BootstrapVue CSS files (order is important)
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'

// Make BootstrapVue available throughout your project
Vue.use(BootstrapVue)
// Optionally install the BootstrapVue icon components plugin
Vue.use(IconsPlugin)

Vue.config.productionTip = false

new Vue({
  render: h => h(App),
}).$mount('#app')
