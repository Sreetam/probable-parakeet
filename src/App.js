import React from "react";
import './App.css';
import News from "./news.js";
import Breaking from "./breaking.js";

const breaking = require("./data/breaking.json");

export default function App() {

  const { data } = breaking;

  return (
    <div className="container-fluid">
      <div>{Breaking(Object.values(data))}</div>
    </div>
  );
}