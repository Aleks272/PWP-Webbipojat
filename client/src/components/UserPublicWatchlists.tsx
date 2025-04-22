import { useEffect, useState } from "react"
import { Watchlist } from "../types/Watchlist"
import watchlistService from "../services/watchlistService"

export interface UserPublicWatchlistsProps {
    username: string
}

interface WatchlistItemProps {
    watchlist: Watchlist
}

interface WatchlistCollectionProps {
    watchlists: Watchlist[]
}

const WatchlistItem = (props: WatchlistItemProps) => {
    return (
        <div>
            <p>Note: {props.watchlist.user_note}</p>
            <h4>Content on list</h4>
            <ul>
            {props.watchlist.content.map(contentItem => {
                return <li>{contentItem.name}</li>
            })}
            </ul>
        </div>
    )
}

const WatchlistCollection = (props: WatchlistCollectionProps) => {
    return (
        <>
            {props.watchlists.map(watchlist => 
            <WatchlistItem key={watchlist.watchlist_id}
                           watchlist={watchlist}/>)}
        </>
    )
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

    return(
        <>
        <h3>{props.username}'s public Watchlists</h3>
         {watchlists ? <WatchlistCollection watchlists={watchlists}/> : null}
        </>
    )

}