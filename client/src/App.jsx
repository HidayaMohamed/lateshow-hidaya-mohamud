import { useEffect, useState } from "react";
import EpisodesList from "./components/EpisodesList";
import EpisodeDetails from "./components/EpisodeDetails";
import GuestsList from "./components/GuestsList";
import AppearanceForm from "./components/AppearanceForm";

function App() {
  const [episodes, setEpisodes] = useState([]);
  const [guests, setGuests] = useState([]);
  const [selectedEpisode, setSelectedEpisode] = useState(null);

  useEffect(() => {
    fetch("http://127.0.0.1:5000/episodes")
      .then(res => res.json())
      .then(setEpisodes);

    fetch("http://127.0.0.1:5000/guests")
      .then(res => res.json())
      .then(setGuests);
  }, []);

  function loadEpisode(id) {
    fetch(`http://127.0.0.1:5000/episodes/${id}`)
      .then(res => res.json())
      .then(setSelectedEpisode);
  }

  return (
    <div style={{ padding: "20px" }}>
      <h1>Podcast App</h1>

      <EpisodesList
        episodes={episodes}
        onSelectEpisode={loadEpisode}
      />

      <EpisodeDetails episode={selectedEpisode} />

      <GuestsList guests={guests} />

      <AppearanceForm
        episodes={episodes}
        guests={guests}
        onSuccess={loadEpisode}
      />
    </div>
  );
}

export default App;
