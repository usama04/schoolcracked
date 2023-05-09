import React, {useEffect, useState} from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import { ErrorMessage } from './ErrorMessage'

const VerifyEmail = () => {
    const [errorMessages, setErrorMessages] = useState([])
    const [successMessages, setSuccessMessages] = useState([])
    const { token } = useParams();
    const navigate = useNavigate();
    useEffect(() => {
        const verifyEmail = async () => {
            const response = await fetch(`${process.env.REACT_APP_API_URL}/api/verify-email/${token}`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                }
            });
            const data = await response.json();
            if (data.error) {
                console.log(data.detail);
                setErrorMessages(data.detail);
            } else {
                setSuccessMessages(data.detail);
                navigate('/login');
            }
        }
        verifyEmail();
    }, [navigate, token])

  return (
    <div className='app'>
        {errorMessages.map((message, index) => (
            <ErrorMessage key={index} message={message} />
        ))}
        {successMessages.map((message, index) => (
            <ErrorMessage key={index} message={message} />
        ))}
    </div>
  )
}

export { VerifyEmail }