
import React from 'react'
import { useState, useEffect } from "react"
import { useNavigate } from 'react-router-dom'
import "./styles/main-menu.css"
import "./styles/font.css"
import { useUser } from './Profile'

const MainMenu = () => {

    const user=useUser()
    const navigate = useNavigate()
    
    return (
        <div className='container'>
            <div className='wrapper'>
                <div id="welcome">
                    <h2> 
                        <span className='welcome-text'>  Welcome, </span>
                        <span className='username-text'> {user.username} </span>
                    </h2>
                </div>

                <div id="options">

                    <div className='horizontal-btn'>
                        <button onClick={() => navigate("/profile")}> <img className='btn-icon' src='images/profile-btn.png' /> Profile </button>
                        <button id='logout-btn'> <img className='btn-icon' src='images/logout-btn.webp' /> Log Out </button>
                    </div>
                    <button> <img className='btn-icon' src='images/graph-btn.webp' /> Generate Visual and Analysis </button>
                    <button> <img className='btn-icon' src='images/database-btn.webp' /> Data Source </button>
                    <button> <img className='btn-icon' src='images/folder-btn.png' /> Saved Visual and Analysis </button>
                    <button> <img className='btn-icon' src='images/settings-btn.png' /> Settings </button>

                </div>
            </div>
        </div>
       
    )

  }

export default MainMenu;