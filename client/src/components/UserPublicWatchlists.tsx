import { useEffect, useState } from "react"
import { Watchlist } from "../types/Watchlist"
import watchlistService from "../services/watchlistService"
import WatchlistCollection from "./WatchlistCollection"

export interface UserPublicWatchlistsProps {
    username: string
}

export const UserPublicWatchlists = (props: UserPublicWatchlistsProps) => {

    const [watchlists, setWatchlists] = useState<Watchlist[]|null>()

    useEffect(() => {
        const effect = async () => {
            try {
                const response = await watchlistService.getPublicWatchlists(props.username)
                setWatchlists(response)
            }
            catch(e) {
                console.log(e)
            }
        }
        effect()
    },[props.username])

    if (watchlists) {
        if (watchlists.length > 0)
            return (
            <>
                <h3>{props.username}'s public Watchlists</h3>
                <WatchlistCollection
                    inProfile={false} 
                    watchlists={watchlists}
                    deleteWatchlist={() => {}}/>
            </>
            )
        return <p style={{color: '#6d6d6d'}}>
                User {props.username} does not have any public watchlists
               </p>
    }
    return null

}