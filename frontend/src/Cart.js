import "./Cart.css";
import { useState, useEffect } from "react";
import { useCookies } from "react-cookie";
import { Form } from "react-bootstrap";
import { EventPreview } from "./event/EventList.js";
import { eventGet } from "./REST";
import { cartPost, cartGet } from "./REST";

function Ticket({ ticket }) {
  const init = { location: "" };
  const [eventDetails, setEventDetails] = useState(init);
  const [cookies, setCookie, removeCookie] = useCookies(["cart", "user"]);
  const user = cookies["user"];
  if (user !== undefined) {
    useEffect(() => {
      cartGet(cookies["user"].token).then((data) => setCookie("cart", data));
    }, []);
  }
  function quantityChange() {
    const cart = cookies["cart"];
    if (cart === undefined) return;
    const value = event.target.value;
    const el = cart.findIndex((el) => el.id === ticket.id);
    if (el !== -1) {
      const newCart =
        +value < 1
          ? [...cart.splice(0, el), ...cart.splice(el + 1)]
          : [
              ...cart.splice(0, el),
              { ...cart[el], quantity: value },
              ...cart.splice(el + 1),
            ];
      setCookie("cart", newCart);
      if (user !== undefined) cartPost(user.token, newCart);
    }
  }
  if (eventDetails === init && ticket.event !== undefined)
    eventGet(ticket.event).then((data) => setEventDetails(data));
  return (
    <div className="ticket">
      <EventPreview
        title={eventDetails.title}
        image="https://weknowyourdreams.com/images/party/party-12.jpg"
        location={eventDetails.location.address_line}
        date={eventDetails.date}
      />
      <Form>
        <div className="side-by-side">
          <Form.Text>Type (price)</Form.Text>
          <Form.Text>Quantity</Form.Text>
          <Form.Text>Total</Form.Text>
        </div>
        <hr />
        <div className="side-by-side">
          <Form.Text>Normal ({ticket.amount}zł)</Form.Text>
          <Form.Control
            type="number"
            className="ticket-quantity"
            defaultValue={ticket.quantity}
            onInput={quantityChange}
          />
          <Form.Text>
            {(ticket.amount * ticket.quantity).toFixed(2)}zł
          </Form.Text>
        </div>
      </Form>
    </div>
  );
}

export function addTicket(cookies, setCookie, ticket, event) {
  const cart = cookies["cart"];
  const user = cookies["user"];
  if (user !== undefined)
    cartGet(cookies["user"].token).then((data) => setCookie("cart", data));
  if (cart === undefined) return;
  const el = cart.findIndex((el) => el.id === ticket.id);
  const newCart =
    el === -1
      ? [...cart, { ...ticket, event: event, quantity: 1, ticket_type: 1 }]
      : [
          ...cart.slice(0, el),
          { ...cart[el], quantity: +cart[el].quantity + 1, ticket_type: 1 },
          ...cart.slice(el + 1),
        ];
  setCookie("cart", newCart);
  if (user !== undefined) cartPost(user.token, newCart);
}

export default function Cart() {
  const [cookies, setCookie, removeCookie] = useCookies(["cart", "user"]);
  const user = cookies["user"];
  const cart = cookies["cart"];
  if (user !== undefined) {
    useEffect(() => {
      cartGet(user.token).then((data) => setCookie("cart", data));
    }, []);
  } else if (cart === undefined) {
    setCookie("cart", []);
    return;
  }
  if (cart === undefined) return;
  return (
    <div className="cart-container">
      {cart.map((val, index) => (
        <Ticket ticket={val} key={val.id} />
      ))}
    </div>
  );
}
