<template>
  <main class="home">
    <section class="hero">
      <div class="hero-content">
        <h1>Welcome to Our Blog</h1>
        <p>Discover the latest stories and insights from our team</p>
        <router-link to="/blog" class="btn">Explore Blog</router-link>
      </div>
    </section>

    <section class="featured-posts">
      <h2>Featured Posts</h2>
      <div v-if="blogStore.loading">Loading featured posts...</div>
      
      <div v-else class="post-grid">
        <div v-for="post in featuredPosts" :key="post.id" class="post-card">
          <h3>{{ post.title }}</h3>
          <p class="post-meta">
            {{ formatDate(post.created_at) }} • 
            <span v-if="post.category">{{ post.category.name }}</span>
          </p>
          <p class="post-excerpt">{{ post.content.substring(0, 100) }}...</p>
          <router-link :to="'/blog/post/' + post.slug" class="read-more">
            Read More
          </router-link>
        </div>
      </div>
    </section>
  </main>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useBlogStore } from '@/stores/blogStore'

const blogStore = useBlogStore()
const featuredPosts = ref([])

onMounted(async () => {
  await blogStore.fetchPosts()
  // Get first 3 posts as featured (you might want different logic)
  featuredPosts.value = blogStore.posts.slice(0, 3)
})

const formatDate = (dateString) => {
  const options = { year: 'numeric', month: 'long', day: 'numeric' }
  return new Date(dateString).toLocaleDateString(undefined, options)
}
</script>

<style scoped>
.home {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.hero {
  background: linear-gradient(rgba(0,0,0,0.4), rgba(0,0,0,0.4)), url('https://via.placeholder.com/1200x400') center/cover no-repeat;
  border-radius: 10px;
  padding: 4rem 2rem;
  text-align: center;
  margin-bottom: 3rem;
  color: white;
}

.hero-content h1 {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.hero-content p {
  font-size: 1.5rem;
  margin-bottom: 2rem;
}

.btn {
  display: inline-block;
  background: #41b883;
  color: white;
  padding: 0.8rem 1.5rem;
  border-radius: 5px;
  text-decoration: none;
  font-weight: bold;
  transition: background 0.3s;
}

.btn:hover {
  background: #3daa78;
}

.featured-posts h2 {
  text-align: center;
  margin-bottom: 2rem;
  color: #2c3e50;
}

.post-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 2rem;
}

.post-card {
  background: white;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0,0,0,0.1);
  padding: 1.5rem;
  transition: transform 0.3s;
}

.post-card:hover {
  transform: translateY(-5px);
}

.post-meta {
  color: #7f8c8d;
  font-size: 0.9rem;
  margin: 0.5rem 0;
}

.post-excerpt {
  margin: 1rem 0;
  color: #34495e;
}

.read-more {
  color: #41b883;
  text-decoration: none;
  font-weight: 600;
}

.read-more:hover {
  text-decoration: underline;
}
</style>