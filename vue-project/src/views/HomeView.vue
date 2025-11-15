<template>
  <div class="home">
    <h1>Welcome to My Blog</h1>
    <p>This is the main landing page powered by Vue.js.</p>
    <router-link to="/blog" class="btn btn-primary">Read Blog</router-link>
  </div>
</template>

<script>
export default {
  name: 'HomeView'
}
</script>