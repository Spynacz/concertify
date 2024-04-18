import "bootstrap/dist/css/bootstrap.css";
import React from "react";
import { createRoot } from "react-dom/client";
import { RouterProvider, createBrowserRouter } from "react-router-dom";
import App from "./App.js";

const router = createBrowserRouter([
  {
    path: "/",
    element: <App />,
  },
]);

const root = createRoot(document.getElementById("root"));
root.render(
  <React.StrictMode>
    <RouterProvider router={router} />
  </React.StrictMode>,
);
