import { Form, Button } from "react-bootstrap";
import "./UserForm.css";
import React, { useState } from "react";

export function ErrorField({ text }) {
  if (text !== [] && text !== undefined && text !== "")
    return text.map((msg) => <Form.Text>{msg}</Form.Text>);
}

function PasswordMismatch(passwords) {
  if (passwords[0].length == 0 || passwords[1].length == 0) return false;
  if (passwords[0] === passwords[1]) return false;
  return true;
}

function PasswordShort(password) {
  if (password.length < 8 && password.length > 0) return true;
  return false;
}

function PasswordNumeric(password) {
  if (password.length == 0) return false;
  if (!isNaN(password)) return true;

  return false;
}

function PasswordInvalid(password) {
  return PasswordNumeric(password) || PasswordShort(password);
}

function PasswordMismatchText({ passwords }) {
  if (PasswordMismatch(passwords))
    return <Form.Text>Passwords do not match</Form.Text>;

  return null;
}

function PasswordInvalidText({ password }) {
  function LengthCheck({ password }) {
    if (PasswordShort(password))
      return <Form.Text>Password too short</Form.Text>;

    return null;
  }

  function NumericCheck({ password }) {
    if (PasswordNumeric(password))
      return <Form.Text>Password numeric</Form.Text>;

    return null;
  }

  return (
    <>
      <LengthCheck password={password} />
      <NumericCheck password={password} />
    </>
  );
}

function EmailInvalidText({ email }) {
  if (EmailInvalid(email)) return <Form.Text>Email Invalid</Form.Text>;
}

function SideBySide({ children }) {
  return <div className="side-by-side">{children}</div>;
}

function UserFormControl({ type, name, value, label, onChange }) {
  return (
    <div className="labeled">
      <Form.Label>{label ? label : name.replace("_", " ")}</Form.Label>
      <Form.Control
        type={type}
        name={name}
        defaultValue={value}
        onChange={onChange}
      />
    </div>
  );
}

export function UsernameField({ err, value, label }) {
  return (
    <>
      <UserFormControl
        type="text"
        name="username"
        value={value}
        label={label}
      />
      <ErrorField text={err} />
    </>
  );
}

export function EmailField({ err, value, label }) {
  const [email, setEmail] = useState("");
  return (
    <>
      <UserFormControl
        type="email"
        name="email"
        value={value}
        label={label}
        onChange={() => setEmail(event.target.value)}
      />
      <EmailInvalidText email={email} />
      <ErrorField text={err} />
    </>
  );
}

export function EmailInvalid(email) {
  return email !== "" && !/.+@.+\..+/.test(email);
}

export function PasswordConfirmationInvalid(password1, password2) {
  return PasswordMismatch([password1, password2]) || PasswordInvalid(password1);
}

export function PasswordConfirmationField({ err, labels }) {
  const [password, setPassword] = useState("");
  const [password2, setPassword2] = useState("");

  if (labels) {
    return (
      <>
        <UserFormControl
          type="password"
          name="password1"
          onChange={() => setPassword(event.target.value)}
          label={labels[0]}
        />
        <PasswordInvalidText password={password} />
        <ErrorField text={err} />
        <UserFormControl
          type="password"
          name="password2"
          onChange={() => setPassword2(event.target.value)}
          label={labels[1]}
        />
        <PasswordMismatchText passwords={[password, password2]} />
      </>
    );
  } else {
    return (
      <>
        <UserFormControl
          type="password"
          name="password1"
          onChange={() => setPassword(event.target.value)}
        />
        <PasswordInvalidText password={password} />
        <ErrorField text={err} />
        <UserFormControl
          type="password"
          name="password2"
          onChange={() => setPassword2(event.target.value)}
        />
        <PasswordMismatchText passwords={[password, password2]} />
      </>
    );
  }
}

export function PasswordOldField({ err }) {
  return (
    <>
      <UserFormControl type="password" name="old_password" />
      <ErrorField text={err} />
    </>
  );
}

export function PasswordField({ err, label }) {
  return (
    <>
      <UserFormControl type="password" name="password" label={label} />
      <ErrorField text={err} />
    </>
  );
}

export function NamesField({ values }) {
  if (values) {
    return (
      <SideBySide>
        <UserFormControl type="text" name="first_name" value={values.first} />
        <UserFormControl type="text" name="last_name" value={values.last} />
      </SideBySide>
    );
  } else {
    return (
      <SideBySide>
        <UserFormControl type="text" name="first_name" />
        <UserFormControl type="text" name="last_name" />
      </SideBySide>
    );
  }
}

export function SubmitButton({ value }) {
  return (
    <Button className="accent-button" type="submit">
      {value}
    </Button>
  );
}

export function PaymentField({ values, err }) {
  if (values) {
    return (
      <>
        <UserFormControl type="text" name="line1" value={values.line1} />
        <ErrorField text={err.line1} />
        <UserFormControl type="text" name="line2" value={values.line2} />
        <ErrorField text={err.line2} />
        <UserFormControl type="text" name="city" value={values.city} />
        <ErrorField text={err.city} />
        <SideBySide>
          <UserFormControl
            type="text"
            name="postal_code"
            value={values.postal_code}
          />
          <ErrorField text={err.postal_code} />
          <UserFormControl type="text" name="country" value={values.country} />
          <ErrorField text={err.country} />
        </SideBySide>
        <SideBySide>
          <UserFormControl
            type="tel"
            name="telephone"
            value={values.telephone}
          />
          <ErrorField text={err.telephone} />
          <UserFormControl type="tel" name="mobile" value={values.mobile} />
          <ErrorField text={err.mobile} />
        </SideBySide>
      </>
    );
  } else {
    return (
      <>
        <UserFormControl type="text" name="line1" />
        <ErrorField text={err.line1} />
        <UserFormControl type="text" name="line2" />
        <ErrorField text={err.line2} />
        <UserFormControl type="text" name="city" />
        <ErrorField text={err.city} />
        <SideBySide>
          <UserFormControl type="text" name="postal_code" />
          <ErrorField text={err.postal_code} />
          <UserFormControl type="text" name="country" />
          <ErrorField text={err.country} />
        </SideBySide>
        <SideBySide>
          <UserFormControl type="tel" name="telephone" />
          <ErrorField text={err.telephone} />
          <UserFormControl type="tel" name="mobile" />
          <ErrorField text={err.mobile} />
        </SideBySide>
      </>
    );
  }
}

export function UserForm({ children, className, onSubmit }) {
  return (
    <Form
      className={"userform" + (className ? " " + className : "")}
      onSubmit={onSubmit}
    >
      {children}
    </Form>
  );
}
