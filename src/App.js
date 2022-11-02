// import React, { Component } from "react";
// import Container from 'react-bootstrap/Container';
// import Nav from 'react-bootstrap/Nav';
// import Navbar from 'react-bootstrap/Navbar';
// import NavDropdown from 'react-bootstrap/NavDropdown';
import React from "react";
import News from "./news.js"
const breaking = require("./data/breaking.json");

export default function App() {
  const { data } = breaking;
  return (
    <div className="container">
      {Object.values(data).map((val) => (
        <div>{News(val)}</div>
      ))}
    </div>
  );
}