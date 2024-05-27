import { Container } from "react-bootstrap";
import { useCookies } from "react-cookie";
import { useParams } from "react-router-dom";
import { useEffect, useState } from "react";
import { eventGet } from "../REST";
import EventDetails from "./EventDetails";
import "./EventPage.css";
import JoinButton from "./JoinButton";
import PostList from "./PostList";

export default function EventPage() {
  const initialState = {
    id: -1,
    event_contacts: [],
    social_media: [],
    location: {
      id: -1,
      name: "",
      address_line: "",
      postal_code: "",
      country: "",
    },
    title: "",
    desc: "",
    picture: null,
    start: "",
    end: "",
    ticket: {},
  };
  const { id } = useParams();
  const [cookies, setCookie, removeCookie] = useCookies(["user"]);
  const [eventData, setEventData] = useState(initialState);
  useEffect(() => {
    eventGet(id).then((data) => setEventData(data));
  }, []);

  return (
    <Container fluid style={{ display: "block", padding: "0" }}>
      <EventDetails eventData={eventData} />
      <JoinButton tickets={eventData.ticket} eventId={id} />
      <PostList eventId={id} />
    </Container>
  );
}
