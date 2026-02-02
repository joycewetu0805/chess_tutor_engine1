import React from "react";

export default function GameControls({ prev, next, reload, index, total, loading }) {
  return (
    <div className="controls">
      <button onClick={prev} disabled={index <= 0 || loading} title="Coup precedent">
        &#9664;
      </button>
      <span className="move-counter">
        {total > 0 ? `${index} / ${total - 1}` : "--"}
      </span>
      <button onClick={next} disabled={index >= total - 1 || loading} title="Coup suivant">
        &#9654;
      </button>
      <button onClick={reload} disabled={loading} className="btn-new" title="Nouvelle partie">
        Nouvelle partie
      </button>
    </div>
  );
}
