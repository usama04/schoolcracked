import React, { useState } from 'react'
import { ErrorMessage } from './ErrorMessage'
import { SuccessMessage } from './SuccessMessage'

const AltAnswer = (props) => {
    const [altAnswer, setAltAnswer] = useState([])
    const [errorMessages, setErrorMessages] = useState([])
    const [successMessages, setSuccessMessages] = useState([])

    const handleSubmit = async (e) => {
        e.preventDefault();
        const response = await fetch(`${process.env.REACT_APP_API_URL}/api/chat-history/${props.questionId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('usertoken')}`
            },
            body: JSON.stringify({
                response_rating: props.responseRating,
                alt_response: altAnswer
            })
        });
        const data = await response.json();
        if (data.error) {
            setErrorMessages(data.detail);
        } else {
            setSuccessMessages(data.message);
            props.setAnswerTrigger(false);
        }
    }
  return (
    <div className='popup2'>
        <div className='popup-inner2'>
        <button className="btn btn-danger btn-close" onClick={() => props.setAnswerTrigger(false)}></button>
                {errorMessages.length > 0 && <ErrorMessage message={errorMessages} />}
                {successMessages.length > 0 && <SuccessMessage message={successMessages} />}
            <form>
                <h1 className="h3 mb-3 fw-normal">Add an alternative answer</h1>
                <div className="form-group">
                    <label htmlFor="altAnswer">Alternative Answer</label>
                    <textarea className="form-control rounded-2" id="altAnswer" placeholder="Alternative Answer" onChange={(e) => setAltAnswer(e.target.value)} value={altAnswer} rows={8} />
                </div>
                <button className="btn btn-primary" onClick={handleSubmit}>Add Alternative Answer</button>
            </form>
        </div>
    </div>
  );
}

export { AltAnswer }