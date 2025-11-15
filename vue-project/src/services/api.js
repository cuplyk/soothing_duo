import axios from 'axios'

const apiClient = axios.create({
  baseURL: '/api',  // Proxied via Vite
  withCredentials: true  // Keeps Django session
})

export default apiClient