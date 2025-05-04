
import React from 'react'
import { useState, useEffect } from "react"
import { useNavigate } from 'react-router-dom'
import "./styles/font.css"
import "./styles/back-btn.css"
import "./styles/query.css"

const Query=()=>{
    const [inputText, setInputText]=useState("")
    const [sidebarOpen, setSidebarOpen]=useState(false)
    const [dbStatus, setStatus]=useState(false)
    const [visualization, setVisual]=useState(false)
    const [analysis, setAnalysis]=useState(false)


    const navigate=useNavigate()

    const handleChange = (event) => {
		setInputText(event.target.value)
	}

    const handleSubmit = async(event) => {
		event.preventDefault()
		console.log("Submitted:", inputText)


        try{

            // const res = await fetch("http://127.0.0.1:5001/data-source/db-status")
            // const data = await res.json()

            // if (data.status === "connected") {
            //     setStatus(true)
            //     console.log("db found")
            // } else {
            //     setStatus(false)
            //     alert("You are NOT connected to a database.")
            //     return // prevent going further
            // }
            
            const dbStatus=await fetch("http://127.0.0.1:5001/data-source/db-status", {
                    method: "GET"
                })
                .then(res=>res.json())
                .then(data=>{
                    if(data.status==="connected"){
                        setStatus(true) // db status
                        console.log("db found")

                    }else {
                        setStatus(false);
                        alert(`You are NOT connected to a database. Please make a connection to your database`)
                        return
                    }
                })
            } 
        catch(err){
            console.error(err)
        }

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
        }
	}

    const toggleSidebar=()=>{
        setSidebarOpen(!sidebarOpen)
    }

    const getStateAttr=async(event)=>{
        const response= await fetch("http://127.0.0.1:5001/query/query-output", {
            method: "GET",
            headers: {
                "Content-Type": "application/json"
            }
        })
        
        const data= await response.json();
        if(data.error){
            console.error("Server error:", data.error)
            alert(`Something went wrong: ${data.error}`)
        }else{
            console.log(data)
        }
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
        if (visualization) {
            fetch("http://127.0.0.1:5001/query/generated-analysis")
                .then(res => res.text())
                .then(text => setAnalysis(text))
                .catch(err => console.error("Failed to fetch analysis:", err))
        }
    }, [visualization])


    return (
        <div className={`container ${sidebarOpen ? 'shrinked' : ''}`}>
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

                        <p>{analysis}</p>

                    </div>
                )}
            </div>


            <div className={`sidebar ${sidebarOpen ? 'open' : ''}`}>
                <h2>Sidebar</h2>
                <p>Extra tools or settings</p>

                <h2>Execution Flow Graph</h2>
                        <img
                            src="http://127.0.0.1:5001/query/generated-graph"
                            alt="Agents Workflow"
                            style={{
                                width: '100%',
                                maxHeight: '500px',
                                objectFit: 'contain',
                                marginTop: '20px',
                                border: '1px solid #ccc',
                                borderRadius: '8px'
                            }}
                        />

                <div className='side-btn-div'>
                    <button className='side-btn-open' id='select-graph-btn'>Select Graphs/Charts</button>
                    <button className='side-btn-open' id='llm-details-btn'>View LLM Details</button>
                    <button onClick={getStateAttr} className='side-btn-open' id='output-details-btn'>View Output</button>
                </div>

            </div>
		</div>
	)
}

export default Query;