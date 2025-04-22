import axios from 'axios'

import { API_URL } from '../constants'
import { Watchlist } from '../types/Watchlist'

const getPublicWatchlists = async (username: string): Promise<[Watchlist]> => 
    (await axios.get(`${API_URL}/users/${username}/watchlists/public/`)).data.watchlists

export default {
    getPublicWatchlists
}