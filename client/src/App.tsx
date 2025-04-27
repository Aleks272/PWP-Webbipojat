import { useState } from "react"
import UserSearch from "./components/UserSearch"

import './styles/App.css'
import Login from "./components/Login"
import Profile from "./components/Profile"
import TopMenu from "./components/TopMenu"
import { AppState } from "./types/AppState"
import { AppViewState } from "./enums/AppViewState"

interface AppViewProps {
  appState: AppState
  setAppState: React.Dispatch<AppState>
}

/**
 * This component returns either Login, Profile or UserSearch component depending on the 
 * current state of the app.
 * @param props properties of this component, includes the current state of the app and a function to 
 *              set the state.
 * @returns Login, Profile or UserSearch-component, depending on the current app state.
 */
const AppView = (props: AppViewProps) => {
  switch(props.appState.currentView) {
    case AppViewState.LOGIN:
      return <Login 
              setAppState={props.setAppState}/>
    case AppViewState.PROFILE:
      return <Profile appState={props.appState}/>
    default:
      return <UserSearch/>
  }
}

/**
 * This function is the root component of our app, it draws the TopMenu and an AppView that displays the
 * needed component to match the current app state.
 * @returns the main App component
 */
function App() {

  const [appState, setAppState] = useState<AppState>({
    isLoggedIn: false,
    currentView: AppViewState.SEARCH,
    username: null
  })

  return (
    <div className="main-container">
      <TopMenu appState={appState} setAppState={setAppState}/>      
      <AppView appState={appState} setAppState={setAppState}/>
    </div>
  )
}

export default App