
const Login = () => {
    
    const login = (event: React.FormEvent<HTMLFormElement>) => {
        event.preventDefault()
    }
    
    return (
        <>
            <form onSubmit={(e) => login(e)}>
                <input
                    placeholder="Username"/>
                <input
                    placeholder="Password"/>
                <input
                    type="submit"
                    value="Login"/>
            </form>
        </>
    )
}

export default Login