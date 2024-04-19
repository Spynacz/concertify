import { Card, Container, Nav } from "react-bootstrap";
import "./Event.css";
import { Link } from "react-router-dom";
import { useEffect, useState } from "react";

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

export function EventList() {
  const get = async() => {
    const options = {
      weekday: "long",
      year: "numeric",
      month: "long",
      day: "numeric",
    };
    await fetch('http://localhost:8000/event', {
      method: 'GET',
    })
      .then((response) => {
        if(!response.ok) throw new Error(response.status);
        return response.json();
      })
      .then((data) => {
        const newEvents = 
          data.results.map(event => 
                           ({
                             ...event,
                             start: new Date(event.start).toLocaleDateString(undefined, options)
                           }));
        console.log(newEvents);
        setEvents([...events, ...newEvents]);
      })
      .catch((err) => {
        console.log(err.message);
      });
  }
  const [events, setEvents] = useState([]);
  useEffect(() => {get();}, []);

  return (
    <Container fluid>
      <ul className="event-list">
        {events.map((event) => (
          <li key={event.id}>
            <Nav.Link role="button">
              <Link to={"/event/" + event.id}>
              <EventPreview
                title={event.title}
                image="https://weknowyourdreams.com/images/party/party-12.jpg"
                location={event.location}
                date={event.start}
              />
              </Link></Nav.Link>
          </li>
        ))}
      </ul>
    </Container>
  );
}
