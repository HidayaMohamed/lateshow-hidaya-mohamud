function GuestsList({ guests }) {
  return (
    <div>
      <h2>Guests</h2>
      <ul>
        {guests.map((guest) => (
          <li key={guest.id}>
            {guest.name} ({guest.occupation})
          </li>
        ))}
      </ul>
    </div>
  );
}

export default GuestsList;
