import { React, useState, useEffect } from 'react';
import ChatMessage from '../components/ChatMessage';
import { Sidemenu } from '../components/Sidemenu';
import { useNavigate } from 'react-router-dom';
import '../styles/Sidemenu.css'
import { ThreeDotsVertical, SendFill } from 'react-bootstrap-icons';


const Chat = () => {

  // add state for input and chat log
  const [input, setInput] = useState('');
  const [chatLog, setChatLog] = useState([]);
  const [fullChatLog, setFullChatLog] = useState([]);
  const token = localStorage.getItem('access');
  const navigate = useNavigate();
  const [toggleSideMenu, setToggleSideMenu] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [messages, setMessages] = useState([
    "Researching",
    "I am analysing my research",
    "thinking how to respond best",
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

  useEffect(() => {
    if (token === null || token === undefined) {
      navigate('/login');
    }
  }, [token, navigate]);

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
      const response = await fetch(`${process.env.REACT_APP_API_URL}/api/chatbot`, {
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
    <div className="App">
      <Sidemenu chatLog={chatLog} setChatLog={setChatLog} toggleSideMenu={toggleSideMenu} />
      <section className="chatbox">
        <div className="chatbox-container">
          <div className="chat-log">
            {chatLog.map((message, index) => (
              <ChatMessage key={index} message={message} chatLog={chatLog} />
            ))}

          </div>
          <div className="chat-input-holder">
            <div className="side-menu-toggle-btn" onClick={() => setToggleSideMenu(!toggleSideMenu)}>
              <ThreeDotsVertical />
            </div>
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

export { Chat };