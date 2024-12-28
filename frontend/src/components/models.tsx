"use client"
import React, { useState } from "react";

const ModelSelectionForm: React.FC = () => {
  const [selectedModel, setSelectedModel] = useState<string>("model_1");

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();

    try {
      const response = await fetch("http://localhost:5000/process", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ model: selectedModel }),
      });
      

      if (response.ok) {
        const data = await response.json();
        alert("Model selected and processing started: " + data.message);
      } else {
        console.error("Failed to process the request.");
        alert("Error processing request.");
      }
    } catch (error) {
      console.error("Error:", error);
      alert("An error occurred.");
    }
  };

  return (
    <form onSubmit={handleSubmit} className="flex flex-col space-y-4">
      <label htmlFor="model" className="font-semibold">
        Select Model:
      </label>
      <select
        name="model"
        id="model"
        value={selectedModel}
        onChange={(e) => setSelectedModel(e.target.value)}
        className="p-2 border rounded"
      >
        <option value="model_1">Model 1</option>
        <option value="model_2">Model 2</option>
        <option value="model_3">Model 3</option>
      </select>
      <button
        type="submit"
        className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
      >
        Start Classification
      </button>
    </form>
  );
};

export default ModelSelectionForm;
