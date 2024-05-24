import { Button, Card, Container, Form, Nav, Navbar } from "react-bootstrap";
import "./NavBar.css";
import { LinkContainer } from "react-router-bootstrap";
import { useCookies, Cookies } from "react-cookie";
import { Logout } from "./Login.js";
import { useEffect, useState } from "react";

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
  const [cookies, setCookie, removeCookie] = useCookies(["user"]);
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);

  const fetchSearch = async () => {
    await fetch("http://localhost:8000/event", {
      method: "GET",
    })
      .then((response) => {
        if (!response.ok) throw new Error(response.status);
        return response.json();
      })
      .then((data) => {
        setResults(
          data.results.filter((item) => {
            return item.title.toLowerCase().includes(query.toLowerCase());
          }),
        );
      })
      .catch((err) => {
        console.log(err.message);
      });
  };

  useEffect(() => {
    if (query !== "") {
      fetchSearch();
      console.log(results);
    } else {
      setResults([]);
    }
  }, [query]);

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
          <Form className="d-flex position-relative">
            <Form.Control
              type="text"
              placeholder="Search"
              className="me-2"
              onChange={(e) => setQuery(e.target.value)}
              value={query}
            />
            <Button type="submit" className="search-button accent-button">
              Search
            </Button>
            <div className="search-results">
              {results.map((item) => (
                <a key={item.id}>{item.title}</a>
              ))}
            </div>
          </Form>
          <Nav>
            <LinkContainer to="/cart">
              <Nav.Link as="div" role="button">
                Cart
              </Nav.Link>
            </LinkContainer>
            {"user" in cookies ? <UserNavBar /> : <GuestNavBar />}
          </Nav>
        </Navbar.Collapse>
      </Container>
    </Navbar>
  );
}
