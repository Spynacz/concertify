import { useState } from "react";
import { Button, Form, Image } from "react-bootstrap";
import { useCookies } from "react-cookie";
import { eventPost, uploadImageToS3 } from "../REST";
import "./NewEvent.css";

export default function NewEvent() {
  const [social, setSocial] = useState([""]);
  const [preview, setPreview] = useState(null);
  const [cookies] = useCookies(["user"]);
  const user = cookies["user"];

  const submit = (event) => {
    event.preventDefault();

    const t = event.target;
    if (eventImage.files[0]) {
      let imageUrl;
      uploadImageToS3(eventImage.files[0])
        .then((location) => {
          imageUrl = location;
          console.log(imageUrl);
          eventPost(
            user.token,
            t.title.value,
            imageUrl,
            t.location.value,
            t.start_date.value,
            t.end_date.value,
            social,
            t.desc.value,
          ).catch((err) => console.log(err));
        })
        .catch((err) => console.log(err));
    } else {
      eventPost(
        user.token,
        t.title.value,
        "",
        t.location.value,
        t.start_date.value,
        t.end_date.value,
        social,
        t.desc.value,
      ).catch((err) => console.log(err));
    }
  };

  const change = (event) => {
    const t = event.target;
    const index = +t.name.split("-")[1];
    const changed = [
      ...social.slice(0, index),
      t.value,
      ...social.slice(index + 1),
    ].filter((x) => x !== "");

    const n = [...changed, ""];
    setSocial(n);
  };

  return (
    <div className="new-event-container">
      <Form onSubmit={submit} className="new-event-form">
        <div className="new-event-image-data">
          <div className="new-event-image">
            {preview && (
              <Image src={URL.createObjectURL(preview)} rounded fluid />
            )}
            <Form.Group controlId="eventImage">
              <Form.Control
                type="file"
                onChange={(event) => {
                  setPreview(event.target.files[0]);
                }}
              />
            </Form.Group>
          </div>
          <div className="new-event-data">
            <Form.Label> Title </Form.Label>
            <Form.Control className="title" type="text" name="title" />
            <Form.Label> Location </Form.Label>
            <Form.Control className="location" type="text" name="location" />
            <Form.Label> Date </Form.Label>
            <Form.Control
              className="date"
              type="datetime-local"
              name="start_date"
            />
            <Form.Control
              className="date"
              type="datetime-local"
              name="end_date"
            />
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
          Create event
        </Button>
      </Form>
    </div>
  );
}
