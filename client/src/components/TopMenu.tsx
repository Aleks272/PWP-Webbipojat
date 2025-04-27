import { AppState } from "../types/AppState"
import { AppViewState } from "../enums/AppViewState"

interface TopMenuProps {
    appState: AppState
    setAppState: React.Dispatch<AppState>
}

/**
 * A component that shows the clickable text "Watchlists", and either a "Login"-button (if not logged in),
 * or a "Profile" and "Log out"-buttons (if the user is logged in)
 * When the header is clicked, it takes the user to the Search-page
 * @param props Properties of this component, includes the current app state and a function
 *              to set the app state
 * @returns a TopMenu-component
 */
const TopMenu = (props: TopMenuProps) => {
    
    /**
     * Logs the user out by setting AppState.isLoggedIn to `false` and AppState.username to `null`.
     * Also changes the current view to Search.
     */
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