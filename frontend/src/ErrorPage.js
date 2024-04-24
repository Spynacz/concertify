import { Container, Row } from "react-bootstrap";
import { useRouteError } from "react-router-dom";

export default function ErrorPage() {
  const error = useRouteError();
  console.error(error);

  return (
    <Container>
      <Row className="text-center">
        <h1>Oops!</h1>
      </Row>
      <Row className="text-center">
        <p>
          <i>{error.statusText || error.message}</i>
        </p>
      </Row>
    </Container>
  );
}
