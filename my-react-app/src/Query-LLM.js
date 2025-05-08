
import "./styles/font.css"
import "./styles/back-btn.css"

const LLMOutput = ({ output, onClose }) => {
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
  
        <h2>Large Language Model</h2>
        <p>{output.llm || "N/A"}</p>
  
        <h2>Prompt</h2>
        <p>{output.prompt || "N/A"}</p>
  
        <h2>Tools (Plotly Functions)</h2>
        <p>{output.tools || "N/A"}</p>
      </section>
    );
  };
  
  export default LLMOutput;