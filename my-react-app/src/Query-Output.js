
import "./styles/font.css"
import "./styles/back-btn.css"

const StateOutput = ({ output, onClose }) => {
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

        <h2>Question</h2>
        <p>{output.question || "N/A"}</p>
  
        <h2>Query</h2>
        <p>{output.query || "N/A"}</p>
  
        <h2>Result</h2>
        <p>{output.result || "N/A"}</p>
  
        <h2>Analysis</h2>
        <p>{output.analysis || "N/A"}</p>
  
        <h2>Router Count</h2>
        <p>{output.routerCount}</p>
  
        <h2>Visualization</h2>
        <p>{output.visualization !== null ? output.visualization : "No visualization"}</p>

        <h2>Sidebar</h2>
          <p>Extra tools or settings</p>

          <h2>Agents Workflow</h2>
              <img
                src="http://127.0.0.1:5001/query/generated-graph"
                alt="Agents Workflow"
                style={{
                    width: '100%',
                    maxHeight: '500px',
                    objectFit: 'contain',
                    marginTop: '20px',
                    border: '1px solid #ccc',
                    borderRadius: '8px'
                }}
              />
      </section>
    );
  };
  
  export default StateOutput;