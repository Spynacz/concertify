import { Button } from "react-bootstrap";
import "./EventPage.css";

export default function EventDetails({ eventData }) {
  return (
    <div className="event-details">
      <div className="parallax parallax-image"></div>
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
      <div className="event-desc mx-4">
        {eventData.desc}
        Lorem ipsum dolor sit amet, officia excepteur ex fugiat reprehenderit
        enim labore culpa sint ad nisi Lorem pariatur mollit ex esse
        exercitation amet. Nisi anim cupidatat excepteur officia. Reprehenderit
        nostrud nostrud ipsum Lorem est aliquip amet voluptate voluptate dolor
        minim nulla est proident. Nostrud officia pariatur ut officia. Sit irure
        elit esse ea nulla sunt ex occaecat reprehenderit commodo officia dolor
        Lorem duis laboris cupidatat officia voluptate. Culpa proident
        adipisicing id nulla nisi laboris ex in Lorem sunt duis officia eiusmod.
        Aliqua reprehenderit commodo ex non excepteur duis sunt velit enim.
        Voluptate laboris sint cupidatat ullamco ut ea consectetur et est culpa
        et culpa duis.Lorem ipsum dolor sit amet, officia excepteur ex fugiat
        reprehenderit enim labore culpa sint ad nisi Lorem pariatur mollit ex
        esse exercitation amet. Nisi anim cupidatat excepteur officia.
        Reprehenderit nostrud nostrud ipsum Lorem est aliquip amet voluptate
        voluptate dolor minim nulla est proident. Nostrud officia pariatur ut
        officia. Sit irure elit esse ea nulla sunt ex occaecat reprehenderit
        commodo officia dolor Lorem duis laboris cupidatat officia voluptate.
        Culpa proident adipisicing id nulla nisi laboris ex in Lorem sunt duis
        officia eiusmod. Aliqua reprehenderit commodo ex non excepteur duis sunt
        velit enim. Voluptate laboris sint cupidatat ullamco ut ea consectetur
        et est culpa et culpa duis.Lorem ipsum dolor sit amet, officia excepteur
        ex fugiat reprehenderit enim labore culpa sint ad nisi Lorem pariatur
        mollit ex esse exercitation amet. Nisi anim cupidatat excepteur officia.
        Reprehenderit nostrud nostrud ipsum Lorem est aliquip amet voluptate
        voluptate dolor minim nulla est proident. Nostrud officia pariatur ut
        officia. Sit irure elit esse ea nulla sunt ex occaecat reprehenderit
        commodo officia dolor Lorem duis laboris cupidatat officia voluptate.
        Culpa proident adipisicing id nulla nisi laboris ex in Lorem sunt duis
        officia eiusmod. Aliqua reprehenderit commodo ex non excepteur duis sunt
        velit enim. Voluptate laboris sint cupidatat ullamco ut ea consectetur
        et est culpa et culpa duis.
      </div>
    </div>
  );
}
