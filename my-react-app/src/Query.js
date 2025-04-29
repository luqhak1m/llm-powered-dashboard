
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
    const navigate=useNavigate()

    const handleChange = (event) => {
		setInputText(event.target.value)
	}

    const handleSubmit = async(event) => {
		event.preventDefault()
		console.log("Submitted:", inputText)

        try{
            
            fetch("http://127.0.0.1:5001/data-source/db-status", {
                    method: "GET"
                })
                .then(res=>res.json())
                .then(data=>{
                    if(data.status==="connected"){
                        setStatus(true) // db status

                    }else {
                        setStatus(false);
                        alert(`You are NOT connected to a database. Please make a connection to your database`)
                    }
                })
            }
        catch(err){
            console.error(err)
        }

        try{
            const response= await fetch("http://127.0.0.1:5001/query/query-input", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    query: inputText
                })
            })

            const data=await response.json()
            if(data.status=="success"){
                setVisual("true")
            }
        }catch(err){
            console.error(err)
        }
	}

    const toggleSidebar=()=>{
        setSidebarOpen(!sidebarOpen)
    }

    return (
		<div className="container">
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
                    
                    {visualization && (
                        <iframe
                            src="/generated-visual/visual.html"
                            title="Visualization"
                            style={{ width: '100%', height: '600px', border: 'none', marginTop: '20px' }}
                        ></iframe>
                    )}
				</form>
			</div>
            </div>


            <div className={`sidebar ${sidebarOpen ? 'open' : ''}`}>
                <h2>Sidebar</h2>
                <p>Extra tools or settings</p>

                <div className='side-btn-div'>
                    <button className='side-btn-open' id='select-graph-btn'>Select Graphs/Charts</button>
                    <button className='side-btn-open' id='llm-details-btn'>View LLM Details</button>
                    <button className='side-btn-open' id='output-details-btn'>View Output</button>
                </div>

            </div>
		</div>
	)
}

export default Query;