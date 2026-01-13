import React from "react";

// EpisodesList component shows a list of episodes with buttons
function EpisodesList({ episodes, onSelectEpisode }) {
  return (
    <div>
      <h2>Episodes</h2>
      {episodes.map((ep) => (
        <button
          key={ep.id}
          onClick={() => onSelectEpisode(ep.id)}
          style={{ marginRight: "5px", background:"#63C5DA" }}
        >
          Episode {ep.number}
        </button>
      ))}
    </div>
  );
}

export default EpisodesList;
