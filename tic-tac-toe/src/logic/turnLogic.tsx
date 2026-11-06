export const calculateTurn = (squares : any[]) => {
    return squares.filter(sq => !sq).length; 
}