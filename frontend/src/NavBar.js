import { Button, Container, Form, Nav, Navbar } from "react-bootstrap";
import { BrowserRouter as Router, Route, Link } from "react-router-dom";
import "./NavBar.css";

function UserNavBar() {
  return (
    <>
      <Nav.Link role="button" href="/new-event">
        New Event
      </Nav.Link>
      <Nav.Link role="button" href={"/user/" + user.id}>
        Profile
      </Nav.Link>
      <Nav.Link role="button" href="/logout">
        Logout
      </Link></Nav.Link>
    </>
  );
}

function GuestNavBar() {
  return (
    <>
      <Nav.Link role="button" href="/login">
        Login
      </Nav.Link>
      <Nav.Link role="button" href="/register">
        Register
      </Link></Nav.Link>
    </>
  );
}

export default function NavBar({ isGuest }) {
  return (
    <Navbar expand="sm">
      <Container fluid>
        <Navbar.Brand role="button" id="logo" href="/">
          concertify
        </Navbar.Brand>
        <Navbar.Toggle />
        <Navbar.Collapse id="navbar-nav" className="justify-content-end">
          <Form className="d-flex">
            <Form.Control type="text" placeholder="Search" className="me-2" />
            <Button type="submit" className="search-button accent-button">
              Search
            </Button>
          </Form>
          <Nav>
            <Nav.Link role="button" href="/cart">
              Cart
            </Nav.Link>
            {isGuest ? <GuestNavBar /> : <UserNavBar />}
          </Nav>
        </Navbar.Collapse>
      </Container>
    </Navbar>
  );
}
