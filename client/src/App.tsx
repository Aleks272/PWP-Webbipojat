import { useState } from "react"
import UserSearch from "./components/UserSearch"

import './styles/App.css'
import Login from "./components/Login"

export enum AppState {
  SEARCH,
  LOGIN,
  PROFILE
}

interface AppViewProps {
  appState: AppState
  setAppState: React.Dispatch<AppState>
}

const AppView = (props: AppViewProps) => {
  switch(props.appState) {
    case AppState.LOGIN:
      return <Login setAppState={props.setAppState}/>
    case AppState.PROFILE:
      return <></>
    default:
      return <UserSearch/>
  }
}

function App() {

  const [appState, setAppState] = useState<AppState>(AppState.SEARCH)

  return (
    <>
      <div className='header-container'>
        <h1 onClick={() => setAppState(AppState.SEARCH)}>
          Watchlists
        </h1>
        <button onClick={() => setAppState(AppState.LOGIN)}>
          Login
        </button>
      </div>
      <AppView appState={appState} setAppState={setAppState}/>
    </>
  )
}

export default App
