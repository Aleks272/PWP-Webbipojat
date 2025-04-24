import { AppState, AppViewState } from "../App"

interface TopMenuProps {
    appState: AppState
    setAppState: React.Dispatch<AppState>
}

const TopMenu = (props: TopMenuProps) => {
    
    const logout = () => {
        props.setAppState({
          isLoggedIn: false,
          username: null,
          currentView: AppViewState.SEARCH
        })
      }

    return(
        <div className='header-container'>
        <h1 onClick={() => props.setAppState({
                            ...props.appState,
                            currentView: AppViewState.SEARCH})}>
          Watchlists
        </h1>
        {props.appState.isLoggedIn ?
          <div>
            <button onClick={() => 
              props.setAppState({
              ...props.appState,
              currentView: AppViewState.PROFILE})}>
            My profile</button>
            <button onClick={() => logout()}>
              Log out
            </button>
          </div> :
        <button onClick={() => props.setAppState({
                                ...props.appState,
                                currentView: AppViewState.LOGIN})}>
          Login
        </button>}
      </div>
    )
}

export default TopMenu