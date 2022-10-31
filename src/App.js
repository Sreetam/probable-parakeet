// App.js
import { useEffect, useState } from "react";
import "./App.css";

function App() {
  const [data, setData] = useState([]);

  const fetchData = () => {
    fetch(`./data/breaking.json`)
      .then((response) => response.json())
      .then((actualData) => {
        console.log(actualData);
        setData(actualData.products);
        console.log(data);
      })
      .catch((err) => {
        console.log(err.message);
      });
  };

  useEffect(() => {
    fetchData();
  }, []);

  return (
    <div className="App">
      {<tbody>
        <tr>
          <th>Date</th>
          <th>Title</th>
          <th>Description</th>
        </tr>
        {data.map((item) => (
          <tr>
            <td>{item.pubDate}</td>
            <td>{item.title}</td>
            <td>{item.description}</td>
          </tr>
        ))}
      </tbody>}
    </div>
  );
}

export default App;