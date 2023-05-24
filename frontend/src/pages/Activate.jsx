import React, {useState, useEffect} from 'react'
import { useParams } from 'react-router-dom'
import axios from 'axios'
import { SuccessMessage } from '../components/SuccessMessage'
import { ErrorMessage } from '../components/ErrorMessage'

const Activate = () => {
  const { uid, token } = useParams()
  const [errorMessages, setErrorMessages] = useState([])
  const [successMessage, setSuccessMessage] = useState([])

  useEffect(() => {
    const requestbody = {
      uid: uid,
      token: token
    }
    try {
      const response = axios.post(`${process.env.REACT_APP_AUTH_URL}/auth/users/activation/`, requestbody);
      const status = response.status;
      if (status === 204) {
        setSuccessMessage(['Your account has been activated. You can now login.']);
      } else if (status === 403) {
        const detail = response.data.detail;
        setErrorMessages([detail]);
      }
    } catch (error) {
      setErrorMessages(['Something went wrong. Please try again.']);
    }
  }, [token, uid])

  return (
    <main className='form-signin w-100 m-auto pt-5 mt-5'>
      <div className='mt-5 pt-5'>
        {errorMessages.length > 0 && <ErrorMessage message={errorMessages} />}
        {successMessage.length > 0 && <SuccessMessage message={successMessage} />}
      </div>
    </main>
  )
}

export default Activate