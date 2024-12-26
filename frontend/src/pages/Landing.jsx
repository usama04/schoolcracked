import React, { useEffect } from 'react'
import { BiCodeAlt } from 'react-icons/bi'
import { TbMathIntegralX } from 'react-icons/tb'
import { GiArchiveResearch } from 'react-icons/gi'
import { HiDocument } from 'react-icons/hi'
import { BiImage } from 'react-icons/bi'
import { BsPencilFill } from 'react-icons/bs'
import { useNavigate } from 'react-router-dom'
import '../fonts/icomoon/style.css'
import '../fonts/brand/style.css'
import '../styles/landing/css/bootstrap.min.css'
import '../styles/landing/css/bootstrap-datepicker.css'
import '../styles/landing/css/jquery.fancybox.min.css'
import '../styles/landing/css/owl.carousel.min.css'
import '../styles/landing/css/owl.theme.default.min.css'
import '../styles/landing/css/aos.css'
import '../styles/landing/css/style.css'


const Landing = () => {
  const navigate = useNavigate()

  useEffect(() => {
    //loadScripts(scripts)
    try {
      const token = localStorage.getItem('access')
      if (token.length > 5) {
        navigate('/chat')
      }
    } catch (error) {

    }
  }, [navigate])

  const carousel = {
    'backgroundImage': 'linear-gradient(rgba(0, 0, 0, 0.30), rgba(0, 0, 0, 0.30)), url("static/images/Carousel.png")',
    'backgroundRepeat': 'no-repeat',
    'backgroundSize': 'cover',
    'backgroundPosition': 'center center',
  }

  return (
      <div className="site-wrap" id="home-section">

        <div className="site-mobile-menu site-navbar-target">
          <div className="site-mobile-menu-header">
            <div className="site-mobile-menu-close mt-3">
              <span className="icon-close2 js-menu-toggle"></span>
            </div>
          </div>
          <div className="site-mobile-menu-body"></div>
        </div>

        <div className="site-section-cover overlay" style={carousel}>

          <div className="container">
            <div className="row align-items-center justify-content-center">
              <div className="col-lg-10 text-center">
                <h1>Your <strong>AI</strong> Teaching <strong>Assistant</strong></h1>
              </div>
            </div>
          </div>
        </div>

        <div className="site-section bg-dark" id="features-section">
        <div className="container">
          <div className="row">
            <div className="col">
              <div className="heading mb-4">
                <span className="caption">I AM A TEACHING ASSISTANT CHATBOT</span>
                <h2>CAPABILITIES</h2>
              </div>
            </div>  
          </div>
          <div className="row align-items-stretch">
            <div className="col-lg-2">
              <div className="course bg-dark">
                <span className="wrap-icon"><BiCodeAlt /></span>
                <h3>Write Code</h3>
              </div>
            </div>
            <div className="col-lg-2">
              <div className="course bg-dark">
                <span className="wrap-icon"><TbMathIntegralX /></span>
                <h3>Advanced Math</h3>
              </div>
            </div>
            
            <div className="col-lg-2">
              <div className="course bg-dark">
                <span className="wrap-icon"><GiArchiveResearch /></span>
                <h3>Research Assistance</h3>
              </div>
            </div>
            
            <div className="col-lg-2">
              <div className="course bg-dark">
                <span className="wrap-icon"><HiDocument /></span>
                <h3>Chat with Documents</h3>
              </div>
            </div>

            <div className="col-lg-2">
              <div className="course bg-dark">
                <span className="wrap-icon"><BiImage /></span>
                <h3>Chat with Images</h3>
              </div>
            </div>

            <div className="col-lg-2">
              <div className="course bg-dark">
                <span className="wrap-icon"><BsPencilFill /></span>
                <h3>Plagiarism Checker</h3>
              </div>
            </div>

          </div>
        </div>
      </div>

      </div>

  )
}

export default Landing