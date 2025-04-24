// service module for user-specific operations
import 'axios'

import { API_URL } from '../constants'
import axios from 'axios'
import { User } from '../types/User'

const BASE_URL = `${API_URL}/users`

// get user data based on username
const getUser = async (username: string): Promise<User> => (await axios.get(`${BASE_URL}/${username}/`)).data

const putUser = async (username: string, email: string, password: string): Promise<User> => {
    const body = {username, email, password};
    const response = await axios.put(`${BASE_URL}/${username}/`, body);
    return response.data
};

export default {
    getUser,
    putUser
}