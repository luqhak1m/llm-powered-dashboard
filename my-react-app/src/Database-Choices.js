
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
                        <button className="back-btn" onClick={() => navigate("/mainmenu")}>
                            ⬅
                        </button>
                    </div>
                    <div className='title-ul'>
                        <h1>Connect to your Database</h1>
                    </div>
                </div>  

                <div id="options">

                <button onClick={() => navigate("/connect-cloud")}>
                    <img className='btn-icon' src='images/cloud-btn.png' /> Connect via Cloud Service
                </button>

                <button onClick={() => navigate("/connect-ssh")}>
                    <img className='btn-icon' src='images/ssh-btn.png' /> Connect via SSH Tunnel
                </button>

                <button onClick={() => navigate("/local-db")}>
                    <img className='btn-icon' src='images/local-db-btn.png'/> Connect to Local Database
                </button>

                <button onClick={() => navigate("/connect-sample")}>
                    <img className='btn-icon' src='images/sample-db-btn.png' /> Connect to Sample Database
                </button>

                </div>
            </div>
        </div>
    )
}

export default DatabaseChoices;