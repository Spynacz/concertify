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

function SideBySide({ children }) {
  return <div className="side-by-side">{children}</div>;
}

function UserFormControl({ type, name, value, onChange }) {
  if (typeof onChange !== "undefined") {
    return (
      <div className="labeled">
        <Form.Label>{name.replace("_", " ")}</Form.Label>
        <Form.Control
          type={type}
          name={name}
          value={value}
          onChange={onChange}
        />
      </div>
    );
  } else {
    return (
      <div className="labeled">
        <Form.Label>{name.replace("_", " ")}</Form.Label>
        <Form.Control type={type} name={name} />
      </div>
    );
  }
}

export function UsernameField({ err, value, onChange }) {
  return (
    <>
      <UserFormControl
        type="text"
        name="username"
        value={value}
        onChange={onChange}
      />
      <ErrorField text={err} />
    </>
  );
}

export function EmailField({ err, value, onChange }) {
  return (
    <>
      <UserFormControl
        type="email"
        name="email"
        value={value}
        onChange={onChange}
      />
      <ErrorField text={err} />
    </>
  );
}

export function PasswordConfirmationInvalid(password1, password2) {
  return PasswordMismatch([password1, password2]) || PasswordInvalid(password1);
}

export function PasswordConfirmationField({ err }) {
  function changePassword(event) {
    setPassword(event.target.value);
  }

  function changePassword2(event) {
    setPassword2(event.target.value);
  }

  const [password, setPassword] = useState("");
  const [password2, setPassword2] = useState("");

  return (
    <>
      <UserFormControl
        type="password"
        name="password1"
        onChange={changePassword}
      />
      <PasswordInvalidText password={password} />
      <ErrorField text={err} />
      <UserFormControl
        type="password"
        name="password2"
        onChange={changePassword2}
      />
      <PasswordMismatchText passwords={[password, password2]} />
    </>
  );
}

export function PasswordOldField({ err }) {
  return (
    <>
      <UserFormControl type="password" name="old_password" />
      <ErrorField text={err} />
    </>
  );
}

export function PasswordField({ err }) {
  return (
    <>
      <UserFormControl type="password" name="password" />
      <ErrorField text={err} />
    </>
  );
}

export function NamesField({ values, onChanges }) {
  if (values && onChanges) {
    return (
      <SideBySide>
        <UserFormControl
          type="text"
          name="first_name"
          value={values.first}
          onChange={onChanges.first}
        />
        <UserFormControl
          type="text"
          name="last_name"
          value={values.last}
          onChange={onChanges.last}
        />
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

export function PaymentField({ values, onChanges, err }) {
  if (values && onChanges) {
    return (
      <>
        <UserFormControl
          type="text"
          name="line1"
          value={values.line1}
          onChange={onChanges.line1}
        />
        <ErrorField text={err.line1} />
        <UserFormControl
          type="text"
          name="line2"
          value={values.line2}
          onChange={onChanges.line2}
        />
        <ErrorField text={err.line2} />
        <UserFormControl
          type="text"
          name="city"
          value={values.city}
          onChange={onChanges.city}
        />
        <ErrorField text={err.city} />
        <SideBySide>
          <UserFormControl
            type="text"
            name="postal_code"
            value={values.postal_code}
            onChange={onChanges.postal_code}
          />
          <ErrorField text={err.postal_code} />
          <UserFormControl
            type="text"
            name="country"
            value={values.country}
            onChange={onChanges.country}
          />
          <ErrorField text={err.country} />
        </SideBySide>
        <SideBySide>
          <UserFormControl
            type="tel"
            name="telephone"
            value={values.telephone}
            onChange={onChanges.telephone}
          />
          <ErrorField text={err.telephone} />
          <UserFormControl
            type="tel"
            name="mobile"
            value={values.mobile}
            onChange={onChanges.mobile}
          />
          <ErrorField text={err.mobile} />
        </SideBySide>
      </>
    );
  } else {
    return (
      <>
        <UserFormControl type="text" name="line1" />
        <UserFormControl type="text" name="line2" />
        <UserFormControl type="text" name="city" />
        <SideBySide>
          <UserFormControl type="text" name="postal_code" />
          <UserFormControl type="text" name="country" />
        </SideBySide>
        <SideBySide>
          <UserFormControl type="tel" name="telephone" />
          <UserFormControl type="tel" name="mobile" />
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
