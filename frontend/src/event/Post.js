import { useCallback, useEffect, useState } from "react";
import { Card, Col, Modal, Row } from "react-bootstrap";
import { useCookies } from "react-cookie";
import { getAuthorization } from "../Utils";
import CommentInput from "./CommentInput";
import CommentVote from "./CommentVote";
import "./Post.css";
import PostVote from "./PostVote";

export default function Post({ id, title, desc, votes, image, hasVoted }) {
  const [comments, setComments] = useState([]);
  const [show, setShow] = useState(false);
  const [voted, setVoted] = useState(hasVoted);
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
                <PostVote postId={id} numVotes={votes} hasVoted={voted} />
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
            {desc}
            <img
              className="img-fluid"
              src="https://media.timeout.com/images/103926031/image.jpg"
            />
          </div>

          {comments.map((comment) => (
            <div className="d-flex my-5" key={comment.id}>
              <img
                className="rounded-circle me-3"
                style={{ width: "50px", height: "50px" }}
                src="https://png.pngtree.com/png-vector/20190710/ourlarge/pngtree-business-user-profile-vector-png-image_1541960.jpg"
              />
              <div className="w-100">
                <h5>{comment.user.username}</h5>
                <div className="d-flex justify-content-between">
                  <p>{comment.desc}</p>
                  <CommentVote
                    commentId={comment.id}
                    numVotes={comment.vote_count}
                  />
                </div>
              </div>
            </div>
          ))}
          {user ? <CommentInput user={user} postId={id} callback={getComments}/> : ""}
        </Modal.Body>
      </Modal>
    </>
  );
}
