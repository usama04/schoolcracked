import React, {useState, useEffect} from 'react'
import { useParams } from 'react-router-dom'
import axios from 'axios'
import { SuccessMessage } from '../components/SuccessMessage'
import { ErrorMessage } from '../components/ErrorMessage'

const Activate = () => {
  const { uid, token } = useParams()
  const [errorMessage, setErrorMessage] = useState(null)
  const [successMessage, setSuccessMessage] = useState(null)

  useEffect(() => {
    const requestbody = {
      uid: uid,
      token: token
    }
    console.log(requestbody)
    try {
      const response = axios.post(`${process.env.REACT_APP_AUTH_URL}/auth/users/activation/`, requestbody);
      console.log(response)
      const data = response.json();
      console.log(data)
      if (response.status === 204) {
        setSuccessMessage('Your account has been activated. You can now login.');
      } else if (response.status === 403) {
        const detail = data.detail;
        setErrorMessage(detail);
      }
    } catch (error) {
      setErrorMessage('Something went wrong. Please try again.');
    }
  }, [token, uid])

  return (
    <main className='form-signin w-100 m-auto pt-5 mt-5'>
      <div className='mt-5 pt-5'>
        {errorMessage? <ErrorMessage message={errorMessage} />: null}
        {successMessage? <SuccessMessage message={successMessage} />: null}
      </div>
    </main>
  )
}

export default Activate