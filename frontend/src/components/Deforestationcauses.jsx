import React, { useState } from "react";
import { ChevronDown, ChevronUp } from "lucide-react";

const causes = [
  {
    title: "Agricultural Expansion 🐄🌾",
    details:
      "Cattle ranching accounts for 80% of Amazon deforestation. Soy farming also contributes significantly, as soy is used for livestock feed globally.",
  },
  {
    title: "Logging (Illegal & Legal) 🪵🚜",
    details:
      "Selective and illegal logging lead to habitat destruction, soil erosion, and ecosystem fragmentation, harming biodiversity.",
  },
  {
    title: "Infrastructure Development 🏗️🚧",
    details:
      "Roads like the BR-163 Highway open up untouched forests to illegal land grabbing, leading to further deforestation and environmental damage.",
  },
  {
    title: "Mining & Extractive Industries ⛏️🥇",
    details:
      "Gold mining releases toxic mercury into rivers, and large-scale mining operations clear thousands of hectares of forest.",
  },
  {
    title: "Climate Change & Forest Fires 🌡️🔥",
    details:
      "Rising temperatures and extreme droughts increase the risk of wildfires, reducing the Amazon's ability to absorb carbon dioxide.",
  },
];

function Deforestationcauses() {
  const [openIndex, setOpenIndex] = useState(null);

  const toggleSection = (index) => {
    setOpenIndex(openIndex === index ? null : index);
  };

  return (
    <div className="mt-20 w-full mx-auto p-6 bg-white rounded-xl shadow-lg">
      <h2 className="text-2xl font-bold text-green-700 text-center mb-4">
        Causes of Deforestation
      </h2>
      <div>
        {causes.map((cause, index) => (
          <div key={index} className="mb-4 border-b pb-2">
            <button
              onClick={() => toggleSection(index)}
              className="flex justify-between w-full text-left text-lg font-semibold text-gray-800 hover:text-green-600"
            >
              {cause.title}
              {openIndex === index ? <ChevronUp /> : <ChevronDown />}
            </button>
            {openIndex === index && (
              <p className="mt-2 text-gray-600">{cause.details}</p>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}

export default Deforestationcauses;