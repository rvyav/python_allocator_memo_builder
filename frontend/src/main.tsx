import React from "react";
import ReactDOM from "react-dom/client";

import { Provider } from "react-redux";

import {
  BrowserRouter,
  Routes,
  Route,
} from "react-router-dom";

import App from "./App";
import Result from "./pages/Result";

import { store } from "./store/store";

ReactDOM.createRoot(
  document.getElementById("root")!
).render(
  <React.StrictMode>
    <Provider store={store}>
      <BrowserRouter>
        <Routes>
          <Route
            path="/"
            element={<App />}
          />

          <Route
            path="/result"
            element={<Result />}
          />
        </Routes>
      </BrowserRouter>
    </Provider>
  </React.StrictMode>
);