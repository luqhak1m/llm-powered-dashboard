import "./styles/font.css"
import "./styles/back-btn.css"
import "./styles/card.css"

const LLMOutput = ({ output }) => {
  if (!output) return null;

  return (
    <section>
      <div style={{ display: 'flex', justifyContent: 'flex-end' }}>
      </div>

      <div className="card-section">
        <h2>Large Language Model</h2>
        <p>{output.model || "N/A"}</p>
      </div>
    </section>
  );
};

export default LLMOutput;
