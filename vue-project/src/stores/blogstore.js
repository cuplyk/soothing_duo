import { defineStore } from 'pinia'
import apiClient from '../services/api'

export const useBlogStore = defineStore('blog', {
  state: () => ({
    posts: [],
    categories: [],
    currentPost: null,
    user: null,
    loading: false
  }),

  actions: {
    async fetchPosts() {
      this.loading = true
      try {
        const res = await apiClient.get('/blog/posts/')
        this.posts = res.data
      } catch (error) {
        console.error("Failed to load posts:", error)
      } finally {
        this.loading = false
      }
    },

    async fetchPost(slug) {
      this.loading = true
      try {
        const res = await apiClient.get(`/blog/posts/${slug}/`)
        this.currentPost = res.data
      } catch (error) {
        console.error("Post not found:", error)
      } finally {
        this.loading = false
      }
    },

    async fetchCategories() {
      const res = await apiClient.get('/blog/categories/')
      this.categories = res.data
    }
  }
})