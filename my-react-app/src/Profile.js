
import React from 'react'
import { useState, useEffect } from "react"
import { useNavigate } from 'react-router-dom'
import "./styles/font.css"
import './styles/profile.css'
import './styles/back-btn.css'

export const useUser = () => {
  const [user, setUser] = useState(null)
  const token = localStorage.getItem("token")
  const navigate = useNavigate()

  useEffect(() => {
    if (!token) {
      navigate("/login")
      return
    }

    fetch("http://127.0.0.1:5001/auth/currentUser", {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })
      .then(async (res) => {
        const data = await res.json()
        if (!res.ok) {
          // Handle errors
          if (data.error === "Token Expired") {
            alert("Session expired. Please log in again.")
            await fetch("http://127.0.0.1:5001/auth/logout", {
                method: "POST",
                headers: {
                Authorization: `Bearer ${localStorage.getItem("token")}`
                }
            });
            localStorage.removeItem("token")
            navigate("/login")
          } else if (data.error === "Missing Token" || data.error === "Invalid Token") {
            await fetch("http://127.0.0.1:5001/auth/logout", {
                method: "POST",
                headers: {
                Authorization: `Bearer ${localStorage.getItem("token")}`
                }
            });
            localStorage.removeItem("token")
            navigate("/login")
          }
          setUser(null)
        } else {
          setUser(data)
        }
      })
      .catch((err) => {
        console.error("Failed to fetch user:", err)
        localStorage.removeItem("token")
        navigate("/login")
      })
  }, [token, navigate])

  return user
}


const Profile = () => {
    const user = useUser()
    const navigate = useNavigate()

    if(!user){
      return <p>... Loading ...</p>
    }
  
    return (
      <div className="container">
        <div className="wrapper">

            <div className='back-parent'>
                <div className='back-div'>
                    <button className="back-btn" onClick={() => navigate("/mainmenu")}>
                        ⬅
                    </button>
                </div>
                <div className='title-ul'>
                    <h1>Profile</h1>
                </div>
            </div>

          <div className="profile-field">
            <label>Username:</label>
            <p>{user.username}</p>
          </div>
  
          <div className="profile-field">
            <label>Email:</label>
            <p>{user.email}</p>
          </div>
  
          <div className="profile-field">
            <label>Password:</label>
            <p>********</p>
          </div>
        </div>
      </div>
    )
  }

export default Profile
