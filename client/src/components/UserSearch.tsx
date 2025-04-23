import { useState } from 'react'

import userService from '../services/userService'
import { User } from '../types/User'
import {UserPublicWatchlists} from './UserPublicWatchlists'

interface UserInfoProps {
    user: User
}

const UserInfo = (props: UserInfoProps) => {
    return(
        <>
            <h3>User profile</h3>
            <p>Name: {props.user.username}</p>
            <p>Email: {props.user.email}</p>
        </>
    )
}

const UserSearch = () => {

    const [searchName, setSearchName] = useState<string>('')
    const [userInfo, setUserInfo] = useState<User|null>()
    const [showUserNotFound, setShowUserNotFound] = useState<boolean>(false)

    const search = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault()
        try {
            const res = await userService.getUser(searchName)
            setUserInfo(res)
            setShowUserNotFound(false)
        }
        catch(e) {
            console.error(e)
            setShowUserNotFound(true)
            setUserInfo(null)
        }
        setSearchName('')
    }

    return(
        <>
            <form onSubmit={(e) => search(e)}>
                <input 
                    type="text"
                    placeholder="Search for users"
                    onChange={(e) => setSearchName(e.target.value)}
                    value={searchName}/>
                <input
                    value="Search"
                    type="submit"/>
            </form>
            {showUserNotFound ? 
            <p style={{color: '#6d6d6d'}}>
                User not found
            </p> : null}
            {userInfo ? <UserInfo user={userInfo}/> : null}
            {userInfo ? <UserPublicWatchlists 
                            username={userInfo.username}/> : null}
        </>
    )
}

export default UserSearch