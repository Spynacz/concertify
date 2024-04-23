import React from "react";
import "./App.css";
import NavBar from "./NavBar";
import { EventList } from "./Event";
import { RouterProvider, createBrowserRouter, Outlet } from "react-router-dom";
import { useState } from "react";
import { useCookies, CookiesProvider } from "react-cookie";
import { Login, Register } from "./Login";

const router = createBrowserRouter([
  {
    element: <Layout />,
    children: [
      {
        path: "/",
        element: <Home />,
      },
      {
        path: "/login",
        element: <Login />,
      },
      {
        path: "/register",
        element: <Register />,
      },
    ],
  },
]);

function Layout() {
  return (
    <>
      <NavBar />
      <Outlet />
    </>
  );
}

export default function App() {
  const [cookies, setCookie, removeCookie] = useCookies([]);
  return (
    <CookiesProvider defaultSetOptions={{ path: "/" }}>
      <div>
        <RouterProvider router={router} />
      </div>
    </CookiesProvider>
  );
}

export function Home() {
  return <EventList count={25} />;
}
