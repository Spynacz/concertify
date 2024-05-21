import "./Cart.css";
import { useState, useEffect } from "react";
import { useCookies } from "react-cookie";
import { Form } from "react-bootstrap";
import { EventPreview } from "./event/EventList.js";
import { getEventDetails } from "./event/EventDetails.js";

function Ticket({ ticket }) {
  const init = { location: "" };
  const [eventDetails, setEventDetails] = useState(init);
  const [cookies, setCookie, removeCookie] = getCartCookie();
  function quantityChange() {
    const cart = cookies["cart"];
    const value = event.target.value;
    const el = cart.findIndex((el) => el.id === ticket.id);
    if (el !== -1) {
      if (+value < 1) {
        setCookie("cart", [...cart.splice(0, el), ...cart.splice(el + 1)]);
      } else {
        setCookie("cart", [
          ...cart.splice(0, el),
          { ...cart[el], quantity: value },
          ...cart.splice(el + 1),
        ]);
      }
    }
  }
  if (eventDetails === init)
    getEventDetails(ticket.event).then((data) => setEventDetails(data));
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

export function getCartCookie() {
  function get() {
    fetch("http://localhost:8000/cart", {
      method: "GET",
      headers: {
        Authorization: "Token " + user.token,
      },
    })
      .then((response) => {
        if (!response.ok) throw new Error(response.status);
        return response.json();
      })
      .then((data) => {
        console.log(data);
      })
      .catch((err) => {
        if (err.message === "400") {
          setCookie("cart", []);
        } else {
          console.log(err.message);
        }
      });
  }
  const [cookies, setCookie, removeCookie] = useCookies(["cart", "user"]);
  const user = cookies["user"];
  if (cookies["cart"] === undefined) {
    get();
  }
  return [cookies, setCookie, removeCookie];
}

export function addTicket(cookies, setCookie, ticket, event) {
  const cart = cookies["cart"];
  const el = cart.findIndex((el) => el.id === ticket.id);
  if (el === -1) {
    setCookie("cart", [
      ...cookies["cart"],
      { ...ticket, event: event, quantity: 1 },
    ]);
  } else {
    setCookie("cart", [
      ...cart.slice(0, el),
      { ...cart[el], quantity: +cart[el].quantity + 1 },
      ...cart.slice(el + 1),
    ]);
  }
}

export default function Cart() {
  const [fetched, setFetched] = useState(false);
  const [cookies, setCookie, removeCookie] = getCartCookie();
  const user = cookies["user"];
  const cart = cookies["cart"];
  return (
    <div className="cart-container">
      {cart.map((val, index) => (
        <Ticket ticket={val} key={val.id} />
      ))}
    </div>
  );
}
