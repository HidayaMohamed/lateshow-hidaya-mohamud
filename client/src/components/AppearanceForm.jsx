import { useState } from "react";

function AppearanceForm({ episodes, guests, onSuccess }) {
  const [rating, setRating] = useState("");
  const [episodeId, setEpisodeId] = useState("");
  const [guestId, setGuestId] = useState("");
  const [errors, setErrors] = useState([]);

  function handleSubmit(e) {
    e.preventDefault();
    setErrors([]);

    fetch("http://127.0.0.1:5000/appearances", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        rating: Number(rating),
        episode_id: Number(episodeId),
        guest_id: Number(guestId),
      }),
    })
      .then((res) => {
        if (!res.ok) {
          return res.json().then((err) => {
            throw err;
          });
        }
        return res.json();
      })
      .then((data) => {
        alert("Appearance created!");
        onSuccess(data.episode_id);
      })
      .catch((err) => {
        setErrors(err.errors || ["Validation error"]);
      });
  }

  return (
    <div>
      <h2>Add Appearance</h2>

      {errors.map((e, i) => (
        <p key={i} style={{ color: "red" }}>
          {e}
        </p>
      ))}

      <form onSubmit={handleSubmit}>
        <input
          placeholder="Rating (1–5)"
          value={rating}
          onChange={(e) => setRating(e.target.value)}
        />

        <select onChange={(e) => setEpisodeId(e.target.value)}>
          <option value="">Select Episode</option>
          {episodes.map((ep) => (
            <option key={ep.id} value={ep.id}>
              Episode {ep.number}
            </option>
          ))}
        </select>

        <select onChange={(e) => setGuestId(e.target.value)}>
          <option value="">Select Guest</option>
          {guests.map((g) => (
            <option key={g.id} value={g.id}>
              {g.name}
            </option>
          ))}
        </select>

        <button type="submit">Create</button>
      </form>
    </div>
  );
}

export default AppearanceForm;
