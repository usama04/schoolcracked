import React from 'react'
import '../styles/navstyle.css'
import { Link } from 'react-router-dom'

const Nav = () => {
  return (
    <nav className="navbar fixed-top navbar-expand-lg navbar-dark bg-dark">
  <div className="container">
    <a className="navbar-brand" href="/"><img src="logo.png" alt="logo" width="30" height="30" className="d-inline-block align-text-top" /></a>
    <button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarCollapse" aria-controls="navbarCollapse" aria-expanded="false" aria-label="Toggle navigation">
      <span className="navbar-toggler-icon"></span>
    </button>
    <div className="collapse navbar-collapse" id="navbarCollapse">
      <ul className="navbar-nav me-auto mb-2 mb-md-0">
      </ul>
      <button className="btn btn-outline-success me-2"><Link to="/login" className='text-white nav-link'>Login</Link></button>
      <button className="btn btn-outline-success"><Link to="/register" className='text-white nav-link'>Register</Link></button>
    </div>
  </div>
</nav>
  )
}

export { Nav }