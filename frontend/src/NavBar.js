import { Button, Container, Form, Nav, Navbar } from "react-bootstrap";
import "./NavBar.css";
import { LinkContainer } from "react-router-bootstrap";
import { useCookies, Cookies } from "react-cookie";
import { Logout } from "./Login.js";

function UserNavBar() {
  const [cookies] = useCookies([]);
  return (
    <>
      <LinkContainer to="/new-event">
        <Nav.Link as="div" role="button">
          New Event
        </Nav.Link>
      </LinkContainer>
      <LinkContainer to="/profile">
        <Nav.Link as="div" role="button">
          Profile
        </Nav.Link>
      </LinkContainer>
      <Nav.Link as="div" role="button">
        <Logout />
      </Nav.Link>
    </>
  );
}

function GuestNavBar() {
  return (
    <>
      <LinkContainer to="/login">
        <Nav.Link as="div" role="button">
          Login
        </Nav.Link>
      </LinkContainer>
      <LinkContainer to="/register">
        <Nav.Link as="div" role="button">
          Register
        </Nav.Link>
      </LinkContainer>
    </>
  );
}

export default function NavBar() {
  const [cookies, setCookie, removeCookie] = useCookies(["user", "cart"]);
  const cart = cookies["cart"];
  return (
    <Navbar expand="sm" className="sticky-top">
      <Container fluid>
        <LinkContainer to="/">
          <Navbar.Brand role="button" id="logo">
            concertify
          </Navbar.Brand>
        </LinkContainer>
        <Navbar.Toggle />
        <Navbar.Collapse id="navbar-nav" className="justify-content-end">
          <Form className="d-flex">
            <Form.Control type="text" placeholder="Search" className="me-2" />
            <Button type="submit" className="search-button accent-button">
              Search
            </Button>
          </Form>
          <Nav>
            <LinkContainer to="/cart">
              <Nav.Link as="div" role="button">
                Cart
                {cart === undefined || cart.length === 0
                  ? ""
                  : " (" + cart.length + ")"}
              </Nav.Link>
            </LinkContainer>
            {"user" in cookies ? <UserNavBar /> : <GuestNavBar />}
          </Nav>
        </Navbar.Collapse>
      </Container>
    </Navbar>
  );
}
