import React, { useRef, useEffect } from "react";

export default function MoveList({ moves, index, goTo }) {
  const activeRef = useRef(null);

  useEffect(() => {
    if (activeRef.current) {
      activeRef.current.scrollIntoView({ block: "nearest", behavior: "smooth" });
    }
  }, [index]);

  return (
    <div className="move-list">
      <div className="move-list-title">Coups joues</div>
      <div className="move-list-scroll">
        {moves.map((m, i) => {
          if (m.move_san === "--") return null;
          return (
            <span
              key={i}
              ref={i === index ? activeRef : null}
              className={`move-item ${i === index ? "move-active" : ""} ${
                m.turn === "Blancs" ? "move-white" : "move-black"
              }`}
              onClick={() => goTo(i)}
            >
              {m.move_san}
            </span>
          );
        })}
      </div>
    </div>
  );
}
