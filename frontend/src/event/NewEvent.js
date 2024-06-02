import { Form, Button, Image } from "react-bootstrap";
import { useState } from "react";
import "./NewEvent.css";

export default function NewEvent() {
  function change() {
    const t = event.target;
    const index = +t.name.split("-")[1];
    const changed = [
      ...social.slice(0, index),
      t.value,
      ...social.slice(index + 1),
    ].filter((x) => x !== "");
    const n = [...changed, ""];
    console.log(n);
    setSocial(n);
  }
  const [social, setSocial] = useState([""]);
  return (
    <div className="new-event-container">
      <Form className="new-event-form">
        <div className="new-event-image-data">
          <Image src="https://wallpaperaccess.com/full/6361597.jpg" fluid />
          <div className="new-event-data">
            <Form.Label> Title </Form.Label>
            <Form.Control className="title" type="text" name="title" />
            <Form.Label> Location </Form.Label>
            <Form.Control className="location" type="text" name="location" />
            <Form.Label> Date </Form.Label>
            <Form.Control className="date" type="date" name="date" />
            <Form.Label> Social </Form.Label>
            {[...Array(social.length).keys()].map((x) => (
              <Form.Control
                className="social"
                value={social[x]}
                onChange={change}
                type="text"
                name={"social-" + x}
                key={x}
              />
            ))}
          </div>
        </div>
        <div className="desc-container">
          <Form.Label> Description </Form.Label>
          <Form.Control
            as="textarea"
            className="desc"
            type="text"
            name="desc"
          />
        </div>
        <Button className="create-button">Create post</Button>
      </Form>
    </div>
  );
}
