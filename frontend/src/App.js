import React from "react";
import { CookiesProvider, useCookies } from "react-cookie";
import { Outlet, RouterProvider, createBrowserRouter } from "react-router-dom";
import "./App.css";
import NavBar from "./NavBar";
import Profile from "./Profile";
import ErrorPage from "./ErrorPage";
import { EventList } from "./Event";
import { Login, Register } from "./Login";

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
        path: "/profile",
        element: <Profile />,
      },
    ],
  },
]);

function Layout() {
  return (
    <>
      <NavBar />
      <div class="container">
        <Outlet />
      </div>
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
