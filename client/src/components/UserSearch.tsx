import { useState } from 'react'

import userService from '../services/userService'

const UserSearch = () => {

    const [searchName, setSearchName] = useState<string>('')

    const search = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault()
        try {
            const res = await userService.getUser(searchName)
            console.log(res)
        }
        catch(e) {
            console.log(e)
        }
    }

    return(
        <>
            <form onSubmit={(e) => search(e)}>
                <input 
                    type="text"
                    placeholder="Search for users"
                    onChange={(e) => setSearchName(e.target.value)}/>
                <input
                    type="submit"/>
            </form>
        </>
    )
}

export default UserSearch