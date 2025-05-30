import { useState, useEffect } from 'react'
import axios from 'axios'
import './styles/card.css' // Reuse existing styles

function ToolSelector({ token: propToken }) {
	const token = propToken || localStorage.getItem("token")
	const [tools, setTools] = useState([])
	const [selected, setSelected] = useState([])

	useEffect(() => {
		const fetchTools = async () => {
			try {
				const allToolsRes = await axios.get('http://127.0.0.1:5001/tools/tools-list')
				const selectedToolsRes = await axios.get('http://127.0.0.1:5001/tools/get-selected-tools', {
					headers: {
						Authorization: `Bearer ${token}`
					}
				})
				setTools(allToolsRes.data || [])
				setSelected(selectedToolsRes.data.tools || [])
			} catch (err) {
				console.error("Error loading tools:", err)
			}
		}
		fetchTools()
	}, [token])

	const toggleTool = tool => {
		setSelected(prev =>
			prev.includes(tool)
				? prev.filter(t => t !== tool)
				: [...prev, tool]
		)
	}

	const saveTools = () => {
		axios.post('http://127.0.0.1:5001/tools/save-tools', { tools: selected }, {
			headers: {
				Authorization: `Bearer ${token}`
			}
		})
		.then(res => alert(res.data.message))
		.catch(err => alert(err.response?.data?.error || "Unknown error"))
	}

	return (
		<div className="card-section">
			<h2>Select Tools</h2>

			<div className="tool-grid">
				{tools.map(tool => (
					<div
						key={tool}
						className={`tool-card ${selected.includes(tool) ? 'selected' : ''}`}
						onClick={() => toggleTool(tool)}
					>
						<img src={`images/${tool}.jpg`} alt={tool} className="tool-img" />
						<p>{tool}</p>
					</div>
				))}
			</div>

			{/* <h3>Selected:</h3>
			<pre>{JSON.stringify(selected, null, 2)}</pre> */}

			<button id="toolSave" onClick={saveTools}>Save Selection</button>
		</div>
	)
}

export default ToolSelector
