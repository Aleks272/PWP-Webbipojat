import { Watchlist } from "../types/Watchlist"

interface WatchlistItemProps {
    watchlist: Watchlist
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

export default WatchlistItem