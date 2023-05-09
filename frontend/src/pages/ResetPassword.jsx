import { useState } from 'react';
import { Nav } from '../components/Nav';
import { useParams } from 'react-router-dom';

const ResetPassword = () => {
    const [newPassword, setNewPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');
    const [error, setError] = useState('');
    const { message, setMessage } = useState('');
    const { token } = useParams();

    const handleResetPassword = async (e) => {
        e.preventDefault();
        if (newPassword !== confirmPassword) {
            setError('Passwords do not match');
            return;
        }

        try {
            const response = await fetch(
                `${process.env.REACT_APP_API_URL}/api/users/reset-password/${token}`,
                {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        password: newPassword,
                        confirm_password: confirmPassword,
                    }),
                }
            );
            console.log(response.data);
            setMessage(response.data.detail);
        } catch (error) {
            //console.error(error.response.data.detail);
            setError("Couldn't reset password");
        }
    };

    return (
        <div className='App'>
            <Nav />
            <main className="form-signin w-100 m-auto mt-5 pt-5">
                {error && <div className="alert alert-danger">{error}</div>}
                {message && <div className="alert alert-success">{message}</div>}
                <h1>Reset Password</h1>
                <form onSubmit={handleResetPassword}>
                    <div>
                        <label>New Password:</label>
                        <input
                            type="password"
                            value={newPassword}
                            className="form-control rounded-2"
                            onChange={(e) => setNewPassword(e.target.value)}
                        />
                    </div>
                    <div>
                        <label>Confirm Password:</label>
                        <input
                            type="password"
                            value={confirmPassword}
                            className="form-control rounded-2"
                            onChange={(e) => setConfirmPassword(e.target.value)}
                        />
                    </div>
                    <div>
                        <button 
                            className="w-100 btn btn-lg btn-primary"
                            type="submit">Reset Password</button>
                    </div>
                </form>
            </main>
        </div>
    );
};

export { ResetPassword };
