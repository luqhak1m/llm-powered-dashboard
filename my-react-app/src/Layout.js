import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Login from "./Login"
import Register from "./Register"

function Layout() {
    return (
      <Router>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
        </Routes>
      </Router>
    )
  }
  
  export default Layout