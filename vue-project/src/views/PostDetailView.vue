<template>
  <div v-if="currentPost">
    <h1>{{ currentPost.title }}</h1>
    <p class="text-muted">
      by {{ currentPost.author.username }} on {{ formatDate(currentPost.created_at) }}
      <span v-if="currentPost.category">in {{ currentPost.category.name }}</span>
    </p>
    <hr />
    <div v-html="currentPost.content"></div>
    <router-link to="/blog">← Back to Blog</router-link>
  </div>
  <div v-else-if="loading">Loading...</div>
  <div v-else>Post not found.</div>
</template>

<script>
import { useBlogStore } from '../stores/blogStore'
import { onMounted } from 'vue'
import { useRoute } from 'vue-router'

export default {
  name: 'PostDetailView',
  setup() {
    const blogStore = useBlogStore()
    const route = useRoute()

    onMounted(async () => {
      await blogStore.fetchPost(route.params.slug)
    })

    return {
      currentPost: blogStore.currentPost,
      loading: blogStore.loading,
      formatDate: (date) => new Date(date).toLocaleDateString()
    }
  }
}
</script>