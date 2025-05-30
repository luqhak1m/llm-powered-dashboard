import React, { useEffect, useState } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import ReactMarkdown from 'react-markdown';
import "./styles/font.css"
import "./styles/back-btn.css"
import "./styles/query.css"
import "./styles/output.css"

const VisualOutput = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const [analysisText, setAnalysisText] = useState("");
  const [stateOutputContent, setStateOutputContent] = useState(null);



  useEffect(() => {
    fetch("http://127.0.0.1:5001/query/generated-analysis")
      .then(res => res.text())
      .then(text => setAnalysisText(text))
      .catch(err => console.error("Failed to fetch analysis:", err));
  }, []);

//   const handleIframeLoad = () => alert("Visualization Success!");
//   const handleIframeError = () => alert("Failed to load the visualization.");

  const saveVisual = async () => {
    try {
      const token = localStorage.getItem("token");
      const res = await fetch("http://127.0.0.1:5001/query/save-visual", {
        method: "POST",
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json",
        },
      });
      const data = await res.json();
      alert(data.message);
    } catch (err) {
      console.error("Failed to save:", err);
      alert("Error saving visual and analysis");
    }
  };

  const getStateAttr = async () => {
    try {
        const response = await fetch("http://127.0.0.1:5001/query/state-details", {
        method: "GET",
        headers: {
            "Content-Type": "application/json"
        }
        });

        const data = await response.json();

        if (data.error) {
        console.error("Server error:", data.error);
        alert(`Something went wrong: ${data.error}`);
        return null;
        } else {
        console.log(data);
        return data;
        }
    } catch (err) {
        console.error("Failed to fetch state details:", err);
        alert("Could not retrieve state output.");
        return null;
    }
    };


    const handleViewStateOutput = async () => {
        const stateData = await getStateAttr();
        if (stateData) {
        navigate("/state-output", { state: { stateData } });
        }
    };

  return (
        <div className='container'>
            <div className='wrapper'>
                <div className='back-parent'>
                        <div className='back-div'>
                            <button
                                className="back-btn"
                                onClick={() => {
                                    const confirmLeave = window.confirm(
                                        "Are you sure you want to go back?\n\nIf you go back, the visual and analysis will be lost.\n\nIf you wish to see this again, please save before going back."
                                    );
                                    if (confirmLeave) {
                                        navigate("/query");
                                    }
                                }}
                            >
                                ⬅
                            </button>
                        </div>
                        <div className='title-ul'>
                            <h1>Result</h1>
                        </div>
                    </div>


                <h2>Visualization</h2>
                <iframe
                    src="http://127.0.0.1:5001/query/generated-visual"
                    title="Visualization"
                    // onLoad={handleIframeLoad}
                    // onError={handleIframeError}
                    style={{
                    width: '100%',
                    height: '600px',
                    border: 'none',
                    }}
                ></iframe>

                <h2>Analysis</h2>
                <div className="analysis-box">
                <ReactMarkdown>{analysisText}</ReactMarkdown>
                </div>


                    <div className="visual-button-group">
                        <button className="visual-btn" onClick={saveVisual}>Save Visual and Analysis</button>
                        <button className="visual-btn" onClick={handleViewStateOutput}>View State Output</button>
                    </div>
                </div>
            </div>
  );
};

export default VisualOutput;
