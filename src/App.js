import "./App.css";
import title from "./data/breaking.json";

export default function App() {
    const { data } = title
    return (
    <div className="App">
      {data}
    </div>
  );
}