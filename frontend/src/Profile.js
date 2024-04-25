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

export function ProfileDetails() {
  function handleSubmit(event) {
    const patch = async () => {
      await fetch("http://localhost:8000/profile", {
        method: "PATCH",
        body: JSON.stringify({
          username: user.username,
          email: user.email,
          first_name: user.names.first,
          last_name: user.names.last,
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
        })
        .catch((err) => {
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
  const onChanges = {
    username: (e) => setCookie("user", { ...user, username: e.target.value }),
    email: (e) => setCookie("user", { ...user, email: e.target.value }),
    names: {
      first: (e) =>
        setCookie("user", {
          ...user,
          names: { ...names, first: e.target.value },
        }),
      last: (e) =>
        setCookie("user", {
          ...user,
          names: { ...names, last: e.target.value },
        }),
    },
  };
  const [err, setErr] = useState({
    username: "",
    email: "",
  });
  return (
    <UserForm onSubmit={handleSubmit}>
      <h3>Change details:</h3>
      <UsernameField
        value={user.username}
        onChange={onChanges.username}
        err={err.username}
      />
      <EmailField
        value={user.email}
        onChange={onChanges.email}
        err={err.email}
      />
      <NamesField values={user.names} onChanges={onChanges.names} />
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
            line1: user.payment.line1,
            line2: user.payment.line2,
            city: user.payment.city,
            postal_code: user.payment.postal_code,
            country: user.payment.country,
            telephone: user.payment.telephone,
            mobile: user.payment.mobile,
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
  const [open, setOpen] = useState(false);
  const onChanges = {
    line1: (e) =>
      setCookie("user", {
        ...user,
        payment: { ...user.payment, line1: e.target.value },
      }),
    line2: (e) =>
      setCookie("user", {
        ...user,
        payment: { ...user.payment, line2: e.target.value },
      }),
    city: (e) =>
      setCookie("user", {
        ...user,
        payment: { ...user.payment, city: e.target.value },
      }),
    postal_code: (e) =>
      setCookie("user", {
        ...user,
        payment: { ...user.payment, postal_code: e.target.value },
      }),
    country: (e) =>
      setCookie("user", {
        ...user,
        payment: { ...user.payment, country: e.target.value },
      }),
    telephone: (e) =>
      setCookie("user", {
        ...user,
        payment: { ...user.payment, telephone: e.target.value },
      }),
    mobile: (e) =>
      setCookie("user", {
        ...user,
        payment: { ...user.payment, mobile: e.target.value },
      }),
  };
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
      <PaymentField values={user.payment} onChanges={onChanges} err={err} />
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
  const [subsite, setSubsite] = useState(0);
  const [cookies, setCookie, removeCookie] = useCookies(["user"]);
  const user = cookies["user"];
  const [fetched, setFetched] = useState(false);
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
