
import React from 'react'
import { useState, useEffect } from "react"

const MainMenu = () => {

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
    
    

    return (
        <div id="welcome">
            <h1> Welcome, {user.username}</h1>
        </div>
    )

  }

export default MainMenu;