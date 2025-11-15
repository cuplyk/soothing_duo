import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import BlogListView from '../views/BlogListView.vue'
import PostDetailView from '../views/PostDetailView.vue'

const routes = [
  { path: '/', name: 'Home', component: HomeView },
  { path: '/blog', name: 'BlogList', component: BlogListView },
  { path: '/blog/post/:slug', name: 'PostDetail', component: PostDetailView }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

export default router