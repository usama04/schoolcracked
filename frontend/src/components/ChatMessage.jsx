import React, { useEffect, useState } from 'react'
import { Profile } from './Profile'
import { HandThumbsUp, HandThumbsDown } from 'react-bootstrap-icons'
import { AltAnswer } from './AltAnswer'
import { ErrorMessage } from './ErrorMessage'
import { SuccessMessage } from './SuccessMessage'


const ChatMessage = ({ message, chatLog }) => {
    const [trigger, setTrigger] = useState(false)
    const [profile_image, setProfileImage] = useState('student.png')
    const [errorMessages, setErrorMessages] = useState([])
    const [successMessages, setSuccessMessages] = useState([])
    const [answerTrigger, setAnswerTrigger] = useState(false)
    const [responseRating, setResponseRating] = useState(0)
    // if messages in the chatlog are updated, re-render the chatlog
    const setProfilePicture = async () => {
        setProfileImage('student.png')
        // const response = await fetch(`${process.env.REACT_APP_API_URL}/api/profile/me`, {
        //     method: 'GET',
        //     headers: {
        //         'Content-Type': 'application/json',
        //         'Authorization': `Bearer ${localStorage.getItem('usertoken')}`
        //     }
        // });
        // const data = await response.json();
        // if (data.error) {
        //     setErrorMessages(data.detail);
        // } else {
        //     if (data.profile_image === null) {
        //         setProfileImage('student.png')
        //     } else {
        //         setProfileImage(data.profile_image);
        //     }
        // }
    }

    useEffect(() => {
        for (let i = 0; i < chatLog.length; i++) {
            message = chatLog[i]
            setProfilePicture()
        }
    }, [])

    return (
        <div className={`chat-message ${message.role === "assistant" && "chatgpt"}`}>
            {errorMessages.length > 0 && <ErrorMessage message={errorMessages} />}
            {successMessages.length > 0 && <SuccessMessage message={successMessages} />}
            <div className="chat-message-center">
                {(message.user === "assistant" || message.role === "assistant") && <img className='avatar chatgpt' src="AIImam.png" alt="Mufti" />}
                {(message.user === "questioner" || message.role === "questioner") && <img className='avatar' src={profile_image} alt="questioner" onClick={() => setTrigger(true)} />}
                <Profile trigger={trigger} setTrigger={setTrigger} />
                <div className="message">
                    {message.message}
                    {(message.user === "assistant" || message.role === "assistant") && <div className="thumbs">
                        <button onClick={() => {
                            setResponseRating(1);
                            const response = fetch(`${process.env.REACT_APP_API_URL}/api/chat-history/${message.chat_id}`, {
                                method: 'PUT',
                                headers: {
                                    'Content-Type': 'application/json',
                                    'Authorization': `Bearer ${localStorage.getItem('usertoken')}`
                                },
                                body: JSON.stringify({
                                    response_rating: responseRating
                                })
                            });
                            if (response.ok) {
                                setSuccessMessages("Your response has been recorded");
                            } else {
                                setErrorMessages("There was an error recording your response");
                            }
                        }}><HandThumbsUp className="thumbs-up" /></button>
                        <button onClick={() => {
                            setResponseRating(-1);
                            const ifScholarTriggerAnswer = async () => {
                                const response = await fetch(`${process.env.REACT_APP_API_URL}/api/users/me`, {
                                    method: 'GET',
                                    headers: {
                                        'Content-Type': 'application/json',
                                        'Authorization': `Bearer ${localStorage.getItem('usertoken')}`
                                    }
                                });
                                const data = await response.json();
                                if (data.scholar === true) {
                                    setAnswerTrigger(true);
                                }
                            }
                            ifScholarTriggerAnswer();
                        }
                        }><HandThumbsDown className="thumbs-down" /></button>
                        {answerTrigger && <AltAnswer answerTrigger={answerTrigger} setAnswerTrigger={setAnswerTrigger} questionId={message.chat_id} responseRating={responseRating} />}
                    </div>
                    }
                </div>
            </div>
        </div>
    )
}

export default ChatMessage