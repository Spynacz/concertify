import React from "react";
import "./App.css";
import { Login, Register } from "./Login"
import NavBar from "./NavBar";
import { EventList } from "./Event";
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";

export default function App() {
  return (
    <Router>
      <NavBar isGuest={true} />
      <Routes>
        <Route path="/" exact element={<Home/>}/>
        <Route path="/login" element={<Login/>}/>
        <Route path="/register" element={<Register/>}/>
      </Routes>
    </Router>
  );
}

function Home() {
  return (
    <EventList count={25} />
  );
}
