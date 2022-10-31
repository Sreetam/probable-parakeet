<<<<<<< node
import React, { Component } from "react";
const breaking = require("./data/breaking.json");

export default function App() {
  const { data } = breaking;

  return (
    <div className="App">
      {Object.values(data).map((val) => (
        <p>{val[2]}</p>
      ))}
    </div>
  );
}
=======