import { createRouter, createWebHistory } from 'vue-router'
import MerchantPage from '@/components/MerchantPage.vue'
import BuyerPage from '@/components/BuyerPage.vue'

const routes = [
  {
    path: '/merchant',
    name: 'MerchantPage',
    component: MerchantPage
  },
  {
    path: '/buyer/:paymentLinkId',
    name: 'BuyerPage',
    component: BuyerPage
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
