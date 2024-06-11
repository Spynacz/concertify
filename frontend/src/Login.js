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
  EmailInvalid,
  NamesField,
  ErrorField,
  SubmitButton,
  UserForm,
} from "./UserForm";

function ErrorMsg({ text }) {
  if (text != []) return text.map((msg) => <Form.Text>{msg}</Form.Text>);
}

export function Logout() {
  const [cookies, setCookie, removeCookie] = useCookies(["user", "cart"]);
  const navigate = useNavigate();
  const user = cookies["user"];

  function logout() {
    logoutPost(user.token)
      .then((response) => {
        if (!response.ok) console.error(response.status);
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

  return <div onClick={logout}>Logout</div>;
}

export function Login() {
  const [cookies, setCookie, removeCookie] = useCookies(["user"]);
  const [usernameMsg, setUsernameMsg] = useState([]);
  const [passMsg, setPassMsg] = useState([]);
  const [globalMsg, setGlobalMsg] = useState([]);
  const navigate = useNavigate();

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
        const expiry = new Date(data.expiry);
        setCookie("user", newUser, { expires: expiry, sameSite: "strict" });
        removeCookie("cart");
        navigate("/");
      })
      .catch((err) => {
        if (err.json) {
          err.json().then((data) => {
            const newdata = nullToX(data, []);
            setUsernameMsg(newdata.username);
            setPassMsg(newdata.password);
            setGlobalMsg(newdata.non_field_errors);
          });
        }
      });
  }

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
  const [usernameMsg, setUsernameMsg] = useState([]);
  const [emailMsg, setEmailMsg] = useState([]);
  const [passMsg, setPassMsg] = useState([]);
  const [globalMsg, setGlobalMsg] = useState([]);
  const navigate = useNavigate();

  function handleSubmit(event) {
    event.preventDefault();
    const t = event.target;
    if (
      PasswordConfirmationInvalid(t.password1.value, t.password2.value) ||
      EmailInvalid(t.email.value)
    ) {
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
