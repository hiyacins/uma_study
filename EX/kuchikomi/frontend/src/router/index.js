import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'

Vue.use(VueRouter)

const routes = [{
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/test',
    name: 'Test',
    // route level code-splitting ---
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import( /* webpackChunkName: "about" */ '../views/test.vue')
  },
  {
    path: '/about',
    name: 'About',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import( /* webpackChunkName: "about" */ '../views/About.vue')
  },
  {
    path: '/create_message',
    name: 'CreateMessage',
    component: () => import( /* webpackChunkName: "about" */ '../views/CreateMessage.vue')
  }, {
    path: '/sns',
    name: 'SNS',
    component: () => import( /* webpackChunkName: "about" */ '../views/SNS.vue')
  }, {
    path: '/analyze',
    name: 'Analyze',
    component: () => import( /* webpackChunkName: "analyze" */ '../views/Analyze.vue')
  }, {
    path: '/enquete',
    name: 'Enquete',
    component: () => import( /* webpackChunkName: "enquete" */ '../views/Enquete.vue')
  }, {
    path: '/kuchikomi',
    name: 'Kuchikomi',
    component: () => import( /* webpackChunkName: "message" */ '../views/Kuchikomi.vue')
  }, {
    path: '/allmessage',
    name: 'AllMessage',
    component: () => import( /* webpackChunkName: "allmessage" */ '../views/AllMessage.vue')
  }, {
    path: '/staff',
    name: 'Staff',
    component: () => import( /* webpackChunkName: "config" */ '../views/Staff.vue')
  }, {
    path: '/qrcode',
    name: 'QRCode',
    component: () => import( /* webpackChunkName: "config" */ '../views/QRCode.vue')
  }, {
    path: '/contact',
    name: 'Contact',
    component: () => import( /* webpackChunkName: "config" */ '../views/Contact.vue')
  }, {
    path: '/payment',
    name: 'Payment',
    component: () => import( /* webpackChunkName: "config" */ '../views/Payment.vue')
  }, {
    path: '/faq',
    name: 'FAQ',
    component: () => import( /* webpackChunkName: "config" */ '../views/FAQ.vue')
  }, {
    path: '/guide',
    name: 'Guide',
    component: () => import( /* webpackChunkName: "config" */ '../views/Guide.vue')
  }, {
    path: '/lodout',
    name: 'Logout',
    component: () => import( /* webpackChunkName: "config" */ '../views/login.vue')
  },
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router