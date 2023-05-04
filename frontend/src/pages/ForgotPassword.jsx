import React, { useState } from 'react'
import { Nav } from '../components/Nav'

const ForgotPassword = () => {
    const [email, setEmail] = useState('');
    const [error, setError] = useState('');
    const [message, setMessage] = useState('');

    const handleForgotPassword = async (e) => {
        e.preventDefault();
        try {
            const response = await fetch(`${process.env.REACT_APP_API_URL}/api/users/forgot-password`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    email: email,
                }),
            });
            //console.log(response.data.message);
            setMessage("Email Sent successfully");
        } catch (error) {
            //console.log(error.detail);
            setError("We encountered an Error");
        }
    };

  return (
    <div className="App">
        <Nav />
        <main className="form-signin w-100 m-auto mt-5 pt-5">
            {error && <div className="alert alert-danger">{error}</div>}
            {message && <div className="alert alert-success">{message}</div>}
            <form>
            <h1 className="h3 mb-3 fw-normal">Forgot Password</h1>
            <div className="form-group">
                <label htmlFor="email" className="form-label">Email address</label>
                <input type="email" className="form-control rounded-2" id="email" aria-describedby="emailHelp" placeholder="Enter email" value={email} onChange={(e) => setEmail(e.target.value)} />
                <div id="emailHelp" className="form-text">We'll never share your email with anyone else.</div>
            </div>
            <button type="submit" className="w-100 btn btn-lg btn-primary" onClick={handleForgotPassword}>Submit</button>
            </form>
        </main>
    </div>
  )
}

export { ForgotPassword }