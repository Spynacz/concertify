import { Button, Container, Form, Nav, Navbar } from "react-bootstrap";
import { BrowserRouter as Router, Route, Link } from "react-router-dom";
import "./NavBar.css";

function UserNavBar() {
  return (
    <>
      <Nav.Link className="nav-link"><Link to="#">
        New Event
      </Link></Nav.Link>
      <Nav.Link className="nav-link"><Link to="#">
        Profile
      </Link></Nav.Link>
      <Nav.Link className="nav-link"><Link to="/logout">
        Logout
      </Link></Nav.Link>
    </>
  );
}

function GuestNavBar() {
  return (
    <>
      <Nav.Link className="nav-link"><Link to="/login">
        Login
      </Link></Nav.Link>
      <Nav.Link className="nav-link"><Link to="/register">
        Register
      </Link></Nav.Link>
    </>
  );
}

export default function NavBar({ isGuest }) {
  return (
    <Navbar expand="sm">
      <Container fluid>
        <Navbar.Brand id="logo"><Link to="/">
            concertify
          </Link></Navbar.Brand>
        <Navbar.Toggle />
        <Navbar.Collapse id="navbar-nav" className="justify-content-end">
          <Form className="d-flex">
            <Form.Control type="text" placeholder="Search" className="me-2" />
            <Button type="submit" className="search-button">
              Search
            </Button>
          </Form>
          <Nav>
            <Nav.Link href="#">Cart</Nav.Link>
            {isGuest ? <GuestNavBar /> : <UserNavBar />}
          </Nav>
        </Navbar.Collapse>
      </Container>
    </Navbar>
  );
}
