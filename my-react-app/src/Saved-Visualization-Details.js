import { useEffect, useState, useRef } from "react"
import { useParams, useNavigate } from "react-router-dom"
import ReactMarkdown from "react-markdown"
import "./styles/main-menu.css"

function SavedVisualDetail() {
	const { id } = useParams()
	const navigate = useNavigate()
	const [item, setItem] = useState(null)
	const containerRef = useRef(null)

	useEffect(() => {
		const fetchItem = async () => {
			try {
				const token = localStorage.getItem("token")
				const res = await fetch(`http://127.0.0.1:5001/query/saved-visuals/${id}`, {
					headers: { Authorization: `Bearer ${token}` }
				})
				const data = await res.json()
				setItem(data)
			} catch (err) {
				console.error("Failed to load visual", err)
			}
		}
		fetchItem()
	}, [id])

	useEffect(() => {
	if (!item || !containerRef.current) return

	const div = containerRef.current
	const html = item.visualization
	div.innerHTML = html

	// 1. Load external Plotly script first
	const externalScripts = Array.from(div.querySelectorAll('script[src]'))
	const loadScript = src =>
		new Promise((resolve, reject) => {
			const script = document.createElement('script')
			script.src = src
			script.async = true
			script.onload = resolve
			script.onerror = reject
			document.head.appendChild(script)
		})

	Promise.all(externalScripts.map(script => loadScript(script.src)))
		.then(() => {
			// 2. Then replace and evaluate inline scripts
			const inlineScripts = div.querySelectorAll('script:not([src])')
			inlineScripts.forEach(oldScript => {
				const newScript = document.createElement("script")
				newScript.textContent = oldScript.textContent
				oldScript.replaceWith(newScript)
			})
		})
		.catch(err => {
			console.error("Failed to load external script:", err)
		})
}, [item])

	if (!item) return <p>Loading...</p>

	return (
		<div className="container">
			<div className="wrapper">
				<div className='back-parent'>
					<div className='back-div'>
						<button className="back-btn" onClick={() => navigate("/saved-visual")}>
							⬅
						</button>
					</div>
					<div className='title-ul'>
						<h1>Saved Detail</h1>
					</div>
				</div>

				<div className="visual-detail">
					{item.prompt && (
					<>
						<p>{new Date(item.timestamp).toLocaleString()}</p>
						<h2 style={{ fontSize: '1.5rem', marginBottom: '10px' }}>User Prompt</h2>
						<div className="analysis-box" style={{ marginTop: '20px' }}>
						<pre style={{
							background: '#f9f9f9',
							padding: '12px',
							borderRadius: '6px',
							whiteSpace: 'pre-wrap',
							wordBreak: 'break-word',
							fontSize: '14px'
						}}>
							{item.prompt}
						</pre>
						</div>
					</>
					)}

					<h2 style={{
						marginTop: '2em',

					}}>Visual</h2>
					<div
						ref={containerRef}
						style={{
							width: '100%',
							height: '600px',
							border: '1px solid #ccc',
							marginTop: '20px',
							overflow: 'auto'
						}}
						dangerouslySetInnerHTML={{ __html: item.visualization }}
					/>

					<h2 style={{
						marginTop: '2em',

					}}>Analysis</h2>
					<div className="analysis-box">
					<pre style={{
							background: '#f9f9f9',
							padding: '12px',
							borderRadius: '6px',
							whiteSpace: 'pre-wrap',
							wordBreak: 'break-word',
							fontFamily: 'monospace',
							fontSize: '14px',
							}}>
							{item.analysis || "N/A"}
						</pre>
					</div>
				</div>
			</div>
		</div>
	)
}

export default SavedVisualDetail