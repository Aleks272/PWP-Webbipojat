import { Content } from "./Content"

export type Watchlist = {
    watchlist_id: number,
    user_note: string,
    person_id: string,
    content: [Content]
}