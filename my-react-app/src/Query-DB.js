
import "./styles/font.css"
import "./styles/back-btn.css"

const DBOutput = ({ output, onClose }) => {
    if (!output) return null;
  
    return (
      <section>

        <div style={{ display: 'flex', justifyContent: 'flex-end' }}>
          <button
            onClick={onClose}
            style={{
              fontSize: '1.5rem',
              border: 'none',
              background: 'none',
              cursor: 'pointer'
            }}
            title="Close"
          >
            ✖
          </button>
        </div>

        <h2>Database Connection</h2>
        <p>{output.db || "N/A"}</p>
  
        <h2>Database Schema</h2>
        <p>{output.schema || "N/A"}</p>
      </section>
    );
  };
  
  export default DBOutput;