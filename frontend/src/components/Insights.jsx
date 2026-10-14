import React, { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'

const Insights = () => {

  const navigate = useNavigate()
  const [images, setImages] = useState([]);
  const [ndviImg, setNdviImg] = useState("");
  const [heatmap, setheatmap] = useState([]);

  useEffect(() => {

    fetch("http://127.0.0.1:5000/images") // Fetch image list from Flask
      .then((res) => {
        console.log("Response Status:", res.status); // Log response status
        return res.json();
      })
      .then((data) => {
        console.log("Fetched Data:", data); // Log received data
        setImages(data.images);
      })
      .catch((error) => console.error("Error fetching images:", error));

      setNdviImg("http://127.0.0.1:5000/ndvi_trend"); // Flask endpoint

      fetch("http://127.0.0.1:5000/heatmaps") // Fetch image list from Flask
      .then((res) => {
        console.log("Response Status:", res.status); // Log response status
        return res.json();
      })
      .then((data) => {
        console.log("Fetched Data:", data); // Log received data
        setheatmap(data.heatmaps);
      })
      .catch((error) => console.error("Error fetching images:", error));
  }, []);


  return (
    <div className='w-full h-full'>
      <div className="header">
        <i onClick={() => navigate(-1)} className=" text-2xl text-green-700 ri-arrow-left-line"></i>
      </div>
      <div className="section1 w-full h-full flex flex-col items-center justify-center">
        <h1 className="text-3xl font-bold text-green-700">Insights</h1>
        <div className='w-full h-full flex flex-col items-center justify-center mt-10'>
          <h1 className="text-2xl text-gray-600 py-10">Amazon Rain Forest Satellite images from years 2015 - 2024</h1>
          <div className="w-full h-full flex flex-wrap  justify-center">

            {images.map((image, index) => (
              <div key={index} className="flex flex-col items-center justify-center m-1">
                <img src={image.url} alt={image.name} className="w-[200px]" />
                <h1 className="text-l  text-green-700">{image.name}</h1>

              </div>
            ))
            }

          </div>

          <div className='w-full h-full flex flex-col items-center justify-center mt-10'>
            <h2 className='text-gray-700 text-2xl mt-30'>NDVI Trend (2015-2024) to Monitor Deforestation Trends</h2>
            {ndviImg ? <img src={ndviImg} alt="NDVI Trend" className='w-[70%]' /> : <p>Loading NDVI Trend...</p>}
          </div>

          <div>
            <ol className="text-gray-500 text-lg mt-10 list-decimal">
              <p className='text-green-800 text-2xl m-5'>NDVI (Normalized Difference Vegetation Index) values range from -1 to 1.</p>
              <li>2015-2016: NDVI is above 0.6, indicating a healthy forest.</li>
              <li>2017-2018: Sharp decline to near 0.0, suggesting massive deforestation.</li>
              <li>2019-2021: Gradual recovery, NDVI increases, showing some reforestation efforts.</li>
              <li>2022-2024: Fluctuations, but NDVI remains below 0.3, indicating that the forest has not fully recovered.</li>
            </ol>
          </div>


          <div className="heatmap w-full h-full  mt-20">
            <h3 className='text-2xl text-gray-700'>Heatmap Images </h3>
            <h5 className='text-l text-gray-500'>2015 and 2024 to get the Difference</h5>
            <div className='w-full h-full flex flex-wrap justify-center items-center mt-20'> 
              {heatmap.map((image, index) => (
                <div key={index} className="flex flex-col items-center justify-center m-1">
                  <img src={image.url} alt={image.name} className="w-[80%]" />
                  <h1 className="text-l  text-green-700">{image.name}</h1>

                </div>
              ))
              }
            </div>
          </div>
        </div>


      </div>
    </div>
  )
}

export default Insights
