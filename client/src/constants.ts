// when running with npm run dev, use dev API server
export const API_URL: string = import.meta.env.DEV ? 'http://127.0.0.1:5000/api' : '/api'
// the same for auth service
export const AUTH_URL: string = import.meta.env.DEV ? 'http://127.0.0.1:5000/auth' : '/auth'