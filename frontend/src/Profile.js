import "./Profile.css";
import { useCookies, Cookies } from "react-cookie";
import { Button, Collapse, Nav } from "react-bootstrap";
import { LinkContainer } from "react-router-bootstrap";
import { nullToX } from "./Utils";
import React, { useState, useEffect } from "react";
import { useNavigate, Outlet } from "react-router-dom";
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

function getData(cookies, setCookie, removeCookie) {
  const user = cookies["user"];
  fetch("http://localhost:8000/profile", {
    method: "GET",
    headers: {
      Authorization: "Token " + user.token,
    },
  })
    .then((response) => {
      if (!response.ok) throw response;
      return response.json();
    })
    .then((data) => {
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
    const patch = async () => {
      await fetch("http://localhost:8000/profile", {
        method: "PATCH",
        body: JSON.stringify({
          username: t.username.value,
          email: t.email.value,
          first_name: t.first_name.value,
          last_name: t.last_name.value,
        }),
        headers: {
          "Content-type": "application/json; charset=UTF-8",
          Authorization: "Token " + cookies["user"].token,
        },
      })
        .then((response) => {
          if (!response.ok) throw response;
          return response.json();
        })
        .then((data) => {
          console.log("Details updated");
          getData(cookies, setCookie, removeCookie);
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
    };
    event.preventDefault();
    const t = event.target;
    patch();
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
    const patch = async () => {
      await fetch("http://localhost:8000/profile", {
        method: "PATCH",
        body: JSON.stringify({
          payment_info: {
            line1: t.line1.value,
            line2: t.line2.value,
            city: t.city.value,
            postal_code: t.postal_code.value,
            country: t.country.value,
            telephone: t.telephone.value,
            mobile: t.mobile.value,
          },
        }),
        headers: {
          "Content-type": "application/json; charset=UTF-8",
          Authorization: "Token " + cookies["user"].token,
        },
      })
        .then((response) => {
          if (!response.ok) throw response;
          return response.json();
        })
        .then((data) => {
          getData(cookies, setCookie, removeCookie);
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
    };
    event.preventDefault();
    const t = event.target;
    patch();
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
    const del = async () => {
      await fetch("http://localhost:8000/profile", {
        method: "DELETE",
        headers: {
          "Content-type": "application/json; charset=UTF-8",
          Authorization: "Token " + cookies["user"].token,
        },
      })
        .then((response) => {
          if (!response.ok) throw response;
          removeCookie("user");
          navigate("/");
          console.log("Account Deleted");
        })
        .catch((err) => {
          console.log(err);
        });
    };
    event.preventDefault();
    del();
  }
  function handleSubmit(event) {
    const put = async () => {
      await fetch("http://localhost:8000/profile/password", {
        method: "PUT",
        body: JSON.stringify({
          old_password: t.old_password.value,
          password1: t.password1.value,
          password2: t.password2.value,
        }),
        headers: {
          "Content-type": "application/json; charset=UTF-8",
          Authorization: "Token " + cookies["user"].token,
        },
      })
        .then((response) => {
          if (!response.ok) throw response;
          return response.json();
        })
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
    };
    event.preventDefault();
    const t = event.target;
    if (PasswordConfirmationInvalid(t.password1.value, t.password2.value)) {
      return false;
    }
    put();
  }
  const [cookies, setCookie, removeCookie] = useCookies(["user"]);
  const navigate = useNavigate();
  const [err, setErr] = useState({
    old_password: "",
    password1: "",
    password2: "",
  });
  return (
    <>
      <UserForm onSubmit={handleSubmit}>
        <h3>Change password:</h3>
        <PasswordOldField err={err.old_password} />
        <PasswordConfirmationField err={err.password1} />
        <SubmitButton value="Confirm" />
      </UserForm>
      <Button className="red-button" onClick={handleDelete}>
        Delete Account
      </Button>
    </>
  );
}

export function Profile() {
  function get() {
    if (!user) {
      navigate("/");
    }
    if (fetched) return;
    getData(cookies, setCookie, removeCookie);
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
