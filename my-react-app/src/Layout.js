import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Login from "./Login"
import Register from "./Register"
import MainMenu from './Main-Menu'
import Profile from './Profile'

function Layout() {
    return (
      <Router>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/mainmenu" element={<MainMenu />} />
          <Route path="/profile" element={<Profile />} />
        </Routes>
      </Router>
    )
  }
  
  export default Layout