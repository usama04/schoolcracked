import React, { useState } from 'react';
import '../styles/sign-in.css';
import { ErrorMessage } from '../components/ErrorMessage';
import { useNavigate, Link } from 'react-router-dom';
import { connect } from 'react-redux';
import { login } from '../actions/auth';


const Login = ({ login, isAuthenticated }) => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [errorMessages, setErrorMessages] = useState([]);
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        login(email, password)
    }
    // Is the user logged in?
    // If so, redirect them to the chat page

    if (isAuthenticated) {
        navigate('/chat')
    }

    return (
            <div className="container mt-5 pt-5">
                <main className="form-signin w-100 m-auto mt-5 pt-5">
                    {errorMessages.length > 0 && <ErrorMessage message={errorMessages} />}
                    <form onSubmit={handleSubmit}>
                        <h1 className="h3 mb-3 fw-normal">Please Login</h1>
                        <div className="form-group">
                            <label htmlFor="username" className="control-label">Email</label>
                            <input type="email" className="form-control rounded-2" id="username" placeholder="Email" onChange={(e) => setEmail(e.target.value)} value={email} />
                        </div>
                        <div className="form-group">
                            <label htmlFor="password">Password</label>
                            <input type="password" className="form-control rounded-2" id="password" placeholder="Password" onChange={(e) => setPassword(e.target.value)} value={password} />
                        </div>
                        <button className="w-100 btn btn-lg btn-primary" type="submit">Login</button>
                        <Link to="/forgot-password" className="mt-3">Forgot Password?</Link>
                    </form>
                    <hr />
                    <p>Don't have an account?</p>
                    <Link to="/register" className="w-100 btn btn-lg btn-success">Register</Link>
                </main>
            </div>
    )
}

const mapStateToProps = state => ({
    isAuthenticated: state.auth.isAuthenticated
});

export default connect(mapStateToProps, { login })(Login);