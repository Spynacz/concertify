import React from "react";
import { CookiesProvider, useCookies } from "react-cookie";
import {
  Outlet,
  RouterProvider,
  createBrowserRouter,
  Navigate,
} from "react-router-dom";
import "./App.css";
import NavBar from "./NavBar";
import {
  Profile,
  ProfileDetails,
  ProfilePayment,
  ProfileSecurity,
} from "./Profile";
import ErrorPage from "./ErrorPage";
import Cart from "./Cart";
import { Login, Register } from "./Login";
import EventList from "./event/EventList";
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
        path: "/cart",
        element: <Cart />,
      },
      {
        path: "/event/:id",
        element: <EventPage />,
      },
      {
        path: "/profile",
        element: <Profile />,
        children: [
          {
            index: true,
            element: <Navigate to="details" replace />,
          },
          {
            path: "details",
            element: <ProfileDetails />,
          },
          {
            path: "payment",
            element: <ProfilePayment />,
          },
          {
            path: "security",
            element: <ProfileSecurity />,
          },
        ],
      },
    ],
  },
]);

function Layout() {
  return (
    <>
      <NavBar />
      <div className="app-container">
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
