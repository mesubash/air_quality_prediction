//Forecast visualization
import React, { useState, useEffect } from "react";
import axios from "axios";

function Forecast() {
  const [forecastData, setForecastData] = useState(null);

  useEffect(() => {
    axios.get("http://127.0.0.1:5000/forecast")
      .then(response => setForecastData(response.data))
      .catch(error => console.log(error));
  }, []);

  return (
    <div>
      <h2>Forecast AQI</h2>
      <pre>{JSON.stringify(forecastData, null, 2)}</pre>
    </div>
  );
}

export default Forecast;
