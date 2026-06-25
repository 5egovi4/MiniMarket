import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'

export default function Login() {
    useEffect(() => {
        document.body.className = 'login-body'
    }, [])
    
    const [email, setEmail] = useState('')
    const [contraseña, setContraseña] = useState('')
    const navigate = useNavigate()

    async function iniciarSesion() {
        const res = await fetch('http://127.0.0.1:8000/api/usuarios/login/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, contraseña })
        })

        const data = await res.json()

        if (res.ok) {
            localStorage.setItem('usuarioId', data.usuario.id_usuario)
            localStorage.setItem('rol', data.usuario.rol)

            if (data.usuario.rol === 'admin') {
                navigate('/dashboard')
            } else {
                navigate('/home')
            }
        } else {
            alert('Credenciales incorrectas')
        }
    }

    return (
        <div className="container-login">
            <h1>Inicia Sesión</h1>
            <div className="cuadrado-login">
                <label>Correo Electrónico</label>
                <input
                    type="text"
                    placeholder="Correo Electrónico"
                    value={email}
                    onChange={e => setEmail(e.target.value)}
                />
                <label>Contraseña</label>
                <input
                    type="password"
                    placeholder="Contraseña"
                    value={contraseña}
                    onChange={e => setContraseña(e.target.value)}
                />
                <div className="login-button">
                    <button onClick={iniciarSesion}>Iniciar Sesión</button>
                </div>
            </div>
        </div>
    )
}