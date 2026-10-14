import React, { useEffect, useState } from "react";

const TemperatureComparison = () => {
  const [data, setData] = useState(null);

  useEffect(() => {
    fetch("http://localhost:5000/temperature-india")
      .then((res) => res.json())
      .then(setData)
      .catch((err) => console.error("Failed to fetch temperature data", err));
  }, []);

  if (!data) {
    return <div className="text-center mt-10 text-gray-500">Loading data...</div>;
  }

  return (
    <div className="max-w-xl mx-auto mt-10 p-6 rounded-2xl shadow-lg bg-white">
      <h2 className="text-2xl font-bold text-center mb-4 text-blue-700">
       In India Temperature Comparison
      </h2>

      <div className="grid grid-cols-2 gap-6 text-center text-lg">
        <div className="bg-blue-100 rounded-xl p-4">
          <h3 className="font-semibold">2023 Average</h3>
          <p className="text-2xl text-blue-700 font-bold">{data.avg_2023}°C</p>
        </div>
        <div className="bg-red-100 rounded-xl p-4">
          <h3 className="font-semibold">2024 Average</h3>
          <p className="text-2xl text-red-600 font-bold">{data.avg_2024}°C</p>
        </div>
      </div>

      <div className="mt-6 text-center">
        <p className="text-xl font-medium">
          🌡️ Temperature Change:
          <span
            className={`ml-2 font-bold ${
              data.change > 0 ? "text-red-600" : "text-blue-600"
            }`}
          >
            {data.change > 0 ? "+" : ""}
            {data.change}°C {data.change > 0 ? "🔺" : "🔻"}
          </span>
        </p>
      </div>
    </div>
  );
};

export default TemperatureComparison;
