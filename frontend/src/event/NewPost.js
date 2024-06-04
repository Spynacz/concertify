import { useLayoutEffect, useRef, useState } from "react";
import { Button, Form, Modal } from "react-bootstrap";
import { getAuthorization } from "../Utils";
import "./NewPost.css";

const MIN_BODYTEXT_HEIGHT = 10;

export default function NewPost({ eventId, user }) {
  const [show, setShow] = useState(false);
  const bodyRef = useRef();
  const [body, setBody] = useState("");

  const handleClose = () => setShow(false);
  const handleShow = () => setShow(true);

  const handleOnChange = (event) => {
    event.preventDefault();
    setBody(event.target.value);
  };

  const handleSubmit = (event) => {
    event.preventDefault();

    fetch("http://localhost:8000/post", {
      method: "POST",
      headers: {
        "Content-type": "application/json",
        Authorization: getAuthorization(user),
      },
      body: JSON.stringify({
        title: postTitle.value,
        desc: postBody.value,
        event: eventId,
      }),
    })
      .then((response) => {
        if (!response.ok) throw new Error(response.status);
      })
      .catch((err) => console.error(err.message));

    event.target.reset();
  };

  useLayoutEffect(() => {
    if (bodyRef.current) {
      bodyRef.current.style = "inherit";

      bodyRef.current.style.height = `${Math.max(
        bodyRef.current.scrollHeight,
        MIN_BODYTEXT_HEIGHT,
      )}px`;
    }
  }, [body]);

  return (
    <>
      <Button type="button" onClick={handleShow} className="newpost-button">
        New post
      </Button>

      <Modal
        fullscreen="lg-down"
        size="lg"
        show={show}
        onHide={handleClose}
        centered
      >
        <Modal.Header closeButton>
          <Modal.Title>Creating new post</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <div className="d-flex flex-column">
            <Form onSubmit={handleSubmit}>
              <Form.Group controlId="postTitle">
                <Form.Control
                  type="text"
                  placeholder="Title your post"
                  style={{ fontSize: "1.2em" }}
                />
              </Form.Group>

              <Form.Group controlId="postBody">
                <Form.Control
                  type="text"
                  as="textarea"
                  placeholder="Share some thoughts"
                  style={{ wordBreak: "break-all", resize: "none" }}
                  value={body}
                  ref={bodyRef}
                  onChange={handleOnChange}
                />
              </Form.Group>

              <Form.Group controlId="postImages">
                <Form.Control type="file" placeholder="Attach" />
              </Form.Group>
              <Button type="submit" className="mt-2 float-end">
                Publish
              </Button>
            </Form>
          </div>
        </Modal.Body>
      </Modal>
    </>
  );
}
