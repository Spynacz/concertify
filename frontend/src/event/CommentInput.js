import { Button, Form } from "react-bootstrap";
import { getAuthorization } from "../Utils";
import { useLayoutEffect, useRef, useState } from "react";

const MIN_COMMENTTEXT_HEIGHT = 3;

export default function CommentInput({ user, postId, callback }) {
  const commentTextRef = useRef();
  const [commentValue, setCommentValue] = useState("");

  const handleOnChange = (event) => {
    event.preventDefault();
    setCommentValue(event.target.value);
  };

  const handleSubmit = (event) => {
    event.preventDefault();

    fetch("http://localhost:8000/comment", {
      method: "POST",
      headers: {
        "Content-type": "application/json",
        Authorization: getAuthorization(user),
      },
      body: JSON.stringify({
        title: "Should comments really have titles?",
        desc: newComment.value,
        post: postId,
      }),
    })
      .then((response) => {
        if (!response.ok) throw new Error(response.status);
      })
      .catch((err) => console.error(err.message));

    callback();
    event.target.reset();
  };

  useLayoutEffect(() => {
    commentTextRef.current.style.height = "inherit";

    commentTextRef.current.style.height = `${Math.max(
      commentTextRef.current.scrollHeight,
      MIN_COMMENTTEXT_HEIGHT,
    )}px`;
  }, [commentValue]);

  return (
    <div className="d-flex flex-row mt-5">
      <img
        className="rounded-circle me-3"
        style={{ width: "30px", height: "30px" }}
        src="https://png.pngtree.com/png-vector/20190710/ourlarge/pngtree-business-user-profile-vector-png-image_1541960.jpg"
      />
      <Form className="w-100" onSubmit={handleSubmit}>
        <Form.Group className="mb-3" controlId="newComment">
          <Form.Control
            as="textarea"
            placeholder="Your comment"
            style={{ wordBreak: "break-all", resize: "none" }}
            ref={commentTextRef}
            value={commentValue}
            onChange={handleOnChange}
          />
        </Form.Group>
        <Button variant="primary" type="submit" className="mt-2 float-end">
          Comment
        </Button>
      </Form>
    </div>
  );
}
