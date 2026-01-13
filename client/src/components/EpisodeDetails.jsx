function EpisodeDetails({ episode }) {
  if (!episode) return null;

  return (
    <div>
      <h2>Episode {episode.number}</h2>
      <p>Date: {episode.date}</p>

      <h3>Appearances</h3>
      <ul>
        {episode.appearances.map((app) => (
          <li key={app.id}>
            {app.guest.name} — Rating: {app.rating}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default EpisodeDetails;
