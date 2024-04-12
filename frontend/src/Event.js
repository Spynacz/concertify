import { Card, Container } from "react-bootstrap";
import "./Event.css";

export function EventPreview({ title, location, date, image }) {
  return (
    <Card className="event-preview">
      <Card.Img src={image} className="event-preview-image-container" />
      <Card.Body className="event-preview-data">
        <Card.Title className="event-preview-title">{title}</Card.Title>
        <div className="event-preview-info">
          <Card.Text className="event-preview-location">{location}</Card.Text>
          <Card.Text className="event-preview-date">{date}</Card.Text>
        </div>
      </Card.Body>
    </Card>
  );
}

export function EventList({ count }) {
  return (
    <Container fluid>
      <ul className="event-list">
        {Array.from({ length: count }, (_, i) => (
          <li key={i}>
            <EventPreview
              title="Kinda normal length test title"
              image="https://weknowyourdreams.com/images/party/party-12.jpg"
              location="Somewhere 23/15"
              date="12/04/2024"
            />
          </li>
        ))}
      </ul>
    </Container>
  );
}
