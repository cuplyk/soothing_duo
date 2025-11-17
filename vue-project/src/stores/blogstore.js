import { defineStore } from 'pinia'
import apiClient from '../services/api'

export const useBlogStore = defineStore('blog', {
  state: () => ({
    posts: [],
    categories: [],
    currentPost: null,
    loading: false
  }),
  
  actions: {
    async fetchPosts() {
      this.loading = true
      try {
        const response = await apiClient.get('/blog/posts/')
        this.posts = response.data
      } catch (error) {
        console.error('Error fetching posts:', error)
      } finally {
        this.loading = false
      }
    },
    
    async fetchCategories() {
      try {
        const response = await apiClient.get('/blog/categories/')
        this.categories = response.data
      } catch (error) {
        console.error('Error fetching categories:', error)
      }
    },
    
    async fetchPost(slug) {
      this.loading = true
      try {
        const response = await apiClient.get(`/blog/posts/${slug}/`)
        this.currentPost = response.data
      } catch (error) {
        console.error('Error fetching post:', error)
      } finally {
        this.loading = false
      }
    }
  }
})