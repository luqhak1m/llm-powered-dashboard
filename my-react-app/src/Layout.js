import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Login from "./Login"
import Register from "./Register"
import MainMenu from './Main-Menu'

function Layout() {
    return (
      <Router>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/mainmenu" element={<MainMenu />} />
        </Routes>
      </Router>
    )
  }
  
  export default Layout