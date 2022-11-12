import React, { useEffect, useReducer } from "react";
import News from "./news.js"

// const breaking = require("./data/breaking.json");

// const reducer = (val, action) => {
//   switch(action) {
//     case 1:
//       // return [val.shift(), ...val];
//       return val;
//     default:
//       return val;
//   }
// }
export default function Breaking(content) {

  // const { data } = breaking;
  // const [content, setNews] = useReducer(reducer, Object.values(data));
  // console.log(content[0]);

  // setNews(1);

  // useEffect(() => {
  //   const intervalRef = setInterval(() => {
  //     setNews(1);
  //   }, 1000);

  //   return () => {
  //     clearInterval(intervalRef);
  //   }
  // },[]);

  return (
    <div className="row">
      <div className="col-3">
        {content.slice(0,4).map((val) => (
          <div>{News(val)}</div>
        ))}
      </div>
      <div className="col-3">
        {content.slice(5,9).map((val) => (
          <div>{News(val)}</div>
        ))}
      </div>
      <div className="col-3">
        {content.slice(10,14).map((val) => (
          <div>{News(val)}</div>
        ))}
      </div>
    </div>
  );
}