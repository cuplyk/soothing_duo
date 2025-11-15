import { defineStore } from 'pinia'
import apiClient from '../services/api'

export const useBlogStore = defineStore('blog', {
  state: () => ({
    posts: [],
    categories: [],
    currentPost: null,
    loading: false,
  }),

  actions: {
    async fetchPosts() {
      this.loading = true
      const response = await apiClient.get('posts/')
      this.posts = response.data
      this.loading = false
    },

    async fetchPost(slug) {
      const response = await apiClient.get(`posts/${slug}/`)
      this.currentPost = response.data
    },

    async fetchCategories() {
      const response = await apiClient.get('categories/')
      this.categories = response.data
    }
  }
})