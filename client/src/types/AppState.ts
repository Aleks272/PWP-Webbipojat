import { AppViewState } from "../enums/AppViewState"

export type AppState = {
    isLoggedIn: boolean
    currentView: AppViewState
    username: string|null
  }