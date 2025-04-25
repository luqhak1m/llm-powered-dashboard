
import React from 'react'
import { useState } from "react"
import { Link, useNavigate } from 'react-router-dom'
import "./styles/back-btn.css"
import "./styles/font.css"


const LocalDB = () => {

    const [username, setUsername]=useState("")
    const [host, setHost]=useState("")
    const [database, setDatabase]=useState("")
    const [password, setPassword]=useState("")
  
    const handleChange=(setValue)=>(event)=>{
      {setValue(event.target.value)}
    }

    const navigate = useNavigate()

    const handleSubmit=async (event)=>{
        event.preventDefault()

        try{
            const response= await fetch("http://127.0.0.1:5001/data-source/db-connection", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    username: username,
                    host: host,
                    database: database,
                    password: password
                })
            })
            const data=await response.json()
            if(response.ok){
                alert(`${data.message}!`)
            } else {
                alert(`Login failed: ${data.error}`)
            }
        }catch(err){
            alert("Something went wrong")
            console.error(err)
        }
    }

  
    return (
      <div className="container">
        <div className="wrapper">
  
          <div className="back-parent">
            <div className='back-div'>
                <button className="back-btn" onClick={() => navigate("/db-choices")}>
                    ⬅
                </button>
            </div>
            <div className='title-ul'>
                <h1>Connect to your Database</h1>
            </div>
          </div>  

          <form 
            method="POST"
            action="#"
            onSubmit={handleSubmit}>
  
            <div className="row">
              {/* <i className="fas fa-user"></i> */}
              <input 
                type="text" 
                placeholder="Username" 
                value={username}
                onChange={handleChange(setUsername)}
                required />
            </div>
  
            <div className="row">
              {/* <i className="fas fa-lock"></i> */}
              <input 
                type="text" 
                placeholder="Host"
                value={host}
                onChange={handleChange(setHost)}
                required />
            </div>

            <div className="row">
              {/* <i className="fas fa-lock"></i> */}
              <input 
                type="text" 
                placeholder="Database"
                value={database}
                onChange={handleChange(setDatabase)}
                required />
            </div>

            <div className="row">
              {/* <i className="fas fa-lock"></i> */}
              <input 
                type="password" 
                placeholder="Password"
                value={password}
                onChange={handleChange(setPassword)}
                required />
            </div>

            <div className="row button">
              <input 
                type="submit" 
                value="Verify Connection" />
            </div>

          </form>
        </div>
      </div>
    )
  }

export default LocalDB;