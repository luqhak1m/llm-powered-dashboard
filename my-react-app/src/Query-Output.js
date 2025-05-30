import "./styles/font.css";
import "./styles/back-btn.css";
import { useLocation } from 'react-router-dom';
import { useNavigate } from 'react-router-dom'


const AgentCard = ({ title, description, content, contentList }) => (
  <div style={{
    border: '1px solid #ccc',
    borderRadius: '10px',
    padding: '16px',
    marginBottom: '16px',
    boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
    backgroundColor: '#fff'
  }}>
    <h3 style={{ marginTop: 0 }}>{title}</h3>
    <p style={{ fontStyle: 'italic', color: '#666' }}>{description}</p>
    
    {contentList ? (
      contentList.map(({ label, value }, idx) => (
        <div key={idx} style={{ marginBottom: '12px' }}>
          <strong>{label}</strong>
          <pre style={{
            background: '#f9f9f9',
            padding: '12px',
            borderRadius: '6px',
            whiteSpace: 'pre-wrap',
            wordBreak: 'break-word'
          }}>
            {value || "N/A"}
          </pre>
        </div>
      ))
    ) : (
      <pre style={{
        background: '#f9f9f9',
        padding: '12px',
        borderRadius: '6px',
        whiteSpace: 'pre-wrap',
        wordBreak: 'break-word'
      }}>
        {content || "N/A"}
      </pre>
    )}
  </div>
);


const StateOutput = () => {

  const location = useLocation();
  const navigate=useNavigate()
  const output = location.state?.stateData;

  if (!output) {
    return <p>No state output available. Please try again from the Visual Output page.</p>;
  }

  return (
      <div className="container">
          <div className="wrapper">

            <div className='back-parent'>
                <div className='back-div'>
                    <button className="back-btn" onClick={() => navigate("/visual-output")}>
                        ⬅
                    </button>
                </div>
                <div className='title-ul'>
                    <h1>Enter Your Query</h1>
                </div>
            </div>


          <h2 style={{ marginTop: '32px' }}>Agents Workflow</h2>

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

          <h2 style={{ fontSize: '1.75rem', marginBottom: '10px', marginTop: '32px' }}>Agent Pipeline Output</h2>

          <AgentCard
            title="writeQuery Agent"
            description="Generates the SQL query based on the user's question."
            content={output.query}
          />

          <AgentCard
            title="validateQuery Agent"
            description="Runs and validates the generated SQL query."
            contentList={[
              {
                label: "Query Result",
                value: JSON.stringify(output.result, null, 2)
              },
              {
                label: "SQL Validity",
                value: output.SQLValidity || "Unknown"
              }
            ]}
          />

          <AgentCard
            title="improveQuery Agent"
            description="Improves the query if validation fails."
            contentList={[
              {
                label: "Retry Attempts",
                value: output.retry || "None"
              }
            ]}
          />

          <AgentCard
            title="generateDF Agent"
            description="Parses the SQL result into a structured dictionary."
            content={JSON.stringify(output.data, null, 2)}
          />

          <AgentCard
            title="chooseVisualization Agent"
            description="Chooses and renders the appropriate visualization for the result."
            content={output.visualization || "No visualization"}
          />

          <AgentCard
            title="generateAnalysis Agent"
            description="Performs human-readable reasoning on the result."
            content={output.analysis}
          />

          <AgentCard
            title="dfValidator Agent"
            description="Routes to the next step based on data validity."
            content={`Router Count: ${output.routerCount}`}
          />
        </div>
    </div>
  );
};

export default StateOutput;
