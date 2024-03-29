import './Event.css'

export function EventPreview() {
  return (
    <div className="event-preview">
    </div>
  );
}

export function EventList({ count }) {
  return (
    <div className="event-list-container">
      <ul className="event-list-tools">
        <li>Sort</li>
        <li>Filter</li>
        <li>Search</li>
      </ul>
      <ul className="event-list">
        {
          Array.from({length: count}, (_, i) => <li key={i}><EventPreview/></li>)
        }
      </ul>
    </div>
  );
}
