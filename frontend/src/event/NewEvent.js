import { Form, Button, Image } from "react-bootstrap";
import { useState } from "react";
import "./NewEvent.css";
import { eventPost } from "../REST";
import { useCookies } from "react-cookie";

export default function NewEvent() {
  function submit() {
    event.preventDefault();
    const t = event.target;
    eventPost(
      user.token,
      t.title.value,
      "",
      t.location.value,
      t.date.value,
      social,
      t.desc.value,
    ).then((data) => {
      console.log(data);
    });
  }
  function change() {
    const t = event.target;
    const index = +t.name.split("-")[1];
    const changed = [
      ...social.slice(0, index),
      t.value,
      ...social.slice(index + 1),
    ].filter((x) => x !== "");
    const n = [...changed, ""];
    setSocial(n);
  }
  const [social, setSocial] = useState([""]);
  const [cookies] = useCookies(["user"]);
  const user = cookies["user"];
  return (
    <div className="new-event-container">
      <Form onSubmit={submit} className="new-event-form">
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
        <Button type="submit" className="create-button">
          Create post
        </Button>
      </Form>
    </div>
  );
}
