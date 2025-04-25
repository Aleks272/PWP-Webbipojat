import { Watchlist } from "../types/Watchlist"

import '../styles/WatchlistItem.css'

interface WatchlistItemProps {
    watchlist: Watchlist
    inProfile: boolean
    deleteWatchlist: (id: number) => void
}

const WatchlistItem = (props: WatchlistItemProps) => {
    return (
            <div className="watchlist-item-container">
                <details>
                    <summary 
                        style={{cursor: 'pointer'}}>
                            <span
                                className="watchlist-item-summary">
                                <b>
                                    {props.watchlist.user_note}
                                </b>
                                {props.inProfile ? 
                                    <button onClick={() => props.deleteWatchlist(props.watchlist.watchlist_id)}>Delete</button>:
                                    null}
                            </span>
                    </summary>
                    <div className="watchlist-item-content">
                    <ul>
                    {props.watchlist.content.map(contentItem => {
                        return(
                        <li key={contentItem.content_id}>
                            {contentItem.name}
                        </li>)
                    })}
                    </ul>
                    </div>
                </details>            
            </div>
        )
}

export default WatchlistItem
