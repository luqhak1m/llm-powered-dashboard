import React from 'react'
import { useState } from "react"
import { Link } from 'react-router-dom'


const Login = () => {

    const [username, setUsername]=useState("")
    const [password, setPassword]=useState("")
  
    const handleChange=(setValue)=>(event)=>{
      {setValue(event.target.value)}
    }
  
    const handleSubmit=async (event)=>{
        event.preventDefault()

        try{
            const response= await fetch("http://127.0.0.1:5000/auth/login", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    username: username,
                    password: password
                })
            })

            const data=await response.json()
            if(response.ok){
                alert(`Login success: ${data.username}`)
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
  
          <div className="title">
            <span>Welcome!</span>
          </div>
          <p className='title_para'>Please enter your details to sign in.</p>
  
          <form 
            method="POST"
            action="#"
            onSubmit={handleSubmit}>
  
            <div className="row">
              {/* <i className="fas fa-user"></i> */}
              <input 
                type="text" 
                placeholder="Enter your email..." 
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
            <div className="pass"><a href="#">Forgot password?</a></div>
            <div className="row button">
              <input 
                type="submit" 
                value="Login" />
            </div>
            <div className="signup-link"> Not a member? <Link to="/register">Sign Up</Link></div>

          </form>
        </div>
      </div>
    )
  }

export default Login;