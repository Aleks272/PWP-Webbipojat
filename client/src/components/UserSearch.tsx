import { useState } from 'react'

import userService from '../services/userService'
import { User } from '../types/User'

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
    const [userInfo, setUserInfo] = useState<User>()

    const search = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault()
        try {
            const res = await userService.getUser(searchName)
            setUserInfo(res)
        }
        catch(e) {
            console.log(e)
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
                    type="submit"/>
            </form>
            {userInfo ? <UserInfo user={userInfo}/> : null}
        </>
    )
}

export default UserSearch