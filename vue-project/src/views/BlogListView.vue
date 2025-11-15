<template>
  <div>
    <h1>Blog Posts</h1>
    <div v-if="loading">Loading...</div>
    <div v-else>
      <div v-for="post in posts" :key="post.id" class="blog-excerpt my-4">
        <h3>{{ post.title }}</h3>
        <p class="text-muted">
          by {{ post.author.username }} on {{ formatDate(post.created_at) }}
          <span v-if="post.category">in {{ post.category.name }}</span>
        </p>
        <p>{{ post.content.substring(0, 150) }}...</p>
        <router-link :to="{ name: 'PostDetail', params: { slug: post.slug } }">
          Read More
        </router-link>
      </div>
    </div>
  </div>
</template>

<script>
import { useBlogStore } from '../stores/blogStore'
import { onMounted } from 'vue'

export default {
  name: 'BlogListView',
  setup() {
    const blogStore = useBlogStore()

    onMounted(async () => {
      await blogStore.fetchPosts()
      await blogStore.fetchCategories()
    })

    return {
      posts: blogStore.posts,
      loading: blogStore.loading,
      formatDate: (date) => new Date(date).toLocaleDateString()
    }
  }
}
</script>