
import { useState } from "react"
import { useNavigate } from 'react-router-dom'
import "./styles/font.css"
import "./styles/back-btn.css"
import "./styles/query.css"

import LLMOutput from './Query-LLM';
import DBOutput from './Query-DB';
import ToolSelector from './Query-Tools'


const Query=()=>{
    const [inputText, setInputText]=useState("")
    const [showLLMOutput, setShowLLMOutput] = useState(false);
    const [LLMOutputContent, setLLMOutputContent] = useState(null);
    const [showDBOutput, setShowDBOutput] = useState(false);
    const [DBOutputContent, setDBOutputContent] = useState(null);
    const [showToolSelector, setShowToolSelector] = useState(false);

    const [isLoading, setIsLoading] = useState(false);



    const navigate=useNavigate()

    const handleChange = (event) => {
		setInputText(event.target.value)
	}

    const handleSubmit = async(event) => {
		event.preventDefault()
        setIsLoading(true); // show loading screen

		console.log("Submitted:", inputText)

        let dbConnection=false;
        try{
            
            const dbStatus=await fetch("http://127.0.0.1:5001/data-source/db-status", {
                    method: "GET"
                })
                .then(res=>res.json())
                .then(data=>{
                    if(data.status==="connected"){
                        dbConnection=true // db status
                        console.log("db found")

                    }else {
                        dbConnection=false;
                        alert(`You are NOT connected to a database. Please make a connection to your database`)
                        setIsLoading(false);
                        return
                    }
                })
            } 
        catch(err){
            console.error(err)
            alert(err)
        }

        console.log(dbConnection);

        if(dbConnection===true){
            try {
                const response = await fetch("http://127.0.0.1:5001/query/query-input", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({ question: inputText })
                })
    
                
                const data = await response.json()


                if (!response.ok){
                    if (data.error && Array.isArray(data.error)) {
                        alert("Errors:\n" + data.error.join("\n"));
                    } else if (typeof data.error === "string") {
                        alert("Error:\n" + data.error);
                    } else {
                        alert(`Unknown error occurred (HTTP ${response.status})`);
                    }
                    return;
                }


                if (data.status === "success"){
                    console.log("backend (/query-input) return success")
                    navigate("/visual-output",  { state: { inputText } })
                }else throw new Error("Backend responded with failure status")
            } catch (err) {
                console.error("Error submitting query:", err)
                alert(err.message)
            } finally{
                setIsLoading(false);
            }
        }
	}

const getToolSelector = async () => {
    const shouldShow = !showToolSelector;
    setShowToolSelector(shouldShow);
};

const getDBAttr = async () => {
    const shouldShow = !showDBOutput;
    setShowDBOutput(shouldShow);

    if (shouldShow && !DBOutputContent) {
        const response = await fetch("http://127.0.0.1:5001/query/db-details", {
            method: "GET",
            headers: { "Content-Type": "application/json" }
        });
        const data = await response.json();
        setDBOutputContent(data);
        if (data.error) {
            console.error("Server error:", data.error);
            alert(`Something went wrong: ${data.error}`);
        }
    }
};

const getLLMAttr = async () => {
    const shouldShow = !showLLMOutput;
    setShowLLMOutput(shouldShow);

    if (shouldShow && !LLMOutputContent) {
        const response = await fetch("http://127.0.0.1:5001/query/llm-details", {
            method: "GET",
            headers: { "Content-Type": "application/json" }
        });
        const data = await response.json();
        setLLMOutputContent(data);
        if (data.error) {
            console.error("Server error:", data.error);
            alert(`Something went wrong: ${data.error}`);
        }
    }
};


    return (
        <div className="container">
            {isLoading && (
                <div className="loading-overlay">
                    <div className="spinner"></div>
                    <p>Processing your query...</p>
                </div>
            )}
            <div className="wrapper">
                <div className='back-parent'>
                    <div className='back-div'>
                        <button className="back-btn" onClick={() => navigate("/mainmenu")}>
                            ⬅
                        </button>
                    </div>
                    <div className='title-ul'>
                        <h1>Enter Your Query</h1>
                    </div>
                </div>
                <form onSubmit={handleSubmit}>
                    <div className="row">
                        <textarea
                            placeholder="Create a graph for ..."
                            value={inputText}
                            onChange={handleChange}
                            required
                        />
                    </div>

                    <div className="row button">
                        <input type="submit" value="Submit" />
                    </div>

                </form>

                <div className="dropdowns">
                    <button onClick={getToolSelector}>Choose Tools</button>
                    {showToolSelector && (
                        <ToolSelector token={localStorage.getItem("token")} onClose={() => setShowToolSelector(false)} />
                    )}

                    <button onClick={getDBAttr}>DB Details</button>
                    {showDBOutput && (
                        <DBOutput output={DBOutputContent} onClose={() => setShowDBOutput(false)} />
                    )}

                    <button onClick={getLLMAttr}>LLM Details</button>
                    {showLLMOutput && (
                        <LLMOutput output={LLMOutputContent} onClose={() => setShowLLMOutput(false)} />
                    )}
                </div>
        </div>
    </div>
	)
}

export default Query;