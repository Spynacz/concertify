import { Button } from "react-bootstrap";
import "./EventPage.css";

export default function EventDetails({ eventData }) {
  return (
    <div className="event-details">
      <div
        className="parallax parallax-image"
        style={{
          backgroundImage: `url(${eventData.picture})`,
        }}
      ></div>
      <h1 className="event-title text-center">{eventData.title}</h1>
      <div className="event-date text-center">
        {eventData.start} - {eventData.end}
      </div>
      <div className="event-location text-center">
        {eventData.location.address_line}
      </div>
      <div className="text-center mt-4">
        {eventData.social_media.map((item) => (
          <Button key={item.id} className="mx-2">
            <i className={"fab" + " fa-" + item.platform.toLowerCase()}></i>
          </Button>
        ))}
      </div>
      <div className="event-desc mx-4">{eventData.desc}</div>
    </div>
  );
}
