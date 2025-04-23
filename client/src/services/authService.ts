import axios from 'axios'

import { AUTH_URL } from '../constants'

interface Credentials {
    username: string,
    password: string
}

const login = async (credentials: Credentials) => {
    const response = (await axios.post(`${AUTH_URL}/login/`, credentials)).data
    const token = response.token
    axios.defaults.headers.common = {
        'Authorization': `Bearer ${token}`
    }
}

export default {
    login
}