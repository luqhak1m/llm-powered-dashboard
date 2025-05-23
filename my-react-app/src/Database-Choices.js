
import React from 'react'
import { useUser } from './Profile'
import { useNavigate } from 'react-router-dom'
import "./styles/font.css"
import './styles/back-btn.css'


const DatabaseChoices=()=>{

    const user=useUser()

    const navigate = useNavigate()
    

    return(
        <div className='container'>
            <div className='wrapper'>

                <div className="back-parent">
                    <div className='back-div'>
                        <button className="back-btn" onClick={() => navigate("/db-preview")}>
                            ⬅
                        </button>
                    </div>
                    <div className='title-ul'>
                        <h1>Connect to your Database</h1>
                    </div>
                </div>  

                <div id="options">

                <button onClick={() => navigate("/local-db")}>
                    <img className='btn-icon' src='images/database-btn.webp'/> Connect to Local Database
                </button>

                <button onClick={() => navigate("/connect-sample")}>
                    <img className='btn-icon' src='images/laptop-btn.png' /> Connect to Sample Database
                </button>

                </div>
            </div>
        </div>
    )
}

export default DatabaseChoices;