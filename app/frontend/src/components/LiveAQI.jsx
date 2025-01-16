//Live AQI data

import React, { useState, useEffect } from "react";
import axios from "axios";

function LiveAQI() {
  const [aqiData, setAqiData] = useState(null);

  useEffect(() => {
    axios.get("http://127.0.0.1:5000/live_aqi")
      .then(response => setAqiData(response.data))
      .catch(error => console.log(error));
  }, []);

  return (
    <div>
      <h2>Live AQI Data</h2>
      <pre>{JSON.stringify(aqiData, null, 2)}</pre>
    </div>
  );
}

export default LiveAQI;