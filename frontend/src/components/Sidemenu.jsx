import React, { useState, useEffect } from 'react'
import { Trash } from 'react-bootstrap-icons'
import "../styles/Sidemenu.css"
import { connect } from 'react-redux';

const Sidemenu = ({ chatLog, setChatLog, toggleSideMenu, user }) => {
    // const [passTrigger, setPassTrigger] = useState(false);
    const token = localStorage.getItem('access');
    const [prompts, setPrompts] = useState([]);

    function clearChat() {
        setChatLog([]);
    }

    useEffect(() => {
        if (user !== null) {
            fetch(`${process.env.REACT_APP_API_URL}/api/chats/${user.id}`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                }
            })
                .then(response => response.json())
                .then(data => {
                    const prompts = data.map(item => {
                        let decode;
                        let promptList;
                        if (typeof (item.prompt) === 'string') {
                          promptList = JSON.parse(item.prompt);
                          if (Array.isArray(promptList)) {
                            decode = promptList;
                          } else {
                            decode = JSON.parse(promptList)
                          }
                        }
                        else if (Array.isArray(item.prompt)) {
                          decode = item.prompt;
                        }
                        else {
                          decode = JSON.parse(item.prompt)
                        }
                        try {
                          const messages = decode.map(prompt => prompt.message);
                          const filteredMessages = messages.filter(message => message !== undefined && message.length > 5);
                          if (filteredMessages.length > 0) {
                            return [filteredMessages[0].toString().slice(0, 20), item._id];
                          }
                        }
                        catch {
                          console.log("Unable to fetch history")
                        }
                      })
                      setPrompts(prompts);
                })
                .catch(error => console.log(error));
        }
    }, [user, token])

    async function get_chat_history({ id }) {
        const response = await fetch(`${process.env.REACT_APP_API_URL}/api/chats/${user.id}/${id}/`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            }
        })
        const data = await response.json();
        const prompt = data.prompt
        const bot_response = data.generated
        // console.log(bot_response)
        // const bot_response_dict = JSON.parse(bot_response)
        const bot_response_dict = bot_response
        // const promptDict = JSON.parse(prompt);
        const promptDict = prompt;
        if (promptDict !== null) {
            if (Array.isArray(promptDict)) {
                const messages = promptDict.map((message) => ({
                    role: message.role,
                    message: message.message,
                }));
                const newAssistantMessage = { role: bot_response_dict.user, message: bot_response_dict.message };
                setChatLog([...messages, newAssistantMessage]);
            } else {
                const messages = JSON.parse(promptDict).map((message) => ({
                    role: message.role,
                    message: message.message,
                }));
                const newAssistantMessage = { role: bot_response_dict.user, message: bot_response_dict.message };
                setChatLog([...messages, newAssistantMessage]);
            }
            
        } else {
            
        }

    }

    async function delete_chat_history({ id }) {
        const response = await fetch(`${process.env.REACT_APP_API_URL}/api/chats/${user.id}/${id}/`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            }
        })
        const data = await response.json();
    }

    return (toggleSideMenu &&
        <aside className="sidemenu">
            {/* <div className="sidemenu__button mb-3" onClick={() => {setPassTrigger(true); console.log("Change Password")}}>
                Change Password
            </div>
            <ChangePassword passTrigger={passTrigger} setPassTrigger={setPassTrigger} /> */}
            <div className="sidemenu__button" onClick={clearChat}>
                <span>+</span>
                New Chat
            </div>
            <div>
                {prompts && prompts.map(prompt =>
                    prompt ? (
                        <div className="sidemenu__history" key={prompt}>
                            <span onClick={() => get_chat_history({ id: prompt[1] })}>{prompt[0]}</span><span onClick={() => delete_chat_history({ id: prompt[1] })} id="delete"><Trash /></span>
                        </div>
                    ) : null
                )}
            </div>
        </aside>
    )
}

const mapStateToProps = state => ({
    user: state.auth.user
});

export default connect(mapStateToProps)(Sidemenu);