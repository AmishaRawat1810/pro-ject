export const Square = ({ value, onSquareClick }: { value: string | null; onSquareClick?: () => void }) => {
  return (
    <button
      onClick={onSquareClick}
      style={{
        width: '100%',
        height: '100%',
        border: '1px solid #999',
        backgroundColor: 'rgba(207, 245, 255, 0.2)',
        fontSize: '2rem',
        fontWeight: 'bold',
        cursor: 'pointer',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        padding: '0',
        margin: '0',
        minHeight: '0',
        boxShadow: 'none'
      }}
    >
      {value}
    </button>
  )
}