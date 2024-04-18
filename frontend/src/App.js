import React from "react";
import "./App.css"
import NavBar from "./NavBar";
import { EventList } from "./Event";
import { RouterProvider, createBrowserRouter, Outlet } from "react-router-dom";
import { useState } from "react";
import { Login, Register } from "./Login"

export const UserContext = React.createContext(null);

const router = createBrowserRouter([
  {
    element: <Layout/>,
    children: [
      {
        path: "/",
        element: <Home/>,
      },
      {
        path: "/login",
        element: <Login/>,
      },
      {
        path: "/register",
        element: <Register/>,
      }
    ]
  }
]);

function Layout() {
  return (
    <>
      <UserContext.Provider value={{ user: user, setUser: setUser }}>
        <NavBar/>
        <Outlet/>
      </UserContext.Provider>
    </>
  );
}

export default function App() {
  const [user, setUser] = useState(null);
  return (
    <RouterProvider router={router}/>
  );
}

export function Home() {
  return (
    <EventList count={25} />
  );
}
