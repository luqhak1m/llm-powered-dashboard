
import React from 'react'
import { useState, useEffect } from "react"
import { useNavigate } from 'react-router-dom'
import "./styles/font.css"
import "./styles/back-btn.css"
import "./styles/query.css"
import ReactMarkdown from 'react-markdown'
import StateOutput from './Query-Output';
import LLMOutput from './Query-LLM';
import DBOutput from './Query-DB';
import ToolSelector from './Query-Tools'


const Query=()=>{
    const [inputText, setInputText]=useState("")
    const [sidebarOpen, setSidebarOpen]=useState(false)
    const [visualization, setVisual]=useState(false)
    const [analysis, setAnalysis]=useState(false)
    const [analysisText, setAnalysisText]=useState("")


    const [showStateOutput, setShowStateOutput] = useState(false);
    const [stateOutputContent, setStateOutputContent] = useState(null);

    const [showLLMOutput, setShowLLMOutput] = useState(false);
    const [LLMOutputContent, setLLMOutputContent] = useState(null);

    const [showDBOutput, setShowDBOutput] = useState(false);
    const [DBOutputContent, setDBOutputContent] = useState(null);

    const [showToolSelector, setShowToolSelector] = useState(false);


    const navigate=useNavigate()

    const handleChange = (event) => {
		setInputText(event.target.value)
	}

    const handleSubmit = async(event) => {
		event.preventDefault()
		console.log("Submitted:", inputText)
        setVisual(false)
        setAnalysis(false)

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
            
                if (!response.ok) throw new Error(`HTTP ${response.status}`)
            
                const data = await response.json()
                if (data.status === "success"){
                    setVisual(true)
                    setAnalysis(true)
                    console.log("backend (/query-input) return success")
                }
                    
                else throw new Error("Backend responded with failure status")
            } catch (err) {
                console.error("Error submitting query:", err)
                alert(err)
            }
        }
	}

    const toggleSidebar=()=>{
        setSidebarOpen(!sidebarOpen)
    }

    const getStateAttr=async(event)=>{
        const response= await fetch("http://127.0.0.1:5001/query/state-details", {
            method: "GET",
            headers: {
                "Content-Type": "application/json"
            }
        })
        
        const data= await response.json();
        setStateOutputContent(data);
        setShowToolSelector(false);
        setShowStateOutput(true);
        setShowLLMOutput(false);
        setShowDBOutput(false);

        if(data.error){
            console.error("Server error:", data.error)
            alert(`Something went wrong: ${data.error}`)
        }else{
            console.log(data)
        }
        event.preventDefault()
    }

    const getLLMAttr=async(event)=>{
        const response= await fetch("http://127.0.0.1:5001/query/llm-details", {
            method: "GET",
            headers: {
                "Content-Type": "application/json"
            }
        })
        
        const data= await response.json();
        setLLMOutputContent(data);
        setShowToolSelector(false);
        setShowLLMOutput(true);
        setShowStateOutput(false);
        setShowDBOutput(false);

        if(data.error){
            console.error("Server error:", data.error)
            alert(`Something went wrong: ${data.error}`)
        }else{
            console.log(data)
        }
        event.preventDefault()
    }

    const getDBAttr=async(event)=>{
        const response= await fetch("http://127.0.0.1:5001/query/db-details", {
            method: "GET",
            headers: {
                "Content-Type": "application/json"
            }
        })
        
        const data= await response.json();
        setDBOutputContent(data);
        setShowToolSelector(false);
        setShowDBOutput(true);
        setShowStateOutput(false);
        setShowLLMOutput(false);

        if(data.error){
            console.error("Server error:", data.error)
            alert(`Something went wrong: ${data.error}`)
        }else{
            console.log(data)
        }
        event.preventDefault()
    }

    const getToolSelector=async(event)=>{

        setShowToolSelector(true);
        setShowDBOutput(false);
        setShowStateOutput(false);
        setShowLLMOutput(false);

        event.preventDefault()
    }

    const handleIframeError = () => {
        console.log("Failed to load the visualization iframe.")
        alert("Failed to load the visualization. Please try again later.")
    }

    const handleIframeLoad = (event) => {
        alert("Visualization Success!")
    }

    useEffect(() => {
        if (analysis) {
            fetch("http://127.0.0.1:5001/query/generated-analysis")
                .then(res => res.text())
                .then(text => setAnalysisText(text))
                .catch(err => console.error("Failed to fetch analysis:", err))
        }
    }, [analysis])


    return (
        <div className={`container ${sidebarOpen ? 'shrinked' : ''}`}>
            <div className="wrapper">
                {showStateOutput ? (
                    <StateOutput output={stateOutputContent} onClose={() => setShowStateOutput(false)}/>
                ) : showLLMOutput ? (
                    <LLMOutput output={LLMOutputContent} onClose={() => setShowLLMOutput(false)}/>
                ) : showDBOutput ? (
                    <DBOutput output={DBOutputContent} onClose={() => setShowDBOutput(false)}/>
                ) : showToolSelector ? (
                    <ToolSelector token={localStorage.getItem("token")} onClose={() => setShowToolSelector(false)}/>                ) : (


                    <>
                        <div className='back-parent'>
                            <div className='back-div'>
                                <button className="back-btn" onClick={() => navigate("/mainmenu")}>
                                    ⬅
                                </button>
                            </div>
                            <div className='title-ul'>
                                <h1>Enter Your Query</h1>
                            </div>
                            <div className='sidebar-parent'>
                                <button className="sidebar-btn" onClick={toggleSidebar}>
                                    ☰
                                </button>
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

                        {visualization===true &&(
                            <div className='result-div'>
                        
                                <h2>Visual</h2>
                        
                                <iframe
                                    src="http://127.0.0.1:5001/query/generated-visual"                        
                                    title="Visualization"
                                    onLoad={handleIframeLoad}
                                    onError={handleIframeError}
                                    style={{
                                        width: '100%',
                                        height: '600px',
                                        border: 'none',
                                        marginTop: '20px',
                                    }}
                                ></iframe>
                        
                                <h2>Analysis</h2>
                        
                                <div className='analysis-div'>
                        
                                <ReactMarkdown>{analysisText}</ReactMarkdown>
                        
                                </div>

                                <button
                                    onClick={async () => {
                                        try {
                                            const token = localStorage.getItem("token")
                                            const res = await fetch("http://127.0.0.1:5001/query/save-visual", {
                                                method: "POST",
                                                headers: {
                                                    Authorization: `Bearer ${token}`,
                                                    "Content-Type": "application/json"
                                                }
                                            })
                                            const data = await res.json()
                                            alert(data.message)
                                        } catch (err) {
                                            console.error("Failed to save:", err)
                                            alert("Error saving visual and analysis")
                                        }
                                    }}
                                >
                                    Save Visual and Analysis
                                </button>
                        
                        
                            </div>
                        )}
                    </>

                )}

                <div className={`sidebar ${sidebarOpen ? 'open' : ''}`}>
                    <div className='side-btn-div'>
                        <button onClick={getToolSelector} className='side-btn-open' id='select-graph-btn'>Select Graphs/Charts</button>
                        <button onClick={getDBAttr} className='side-btn-open' id='db-details-btn'>View Database Details</button>
                        <button onClick={getLLMAttr} className='side-btn-open' id='llm-details-btn'>View LLM Details</button>
                        <button onClick={getStateAttr} className='side-btn-open' id='output-details-btn'>View State Output</button>
                    </div>

                </div>
		    </div>
        </div>
	)
}

export default Query;