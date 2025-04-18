// service module for user-specific operations
import 'axios'

import { API_URL } from '../constants'
import axios from 'axios'

const BASE_URL = `${API_URL}/users`

// get user data based on username
const getUser = async (username: string) => await axios.get(`${BASE_URL}/${username}/`)

export default {
    getUser
}