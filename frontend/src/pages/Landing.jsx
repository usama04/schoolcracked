import React, { useEffect } from 'react'
import { Nav } from '../components/Nav'
import { useNavigate, Link } from 'react-router-dom'
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
      const token = localStorage.getItem('usertoken')
      if (token.length > 5) {
        navigate('/chat')
      }
    } catch (error) {

    }
  }, [navigate])

  return (
    <div className='App'>
      <div className="site-wrap" id="home-section">

        <div className="site-mobile-menu site-navbar-target">
          <div className="site-mobile-menu-header">
            <div className="site-mobile-menu-close mt-3">
              <span className="icon-close2 js-menu-toggle"></span>
            </div>
          </div>
          <div className="site-mobile-menu-body"></div>
        </div>



        <Nav />

        <div className="site-section-cover overlay" style={{ backgroundImage: 'url("Carousel.png")' }}>

          <div className="container">
            <div className="row align-items-center justify-content-center">
              <div className="col-lg-10 text-center">
                <h1>The <strong>Hub</strong> Of <strong>Tutorials</strong></h1>
              </div>
            </div>
          </div>
        </div>

        <div className="site-section bg-light pb-0">
          <div className="container">
            <div className="row align-items-stretch overlap">
              <div className="col-lg-8">
                <div className="box h-100">
                  <div className="d-flex align-items-center">
                    {/* <div className="img"><img src="images/img_1.jpg" className="img-fluid" alt="Image" /></div> */}
                    <div className="text">
                      <Link to="#" className="category">Tutorial</Link>
                      <h3><Link to="#">Learning React Native</Link></h3>
                      <p>Lorem ipsum dolor sit amet, consectetur adipisicing elit. Harum quidem totam exercitationem eveniet blanditiis nulla, et possimus, itaque alias maxime!</p>
                      <p className="mb-0">
                        <span className="brand-react h5"></span>
                        <span className="brand-javascript h5"></span>
                      </p>
                      <p className="meta">
                        <span className="mr-2 mb-2">1hr 24m</span>
                        <span className="mr-2 mb-2">Advanced</span>
                        <span className="mr-2 mb-2">Jun 18, 2020</span>
                      </p>
                    </div>
                  </div>
                </div>
              </div>
              <div className="col-lg-4">
                <div className="box small h-100">
                  <div className="d-flex align-items-center mb-2">
                    {/* <div className="img"><img src="images/img_2.jpg" className="img-fluid" alt="Image" /></div> */}
                    <div className="text">
                      <Link to="#" className="category">Tutorial</Link>
                      <h3><Link to="#">Learning React Native</Link></h3>
                    </div>
                  </div>
                  <div className="d-flex align-items-center mb-2">
                    {/* <div className="img"><img src="images/img_3.jpg" className="img-fluid" alt="Image" /></div> */}
                    <div className="text">
                      <Link to="#" className="category">Tutorial</Link>
                      <h3><Link to="#">Learning React Native</Link></h3>
                    </div>
                  </div>
                  <div className="d-flex align-items-center">
                    {/* <div className="img"><img src="images/img_4.jpg" className="img-fluid" alt="Image" /></div> */}
                    <div className="text">
                      <Link to="#" className="category">Tutorial</Link>
                      <h3><Link to="#">Learning React Native</Link></h3>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

      </div>
    </div>

  )
}

export { Landing }