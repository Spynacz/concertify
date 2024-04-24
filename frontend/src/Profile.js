import "./Profile.css";
import { useCookies, Cookies } from "react-cookie";
import { Form } from "react-bootstrap";
import { nullToX } from "./Utils";
import React, { useState, useEffect } from "react";
import {
  UsernameField,
  EmailField,
  NamesField,
  SubmitButton,
  UserForm,
  PasswordConfirmationField,
  PaymentField,
} from "./UserForm";

export default function Profile() {
  const get = async () => {
    if (fetched) return;
    await fetch("http://localhost:8000/profile", {
      method: "GET",
      headers: {
        Authorization: "Token " + user.token,
      },
    })
      .then((response) => {
        if (!response.ok) throw new Error(response.status);
        return response.json();
      })
      .then((data) => {
        setUsername(data.username);
        setEmail(data.email);
        setNames({ first: data.first_name, last: data.last_name });
        const payment = nullToX(data.payment_info, "");
        setPayment({
          line1: payment.line1,
          line2: payment.line2,
          city: payment.city,
          postal_code: payment.postal_code,
          country: payment.country,
          telephone: payment.telephone,
          mobile: payment.mobile,
        });
        setFetched(true);
      })
      .catch((err) => {
        console.log(err.message);
      });
  };
  useEffect(() => {
    get();
  }, []);
  const [cookies, setCookie, removeCookie] = useCookies(["user"]);
  const user = cookies["user"];
  const [fetched, setFetched] = useState(false);
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [names, setNames] = useState({ first: "", last: "" });
  const nameChanges = {
    first: (e) => setNames({ ...names, first: e.target.value }),
    last: (e) => setNames({ ...names, last: e.target.value }),
  };
  const [payment, setPayment] = useState({
    line1: "",
    line2: "",
    city: "",
    postal_code: "",
    country: "",
    telephone: "",
    mobile: "",
  });
  const paymentChanges = {
    line1: (e) => setPayment({ ...payment, line1: e.target.value }),
    line2: (e) => setPayment({ ...payment, line2: e.target.value }),
    city: (e) => setPayment({ ...payment, city: e.target.value }),
    postal_code: (e) => setPayment({ ...payment, postal_code: e.target.value }),
    country: (e) => setPayment({ ...payment, country: e.target.value }),
    telephone: (e) => setPayment({ ...payment, telephone: e.target.value }),
    mobile: (e) => setPayment({ ...payment, mobile: e.target.value }),
  };
  return (
    <div className="profile-container">
      <UserForm>
        <h3>Change details:</h3>
        <UsernameField value={username} onChange={setUsername} />
        <EmailField value={email} onChange={setEmail} />
        <NamesField values={names} onChanges={nameChanges} />
        <SubmitButton value="Confirm" />
      </UserForm>
      <UserForm>
        <h3>Change Payment info:</h3>
        <PaymentField values={payment} onChanges={paymentChanges} />
        <SubmitButton value="Confirm" />
      </UserForm>
      <UserForm>
        <h3>Change password:</h3>
        <PasswordConfirmationField />
        <SubmitButton value="Confirm" />
      </UserForm>
    </div>
  );
}
