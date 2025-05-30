import "./styles/font.css"
import "./styles/back-btn.css"
import "./styles/card.css"

const DBOutput = ({ output }) => {
    if (!output) return null;
  
    return (
      <section>
        <div style={{ display: 'flex', justifyContent: 'flex-end' }}></div>

        <div className="card-section">
          <h2>Database Connection</h2>
          <p>{output.db || "N/A"}</p>
        </div>
  
        <div className="card-section">
          <h2>Database Schema</h2>
          <p>{output.schema || "N/A"}</p>
        </div>

      </section>
    );
  };
  
  export default DBOutput;