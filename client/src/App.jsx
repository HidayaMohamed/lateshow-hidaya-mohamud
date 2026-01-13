import { useEffect, useState } from "react";
import EpisodesList from "./components/EpisodesList";
import EpisodeDetails from "./components/EpisodeDetails";
import GuestsList from "./components/GuestsList";
import AppearanceForm from "./components/AppearanceForm";

function App() {
  // state for all episodes, guests and selected episodes
  const [episodes, setEpisodes] = useState([]);
  const [guests, setGuests] = useState([]);
  const [selectedEpisode, setSelectedEpisode] = useState(null);

  // useEffect to fetch episodes,from the backend
  useEffect(() => {
    fetch("http://127.0.0.1:5000/episodes")
      .then((res) => res.json())
      .then(setEpisodes);

    //  fetch all guests
    fetch("http://127.0.0.1:5000/guests")
      .then((res) => res.json())
      .then(setGuests);
  }, []);

  //  fetch a single selected episode when selected
  function loadEpisode(id) {
    fetch(`http://127.0.0.1:5000/episodes/${id}`)
      .then((res) => res.json())
      .then(setSelectedEpisode);
  }

  return (
    <div
      style={{ padding: "50px", background: "#0492C2", marginLeft: "500px" }}
    >
      <h1>Podcast App</h1>

      <EpisodesList episodes={episodes} onSelectEpisode={loadEpisode} />

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
