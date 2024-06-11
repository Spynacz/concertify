import { useLayoutEffect, useRef, useState } from "react";
import { Button, Form, Image, Modal } from "react-bootstrap";
import { postPost, uploadImageToS3 } from "../REST";
import "./NewPost.css";

const MIN_BODYTEXT_HEIGHT = 10;

export default function NewPost({ eventId, user }) {
  const [show, setShow] = useState(false);
  const bodyRef = useRef();
  const [body, setBody] = useState("");
  const [preview, setPreview] = useState(null);

  const handleClose = () => setShow(false);
  const handleShow = () => setShow(true);

  const handleOnChange = (event) => {
    event.preventDefault();
    setBody(event.target.value);
  };

  const handleSubmit = (event) => {
    event.preventDefault();

    if (postImages.files[0]) {
      let imageUrl;
      uploadImageToS3(postImages.files[0])
        .then((location) => {
          imageUrl = location;
          console.log(imageUrl);
          postPost(user.token, postTitle.value, body, imageUrl, eventId).catch(
            (err) => console.log(err),
          );
        })
        .catch((err) => console.error(err));
    } else {
      postPost(user.token, postTitle.value, body, "", eventId).catch((err) =>
        console.log(err),
      );
    }
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
                  className="my-1"
                />
              </Form.Group>

              <Form.Group controlId="postBody">
                <Form.Control
                  type="text"
                  as="textarea"
                  placeholder="Share some thoughts"
                  style={{ wordBreak: "break-all", resize: "none" }}
                  className="my-1"
                  value={body}
                  ref={bodyRef}
                  onChange={handleOnChange}
                />
              </Form.Group>

              {preview && (
                <Image src={URL.createObjectURL(preview)} rounded fluid />
              )}
              <Form.Group controlId="postImages">
                <Form.Control
                  type="file"
                  className="my-1"
                  onChange={(event) => {
                    setPreview(event.target.files[0]);
                  }}
                />
              </Form.Group>
              <Button
                type="submit"
                onClick={() => setShow(false)}
                className="mt-2 float-end"
              >
                Publish
              </Button>
            </Form>
          </div>
        </Modal.Body>
      </Modal>
    </>
  );
}
