import React, { useState } from 'react'
import { ErrorMessage } from './ErrorMessage'
import { SuccessMessage } from './SuccessMessage'
import axios from 'axios';

const ChangePassword = (properties) => {
    const [old_password, setOldPassword] = useState('')
    const [new_password, setNewPassword] = useState('')
    const [confirm_password, setConfirmPassword] = useState('')
    const [errorMessages, setErrorMessages] = useState([])
    const [successMessages, setSuccessMessages] = useState([])
    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
          const response = await axios.post(`${process.env.REACT_APP_AUTH_URL}/auth/users/set_password/`, {
            current_password: old_password,
            new_password: new_password,
            re_new_password: confirm_password
          }, {
            headers: {
              'Content-Type': 'application/json',
              'Authorization': `JWT ${localStorage.getItem('access')}`
            }
          });
          if (response.status === 204) {
            setSuccessMessages(['Password changed successfully.']);
          }
        } catch (error) {
          setErrorMessages(['Password change failed.']);
        }
      }

    return (properties.passTrigger) ? (
        <div className="popup2">
            <div className="popup-inner2">
                {errorMessages.length > 0 && <ErrorMessage message={errorMessages} />}
                {successMessages.length > 0 && <SuccessMessage message={successMessages} />}
                <button className="btn btn-danger btn-close" onClick={() => properties.setPassTrigger(false)}></button>
                <form className='mt-5 pt-5' onSubmit={handleSubmit}>
                    <h1 className="h3 mb-3 fw-normal">Change your Password</h1>
                    <div className="form-group">
                        <label htmlFor="password">Old Password</label>
                        <input type="password" className="form-control rounded-2" id="old_password" placeholder="Old Password" onChange={(e) => setOldPassword(e.target.value)} value={old_password} />
                    </div>
                    <div className="form-group">
                        <label htmlFor="new_password">New Password</label>
                        <input type="password" className="form-control rounded-2" id="new_password" placeholder="New Password" onChange={(e) => setNewPassword(e.target.value)} value={new_password} />
                    </div>
                    <div className="form-group">
                        <label htmlFor="confirm_password">Confirm Password</label>
                        <input type="password" className="form-control rounded-2" id="confirm_password" placeholder="Confirm Password" onChange={(e) => setConfirmPassword(e.target.value)} value={confirm_password} />
                    </div>
                    <button className="btn btn-primary" onClick={handleSubmit} type='button'>Change Password</button>
                </form >
            </div>
        </div >
    ) : (
        <div>
        </div>
    );
}

export { ChangePassword }