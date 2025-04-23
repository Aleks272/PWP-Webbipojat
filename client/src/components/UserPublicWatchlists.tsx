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
            <details>
                <summary style={{cursor: 'pointer'}}>
                    <b>
                        {props.watchlist.user_note}
                    </b>
                </summary>
                <p>Content on list:</p>
                <ul>
                {props.watchlist.content.map(contentItem => {
                    return(
                    <li key={contentItem.content_id}>
                        {contentItem.name}
                    </li>)
                })}
                </ul>
            </details>            
        </div>
    )
}

const WatchlistCollection = (props: WatchlistCollectionProps) => {
    if (props.watchlists.length == 0)
        return <p style={{color: '#6d6d6d'}}>User does not have any public watchlists</p>
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