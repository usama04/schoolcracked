import React, { useEffect } from 'react'
import { Nav } from '../components/Nav'
import { useNavigate, Link } from 'react-router-dom'
import '../styles/landing.css'

const Landing = () => {
  const navigate = useNavigate()

  useEffect(() => {
    try {
      const token = localStorage.getItem('usertoken')
      if (token.length > 5) {
        navigate('/chat')
      }
    } catch (error) {
      
    }
  }, [navigate])

  return (
    <div className='App '>
      <div className='section1'>
      <div className="container">
        <Nav />
        <div className="p-5 rounded-lg m-3">
          <section className="py-5 text-center container">
            <div className="row py-lg-5">
              <div className="col-lg-8 col-md-8 mx-auto">
                <h1 className="fw-light"><img src="logo.png" alt="AalimBot" width="200" /></h1>
                <p className="lead text-white fs-3">Your AI Islamic Scholar for Quick Answers on Quran and Sharia. Get instant responses to your questions, based on Quranic and Hadith references. AalimBot is the perfect companion for anyone seeking accessible knowledge on Islamic teachings.</p>
                <p>
                  {/*<Link to="https://forms.gle/uzhDvh95wQCEdyJd7" className='text-white nav-link'><button type="button" className="btn btn-success btn-lg my-2">Join our Waitlist</button></Link>*/}
                  <Link to="/register" className='text-white nav-link'><button type="button" className="btn btn-success btn-lg my-2">Register your account</button></Link>
                </p>
                <br />
                <p className="alert alert-warning">Please note that AalimBot is still a work in progress and we are only in Beta testing. Its responses may not always be fully accurate or authentic. Use the information provided by AalimBot at your own discretion and always verify it with other reliable sources.</p>
              </div>
            </div>
          </section>
        </div>
      </div>
      </div>
    </div>
  )
}

export { Landing }