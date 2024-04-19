import React from "react";
import { Form, Button } from "react-bootstrap";
import "./Login.css";
import { useState } from "react";
import { useCookies } from "react-cookie";
import { useNavigate } from "react-router-dom";

function RegisterPasswordMismatch(passwords) {
  if (passwords[0].length == 0 || passwords[1].length == 0)
    return false;
  if (passwords[0] === passwords[1])
    return false;

  return true;
}

function RegisterPasswordShort(password) {
  if (password.length < 8 && password.length > 0)
    return true;

  return false;
}

function RegisterPasswordNumeric(password) {
  if (password.length == 0)
    return false;
  if (!isNaN(password))
    return true;

  return false;
}

function RegisterPasswordInvalid(password) {
  return RegisterPasswordNumeric(password) || RegisterPasswordShort(password);
}

function PasswordMismatchText({ passwords }) {
  if (RegisterPasswordMismatch(passwords))
    return <Form.Text>Passwords do not match</Form.Text>;

  return null;
}

function PasswordInvalidText({ password }) {
  function LengthCheck({ password }) {
    if (RegisterPasswordShort(password))
      return <Form.Text>Password too short</Form.Text>;

    return null;
  }

  function NumericCheck({ password }) {
    if (RegisterPasswordNumeric(password))
      return <Form.Text>Password numeric</Form.Text>;

    return null;
  }

  return (
    <>
      <LengthCheck password={password} />
      <NumericCheck password={password} />
    </>
  );
}

function RegisterPassword() {
  function changePassword(event) {
    setPassword(event.target.value);
  }

  function changePassword2(event) {
    setPassword2(event.target.value);
  }

  const [password, setPassword] = useState("");
  const [password2, setPassword2] = useState("");

  return (
    <>
      <Form.Control
        type="password"
        name="password"
        placeholder="password"
        onChange={changePassword}
      />
      <PasswordInvalidText password={password} />
      <Form.Control
        type="password"
        name="password2"
        placeholder="password"
        onChange={changePassword2}
      />
      <PasswordMismatchText passwords={[password, password2]} />
    </>
  );
}

export function Logout() {
  const logout = async () => {
    console.log(user.token);
    await fetch("http://localhost:8000/logout", {
      method: "POST",
      headers: {
        Authorization: "Token " + user.token,
      },
    })
      .then((response) => {
        if (!response.ok) throw new Error(response.status);
        removeCookie('user');
        setUser(null);
        console.log("Logout successful");
      })
      .catch((err) => {
        console.log(err.message);
      });
  }
  const [ cookies, setCookie, removeCookie ] = useCookies(['user']);
  const user = cookies['user'];
  return <div onClick={logout}>Logout</div>;
}

export function Login() {
  function handleSubmit(event) {
    const login = async () => {
      await fetch("http://localhost:8000/login", {
        method: "POST",
        body: JSON.stringify({
          username: t.username.value,
          password: t.password.value,
        }),
        headers: { "Content-type": "application/json; charset=UTF-8" },
      })
        .then((response) => {
          if (response.status === 400) {
            console.log("Invalid username/password");
          } else if (response.status == 403) {
            console.log("Probably token limit");
          }
          if (!response.ok) throw new Error(response.status);
          return response.json();
        })
        .then((data) => {
          console.log("Login successful");
          console.log(data);
          const newUser = {
            username: data.user.username,
            token: data.token
          };
          setCookie('user', newUser);
          navigate('/');
        })
        .catch((err) => {
          console.log(err.message);
        });
    };
    event.preventDefault();
    const t = event.target;
    login();
  }
  const [ cookies, setCookie, removeCookie ] = useCookies(['user']);
  const navigate = useNavigate();
  return (
    <div className="login-form-container">
      <Form className="login-form" onSubmit={handleSubmit}>
        <span className="accent-button">Concertify</span>
        <Form.Control type="text" name="username" placeholder="login" />
        <Form.Control type="password" name="password" placeholder="password" />
        <Button className="accent-button" type="submit">
          Login
        </Button>
      </Form>
    </div>
  );
}

export function Register() {
  function handleSubmit(event) {
    const create = async () => {
      await fetch("http://localhost:8000/create", {
        method: "POST",
        body: JSON.stringify({
          username: t.username.value,
          email: t.email.value,
          first_name: t.first_name.value,
          last_name: t.last_name.value,
          password: t.password.value,
          payment_info: {},
        }),
        headers: { "Content-type": "application/json; charset=UTF-8" },
      })
        .then((response) => {
          if (response.status === 400) {
            console.log("Username/Email taken");
          }
          if (!response.ok) throw new Error(response.status);
          return response.json();
        })
        .then((data) => {
          console.log("Registration successful");
          navigate("/login");
        })
        .catch((err) => {
          console.log(err.message);
        });
    };
    event.preventDefault();
    const t = event.target;
    if (
      RegisterPasswordMismatch([t.password.value, t.password2.value]) ||
      RegisterPasswordInvalid(t.password.value)
    ) {
      return false;
    }
    create();
  }

  const navigate = useNavigate();
  return (
    <div className="login-form-container">
      <Form className="login-form" onSubmit={handleSubmit}>
        <span className="accent-button">Concertify</span>
        <Form.Control type="text" name="username" placeholder="username" />
        <Form.Control type="email" name="email" placeholder="email" />
        <RegisterPassword />
        <div className="personal-info-container">
          <Form.Control
            type="text"
            name="first_name"
            placeholder="first name"
          />
          <Form.Control type="text" name="last_name" placeholder="last name" />
        </div>
        <Button className="accent-button" type="submit">
          Register
        </Button>
      </Form>
    </div>
  );
}
