import "./Profile.css";
import { useCookies, Cookies } from "react-cookie";
import { Form } from "react-bootstrap";
import { nullToX } from "./Utils";
import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import {
  UsernameField,
  EmailField,
  NamesField,
  SubmitButton,
  UserForm,
  PasswordConfirmationField,
  PaymentField,
} from "./UserForm";

function Details({ values, onChanges }) {
  return (
    <UserForm>
      <h3>Change details:</h3>
      <UsernameField value={values.username} onChange={onChanges.username} />
      <EmailField value={values.email} onChange={onChanges.email} />
      <NamesField values={values.names} onChanges={onChanges.names} />
      <SubmitButton value="Confirm" />
    </UserForm>
  );
}

function Payment({ values, onChanges }) {
  return (
    <UserForm>
      <h3>Change Payment info:</h3>
      <PaymentField values={values} onChanges={onChanges} />
      <SubmitButton value="Confirm" />
    </UserForm>
  );
}

function Password() {
  return (
    <UserForm>
      <h3>Change password:</h3>
      <PasswordConfirmationField />
      <SubmitButton value="Confirm" />
    </UserForm>
  );
}

export default function Profile() {
  const get = async () => {
    if (fetched) return;
    if (!user) {
      navigate("/login");
      return;
    }
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
        setDetails({
          username: data.username,
          email: data.email,
          names: {
            first: data.first_name,
            last: data.last_name,
          },
        });
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
  const navigate = useNavigate();
  useEffect(() => {
    get();
  }, []);
  const [cookies, setCookie, removeCookie] = useCookies(["user"]);
  const user = cookies["user"];
  const [fetched, setFetched] = useState(false);
  const [details, setDetails] = useState({
    username: "",
    email: "",
    names: {
      first: "",
      last: "",
    },
  });
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
  const detailChanges = {
    username: (e) => setDetails({ ...details, username: e.target.value }),
    email: (e) => setDetails({ ...details, email: e.target.value }),
    names: {
      first: (e) =>
        setDetails({ ...details, names: { ...names, first: e.target.value } }),
      last: (e) =>
        setDetails({ ...details, names: { ...names, last: e.target.value } }),
    },
  };
  return (
    <div className="profile-container">
      <Details values={details} onChanges={detailChanges} />
      <Payment values={payment} onChanges={paymentChanges} />
      <Password />
    </div>
  );
}
