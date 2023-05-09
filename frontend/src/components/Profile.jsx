import React, { useState, useEffect, useRef } from 'react'
import { ErrorMessage } from './ErrorMessage'
import { SuccessMessage } from './SuccessMessage'

function Profile(props) {
    const inputRef = useRef();
    const [firstName, setFirstName] = useState('')
    const [lastName, setLastName] = useState('')
    const [bio, setBio] = useState('')
    const [location, setLocation] = useState('')
    const [dob, setDob] = useState('')
    const [errorMessages, setErrorMessages] = useState([])
    const [successMessages, setSuccessMessages] = useState([])

    useEffect(() => {
        const fetchProfile = async () => {
            const response = await fetch(`${process.env.REACT_APP_API_URL}/api/profile/me`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.getItem('usertoken')}`
                }
            });
            const data = await response.json();
            if (data.error) {
                setErrorMessages(data.detail);
            } else {
                setFirstName(data.first_name);
                setLastName(data.last_name);
                setBio(data.bio);
                setLocation(data.location);
                setDob(data.dob);
            }
        }
        fetchProfile();
    }, [])

    const updateProfile = async () => {
        const response = await fetch(`${process.env.REACT_APP_API_URL}/api/profile/me`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('usertoken')}`
            },
            body: JSON.stringify({
                first_name: firstName,
                last_name: lastName,
                bio: bio,
                location: location,
                dob: dob
            })
        });
        const data = await response.json();
        if (data.error) {
            setErrorMessages(data.detail);
        } else {
            setSuccessMessages(data.detail);
        }
    }

    const delete_user = async () => {
        const response = await fetch(`${process.env.REACT_APP_API_URL}/api/users/me`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('usertoken')}`
            }
        });
        const data = await response.json();
        if (data.error) {
            setErrorMessages(data.detail);
        } else {
            setSuccessMessages(data.detail);
        }

    }

    const handleSubmit = async (e) => {
        e.preventDefault();
        await updateProfile();
    }

    const handleProfilePic = async (e) => {
        e.preventDefault()
        const formData = new FormData();
        formData.append('file', inputRef.current.files[0]);
        const response = await fetch(`${process.env.REACT_APP_API_URL}/api/profile/me/upload-image`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('usertoken')}`
            },
            body: formData
        });
        const data = await response.json();
        if (data.error) {
            setErrorMessages(data.detail);

        } else {
            setSuccessMessages(data.detail);
        }
    };

    return (props.trigger) ? (
        <div className='popup'>
            <div className="popup-inner">
                {/*errorMessages.map((message, index) => {
                    return <ErrorMessage key={index} message={message} />
                })}
                {successMessages.map((message, index) => {
                    return <SuccessMessage key={index} message={message} />
                })*/}
                <button className="btn btn-danger btn-close" onClick={() => props.setTrigger(false)}></button>
                {props.children}
                <h1 className="h3 mb-3 fw-normal">Edit Profile</h1>
                {/*}
                <form className="form-group">
                    <label htmlFor="file" className="control-label">Profile Picture</label>
                    <input type="file" className="form-control rounded-2" id="file" name="file" aria-describedby="button-addon2" ref={inputRef} />
                    <button className="btn btn-outline-primay btn-success mt-3" onClick={handleProfilePic} id="button-addon2" type='button'>Upload</button>
                </form>
                */}
                <form className="form-group">
                    <label htmlFor="firstName" className="control-label">First Name</label>
                    <input type="text" className="form-control rounded-2" value={firstName} onChange={(e) => setFirstName(e.target.value)} id="firstName" />
                    <label htmlFor="lastName" className="control-label">Last Name</label>
                    <input type="text" className="form-control rounded-2" value={lastName} onChange={(e) => setLastName(e.target.value)} id="lastName" />
                </form>
                <form>
                    <label htmlFor="bio" className="control-label">Religion</label>
                    <input type="text" className="form-control rounded-2" value={bio} onChange={(e) => setBio(e.target.value)} id="bio" />
                    <label htmlFor="location" className="control-label">Location</label>
                    <input type="text" className="form-control rounded-2" value={location} onChange={(e) => setLocation(e.target.value)} id="location" />
                    {/*<label htmlFor="dob" className="control-label">Date of Birth</label>
                    <input type="text" className="form-control rounded-2" value={dob} onChange={(e) => setDob(e.target.value)} id="dob" />*/}
                </form>
                <button className="w-100 btn btn-lg btn-success mt-3" onClick={handleSubmit} type="button">Update</button>
                <div className='mt-3'>
                    <button className="w-100 btn btn-lg btn-danger" onClick={delete_user} type="button">Delete X</button>
                </div>
            </div>
        </div>
    ) : "";

}

export { Profile }