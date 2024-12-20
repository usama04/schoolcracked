import { React, useState } from 'react';
import ChatMessage from '../components/ChatMessage';
import Sidemenu from '../components/Sidemenu';
import { useNavigate } from 'react-router-dom';
import '../styles/Sidemenu.css'
import { ThreeDotsVertical, SendFill } from 'react-bootstrap-icons';
// import axios from 'axios';
import { checkAuthenticated } from '../actions/auth';
import { connect } from 'react-redux'

const Chat = ({ checkAuthenticated ,isAuthenticated }) => {

  // add state for input and chat log
  const [input, setInput] = useState('');
  const [chatLog, setChatLog] = useState([]);
  const [fullChatLog, setFullChatLog] = useState([]);
  const navigate = useNavigate();
  const [toggleSideMenu, setToggleSideMenu] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [messages, setMessages] = useState([
    "Thinking...",
    "Hmm...",
    "Give me a second...",
    "figuring out the best answer...",
  ]);
  const [currentMessageIndex, setCurrentMessageIndex] = useState(0);
  const [intervalId, setIntervalId] = useState(null);

  const animateMessages = () => {
    setIntervalId(
      setInterval(() => {
        setCurrentMessageIndex((prev) =>
          prev === messages.length - 1 ? 0 : prev + 1
        );
      }, 10000)
    );
  };

  if (!isAuthenticated) {
    navigate('/');
  }

  async function handleSubmit(event) {
    event.preventDefault();
    setIsLoading(true);
    const newMessage = { user: 'questioner', message: input };
    const chatLogNew = [...chatLog, newMessage];
    const fullChatLogNew = [...fullChatLog, newMessage];

    await setInput('');
    setChatLog(chatLogNew);
    setFullChatLog(fullChatLogNew);

    const messages = fullChatLogNew.map((message) => ({
      role: message.user,
      message: message.message,
    }));

    // const response = await fetch(`${process.env.REACT_APP_API_URL}/api/mufti`, {
      animateMessages();
      const response = await fetch(`${process.env.REACT_APP_API_URL}/api/assistant`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + localStorage.getItem('access'),
      },
      body: JSON.stringify({
        messages: messages,
      }),
    });

    const data = await response.json();
    setIsLoading(false);
    clearInterval(intervalId);
    const newAssistantMessage = { user: data.user, message: data.message, chat_id: data.chat_id };
    setChatLog([...chatLogNew, newAssistantMessage]);
    setFullChatLog([...fullChatLogNew, newAssistantMessage]);
  }

  return (
    <div className='mainChat'>
    <Sidemenu chatLog={chatLog} setChatLog={setChatLog} toggleSideMenu={toggleSideMenu} />
      <section className="chatbox">
        <div className="chatbox-container">
        <div className="side-menu-toggle-btn" onClick={() => setToggleSideMenu(!toggleSideMenu)}>
            <ThreeDotsVertical />
          </div>
          <div className="chat-log">
            {chatLog.map((message, index) => (
              <ChatMessage key={index} message={message} chatLog={chatLog} />
            ))}
          </div>
          <div className="chat-input-holder">
            <div className="animation-container">
              {isLoading && <div className="loading-animation"></div>}
              <div className="thought-messages">
              {isLoading && messages.map((message, index) => (
                <span
                  key={index}
                  style={{
                    display: currentMessageIndex === index ? "block" : "none",
                  }}
                >
                  {message}
                </span>
              ))}
              </div>
            </div>
            <form onSubmit={handleSubmit}>
              <div className="chat-form-group">

                <div className="chat-input-container">
                  <input
                    rows="1"
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    className="chat-input-textarea"></input>
                  <button type="submit" className="chat-input-button"><SendFill /></button>
                </div>
              </div>
            </form>
          </div>
        </div>
      </section>
    </div>
  );
}

const mapStateToProps = state => ({
  isAuthenticated: state.auth.isAuthenticated
});

export default connect(mapStateToProps, {checkAuthenticated})(Chat);