# Tech Stack Crash Course 🚀

Complete learning guide for the Chatbook Business Frontend tech stack.

## 📚 Learning Path (Recommended Order)

1. JavaScript ES6+ → React Basics → React Hooks → TailwindCSS → React Router → Axios → Vite → ESLint

---

## 1️⃣ JavaScript ES6+ Fundamentals

### Core Concepts You Need:

**Arrow Functions & Destructuring**
```javascript
// Arrow functions (used everywhere in React)
const greetUser = (name) => `Hello, ${name}!`

// Object destructuring
const { name, age } = user
const { name, value } = e.target  // From your BookingForm.jsx

// Array destructuring (React hooks)
const [count, setCount] = useState(0)
```

**Template Literals & Modules**
```javascript
// Template literals
const message = `Welcome, ${userName}! You have ${bookingCount} bookings.`

// ES6 Modules
export const formatDate = (date) => { /* ... */ }  // Named export
export default Button                               // Default export
import { useState } from 'react'                    // Named import
import Button from './components/Button'            // Default import
```

**Async/Await & Spread Operator**
```javascript
// Async/await (from your useApi.js)
const fetchData = async () => {
  try {
    const response = await api.get(endpoint)
    return response.data
  } catch (error) {
    console.error(error)
  }
}

// Spread operator (from your Button.jsx)
<button {...props}>{children}</button>
const updatedUser = { ...user, age: 31 }
```

### 📖 **Official Docs**: [MDN JavaScript](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide) | [ES6 Features](https://es6-features.org/)

---

## 2️⃣ React Basics & JSX

### What React Is:
JavaScript library for building UIs with reusable components.

**JSX Syntax**
```jsx
// JSX looks like HTML but it's JavaScript
const element = <h1>Hello, {name}!</h1>

// From your Dashboard.jsx:
<div className="container py-10">
  <h1 className="text-3xl mb-6">Dashboard</h1>
  <p>You have {bookingCount} upcoming bookings</p>
</div>
```

**Components & Props**
```jsx
// Function component
const Greeting = ({ name, age }) => {
  return (
    <div>
      <h1>Hello, {name}!</h1>
      <p>You are {age} years old</p>
    </div>
  )
}

// Usage
<Greeting name="John" age={30} />

// From your Button.jsx:
const Button = ({ children, variant, size, onClick, ...props }) => {
  return <button onClick={onClick} {...props}>{children}</button>
}
```

**Lists & Conditional Rendering**
```jsx
// Lists (from your Booking.jsx)
{bookings.map(booking => (
  <tr key={booking.id}>
    <td>{booking.client}</td>
    <td>{booking.date}</td>
  </tr>
))}

// Conditional rendering
{user ? <h1>Welcome, {user.name}!</h1> : <h1>Please log in</h1>}
{user && <p>Email: {user.email}</p>}
```

### 📖 **Official Docs**: [React.dev](https://react.dev/) | [JSX Guide](https://react.dev/learn/writing-markup-with-jsx)

---

## 3️⃣ React Hooks & State

### useState - Component State
```jsx
import { useState } from 'react'

// Basic state
const [count, setCount] = useState(0)

// Object state (from your BookingForm.jsx)
const [formData, setFormData] = useState({
  clientName: '',
  date: '',
  time: '',
  duration: '60'
})

// Update object state
const handleChange = (e) => {
  const { name, value } = e.target
  setFormData(prev => ({ ...prev, [name]: value }))
}
```

### useEffect - Side Effects
```jsx
import { useEffect } from 'react'

// Run on mount and when userId changes
useEffect(() => {
  fetchUser(userId).then(setUser)
}, [userId])

// Run once on mount
useEffect(() => {
  fetchData()
}, [])

// Cleanup (timers, subscriptions)
useEffect(() => {
  const timer = setInterval(() => {}, 1000)
  return () => clearInterval(timer)  // Cleanup
}, [])
```

### Custom Hooks (from your useApi.js)
```jsx
export function useApi(endpoint) {
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  
  const fetchData = async () => {
    setLoading(true)
    try {
      const response = await api.get(endpoint)
      setData(response.data)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }
  
  return { data, loading, error, fetchData }
}
```

### 📖 **Official Docs**: [React Hooks](https://react.dev/reference/react) | [useState](https://react.dev/reference/react/useState) | [useEffect](https://react.dev/reference/react/useEffect)

---

## 4️⃣ TailwindCSS

### Utility-First CSS Framework
Instead of writing CSS, use pre-built classes.

**Common Classes (from your project)**
```html
<!-- Layout & Spacing -->
<div class="container py-10">           <!-- Custom container + padding -->
<div class="grid grid-cols-1 md:grid-cols-3 gap-6">  <!-- Responsive grid -->
<div class="p-6 rounded-lg shadow-md">  <!-- Padding, rounded corners, shadow -->

<!-- Typography -->
<h1 class="text-3xl mb-6">Dashboard</h1>  <!-- Large text + margin -->
<p class="text-primary-700">Recent Bookings</p>  <!-- Custom color -->

<!-- Backgrounds & Colors -->
<div class="bg-white">White background</div>
<div class="bg-primary-600 text-white">Blue background, white text</div>

<!-- Interactive States -->
<button class="bg-blue-600 hover:bg-blue-700 focus:ring-blue-500">
  Hover and focus effects
</button>
```

**Responsive Design**
```html
<!-- Mobile-first breakpoints -->
<div class="w-full md:w-1/2 lg:w-1/3">
  <!-- Full width mobile, half tablet, third desktop -->
</div>

<!-- Breakpoints: sm(640px), md(768px), lg(1024px), xl(1280px) -->
```

**Custom Configuration (your tailwind.config.js)**
```javascript
export default {
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#f0f9ff',
          600: '#0284c7',    // Your brand color
          700: '#0369a1',
        },
      },
    },
  },
}
```

### 📖 **Official Docs**: [TailwindCSS](https://tailwindcss.com/docs) | [Utility Classes](https://tailwindcss.com/docs/utility-first)

---

## 5️⃣ React Router

### Navigation Without Page Refreshes

**Basic Setup (from your App.jsx)**
```jsx
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom'

const App = () => {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/booking" element={<Booking />} />
        <Route path="*" element={<NotFound />} />  {/* 404 */}
      </Routes>
    </BrowserRouter>
  )
}
```

**Navigation**
```jsx
import { Link, useNavigate } from 'react-router-dom'

// Declarative navigation (from your Dashboard.jsx)
<Link to="/booking" className="btn-primary">
  View Bookings
</Link>

// Programmatic navigation
const navigate = useNavigate()
const goToBookings = () => navigate('/bookings')
```

**URL Parameters**
```jsx
// Route with parameter
<Route path="/booking/:id" element={<BookingDetail />} />

// Get parameter in component
import { useParams } from 'react-router-dom'
const { id } = useParams()
```

**Lazy Loading (from your App.jsx)**
```jsx
import { lazy, Suspense } from 'react'

const Dashboard = lazy(() => import('./pages/Dashboard'))
const Booking = lazy(() => import('./pages/Booking'))

<Suspense fallback={<div>Loading...</div>}>
  <Routes>...</Routes>
</Suspense>
```

### 📖 **Official Docs**: [React Router](https://reactrouter.com/) | [Tutorial](https://reactrouter.com/en/main/start/tutorial)

---

## 6️⃣ Axios & API Integration

### HTTP Client for API Calls

**Basic Usage**
```javascript
import axios from 'axios'

// GET request
const fetchUsers = async () => {
  const response = await axios.get('/api/users')
  return response.data
}

// POST request
const createUser = async (userData) => {
  const response = await axios.post('/api/users', userData)
  return response.data
}
```

**Axios Instance (from your useApi.js)**
```javascript
// Create configured instance
const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000/api',
  headers: { 'Content-Type': 'application/json' },
})

// Add auth to every request
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('auth_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})
```

**Error Handling**
```javascript
try {
  const response = await api.get(endpoint)
  return response.data
} catch (err) {
  if (err.response) {
    // Server error (4xx, 5xx)
    console.error('Server error:', err.response.status)
  } else if (err.request) {
    // Network error
    console.error('Network error')
  }
  throw err
}
```

### 📖 **Official Docs**: [Axios](https://axios-http.com/docs/intro) | [Request Config](https://axios-http.com/docs/req_config)

---

## 7️⃣ Vite Build Tool

### Fast Development & Build Tool

**Key Features:**
- ⚡ Instant hot reload
- 📦 Optimized builds
- 🔧 Zero config for React

**Configuration (your vite.config.js)**
```javascript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    open: true,  // Auto-open browser
  },
  build: {
    outDir: 'dist',
    sourcemap: true,
  },
})
```

**Environment Variables**
```bash
# .env file
VITE_API_URL=http://localhost:8000/api
VITE_APP_TITLE=Chatbook Business
```

```javascript
// Usage in code
const apiUrl = import.meta.env.VITE_API_URL
const isDev = import.meta.env.DEV
const isProd = import.meta.env.PROD
```

**Commands**
```bash
npm run dev      # Development server
npm run build    # Production build
npm run preview  # Preview production build
```

### 📖 **Official Docs**: [Vite](https://vitejs.dev/guide/) | [Environment Variables](https://vitejs.dev/guide/env-and-mode.html)

---

## 8️⃣ ESLint & Code Quality

### Code Linting & Error Detection

**Configuration (your .eslintrc.js)**
```javascript
export default {
  env: { browser: true, es2020: true },
  extends: [
    'eslint:recommended',
    'plugin:react/recommended',
    'plugin:react-hooks/recommended',
  ],
  rules: {
    'react-refresh/only-export-components': 'warn',
    'no-console': ['error', { allow: ['warn', 'error'] }],
    'react/prop-types': 'error',
  },
}
```

**Common Rules**
```javascript
{
  'no-unused-vars': 'error',        // No unused variables
  'no-console': 'warn',             // Warn on console.log
  'react/prop-types': 'error',      // Require prop validation
  'react-hooks/rules-of-hooks': 'error',     // Hook rules
  'react-hooks/exhaustive-deps': 'warn',     // Hook dependencies
}
```

**Commands**
```bash
npm run lint              # Check all files
npm run lint -- --fix     # Auto-fix issues
```

### 📖 **Official Docs**: [ESLint](https://eslint.org/docs/user-guide/) | [React ESLint](https://github.com/jsx-eslint/eslint-plugin-react)

---

## 🎯 Learning Resources

### **Free Courses:**
- **React Official Tutorial**: https://react.dev/learn
- **freeCodeCamp React**: https://www.freecodecamp.org/learn/front-end-development-libraries/
- **JavaScript.info**: https://javascript.info/
- **TailwindCSS Tutorial**: https://tailwindcss.com/docs/utility-first

### **Practice Projects:**
1. **Todo App** - useState, event handling, lists
2. **Weather App** - API calls, useEffect, conditional rendering  
3. **Blog with Router** - Multiple pages, navigation
4. **E-commerce** - Complex state, forms, API integration

### **Next Steps:**
1. ✅ Master JavaScript fundamentals
2. ✅ Build React components with hooks
3. ✅ Style with TailwindCSS
4. ✅ Add routing and API integration
5. ✅ Set up development environment
6. 🚀 Build your own projects!

---

## 🚀 Quick Start Checklist

- [ ] Review JavaScript ES6+ syntax
- [ ] Create React components with JSX
- [ ] Practice useState and useEffect hooks
- [ ] Build forms with controlled inputs
- [ ] Style with TailwindCSS utility classes
- [ ] Add navigation with React Router
- [ ] Make API calls with Axios
- [ ] Configure Vite development environment
- [ ] Set up ESLint for code quality

**Happy learning! 🎉** 