
import React from 'react'
import { useState, useEffect } from "react"
import { useNavigate } from 'react-router-dom'
import "./styles/font.css"
import './styles/profile.css'

export const useUser=()=>{
    const [user, setUser]=useState("")
    const token=localStorage.getItem("token")

    useEffect(()=>{
        fetch("http://127.0.0.1:5001/auth/currentUser", {
            headers: {
                Authorization: `Bearer ${token}`
            }
        })
        .then(res=>res.json())
        .then(user=>{
            setUser(user)
        })
    }, [])

    return user
}


const Profile = () => {
    const user = useUser()
    const navigate = useNavigate()
  
    return (
      <div className="container">
        <div className="wrapper">

            <div className='profile'>
                <div className='back-div'>
                    <button className="back-btn" onClick={() => navigate("/mainmenu")}>
                        ⬅
                    </button>
                </div>
                <div className='profile-ul'>
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
