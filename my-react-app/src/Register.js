import React from 'react'
import { useState } from "react"

const Register = () => {

    const [email, setEmail]=useState("")
    const [username, setUsername]=useState("")
    const [password, setPassword]=useState("")
  
    const handleChange=(setValue)=>(event)=>{
      {setValue(event.target.value)}
    }
  
    const handleSubmit=async (event)=>{
        event.preventDefault()

        try{
            fetch("http://127.0.0.1:5000/auth/register", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    email: email,
                    username: username,
                    password: password
                })
            })

        }catch(err){
            alert("Something went wrong")
            console.error(err)
        }
    }
  
    return (
      <div className="container">
        <div className="wrapper">
  
          <div className="title">
            <span>Register</span>
          </div>
          <p className='title_para'>Please enter your details to register an account.</p>
  
          <form 
            method="POST"
            action="#"
            onSubmit={handleSubmit}>
  
            <div className="row">
              {/* <i className="fas fa-user"></i> */}
              <input 
                type="text" 
                placeholder="Enter your email" 
                value={email}
                onChange={handleChange(setEmail)}
                required />
            </div>

            <div className="row">
              {/* <i className="fas fa-user"></i> */}
              <input 
                type="text" 
                placeholder="Enter your username" 
                value={username}
                onChange={handleChange(setUsername)}
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
                value="Register" />
            </div>
            <div className="signup-link">Already has an account? <a href="/login">Login</a></div>
          </form>
        </div>
      </div>
    )
  }

export default Register;