import { useCallback, useEffect, useState } from "react";
import { Card, Col, Modal, Row } from "react-bootstrap";
import { useCookies } from "react-cookie";
import { getAuthorization } from "../Utils";
import CommentInput from "./CommentInput";
import CommentVote from "./CommentVote";
import "./Post.css";
import PostVote from "./PostVote";
import Comment from "./Comment";

export default function Post({ id, title, desc, numVotes, image, hasVoted }) {
  const [comments, setComments] = useState([]);
  const [show, setShow] = useState(false);
  const [voted, setVoted] = useState(hasVoted);
  const [votes, setVotes] = useState(numVotes);
  const [cookies, setCookie, removeCookie] = useCookies();

  const handleClose = () => setShow(false);
  const handleShow = () => setShow(true);

  const user = cookies["user"];
  const getComments = useCallback(async () => {
    await fetch(`http://localhost:8000/comment?post=${id}`, {
      method: "GET",
      headers: { Authorization: getAuthorization(user) },
    })
      .then((response) => {
        if (!response.ok) throw new Error(response.status);
        return response.json();
      })
      .then((data) => {
        setComments(data.results);
      })
      .catch((err) => {
        console.log(err.message);
      });
  }, []);

  useEffect(() => {
    getComments();
  }, [getComments]);

  const updateCommentVotes = (id, votes, voted) => {
    const newComments = comments.slice();
    const updatedComment = newComments.find((c) => c.id === id);
    updatedComment.vote_count = votes;
    updatedComment.has_voted = voted;
    setComments(newComments);
  };

  return (
    <>
      <Row className="justify-content-center my-3">
        <Col sm={9} md={8} lg={7} xl={6} xxl={5}>
          <Card onClick={handleShow} className="post">
            <Card.Img
              variant="top"
              src="https://media.timeout.com/images/103926031/image.jpg" /* src={image} */
            />
            <Card.Body>
              <Card.Title>{title}</Card.Title>
              <div className="d-flex justify-content-between">
                <Card.Text>{desc}</Card.Text>
                <PostVote
                  postId={id}
                  numVotes={votes}
                  voted={voted}
                  setVoted={setVoted}
                  votes={votes}
                  setVotes={setVotes}
                />
              </div>
            </Card.Body>
          </Card>
        </Col>
      </Row>

      <Modal
        fullscreen="lg-down"
        size="lg"
        show={show}
        onHide={handleClose}
        centered
      >
        <Modal.Header closeButton>
          <Modal.Title>{title}</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <div className="d-flex flex-column">
            <p className="mb-2">{desc}</p>
            <img
              className="img-fluid rounded-2"
              src="https://media.timeout.com/images/103926031/image.jpg"
            />
          </div>
          <PostVote
            postId={id}
            numVotes={votes}
            voted={voted}
            setVoted={setVoted}
            votes={votes}
            setVotes={setVotes}
          />

          {comments.map((comment) => (
            <Comment
              id={comment.id}
              user={comment.user.username}
              desc={comment.desc}
              numVotes={comment.vote_count}
              hasVoted={comment.has_voted}
              callback={updateCommentVotes}
              key={comment.id}
            />
          ))}
          {user ? (
            <CommentInput user={user} postId={id} callback={getComments} />
          ) : (
            ""
          )}
        </Modal.Body>
      </Modal>
    </>
  );
}
