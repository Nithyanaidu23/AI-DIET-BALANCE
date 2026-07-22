import api from './api'

export const authService = {
  register: (data) => api.post('/register/', data),
  login:    (data) => api.post('/login/', data),
  me:       ()     => api.get('/me/'),
  updateMe: (data) => api.patch('/me/', data),
  changePassword: (data) => api.post('/change-password/', data),
}

export const profileService = {
  get:    ()     => api.get('/profile/'),
  update: (data) => api.patch('/profile/', data),
}

export const mealService = {
  getPlans:       (params) => api.get('/meal-plans/', { params }),
  getPlan:        (id)     => api.get(`/meal-plans/${id}/`),
  deletePlan:     (id)     => api.delete(`/meal-plans/${id}/`),
  toggleFavorite: (id)     => api.post(`/meal-plans/${id}/favorite/`),
  getGrocery:     (id)     => api.get(`/meal-plans/${id}/grocery/`),
  getFavorites:   ()       => api.get('/favorites/'),
  updateGroceryItem: (id, data) => api.patch(`/grocery/${id}/`, data),
  generatePlan:   (data)   => api.post('/generate-plan/', data),
}

export const nutritionService = {
  getFoods: (params) => api.get('/foods/', { params }),
  getFood:  (id)     => api.get(`/foods/${id}/`),
}

export const healthService = {
  calculateBMI:     (data) => api.post('/bmi/', data),
  getBMIHistory:    (days) => api.get('/bmi/history/', { params: { days } }),
  calculateCalorie: (data) => api.post('/calorie/', data),
  getWater:         ()     => api.get('/water/'),
  updateWater:      (data) => api.patch('/water/', data),
  getDashboard:     ()     => api.get('/dashboard/'),
}

export const exportService = {
  getExports:    ()  => api.get('/exports/'),
  syncExports:   ()  => api.post('/exports/sync/'),
  downloadZip:   ()  => window.open('/api/exports/download-zip/', '_blank'),
  downloadFile:  (fn)=> window.open(`/api/exports/download/?file=${fn}`, '_blank'),
}

export const adminService = {
  getAnalytics:  ()       => api.get('/admin/analytics/'),
  getUsers:      (params) => api.get('/admin/users/', { params }),
  updateUser:    (data)   => api.patch('/admin/users/', data),
  getAILogs:     ()       => api.get('/admin/ai-logs/'),
  getSystemStatus: ()     => api.get('/admin/system/'),
}


