import Board from "./components/board";
import useGameStore from "./state/boardState";

const Game = () => {
  const history = useGameStore(state => state.history);
  const setHistory = useGameStore(state => state.setHistory);
  const xIsNext = useGameStore(state => state.xIsNext);
  const setIsNextX = useGameStore(state => state.setIsNextX);
  const currentSquare = history[history.length - 1];

  const handleToPlay = (nextSquares : any[]) => {
    setHistory(prev => prev.concat([nextSquares]));
    setIsNextX(prev => !prev);
  };

  return (
    <div style={{
      background: 'aliceblue',
      display: 'flex',
      flexDirection: 'column',
      gap: '2rem',
      fontSize: '1.5rem',
      fontFamily:'monospace',
      justifyContent: 'center',
      alignItems: 'center',
      width: '100vw',
      height: '100vh'}}>
      <div>
        <Board xIsNext={xIsNext} squares={currentSquare} onPlay={handleToPlay}/>
      </div>
      <div>
        <ol>history</ol>
      </div>
    </div>
  )
}
export default Game;