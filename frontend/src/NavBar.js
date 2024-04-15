import { Button, Container, Form, Nav, Navbar } from "react-bootstrap";
import "./NavBar.css";

function UserNavBar() {
  return (
    <>
      <Nav.Link className="nav-link" href="#">
        New Event
      </Nav.Link>
      <Nav.Link className="nav-link" href="#">
        Profile
      </Nav.Link>
      <Nav.Link className="nav-link" href="#">
        Logout
      </Nav.Link>
    </>
  );
}

function GuestNavBar() {
  return (
    <>
      <Nav.Link className="nav-link" href="#">
        Login
      </Nav.Link>
      <Nav.Link className="nav-link" href="#">
        Register
      </Nav.Link>
    </>
  );
}

export default function NavBar({ isGuest }) {
  return (
    <Navbar expand="sm">
      <Container fluid>
        <Navbar.Brand id="logo" href="#">
          concertify
        </Navbar.Brand>
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
