import { useState } from 'react'
import '../styles/Login.css'
import authService from '../services/authService'
import { AppState } from '../App'

interface LoginProps {
    setAppState: React.Dispatch<AppState>
}

const Login = (props: LoginProps) => {
    
    const [username, setUsername] = useState<string>('')
    const [password, setPassword] = useState<string>('')
    const [showLoginError, setShowLoginError] = useState<boolean>(false)

    const login = async (event: React.FormEvent<HTMLFormElement>) => {
        event.preventDefault()
        try {
            await authService.login({username, password})
            props.setAppState(AppState.PROFILE)
        }
        catch(e) {
            console.error(e)
            setShowLoginError(true)
            setTimeout(() => setShowLoginError(false), 5000)
        }
        setUsername('')
        setPassword('')
    }
    
    return (
        <>
            {showLoginError ? 
                <p className='login-failed-message'>
                    Failed to login, check your username and password
                </p> :
                null}
            <form
                className='login-form'
                onSubmit={(e) => login(e)}>
                <input
                    placeholder="Username"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}/>
                <input
                    placeholder="Password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    type='password'/>
                <input
                    type="submit"
                    value="Login"/>
            </form>
        </>
    )
}

export default Login