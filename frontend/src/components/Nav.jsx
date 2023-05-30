import React, { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { logout } from '../actions/auth'
import { connect } from 'react-redux'
import { ChangePassword } from './ChangePassword'
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

const Nav = ({logout, isAuthenticated, setPassTrigger}) => {
  const navigate = useNavigate();

  const logoutfunc = () => {
    logout();
    navigate('/');
  }


  const guestLinks = (
    <ul className="site-menu main-menu js-clone-nav ml-auto ">
        <li><Link to="index.html" className="nav-link">Home</Link></li>
        <li><Link to="about.html" className="nav-link">About</Link></li>
        <li><Link to="contact.html" className="nav-link">Contact</Link></li>
        <li><Link to="/login" className="nav-link btn btn-primary px-4 py-2 rounded-0"><span className="icon-users"></span> Login</Link></li>
        <li><Link to="/register" className="nav-link btn btn-primary px-4 py-2 rounded-0"><span className="icon-users"></span> Register</Link></li>
      </ul>
  )

  const authLinks = (
      <ul className="site-menu main-menu js-clone-nav ml-auto ">
        <li><Link to="/chat" className="nav-link">Chat TA</Link></li>
        <li onClick={() => setPassTrigger(true)} className="nav-link px-4">Change Password </li>
        <li><button className='nav-link btn btn-danger px-4 py-2' onClick={logoutfunc}> Logout</button></li> 
      </ul>
  )

  return (
    <header className="site-navbar light site-navbar-target" role="banner">
      <div className="container">
        <div className="row align-items-center position-relative">

          <div className="col-3">
            <div className="site-logo">
              <Link to="/"><img src="static/images/logo.png" alt="logo" height="200" className="d-inline-block align-text-top" /></Link>
            </div>
          </div>

          <div className="col-9  text-right">

            <span className="d-inline-block d-lg-none"><Link to="#" className=" site-menu-toggle js-menu-toggle py-5 "><span className="icon-menu h3 text-black"></span></Link></span>
            <nav className="site-navigation text-right ml-auto d-none d-lg-block" role="navigation">

            {isAuthenticated ? authLinks : guestLinks}

            </nav>
          </div>
        </div>
      </div>
    </header>
  )
}



const mapStateToProps = state => ({
  isAuthenticated: state.auth.isAuthenticated
});

export default connect(mapStateToProps, { logout })(Nav)