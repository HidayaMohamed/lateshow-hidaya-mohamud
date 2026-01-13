import { useState } from "react";

function AppearanceForm({ episodes, guests, onSuccess }) {
  // Set state to null for tracking rating input
  const [rating, setRating] = useState("");
  // State to track the selected episode
  const [episodeId, setEpisodeId] = useState("");
  const [guestId, setGuestId] = useState("");
  const [errors, setErrors] = useState([]);

  // Function to handle form submission
  function handleSubmit(e) {
    e.preventDefault();
    // clear previous errors
    setErrors([]);

    // Send POST request to backend
    fetch("http://127.0.0.1:5000/appearances", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        // convert string to number
        rating: Number(rating),
        episode_id: Number(episodeId),
        guest_id: Number(guestId),
      }),
    })
      .then((res) => {
        // If the response is not ok, throw an error to catch block
        if (!res.ok) {
          return res.json().then((err) => {
            throw err;
          });
        }
        return res.json();
      })
      .then((data) => {
        //   Alerts when an appearance is succesfully created
        alert("Appearance created!");
        // reloads episode with new appearance
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
          style={{ width: "100px", height: "30px" }}
          placeholder="Rating (1-5)"
          value={rating}
          onChange={(e) => setRating(e.target.value)}
        />

        <select
          onChange={(e) => setEpisodeId(e.target.value)}
          style={{ width: "150px", height: "35px" }}
        >
          <option value="">Select Episode</option>
          {episodes.map((ep) => (
            <option key={ep.id} value={ep.id}>
              Episode {ep.number}
            </option>
          ))}
        </select>

        <select
          onChange={(e) => setGuestId(e.target.value)}
          style={{ width: "150px", height: "35px" }}
        >
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
