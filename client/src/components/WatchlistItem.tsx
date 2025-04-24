import { Watchlist } from "../types/Watchlist"

interface WatchlistItemProps {
    watchlist: Watchlist
    inProfile: boolean
    deleteWatchlist: Function
}

const WatchlistItem = (props: WatchlistItemProps) => {
    return (
            <div>
                <details>
                    <summary 
                        style={{cursor: 'pointer'}}>
                            <b>
                                {props.watchlist.user_note}
                            </b>
                            {props.inProfile ? 
                            <button onClick={() => props.deleteWatchlist(props.watchlist.watchlist_id)}>Delete</button> :
                            null}
                    </summary>
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

export default WatchlistItem
