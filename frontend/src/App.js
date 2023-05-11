//import logo from './logo.svg';
import React, { useContext} from 'react';
import './App.css';
import './styles/normal.css';
import { Chat } from './pages/Chat';
import { UserContext } from './context/UserContext';
import { Routes, Route } from 'react-router-dom';
import { Landing } from './pages/Landing';
import Login from './pages/Login';
import { Register } from './pages/Register';
import { ResetPassword } from './pages/ResetPassword';
import { ForgotPassword } from './pages/ForgotPassword';
import { VerifyEmail } from './components/VerifyEmail';
import Activate from './pages/Activate';
import { Provider } from 'react-redux';
import Store from './components/Store';
//import { AltAnswer } from './components/AltAnswer';


function App() {
  const { token } = useContext(UserContext);

  return (
    <>
    <Provider store={Store}>
    <Routes>
      <Route path="/" element={<Landing />} />
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />
      {token && <Route path="/chat" element={<Chat />} /> }
      <Route path="/forgot-password" element={<ForgotPassword />} />
      <Route path="/password/reset/confirm/:uid/:token" element={<ResetPassword />} />
      <Route path="/activate/:uid/:token" element={<Activate />} />
      <Route path="*" element={<Landing />} />
    </Routes>
    </Provider>
    </>
    
  );
}

export default App;
