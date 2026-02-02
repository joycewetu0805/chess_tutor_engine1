import React from "react";

const PIECE_UNICODE = {
  K: "\u2654", Q: "\u2655", R: "\u2656", B: "\u2657", N: "\u2658", P: "\u2659",
  k: "\u265A", q: "\u265B", r: "\u265C", b: "\u265D", n: "\u265E", p: "\u265F",
};

function parseFen(fen) {
  if (!fen) return Array(64).fill(null);
  const rows = fen.split(" ")[0].split("/");
  const board = [];
  for (const row of rows) {
    for (const ch of row) {
      if (ch >= "1" && ch <= "8") {
        for (let i = 0; i < parseInt(ch); i++) board.push(null);
      } else {
        board.push(ch);
      }
    }
  }
  return board;
}

export default function ChessBoard({ fen, lastMove }) {
  const squares = parseFen(fen);

  return (
    <div className="board">
      {squares.map((piece, i) => {
        const row = Math.floor(i / 8);
        const col = i % 8;
        const isLight = (row + col) % 2 === 0;
        const file = String.fromCharCode(97 + col);
        const rank = 8 - row;
        const squareName = `${file}${rank}`;

        let extraClass = "";
        if (lastMove && (squareName === lastMove.from || squareName === lastMove.to)) {
          extraClass = " square-highlight";
        }

        return (
          <div
            key={i}
            className={`square ${isLight ? "square-light" : "square-dark"}${extraClass}`}
          >
            {col === 0 && <span className="coord-rank">{rank}</span>}
            {row === 7 && <span className="coord-file">{file}</span>}
            {piece && <span className="piece">{PIECE_UNICODE[piece]}</span>}
          </div>
        );
      })}
    </div>
  );
}
