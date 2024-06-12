import { useEffect, useState } from "react";
import { Container } from "react-bootstrap";
import { useCookies } from "react-cookie";
import { useParams } from "react-router-dom";
import { eventGet } from "../REST";
import EventDetails from "./EventDetails";
import JoinButton from "./JoinButton";
import PostList from "./PostList";
import NewPost from "./NewPost";

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
    permission_level: "",
    title: "",
    desc: "",
    picture: "",
    start: "",
    end: "",
    ticket: {},
  };

  const { id } = useParams();
  const [eventData, setEventData] = useState(initialState);
  const [cookies, setCookie, removeCookie] = useCookies();
  const user = cookies.user;

  useEffect(() => {
    if (user) {
      eventGet(user.token, id).then((data) => {
        setEventData(data);
      });
    } else {
      eventGet(null, id).then((data) => {
        setEventData(data);
      });
    }
  }, []);

  return (
    <Container fluid style={{ display: "block", padding: "0" }}>
      <EventDetails eventData={eventData} />
      <JoinButton tickets={eventData.ticket} eventId={id} />
      <PostList eventId={id} />
      {eventData.permission_level == 3 ? (
        <NewPost eventId={id} user={user} />
      ) : (
        ""
      )}
    </Container>
  );
}
