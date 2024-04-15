import React from "react";
import { Form, Button } from "react-bootstrap";
import "./Login.css";

export function Login() {
  return (
    <div className="login-form-container">
      <Form className="login-form">
        <span className="accent-button">Concertify</span>
        <Form.Control type="text" placeholder="login"/>
        <Form.Control type="password" placeholder="password"/>
        <Button className="accent-button" type="submit">
          Login
        </Button>
      </Form>
    </div>
  );
}

export function Register() {
  return (
    <div className="login-form-container">
      <Form className="login-form">
        <span className="accent-button">Concertify</span>
        <Form.Control type="text" placeholder="username"/>
        <Form.Control type="email" placeholder="email"/>
        <Form.Control type="password" placeholder="password"/>
        <Form.Control type="password" placeholder="password"/>
        <div className="personal-info-container">
          <Form.Control type="text" placeholder="first name"/>
          <Form.Control type="text" placeholder="last name"/>
        </div>
        <Button className="accent-button" type="submit">
          Login
        </Button>
      </Form>
    </div>
  );
}
