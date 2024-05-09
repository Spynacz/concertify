import { useEffect, useState } from "react";
import { Button, Card, Col, Modal, Row } from "react-bootstrap";
import "./Post.css";

export default function Post({ id, title, desc, votes, image }) {
  const [comments, setComments] = useState([]);
  const [show, setShow] = useState(false);

  const handleClose = () => setShow(false);
  const handleShow = () => setShow(true);

  const get = async () => {
    await fetch(`http://localhost:8000/comment?post=${id}`, {
      method: "GET",
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
  };

  useEffect(() => {
    get();
  }, []);

  return (
    <>
      <Row className="justify-content-center my-3 post" onClick={handleShow}>
        <Col sm={9} md={8}>
          <Card>
            <Card.Img
              variant="top"
              src="https://media.timeout.com/images/103926031/image.jpg" /* src={image} */
            />
            <Card.Body>
              <Card.Title>{title}</Card.Title>
              <div className="d-flex justify-content-between">
                <Card.Text>{desc}</Card.Text>
                <a>
                  <i className="fas fa-thumbs-up"></i> {votes}
                </a>
              </div>
            </Card.Body>
          </Card>
        </Col>
      </Row>

      <Modal
        fullscreen="lg-down"
        size="xl"
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
            <div className="d-flex flex-column my-3" key={comment.id}>
              <h5>{comment.user}</h5>
              <div className="d-flex justify-content-between">
                <p>{comment.desc}</p>
                <a>
                  <i className="fas fa-thumbs-up"></i> {comment.vote_count}
                </a>
              </div>
              <hr className="my-1" style={{ height: "3px" }} />
            </div>
          ))}
        </Modal.Body>
      </Modal>
    </>
  );
}
