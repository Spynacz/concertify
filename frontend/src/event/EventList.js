import { Card, Container, Nav } from "react-bootstrap";
import { LinkContainer } from "react-router-bootstrap";
import "./EventList.css";
import { eventList } from "../REST";
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

export default function EventList() {
  function get() {
    eventList(next)
      .then((data) => {
        setEvents([...events, ...data.results]);
        setNext(data.next);
      })
      .catch((err) => {
        console.log(err);
      });
  }
  const [events, setEvents] = useState([]);
  const [next, setNext] = useState("");
  useEffect(() => {
    if (document.body.offsetHeight <= 300) {
      get();
    }
    const onScroll = function () {
      if (
        next !== null &&
        window.innerHeight + window.scrollY >= document.body.offsetHeight
      ) {
        get();
      }
    };
    window.addEventListener("scroll", onScroll);
    return () => window.removeEventListener("scroll", onScroll);
  }, [next]);

  return (
    <Container fluid>
      <ul className="event-list">
        {events.map((event) => (
          <li key={event.id}>
            <LinkContainer to={"/event/" + event.id}>
              <Nav.Link as="div" role="button">
                <EventPreview
                  title={event.title}
                  image="https://weknowyourdreams.com/images/party/party-12.jpg"
                  location={event.location.address_line}
                  date={event.start}
                />
              </Nav.Link>
            </LinkContainer>
          </li>
        ))}
      </ul>
    </Container>
  );
}
