import { useState } from "react"
import UserSearch from "./components/UserSearch"

import './styles/App.css'
import Login from "./components/Login"
import Profile from "./components/Profile"

export enum AppViewState {
  SEARCH,
  LOGIN,
  PROFILE
}

export interface AppState {
  isLoggedIn: boolean
  currentView: AppViewState
  username: string|null
}

interface AppViewProps {
  appState: AppState
  setAppState: React.Dispatch<AppState>
}

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

function App() {

  const [appState, setAppState] = useState<AppState>({
    isLoggedIn: false,
    currentView: AppViewState.SEARCH,
    username: null
  })

  return (
    <>
      <div className='header-container'>
        <h1 onClick={() => setAppState({...appState, currentView: AppViewState.SEARCH})}>
          Watchlists
        </h1>
        {appState.isLoggedIn ?
         <button onClick={() => 
          setAppState({
            ...appState,
            currentView: AppViewState.PROFILE})}>
          My profile</button> :
        <button onClick={() => setAppState({...appState, currentView: AppViewState.LOGIN})}>
          Login
        </button>}
      </div>
      <AppView appState={appState} setAppState={setAppState}/>
    </>
  )
}

export default App
