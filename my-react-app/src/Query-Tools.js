import { useState, useEffect } from 'react'
import axios from 'axios'

function ToolSelector({ token: propToken, onClose }) {
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
		.catch(err => alert(err.response.data.error))
	}

	return (
            <div>
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
			<h2>Select Tools</h2>
			<ul>
				{tools.map(tool => (
					<li key={tool}>
						<label>
							<input
								type="checkbox"
								checked={selected.includes(tool)}
								onChange={() => toggleTool(tool)}
							/>
							<img src={`images/${tool}.jpg`} alt={tool} style={{ width: '24px', height: '24px' }} />

							{tool}
						</label>
					</li>
				))}
			</ul>

			<h3>Selected:</h3>
			<pre>{JSON.stringify(selected, null, 2)}</pre>

            <button onClick={saveTools}>Save Selection</button>
		</div>
	)
}

export default ToolSelector;