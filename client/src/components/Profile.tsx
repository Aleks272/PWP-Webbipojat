import { useEffect, useState } from "react"
import { AppState } from "../types/AppState"
import { Watchlist } from "../types/Watchlist"
import { User } from "../types/User"
import userService from "../services/userService"
import watchlistService from "../services/watchlistService"
import WatchlistCollection from "./WatchlistCollection"

interface ProfileProps {
    appState: AppState
}

const Profile = (props: ProfileProps) => {
    const deleteWatchlist = async (watchlist_id: number) => {
        try {
            await watchlistService.deleteWatchlist(watchlist_id)
            if (userInfo) {
                const updated_public_wl = await watchlistService.getPublicWatchlists(userInfo.username)
                const updated_private_wl = await watchlistService.getPrivateWatchlists(userInfo.username)
                setPublicWatchlists(updated_public_wl)
                setPrivateWatchlists(updated_private_wl)
            }
        } catch (error) {
            console.error(error)
        }
    }
    
    const [publicWatchlists, setPublicWatchlists] = useState<Watchlist[]>()
    const [privateWatchlists, setPrivateWatchlists] = useState<Watchlist[]>()
    const [userInfo, setUserInfo] = useState<User>()
    const [showEmailEdit, setshowEmailEdit] = useState<boolean>(false)
    const [newEmail, setNewEmail] = useState<string>("")
    const [password, setpassword] = useState<string>("")
    
    useEffect(() => {
        const effect = async () => {
            try {
                if(props.appState.username) {
                    setUserInfo(await userService.getUser(props.appState.username))
                    setPublicWatchlists(await watchlistService.getPublicWatchlists(props.appState.username))
                    setPrivateWatchlists(await watchlistService.getPrivateWatchlists(props.appState.username))
                }
            }
            catch(e) {
                console.error(e)
            }
        }
        effect()
    },[])

    const changeEmail = async (event: React.FormEvent<HTMLFormElement>) => {
        event.preventDefault()
        try {
            if(userInfo){
                await userService.putUser(userInfo.username, newEmail, password)
                if(props.appState.username)
                    setUserInfo(await userService.getUser(props.appState.username))
                setNewEmail('')
                setpassword('')
                setshowEmailEdit(false)
            }
        }catch(e){
            console.error(e)
        }
    }

    return(
        <>
            <p>Logged in as user {props.appState.username}</p>
            
            <h3>User info</h3>
            {userInfo ? 
            <div>
                <p>Email: {userInfo.email}</p>
                <button onClick={() => setshowEmailEdit(!showEmailEdit)}>Edit email</button>
                {showEmailEdit ?
                    <form
                        onSubmit={(e) => changeEmail(e)}>
                        <input
                        placeholder="new email address"
                        type="email"
                        onChange={(e) => setNewEmail(e.target.value)}/>
                        <p>
                            Confirm email change with your password
                        </p>
                        <input
                        placeholder="password"
                        type="password"
                        onChange={(e) => setpassword(e.target.value)}/>
                        <button type="submit">Submit</button>
                    </form>
                :null}
                <p>User ID: {userInfo.person_id}</p>
            </div> :
            null}
            
            <h3>Your public watchlists</h3>
                {publicWatchlists ? 
                <WatchlistCollection
                    inProfile={true}
                    watchlists={publicWatchlists}
                    deleteWatchlist={deleteWatchlist}/> :
                null}
            <h3>Your private watchlists</h3>
                {privateWatchlists ? 
                <WatchlistCollection
                    inProfile={true}
                    watchlists={privateWatchlists}
                    deleteWatchlist={deleteWatchlist}/> :
                null}

        </>
    )
}

export default Profile