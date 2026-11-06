import { calculateStatus } from "../logic/gameStatus";
import { calculateTurn } from "../logic/turnLogic";
import { calculateWinner } from "../logic/winnerLogic";
import { Square } from "./square"

const Board = ({xIsNext, squares, onPlay}: {xIsNext: boolean, squares: any[], onPlay: (nextSquares: any[]) => void}) => {
    const player = xIsNext ? 'X' : 'O';
    const winner = calculateWinner(squares);
    const turns = calculateTurn(squares);
    const status = calculateStatus(winner, turns, player);

    const handleClicks = (index : number) => {
        if (squares[index] || winner) return
        const nextSquares = squares.slice();
        nextSquares[index] = player;
        onPlay(nextSquares);
    }

    return (
    <div style={{
        display: 'flex', 
        flexDirection: 'column', 
        alignItems: 'center', 
        justifyContent: 'center',
        gap: '2rem'
    }}>
        <div style={{fontSize: '1.5rem', fontFamily:'monospace' }}>{status}</div>
        <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(3, 1fr)',
        gridTemplateRows: 'repeat(3, 1fr)',
        width: 'calc(3 * 3.5rem)',
        height: 'calc(3 * 3.5rem)',
        gap: '5px'
        }}>
        {squares.map((square, squareIndex) => (
            <Square 
            key={squareIndex} 
            value={square} 
            onSquareClick={() => handleClicks(squareIndex)} 
            />
        ))}
        </div>
    </div>
    );
}

export default Board;