import axios from 'axios'
import Cookies from 'js-cookie'

const axiosInstance = axios.create({
  baseURL: 'http://127.0.0.1:8000',
  timeout: 3000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// 请求拦截器
axiosInstance.interceptors.request.use(
  (config) => {
    const accessToken = Cookies.get('access_token')
    const tokenType = Cookies.get('token_type')

    if (accessToken && tokenType) {
      config.headers.Authorization = `${tokenType} ${accessToken}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  },
)

// 响应拦截器
axiosInstance.interceptors.response.use(
  (response) => {
    return response
  },
  (error) => {
    console.error('请求失败:', error)
    if (error.response.status === 401) {
      console.error('未授权，请登录')
    }
    return Promise.reject(error)
  },
)

export default axiosInstance
