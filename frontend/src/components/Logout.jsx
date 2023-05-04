import React, { useContext } from 'react'
import { UserContext } from '../context/UserContext'
import { useNavigate } from 'react-router-dom'
import '../styles/Sidemenu.css'


const Logout = () => {
    const { setToken } = useContext(UserContext);
    const navigate = useNavigate();

    const logout = () => {
        setToken(null);
        navigate('/');
    }

    return (
        <div className='sidemenu__button mb-3' onClick={logout}>Logout</div>
    )
}

export { Logout }