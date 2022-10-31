import React, { Component } from "react";
const breaking = require("./data/breaking.json");

export default function App() {
  const { data } = breaking;

  return (
    <div className="App">
      {Object.values(data).map((val) => (
        <div>
          <h4>{val[0]} : {val[2]}</h4>
          <p>{val[3]}</p>
        </div>
      ))}
    </div>
  );
}