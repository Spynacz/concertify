import React from "react";
import { Form } from "react-bootstrap";
import "./Login.css";
import { nullToX } from "./Utils";
import { useState } from "react";
import { useCookies } from "react-cookie";
import { useNavigate } from "react-router-dom";
import { logoutPost, loginPost, registerPost } from "./REST";
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
  function logout() {
    logoutPost(user.token)
      .then((response) => {
        removeCookie("user");
        removeCookie("cart");
        navigate("/");
      })
      .catch((err) => {
        removeCookie("user");
        removeCookie("cart");
        navigate("/");
      });
  }
  const [cookies, setCookie, removeCookie] = useCookies(["user", "cart"]);
  const navigate = useNavigate();
  const user = cookies["user"];
  return <div onClick={logout}>Logout</div>;
}

export function Login() {
  function handleSubmit(event) {
    event.preventDefault();
    const t = event.target;
    loginPost(t.username.value, t.password.value)
      .then((data) => {
        console.log("Login successful");
        const newUser = {
          username: data.user.username,
          token: data.token,
        };
        setCookie("user", newUser);
        removeCookie("cart");
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
    event.preventDefault();
    const t = event.target;
    if (PasswordConfirmationInvalid(t.password1.value, t.password2.value)) {
      return false;
    }
    registerPost(
      t.username.value,
      t.password1.value,
      t.email.value,
      t.first_name.value,
      t.last_name.value,
    )
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
