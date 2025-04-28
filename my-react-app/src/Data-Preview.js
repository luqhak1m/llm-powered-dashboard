
import React from 'react'
import { useUser } from './Profile'
import { useNavigate } from 'react-router-dom'
import { useEffect, useState } from 'react'
import "./styles/font.css"
import './styles/back-btn.css'
import './styles/data-preview.css'

const DataPreview=()=>{
    const navigate=useNavigate()
    const [status, setStatus]=useState(false)
    const [dbInfo, setDbInfo]=useState(null)
    const [selectedTable, setSelectedTable]=useState("")
    const [tableInfo, setTableInfo]=useState(null)

    useEffect(()=>{
        fetch("http://127.0.0.1:5001/data-source/db-status", {
            method: "GET"
        })
        .then(res=>res.json())
        .then(data=>{
            if(data.status==="connected"){
                setStatus(true) // db status
                fetch("http://127.0.0.1:5001/data-source/db-tables")
                    .then(res=>res.json())
                    .then(data=>{
                        setDbInfo(data) // dbname, table name, n of table
                    })
            }else {
                setStatus(false);
                setDbInfo(null);
                setSelectedTable("");
                setTableInfo(null);
              }
        })
    }, [])

    const handleTableSelect=(e)=>{
        const tableName=e.target.value;
        setSelectedTable(tableName)

        fetch(`http://127.0.0.1:5001/data-source/db-table-preview/${tableName}`)
            .then(res=>res.json())
            .then(data=>{
                setTableInfo(data) // table name, col, row, row count
            })
    }

    return (
        <div className='container'>
          <div className='wrapper'>
      
            <div className="back-parent">
              <div className='back-div'>
                <button className="back-btn" onClick={() => navigate("/mainmenu")}>
                  ⬅
                </button>
              </div>
              <div className='title-ul'>
                <h1>Database Preview</h1>
              </div>
            </div>  
      
            <div className="profile-field">
              <h3>Basic Info</h3>
              <label>Database Name:</label>
              <p>{dbInfo ? dbInfo.databaseName : ''}</p>
      
              <label>Number of Tables:</label>
              <p>{dbInfo ? dbInfo.tablesCount : ''}</p>
      
              <label>Tables:</label>
              <p>{dbInfo ? dbInfo.tables.join(", ") : ''}</p>
            </div>
      
            <div className="profile-field">
              <h3>Select Table</h3>
              <select onChange={handleTableSelect} value={selectedTable} disabled={!dbInfo}>
                <option value="">-- Choose a Table --</option>
                {dbInfo && dbInfo.tables.map((table, idx) => (
                  <option key={idx} value={table}>{table}</option>
                ))}
              </select>
            </div>
      
            <div className="profile-field">
              <h3>Schema Overview</h3>
              {tableInfo ? (
                <ul>
                  {tableInfo.columns.map((col, idx) => (
                    <li key={idx}>
                      <strong>{col.name}</strong> ({col.type})
                    </li>
                  ))}
                </ul>
              ) : (
                <p>No schema info available.</p>
              )}
            </div>
      
            <div className="profile-field">
              <h3>Table Preview (First 5 Rows)</h3>
              {tableInfo ? (
                <div style={{ overflowX: 'auto' }}>
                  <table>
                    <thead>
                      <tr>
                        {tableInfo.columns.map((col, idx) => (
                          <th key={idx}>{col.name}</th>
                        ))}
                      </tr>
                    </thead>
                    <tbody>
                      {tableInfo.preview.map((row, idx) => (
                        <tr key={idx}>
                          {tableInfo.columns.map((col, cidx) => (
                            <td key={cidx}>{row[col.name]}</td>
                          ))}
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              ) : (
                <p>No preview data available.</p>
              )}
            </div>
      
            <div className="profile-field">
              <h3>Basic Stats</h3>
              <label>Row Count:</label>
              <p>{tableInfo ? tableInfo.rowCount : ''}</p>
            </div>
      
            <div style={{ textAlign: 'center' }}>
              <button className="connect-btn" onClick={() => navigate("/db-choices")}>
                <img className='btn-icon' src='images/local-db-btn.png' alt="connect db" />
                Connect to Database
              </button>
            </div>
      
          </div>
        </div>
      )
}

export default DataPreview;