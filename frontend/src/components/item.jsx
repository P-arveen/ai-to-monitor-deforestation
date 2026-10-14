import React from 'react'
import { useState } from "react";

const item = () => {
  const [year, setYear] = useState(2023);
  const [imageUrl, setImageUrl] = useState("");
  const [metadata, setMetadata] = useState(null);
  const [availableYears, setAvailableYears] = useState([]);

  const fetchImage = async () => {
    const response = await fetch(`http://127.0.0.1:5000/get-image?year=${year}`);
    if (response.ok) {
      setImageUrl(response.url);
    } else {
      alert("Failed to fetch image");
    }
  };
  const allfetchImage = async () => {
    const response = await fetch(`http://127.0.0.1:5000/getimage`);
    if (response.ok) {
      setImageUrl(response.url);
    } else {
      alert("Failed to fetch image");
    }
  };

  const fetchMetadata = async () => {
    const response = await fetch(`http://127.0.0.1:5000/get-metadata?year=${year}`);
    const data = await response.json();
    setMetadata(data);
  };

  const fetchAvailableYears = async () => {
    const response = await fetch(`http://127.0.0.1:5000/get-available-years`);
    const data = await response.json();
    setAvailableYears(data.years);
  };

  return ( 
    <div className="p-4 text-black w-full h-full">
      <h1 className="text-xl font-bold mb-4">Amazon Rainforest Satellite Image</h1>
      
      <div className="mb-4">
        <label className="mr-2">Select Year:</label>
        <select value={year} onChange={(e) => setYear(e.target.value)} className="border p-2 rounded">
          {availableYears.map((y) => (
            <option key={y} value={y}>{y}</option>
          ))}
        </select>
        <button onClick={fetchAvailableYears} className="ml-2 bg-gray-500 text-white p-2 rounded">
          Load Years
        </button>
      </div>

      <button onClick={fetchImage} className="bg-blue-500 text-white p-2 rounded mr-2">
        Get Image
      </button>
      <button onClick={fetchMetadata} className="bg-green-500 text-white p-2 rounded">
        Get Metadata
      </button>

      {imageUrl && (
        <div className="mt-4">
          <img src={imageUrl} alt={`Amazon Rainforest ${year}`} className="w-full rounded shadow" />
        </div>
      )}

      {metadata && (
        <div className="mt-4 bg-gray-100 p-4 rounded">
          <h2 className="text-lg font-bold">Metadata</h2>
          <p>Year: {metadata.year}</p>
          <p>Dataset: {metadata.data_collection}</p>
          <p>Cloud Coverage: {metadata.cloud_coverage}</p>
          <p>Resolution: {metadata.resolution}</p>
        </div>
      )}
    </div>
  );
};

export default item;
