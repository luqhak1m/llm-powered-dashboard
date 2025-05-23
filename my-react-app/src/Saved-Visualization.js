import { useEffect, useState } from "react"
import { useNavigate } from "react-router-dom"
import "./styles/font.css"
import "./styles/saved-visual.css"

function SavedVisualList() {
	const [savedItems, setSavedItems] = useState([])
	const navigate = useNavigate()

	useEffect(() => {
		const fetchSaved = async () => {
			try {
				const token = localStorage.getItem("token")
				const res = await fetch("http://127.0.0.1:5001/query/saved-visuals", {
					headers: { Authorization: `Bearer ${token}` }
				})
				const data = await res.json()
				setSavedItems(data)
			} catch (err) {
				console.error("Failed to fetch saved visuals:", err)
			}
		}
		fetchSaved()
	}, [])

	return (
		<div className="container">
			<div className="wrapper">
                <div className='back-parent'>
                    <div className='back-div'>
                        <button className="back-btn" onClick={() => navigate("/mainmenu")}>
                            ⬅
                        </button>
                    </div>
                    <div className='title-ul'>
                        <h1>Saved Visual</h1>
                    </div>
                </div>
				<div className="card-container">
					{savedItems.map(item => (
						<button
							key={item.id}
							className="visual-card"
							onClick={() => navigate(`/saved-visual/${item.id}`)}
						>
							<h3>{item.prompt}</h3>
							<small>{new Date(item.timestamp).toLocaleString()}</small>
                        </button>
					))}
				</div>
			</div>
		</div>
	)
}

export default SavedVisualList