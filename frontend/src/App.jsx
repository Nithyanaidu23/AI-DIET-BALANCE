import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { AuthProvider, useAuth } from './context/AuthContext'
import { ThemeProvider } from './context/ThemeContext'

// User Pages
import Landing from './pages/Landing'
import Login from './pages/Login'
import Register from './pages/Register'
import Dashboard from './pages/Dashboard'
import Profile from './pages/Profile'
import MealPlanner from './pages/MealPlanner'
import History from './pages/History'
import FoodSearch from './pages/FoodSearch'
import BMICalculator from './pages/BMICalculator'
import Settings from './pages/Settings'
import Grocery from './pages/user/Grocery'
import WaterTracker from './pages/user/WaterTracker'
import Favorites from './pages/user/Favorites'
import NotFound from './pages/NotFound'

// Admin Pages
import AdminDashboard from './pages/admin/AdminDashboard'
import AdminUsers from './pages/admin/AdminUsers'
import AdminFoods from './pages/admin/AdminFoods'
import AdminMealPlans from './pages/admin/AdminMealPlans'
import AdminAILogs from './pages/admin/AdminAILogs'
import AdminAnalytics from './pages/admin/AdminAnalytics'
import AdminReports from './pages/admin/AdminReports'
import AdminSettings from './pages/admin/AdminSettings'

// Layouts
import AppLayout from './components/AppLayout'
import AdminLayout from './components/AdminLayout'
import LoadingSpinner from './components/LoadingSpinner'

function ProtectedRoute({ children }) {
  const { isAuthenticated, loading } = useAuth()
  if (loading) return <LoadingSpinner fullScreen />
  if (!isAuthenticated) return <Navigate to="/login" replace />
  return children
}

function AdminRoute({ children }) {
  const { user, isAuthenticated, loading } = useAuth()
  if (loading) return <LoadingSpinner fullScreen />
  if (!isAuthenticated) return <Navigate to="/login" replace />
  if (!user?.is_admin && user?.role !== 'admin' && !user?.is_staff) {
    return <Navigate to="/dashboard" replace />
  }
  return children
}

function PublicRoute({ children }) {
  const { user, isAuthenticated, loading } = useAuth()
  if (loading) return <LoadingSpinner fullScreen />
  if (isAuthenticated) {
    if (user?.is_admin || user?.role === 'admin' || user?.is_staff) {
      return <Navigate to="/admin/dashboard" replace />
    }
    return <Navigate to="/dashboard" replace />
  }
  return children
}

function AppRoutes() {
  return (
    <Routes>
      {/* Public */}
      <Route path="/" element={<Landing />} />
      <Route path="/login"    element={<PublicRoute><Login /></PublicRoute>} />
      <Route path="/register" element={<PublicRoute><Register /></PublicRoute>} />

      {/* User Dashboard Protected Routes */}
      <Route element={<ProtectedRoute><AppLayout /></ProtectedRoute>}>
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/planner"   element={<MealPlanner />} />
        <Route path="/foods"     element={<FoodSearch />} />
        <Route path="/history"   element={<History />} />
        <Route path="/grocery"   element={<Grocery />} />
        <Route path="/water"     element={<WaterTracker />} />
        <Route path="/bmi"       element={<BMICalculator />} />
        <Route path="/favorites" element={<Favorites />} />
        <Route path="/profile"   element={<Profile />} />
        <Route path="/settings"  element={<Settings />} />
      </Route>

      {/* Admin / Creator Dashboard Protected Routes */}
      <Route element={<AdminRoute><AdminLayout /></AdminRoute>}>
        <Route path="/admin/dashboard"  element={<AdminDashboard />} />
        <Route path="/admin/analytics"  element={<AdminAnalytics />} />
        <Route path="/admin/users"      element={<AdminUsers />} />
        <Route path="/admin/foods"      element={<AdminFoods />} />
        <Route path="/admin/meal-plans" element={<AdminMealPlans />} />
        <Route path="/admin/ai-logs"    element={<AdminAILogs />} />
        <Route path="/admin/reports"    element={<AdminReports />} />
        <Route path="/admin/system"     element={<AdminSystemMonitorViewWrapper />} />
        <Route path="/admin/settings"   element={<AdminSettings />} />
      </Route>

      {/* 404 */}
      <Route path="*" element={<NotFound />} />
    </Routes>
  )
}

function AdminSystemMonitorViewWrapper() {
  return <AdminSettings />
}

export default function App() {
  return (
    <ThemeProvider>
      <AuthProvider>
        <BrowserRouter>
          <AppRoutes />
        </BrowserRouter>
      </AuthProvider>
    </ThemeProvider>
  )
}
