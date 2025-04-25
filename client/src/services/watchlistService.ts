import axios, { AxiosResponse } from 'axios'

import { API_URL } from '../constants'
import { Watchlist } from '../types/Watchlist'

const getPublicWatchlists = async (username: string): Promise<Watchlist[]> =>
    (await axios.get(`${API_URL}/users/${username}/watchlists/public/`)).data.watchlists

const getPrivateWatchlists = async (username: string): Promise<Watchlist[]> =>
    (await axios.get(`${API_URL}/users/${username}/watchlists/private/`)).data.watchlists

const deleteWatchlist = async (watchlistId: number): Promise<AxiosResponse> => 
    await axios.delete(`${API_URL}/watchlists/${watchlistId}/`)

export default {
    getPublicWatchlists,
    getPrivateWatchlists,
    deleteWatchlist
}