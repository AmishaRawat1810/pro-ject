export const calculateStatus = (winner : string, turns : number, player : string) => {
    if (!winner && !turns) return 'DRAW';
    if (winner) return `Winner : ${winner}`;
    return `Next player : ${player}`;
}