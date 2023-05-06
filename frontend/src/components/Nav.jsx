import React, { useContext } from 'react'
import { UserContext } from '../context/UserContext'
import { useNavigate, Link } from 'react-router-dom'
//import '../styles/navstyle.css'
import '../fonts/icomoon/style.css'
import '../fonts/brand/style.css'
import '../styles/landing/css/bootstrap.min.css'
import '../styles/landing/css/bootstrap-datepicker.css'
import '../styles/landing/css/jquery.fancybox.min.css'
import '../styles/landing/css/owl.carousel.min.css'
import '../styles/landing/css/owl.theme.default.min.css'
import '../styles/landing/css/aos.css'
import '../styles/landing/css/style.css'

const Nav = () => {
  const { setToken } = useContext(UserContext);
  const navigate = useNavigate();

  const logout = () => {
    setToken(null);
    navigate('/');
  }

  const navbar_menu_authenticated = (
    <nav className="site-navigation text-right ml-auto d-none d-lg-block" role="navigation">
      <ul className="site-menu main-menu js-clone-nav ml-auto ">
        <li><Link to="/chat" className="nav-link">Chat TA</Link></li>
        <li><button className='nav-link' onClick={logout}>Logout</button></li>
      </ul>
    </nav>
  )

  const navbar_menu_unauthenticated = (
    <nav className="site-navigation text-right ml-auto d-none d-lg-block" role="navigation">
      <ul className="site-menu main-menu js-clone-nav ml-auto ">
        <li><Link to="index.html" className="nav-link">Home</Link></li>
        <li><Link to="about.html" className="nav-link">About</Link></li>
        <li><Link to="contact.html" className="nav-link">Contact</Link></li>
        <li><Link to="/login" className="nav-link btn btn-primary px-4 py-2 rounded-0"><span className="icon-users"></span> Login</Link></li>
        <li><Link to="/register" className="nav-link btn btn-primary px-4 py-2 rounded-0"><span className="icon-users"></span> Register</Link></li>
      </ul>
    </nav>
  )

  return (
    <header className="site-navbar light site-navbar-target" role="banner">
      <div className="container">
        <div className="row align-items-center position-relative">

          <div className="col-3">
            <div className="site-logo">
              <Link to="/"><img src="logo-white.png" alt="logo" height="200" className="d-inline-block align-text-top" /></Link>
            </div>
          </div>

          <div className="col-9  text-right">

            <span className="d-inline-block d-lg-none"><Link to="#" className=" site-menu-toggle js-menu-toggle py-5 "><span className="icon-menu h3 text-black"></span></Link></span>

            {localStorage.getItem('token') > 5 ? navbar_menu_authenticated : navbar_menu_unauthenticated}

          </div>
        </div>
      </div>
    </header>
  )
}

export { Nav }