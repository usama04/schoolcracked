import React, {useState, useEffect} from 'react'
import { useParams, useNavigate } from 'react-router-dom'
// import axios from 'axios'
import { SuccessMessage } from '../components/SuccessMessage'
import { ErrorMessage } from '../components/ErrorMessage'
import { verify } from '../actions/auth'
import { connect } from 'react-redux'

const Activate = ({verify, isAuthenticated}) => {
  const { uid, token } = useParams()
  const [errorMessage, setErrorMessage] = useState(null)
  const [successMessage, setSuccessMessage] = useState(null)
  const [verfied, setVerified] = useState(false)
  const navigate = useNavigate()

  if (isAuthenticated) {
    navigate('/chat')
  }

  // if (verfied) {
  //   setSuccessMessage('Your account has been activated. You can now login.')
  // }

  useEffect(() => {
    // const requestbody = {
    //   uid: uid,
    //   token: token
    // }
    // console.log(requestbody)
    // try {
    //   const response = axios.post(`${process.env.REACT_APP_AUTH_URL}/auth/users/activation/`, requestbody);
    //   console.log(response)
    //   const data = response.json();
    //   console.log(data)
    //   if (response.status === 204) {
    //     setSuccessMessage('Your account has been activated. You can now login.');
    //   } else if (response.status === 403) {
    //     const detail = data.detail;
    //     setErrorMessage(detail);
    //   }
    // } catch (error) {
    //   setErrorMessage('Something went wrong. Please try again.');
    // }
    try {
      verify(uid, token)
      setVerified(true)
      setSuccessMessage('Your account has been activated. You can now login.')
    } catch (error) {
      console.log(error)
      setErrorMessage('Something went wrong. We could not verify your account.')
    }
  }, [uid, token, verify])

  return (
    <main className='form-signin w-100 m-auto pt-5 mt-5'>
      <div className='mt-5 pt-5'>
        {errorMessage? <ErrorMessage message={errorMessage} />: null}
        {successMessage? <SuccessMessage message={successMessage} />: null}
        {verfied? <button className='btn btn-primary' onClick={() => navigate('/login')}>Login</button>: null}
      </div>
    </main>
  )
}

const mapStateToProps = state => ({
  isAuthenticated: state.auth.isAuthenticated
})

export default connect(mapStateToProps, {verify})(Activate)