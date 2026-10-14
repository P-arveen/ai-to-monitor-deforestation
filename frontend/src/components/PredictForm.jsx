import React, { useState } from "react";
import axios from "axios";

export default function PredictForm() {
  const [image, setImage] = useState(null);
  const [preview, setPreview] = useState(null);
  const [result, setResult] = useState("");
  const [percentages, setPercentages] = useState(null);

  const handleImageChange = (e) => {
    const file = e.target.files[0];
    setImage(file);
    setPercentages(null);
    setPreview(URL.createObjectURL(file));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!image) return;

    const formData = new FormData();
    formData.append("image", image);

    try {
      const response = await axios.post("http://127.0.0.1:5000/predict", formData);
      setResult(response.data);
      console.log("Prediction response:", response.data);
    } catch (error) {
      console.error("Prediction failed:", error);
      setResult("Error during prediction.");
    }
  };

  return (
    <div className=" w-1/2 mx-auto mt-20 bg-gray-100 p-6 flex flex-col items-center justify-center shadow-xl rounded-2xl">
      <h1 className="text-3xl font-bold mb-6 text-green-800">Deforestation Image Predictor</h1>

      <form onSubmit={handleSubmit} className="bg-white p-6 rounded-lg shadow-md w-full max-w-md flex flex-col gap-4">
        <input
          type="file"
          accept="image/*"
          onChange={handleImageChange}
          className="file-input file-input-bordered file-input-success w-full"
        />

        {preview && (
          <img
            src={preview}
            alt="Preview"
            className="h-48 object-cover rounded border border-gray-300"
          />
        )}

        <button
          type="submit"
          className="bg-green-600 hover:bg-green-700 text-white py-2 rounded font-semibold"
        >
          Predict
        </button>
      </form>

      {result && (
        <div className="mt-6 p-4 bg-white shadow-lg rounded text-xl text-center w-full max-w-md text-green-700 font-medium">
          <div className="flex flex-col items-center">
            <h2 className="text-2xl font-bold mb-4">Prediction Result</h2> 
            <h4>Prediction: {result.prediction} </h4> 
          
          <h4>Forested Area :{result.forest_percent}%</h4>
            <h4>Deforested Area :{result.deforest_percent}%</h4>
          </div>

         <>
         <div className="mt-4 text-sm text-gray-600">
            {result.prediction === "Deforested" ? (
              <span className="text-red-500">Warning: Deforestation detected!</span>
            ) : (
              <span className="text-green-500">No deforestation detected.</span>
            )}
          </div>
         </>
        </div>
      )}
    </div>
  );
};