import { Watchlist } from "../types/Watchlist"
import WatchlistItem from "./WatchlistItem"
import watchlistService from "../services/watchlistService"

interface WatchlistCollectionProps {
    watchlists: Watchlist[]
    // specifies if displaying collection in profile,
    // used for customized rendering
    inProfile: boolean
    deleteWatchlist: Function
}

const WatchlistCollection = (props: WatchlistCollectionProps) => {

    if (props.watchlists.length == 0)
            return <p style={{color: '#6d6d6d'}}>User does not have any public watchlists</p>
        return (
            <>
                {props.watchlists.map(watchlist => 
                <WatchlistItem key={watchlist.watchlist_id}
                               watchlist={watchlist}
                               inProfile={props.inProfile}
                               deleteWatchlist={props.deleteWatchlist}/>)}
            </>
        )
}

export default WatchlistCollection
