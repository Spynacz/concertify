import React from "react";
import { CookiesProvider, useCookies } from "react-cookie";
import { Outlet, RouterProvider, createBrowserRouter } from "react-router-dom";
import "./App.css";
import ErrorPage from "./ErrorPage";
import EventList from "./event/EventList";
import { Login, Register } from "./Login";
import NavBar from "./NavBar";
import EventPage from "./event/EventPage";

const router = createBrowserRouter([
  {
    path: "/",
    element: <Layout />,
    errorElement: <ErrorPage />,
    children: [
      {
        path: "",
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
      {
        path: "/event/:id",
        element: <EventPage />
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
