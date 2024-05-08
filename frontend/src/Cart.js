import "./Cart.css";
import { Form } from "react-bootstrap";
import { EventPreview } from "./Event.js";

function Ticket({ price, normalQuantity, reducedQuantity }) {
  return (
    <div className="ticket">
      <EventPreview
        title="title"
        image="https://weknowyourdreams.com/images/party/party-12.jpg"
        location="Warsaw"
        date="12/04/2024 12:23"
      />
      <Form>
        <div className="side-by-side">
          <Form.Text>Type (price)</Form.Text>
          <Form.Text>Quantity</Form.Text>
          <Form.Text>Total</Form.Text>
        </div>
        <hr />
        <div className="side-by-side">
          <Form.Text>Normal ({price}zł)</Form.Text>
          <Form.Control
            type="number"
            className="ticket-quantity"
            defaultValue={normalQuantity}
          />
          <Form.Text>{price * normalQuantity}zł</Form.Text>
        </div>
        <div className="side-by-side">
          <Form.Text>Reduced ({price / 2}zł)</Form.Text>
          <Form.Control
            type="number"
            className="ticket-quantity"
            defaultValue={reducedQuantity}
          />
          <Form.Text>{(price * reducedQuantity) / 2}zł</Form.Text>
        </div>
      </Form>
    </div>
  );
}

export default function Cart() {
  return (
    <div className="cart-container">
      <Ticket price={15} normalQuantity={1} reducedQuantity={2} />
      <Ticket price={10} normalQuantity={0} reducedQuantity={2} />
      <Ticket price={20} normalQuantity={4} reducedQuantity={0} />
      <Ticket price={5} normalQuantity={4} reducedQuantity={0} />
    </div>
  );
}
