import { create } from "zustand";
import { combine } from "zustand/middleware";

const useGameStore = create(combine({ history: [Array(9).fill(null)], xIsNext: true } , (set) => {
    return {
        setHistory : (nextHistory : (nextHistory: any[]) => any[]) => {
            set(state => ({
                history: typeof nextHistory === 'function' ? nextHistory(state.history) : nextHistory,
            }))
        }, 
        setIsNextX : (isNextTurnX : (xIsNext : boolean) => boolean) => {
            set(state => ({
                xIsNext: typeof isNextTurnX === 'function' ? isNextTurnX(state.xIsNext) : isNextTurnX,
            }))
        },
    }
}));

export default useGameStore;