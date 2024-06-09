import { Button, Row } from "react-bootstrap";
import { useCookies } from "react-cookie";
import { addTicket } from "../Cart";

export default function JoinButton({ tickets, eventId }) {
  const [cookies, setCookie, removeCookie] = useCookies(["cart", "user"]);
  if (tickets.length === 0) return;
  return (
    <Row className="justify-content-center mx-5">
      <Button
        className="w-25"
        onClick={() => addTicket(cookies, setCookie, tickets[0], eventId)}
      >
        Sign me up
      </Button>
    </Row>
  );
}
