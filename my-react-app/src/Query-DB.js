import "./styles/font.css"
import "./styles/back-btn.css"
import "./styles/card.css"

const DBOutput = ({ output }) => {
    if (!output) return null;
      
    const db = output.db;
    const isConnected = db && db !== "None";  
    
    return (
      <section>
        <div style={{ display: 'flex', justifyContent: 'flex-end' }}></div>

        <div className="card-section">
          <h2>Database Connection</h2>
            <p>
              {isConnected
                ? `Connected: ${typeof db === "object" ? JSON.stringify(db) : db}`
                : "Not Connected"}
            </p>
        </div>
  
        {/* <div className="card-section">
          <h2>Database Schema</h2>
          <p>{output.schema || "N/A"}</p>
        </div> */}

      </section>
    );
  };
  
  export default DBOutput;