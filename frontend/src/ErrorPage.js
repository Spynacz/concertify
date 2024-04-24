import { Col, Container, Row } from "react-bootstrap";
import { useRouteError } from "react-router-dom";

export default function ErrorPage() {
  const error = useRouteError();
  console.error(error);

  return (
    <Container>
      <Row className="text-center">
        <Col>
          <h1>Oops!</h1>
        </Col>
      </Row>
      <Row className="text-center">
        <Col>
          <p>
            <i>{error.statusText || error.message}</i>
          </p>
        </Col>
      </Row>
    </Container>
  );
}
