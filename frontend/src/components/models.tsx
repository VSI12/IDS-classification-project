"use client";

import React from "react";

const ModelSelectionForm: React.FC = () => {
  const handleModelSelect = async (model: string) => {
    try {
      const response = await fetch("http://localhost:5000/process", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ model }),
      });

      if (response.ok) {
        alert(`Model "${model}" submitted successfully!`);
      } else {
        alert(`Error submitting model: ${response.statusText}`);
      }
    } catch (error) {
      alert(`Error connecting to the server: ${error}`);
    }
  };

  return (
    <div style={{ textAlign: "center", padding: "20px" }}>
      <h2>Select a Model for Classification</h2>
      <div style={{ display: "flex", justifyContent: "center", gap: "20px", marginTop: "20px" }}>
        <button
          onClick={() => handleModelSelect("model_1")}
          style={buttonStyle}
        >
          Model 1
        </button>
        <button
          onClick={() => handleModelSelect("model_2")}
          style={buttonStyle}
        >
          Model 2
        </button>
        <button
          onClick={() => handleModelSelect("model_3")}
          style={buttonStyle}
        >
          Model 3
        </button>
      </div>
    </div>
  );
};

const buttonStyle = {
  padding: "15px 30px",
  fontSize: "18px",
  backgroundColor: "#007BFF",
  color: "white",
  border: "none",
  borderRadius: "5px",
  cursor: "pointer",
  textAlign: "center" as "center",
  boxShadow: "0 4px 6px rgba(0, 0, 0, 0.1)",
};

export default ModelSelectionForm;
