import { Watchlist } from "../types/Watchlist"
import WatchlistItem from "./WatchlistItem"

import '../styles/WatchlistCollection.css'

interface WatchlistCollectionProps {
    watchlists: Watchlist[]
    // specifies if displaying collection in profile,
    // used for customized rendering
    inProfile: boolean
    deleteWatchlist: (id: number) => void
}

const WatchlistCollection = (props: WatchlistCollectionProps) => {

    if (props.watchlists.length == 0)
            return <p style={{color: '#6d6d6d'}}>User does not have any public watchlists</p>
        return (
            <div className="watchlist-collection">
                {props.watchlists.map(watchlist => 
                <WatchlistItem key={watchlist.watchlist_id}
                               watchlist={watchlist}
                               inProfile={props.inProfile}
                               deleteWatchlist={props.deleteWatchlist}/>)}
            </div>
        )
}

export default WatchlistCollection
