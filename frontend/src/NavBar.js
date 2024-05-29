import { useEffect, useState } from "react";
import { Container, Form, Nav, Navbar } from "react-bootstrap";
import { useCookies } from "react-cookie";
import { LinkContainer } from "react-router-bootstrap";
import { Link, useNavigate } from "react-router-dom";
import { Logout } from "./Login.js";
import "./NavBar.css";

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
  const [selected, setSelected] = useState(-1);
  const navigate = useNavigate();

  const fetchSearch = async () => {
    await fetch(`http://localhost:8000/event?search=${query}`, {
      method: "GET",
    })
      .then((response) => {
        if (!response.ok) throw new Error(response.status);
        return response.json();
      })
      .then((data) => {
        setResults(data.results);
      })
      .catch((err) => {
        console.log(err.message);
      });
  };

  const handleKeyDown = (e) => {
    if (e.key === "ArrowDown") {
      setSelected((prev) => (prev + 1).mod(results.length));
    } else if (e.key === "ArrowUp") {
      setSelected((prev) => (prev - 1).mod(results.length));
    } else if (e.key === "Enter") {
      navigate("/event/" + results[selected].id);
    }
  };

  useEffect(() => {
    if (query !== "") {
      fetchSearch();
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
          <div className="search-container">
            <Form className="d-flex position-relative">
              <Form.Control
                type="text"
                placeholder="Search"
                className="me-2"
                onChange={(e) => setQuery(e.target.value)}
                onKeyDown={handleKeyDown}
                value={query}
              />
            </Form>
            <div className="search-results">
              {results.map((item, index) => (
                <Link
                  reloadDocument
                  to={"/event/" + item.id}
                  onClick={() => setResults([])}
                  key={index}
                  className={selected === index ? "result selected" : "result"}
                >
                  <img
                    className="rounded"
                    src="https://weknowyourdreams.com/images/party/party-12.jpg"
                  />
                  <p>{item.title}</p>
                </Link>
              ))}
            </div>
          </div>
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
