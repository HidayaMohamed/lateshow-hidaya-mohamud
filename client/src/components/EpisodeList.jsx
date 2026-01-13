function EpisodesList({ episodes, onSelectEpisode }) {
  return (
    <div>
      <h2>Episodes</h2>
      {episodes.map((ep) => (
        <button
          key={ep.id}
          onClick={() => onSelectEpisode(ep.id)}
          style={{ marginRight: "5px" }}
        >
          Episode {ep.number}
        </button>
      ))}
    </div>
  );
}

export default EpisodesList;
