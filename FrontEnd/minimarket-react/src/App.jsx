import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Login from './pages/Login'
import Signin from './pages/Signin'
import Home from './pages/Home'
import Perfil from './pages/Perfil'
import Dashboard from './pages/Dashboard'

function App() {
    return (
        <BrowserRouter>
            <Routes>
                <Route path="/login" element={<Login />} />
                <Route path="/signin" element={<Signin />} />
                <Route path="/home" element={<Home />} />
                <Route path="/perfil" element={<Perfil />} />
                <Route path="/dashboard" element={<Dashboard />} />
            </Routes>
        </BrowserRouter>
    )
}

export default App