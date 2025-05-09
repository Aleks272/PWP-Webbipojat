import { useState } from 'react'
import '../styles/Login.css'
import authService from '../services/authService'
import { AppState } from '../types/AppState'
import { AppViewState } from '../enums/AppViewState'

interface LoginProps {
    setAppState: React.Dispatch<AppState>
}

/**
 * A component that show the login screen with username and password fields, and a "Login"-button.
 * When the button is clicked, the component uses authService to call the API with the credentials
 * provided.
 * If the login fails, shows an error message on top of the fields.
 * @param props properties of this component, includes a function to set the current app state
 * @returns a Login component
 */
const Login = (props: LoginProps) => {

    const [username, setUsername] = useState<string>('')
    const [password, setPassword] = useState<string>('')
    const [showLoginError, setShowLoginError] = useState<boolean>(false)

    const login = async (event: React.FormEvent<HTMLFormElement>) => {
        event.preventDefault()
        try {
            await authService.login({username, password})
            props.setAppState({
                currentView: AppViewState.PROFILE,
                isLoggedIn: true,
                username: username
            })
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