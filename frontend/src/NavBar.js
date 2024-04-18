import { Button, Container, Form, Nav, Navbar } from "react-bootstrap";
import { BrowserRouter as Router, Route, Link } from "react-router-dom";
import "./NavBar.css";
import { useContext } from "react";
import { UserContext } from "./App.js";

function UserNavBar() {
  const { user, setUser } = useContext(UserContext);
  return (
    <>
      <Nav.Link role="button"><Link to="/new-event">
        New Event
      </Link></Nav.Link>
      <Nav.Link role="button"><Link to={"/user/" + user.username}>
        Profile
      </Link></Nav.Link>
      <Nav.Link role="button"><Link to="/logout">
        Logout
      </Link></Nav.Link>
    </>
  );
}

function GuestNavBar() {
  return (
    <>
      <Nav.Link role="button"><Link to="/login">
        Login
      </Link></Nav.Link>
      <Nav.Link role="button"><Link to="/register">
        Register
      </Link></Nav.Link>
    </>
  );
}

export default function NavBar() {
  const { user, setUser } = useContext(UserContext);
  return (
    <Navbar expand="sm">
      <Container fluid>
        <Navbar.Brand role="button" id="logo"><Link to="/">
          concertify
        </Link></Navbar.Brand>
        <Navbar.Toggle />
        <Navbar.Collapse id="navbar-nav" className="justify-content-end">
          <Form className="d-flex">
            <Form.Control type="text" placeholder="Search" className="me-2" />
            <Button type="submit" className="search-button accent-button">
              Search
            </Button>
          </Form>
          <Nav>
            <Nav.Link role="button"><Link to="/cart">
              Cart
            </Link></Nav.Link>
            {user == null ? <GuestNavBar/> : <UserNavBar user={user}/>}
          </Nav>
        </Navbar.Collapse>
      </Container>
    </Navbar>
  );
}
