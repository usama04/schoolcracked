import React, { useEffect, useState } from 'react'
import { ErrorMessage } from './ErrorMessage'
import { SuccessMessage } from './SuccessMessage'
import ReactMarkdown from 'react-markdown';


const ChatMessage = ({ message, chatLog }) => {
    const [trigger, setTrigger] = useState(false)
    const [profile_image, setProfileImage] = useState('static/images/student.png')
    const [errorMessages, setErrorMessages] = useState([])
    const [successMessages, setSuccessMessages] = useState([])
    const [answerTrigger, setAnswerTrigger] = useState(false)
    const [responseRating, setResponseRating] = useState(0)
    // if messages in the chatlog are updated, re-render the chatlog
    const setProfilePicture = async () => {
        setProfileImage('static/images/student.png')
    }

    useEffect(() => {
        for (let i = 0; i < chatLog.length; i++) {
            message = chatLog[i]
            setProfilePicture()
        }
    }, [])

    let parsedMessage = null;
    try {
        parsedMessage = JSON.parse(message.message);
    } catch (error) {
        parsedMessage = null;
    }

    // Check if the parsed message has action_input
    const hasActionInput = parsedMessage && parsedMessage.action_input;

    // Reintroduce the backticks to the code portion
    let actionInputWithBackticks = null;
    if (hasActionInput) {
        const codeBlockRegex = /```(\w+)\n([\s\S]*?)```/g;
        actionInputWithBackticks = parsedMessage.action_input.replace(
        codeBlockRegex,
        '```\n$1\n$2\n```'
        );
    }

    return (
        <div className={`chat-message ${message.user === "assistant" && "chatgpt"}`}>
            {errorMessages.length > 0 && <ErrorMessage message={errorMessages} />}
            {successMessages.length > 0 && <SuccessMessage message={successMessages} />}
            <div className="chat-message-center">
                {(message.user === "assistant" || message.user === "assistant") && <img className='avatar chatgpt' src="static/images/AIImam.png" alt="Mufti" />}
                {(message.user === "questioner" || message.role === "questioner") && <img className='avatar' src={profile_image} alt="questioner" onClick={() => setTrigger(true)} />}
                <span className="message">
                    {/* {message.message} */}
                    {parsedMessage && parsedMessage.action_input ? (
                    // <ReactMarkdown>{parsedMessage.action_input}</ReactMarkdown>
                    <ReactMarkdown>{actionInputWithBackticks}</ReactMarkdown>
                        ) : (message.message)
                    }
                </span>
            </div>
        </div>
    )
}

export default ChatMessage