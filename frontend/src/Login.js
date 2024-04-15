import React from "react";
import "./Login.css";

export function Login() {
  return (
    <div className="login-form-container">
      <form className="login-form">
        <span>Concertify</span>
        <input type="text" placeholder="login"/>
        <input type="password" placeholder="password"/>
        <input type="submit" value="Login"/>
      </form>
    </div>
  );
}

export function Register() {
  return (
    <div className="login-form-container">
      <form className="login-form">
        <span>Concertify</span>
        <input type="text" placeholder="login"/>
        <input type="email" placeholder="email"/>
        <input type="password" placeholder="password"/>
        <input type="password" placeholder="password"/>
        <input type="submit" value="Login"/>
      </form>
    </div>
  );
}
