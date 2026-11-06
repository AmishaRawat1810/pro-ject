import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import "./style.css"
import Game from './App.tsx'
// import {Square} from './components/square.tsx'
// import Board from "./components/board.tsx"

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <Game />
  </StrictMode>,
)
