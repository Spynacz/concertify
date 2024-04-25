import React from "react";
import { Form } from "react-bootstrap";
import "./Login.css";
import { nullToX } from "./Utils";
import { useState } from "react";
import { useCookies } from "react-cookie";
import { useNavigate } from "react-router-dom";
import {
  PasswordConfirmationField,
  PasswordField,
  PasswordConfirmationInvalid,
  UsernameField,
  EmailField,
  NamesField,
  ErrorField,
  SubmitButton,
  UserForm,
} from "./UserForm";

function ErrorMsg({ text }) {
  if (text != []) return text.map((msg) => <Form.Text>{msg}</Form.Text>);
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
        removeCookie("user");
        console.log("Logout successful");
      })
      .catch((err) => {
        console.log(err.message);
      });
  };
  const [cookies, setCookie, removeCookie] = useCookies(["user"]);
  const user = cookies["user"];
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
          if (!response.ok) throw response;
          return response.json();
        })
        .then((data) => {
          console.log("Login successful");
          const newUser = {
            username: data.user.username,
            token: data.token,
          };
          setCookie("user", newUser);
          navigate("/");
        })
        .catch((err) => {
          err.json().then((data) => {
            const newdata = nullToX(data, []);
            setUsernameMsg(newdata.username);
            setPassMsg(newdata.password);
            setGlobalMsg(newdata.non_field_errors);
          });
        });
    };
    event.preventDefault();
    const t = event.target;
    login();
  }
  const [cookies, setCookie, removeCookie] = useCookies(["user"]);
  const [usernameMsg, setUsernameMsg] = useState([]);
  const [passMsg, setPassMsg] = useState([]);
  const [globalMsg, setGlobalMsg] = useState([]);
  const navigate = useNavigate();
  return (
    <div className="login-form-container">
      <UserForm className="login-form" onSubmit={handleSubmit}>
        <span className="accent-button">Concertify</span>
        <ErrorField text={globalMsg} />
        <UsernameField err={usernameMsg} />
        <PasswordField err={passMsg} />
        <SubmitButton value="Login" />
      </UserForm>
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
          password: t.password1.value,
          payment_info: {},
        }),
        headers: { "Content-type": "application/json; charset=UTF-8" },
      })
        .then((response) => {
          if (!response.ok) throw response;
          return response.json();
        })
        .then((data) => {
          console.log("Registration successful");
          navigate("/login");
        })
        .catch((err) => {
          return err.json().then((data) => {
            const newdata = nullToX(data, []);
            setEmailMsg(newdata.email);
            setUsernameMsg(newdata.username);
            setPassMsg(newdata.password);
            setGlobalMsg(newdata.non_field_errors);
          });
        });
    };
    event.preventDefault();
    const t = event.target;
    if (PasswordConfirmationInvalid(t.password1.value, t.password2.value)) {
      return false;
    }
    create();
  }

  const [usernameMsg, setUsernameMsg] = useState([]);
  const [emailMsg, setEmailMsg] = useState([]);
  const [passMsg, setPassMsg] = useState([]);
  const [globalMsg, setGlobalMsg] = useState([]);
  const navigate = useNavigate();
  return (
    <div className="login-form-container">
      <UserForm className="login-form" onSubmit={handleSubmit}>
        <span className="accent-button">Concertify</span>
        <ErrorField text={globalMsg} />
        <UsernameField err={usernameMsg} />
        <EmailField err={emailMsg} />
        <PasswordConfirmationField err={passMsg} />
        <NamesField />
        <SubmitButton value="Register" />
      </UserForm>
    </div>
  );
}
