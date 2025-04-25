import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Login from "./Login"
import Register from "./Register"
import MainMenu from './Main-Menu'
import Profile from './Profile'
import LocalDB from './Data-Source'
import DatabaseChoices from './Database-Choices'

function Layout() {
    return (
      <Router>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/mainmenu" element={<MainMenu />} />
          <Route path="/profile" element={<Profile />} />
          <Route path="/local-db" element={<LocalDB />} />
          <Route path="/db-choices" element={<DatabaseChoices />} />
        </Routes>
      </Router>
    )
  }
  
  export default Layout