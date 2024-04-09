import './Event.css'

export function EventPreview({ title, location, date, image }) {
  return (
    <div className="event-preview">
      <div className="event-preview-image-container">
        <img className="event-preview-image" src={image}/>
      </div>
      <div className="event-preview-data">
        <div className="event-preview-title">{title}</div>
        <div className="event-preview-info">
          <div className="event-preview-location">{location}</div>
          <div className="event-preview-date">{date}</div>
        </div>
      </div>
    </div>
  );
}

export function EventList({ count }) {
  return (
    <div className="event-list-container">
      <ul className="event-list">
        {
          Array.from({length: count}, (_, i) => 
            <li key={i}>
              <EventPreview 
                title="Kinda normal length test title"
                image="https://weknowyourdreams.com/images/party/party-12.jpg"
                location="Somewhere 23/15"
                date="12/04/2024"
              />
            </li>)
        }
      </ul>
    </div>
  );
}
