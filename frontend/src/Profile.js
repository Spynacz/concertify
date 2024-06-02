import "./Profile.css";
import { useCookies, Cookies } from "react-cookie";
import { Button, Collapse, Nav } from "react-bootstrap";
import { LinkContainer } from "react-router-bootstrap";
import { nullToX } from "./Utils";
import React, { useState, useEffect } from "react";
import { useNavigate, Outlet } from "react-router-dom";
import {
  profileGet,
  profilePatch,
  profilePatchPayment,
  profileDelete,
  profilePut,
} from "./REST";
import {
  UsernameField,
  EmailField,
  NamesField,
  SubmitButton,
  UserForm,
  PasswordConfirmationField,
  PasswordConfirmationInvalid,
  PasswordOldField,
  PaymentField,
} from "./UserForm";

export function updateProfileData(cookies, setCookie, removeCookie) {
  const user = cookies["user"];
  profileGet(user.token).then((data) => {
    const payment = nullToX(data.payment_info, "");
    setCookie("user", {
      ...user,
      username: data.username,
      email: data.email,
      names: {
        first: data.first_name,
        last: data.last_name,
      },
      payment: {
        line1: payment.line1,
        line2: payment.line2,
        city: payment.city,
        postal_code: payment.postal_code,
        country: payment.country,
        telephone: payment.telephone,
        mobile: payment.mobile,
      },
    });
  });
}

export function ProfileDetails() {
  function handleSubmit(event) {
    event.preventDefault();
    const t = event.target;
    profilePatch(
      user.token,
      t.username.value,
      t.email.value,
      t.first_name.value,
      t.last_name.value,
    )
      .then((data) => {
        console.log("Details updated");
        updateProfileData(cookies, setCookie, removeCookie);
      })
      .catch((err) => {
        console.log(err);
        err.json().then((data) => {
          setErr({
            username: data.username,
            email: data.email,
          });
        });
      });
  }
  const [cookies, setCookie, removeCookie] = useCookies(["user"]);
  const user = cookies["user"];
  const [err, setErr] = useState({
    username: "",
    email: "",
  });
  return (
    <UserForm onSubmit={handleSubmit}>
      <h3>Change details:</h3>
      <UsernameField value={user.username} err={err.username} />
      <EmailField value={user.email} err={err.email} />
      <NamesField values={user.names} />
      <SubmitButton value="Confirm" />
    </UserForm>
  );
}

export function ProfilePayment() {
  function handleSubmit(event) {
    event.preventDefault();
    const t = event.target;
    profilePatchPayment(
      user.token,
      t.line1.value,
      t.line2.value,
      t.city.value,
      t.postal_code.value,
      t.country.value,
      t.telephone.value,
      t.mobile.value,
    )
      .then((data) => {
        updateProfileData(cookies, setCookie, removeCookie);
        console.log("Payment info updated");
      })
      .catch((err) => {
        err.json().then((data) => {
          setErr({
            line1: data.line1,
            line2: data.line2,
            city: data.city,
            postal_code: data.postal_code,
            country: data.country,
            telephone: data.telephone,
            mobile: data.mobile,
          });
        });
      });
  }
  const [cookies, setCookie, removeCookie] = useCookies(["user"]);
  const user = cookies["user"];
  const [err, setErr] = useState({
    line1: "",
    line2: "",
    city: "",
    postal_code: "",
    country: "",
    telephone: "",
    mobile: "",
  });
  return (
    <UserForm onSubmit={handleSubmit}>
      <h3>Change Payment info:</h3>
      <PaymentField values={user.payment} err={err} />
      <SubmitButton value="Confirm" />
    </UserForm>
  );
}

export function ProfileSecurity() {
  function handleDelete(event) {
    event.preventDefault();
    profileDelete(cookies["user"].token)
      .then((response) => {
        if (!response.ok) throw response;
        removeCookie("user");
        navigate("/");
        console.log("Account Deleted");
      })
      .catch((err) => {
        console.log(err);
      });
  }
  function handleSubmit(event) {
    event.preventDefault();
    const t = event.target;
    if (PasswordConfirmationInvalid(t.password1.value, t.password2.value)) {
      return false;
    }
    profilePut(
      cookies["user"].token,
      t.old_password.value,
      t.password1.value,
      t.password2.value,
    )
      .then((data) => {
        console.log("Password updated");
      })
      .catch((err) => {
        err.json().then((data) => {
          setErr({
            old_password: data.old_password,
            password1: data.password1,
            password2: data.password2,
          });
        });
      });
  }
  const [cookies, setCookie, removeCookie] = useCookies(["user"]);
  const navigate = useNavigate();
  const [err, setErr] = useState({
    old_password: "",
    password1: "",
    password2: "",
  });
  return (
    <div>
      <UserForm onSubmit={handleSubmit}>
        <h3>Change password:</h3>
        <PasswordOldField err={err.old_password} />
        <PasswordConfirmationField
          err={err.password1}
          labels={["New Password", "Repeat New Password"]}
        />
        <SubmitButton value="Confirm" />
      </UserForm>
      <h3>Advanced</h3>
      <br />
      <br />
      <Button className="red-button" onClick={handleDelete}>
        Delete Account
      </Button>
    </div>
  );
}

export function Profile() {
  function get() {
    if (!user) {
      navigate("/");
    }
    if (fetched) return;
    updateProfileData(cookies, setCookie, removeCookie);
    setFetched(true);
  }
  const navigate = useNavigate();
  const [subsite, setSubsite] = useState(0);
  const [cookies, setCookie, removeCookie] = useCookies(["user"]);
  const user = cookies["user"];
  const [fetched, setFetched] = useState(false);
  useEffect(() => {
    get();
  }, []);
  return (
    <div className="profile-container">
      <div className="profile-header">
        <img src="https://png.pngtree.com/png-vector/20190710/ourlarge/pngtree-business-user-profile-vector-png-image_1541960.jpg" />
        <div className="profile-username">{user.username}</div>
      </div>
      <div className="nav-container">
        <Nav
          variant="pills"
          className="flex-column"
          activeKey={subsite}
          onSelect={(key) => setSubsite(key)}
        >
          <Nav.Item>
            <LinkContainer to="details">
              <Nav.Link eventKey={0}>Details</Nav.Link>
            </LinkContainer>
          </Nav.Item>
          <Nav.Item>
            <LinkContainer to="payment">
              <Nav.Link eventKey={1}>Payment</Nav.Link>
            </LinkContainer>
          </Nav.Item>
          <Nav.Item>
            <LinkContainer to="security">
              <Nav.Link eventKey={2}>Security</Nav.Link>
            </LinkContainer>
          </Nav.Item>
        </Nav>
        <div className="form-container">
          <Outlet />
        </div>
      </div>
    </div>
  );
}
