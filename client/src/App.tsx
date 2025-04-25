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
    <div className="main-container">
      <TopMenu appState={appState} setAppState={setAppState}/>      
      <AppView appState={appState} setAppState={setAppState}/>
    </div>
  )
}

export default App