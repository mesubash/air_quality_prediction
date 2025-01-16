import React from "react";
import LiveAQI from "./components/LiveAQI";
import Forecast from "./components/Forecast";

function App() {
  return (
    <div>
      <h1>Air Quality Dashboard</h1>
      <LiveAQI />
      <Forecast />
    </div>
  );
}

export default App;
