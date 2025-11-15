<template>
  <nav class="navbar">
    <div class="container">
      <router-link to="/" class="logo">MyBlog</router-link>
      <div class="nav-links">
        <router-link to="/">Home</router-link>
        <router-link to="/blog">Blog</router-link>
      </div>
      <div class="auth-links">
        <a v-if="!isLoggedIn" href="http://localhost:8000/accounts/login/">Login</a>
        <a v-else href="http://localhost:8000/accounts/logout/">Logout</a>
      </div>
    </div>
  </nav>
</template>

<script>
export default {
  computed: {
    isLoggedIn() {
      return document.cookie.includes('sessionid')
    }
  }
}
</script>

<style scoped>
.navbar {
  background: var(--dark);
  color: white;
  padding: 1rem 0;
  position: sticky;
  top: 0;
  z-index: 100;
  box-shadow: 0 2px 10px rgba(0,0,0,0.2);
}

.navbar .container {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo {
  font-size: 1.8rem;
  font-weight: 700;
  color: var(--primary);
}

.nav-links, .auth-links {
  display: flex;
  gap: 1.5rem;
}

.nav-links a, .auth-links a {
  opacity: 0.9;
  transition: opacity 0.2s;
}

.nav-links a:hover, .auth-links a:hover {
  opacity: 1;
}

.router-link-active {
  color: var(--primary);
  font-weight: 600;
}
</style>