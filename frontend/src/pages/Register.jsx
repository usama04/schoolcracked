import React, { useState } from 'react';
//import { UserContext } from '../context/UserContext';
import '../styles/sign-in.css';
import { ErrorMessage } from '../components/ErrorMessage';
import { SuccessMessage } from '../components/SuccessMessage';
import { useNavigate } from 'react-router-dom';
import { PrivacyPolicy } from '../components/PrivacyPolicy';
import { TermAndConditions } from '../components/TermAndConditions';
// import axios from 'axios';
import { register } from '../actions/auth'
import { connect } from 'react-redux';

const Register = ({ register, isAuthenticated }) => {
    const [firstName, setFirstName] = useState('');
    const [lastName, setLastName] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState(''); // [password, setPassword] = useState('') is a destructuring assignment
    const [confirmPassword, setConfirmPassword] = useState(''); // [confirmPassword, setConfirmPassword] = useState('') is a destructuring assignment
    //const { setToken } = useContext(UserContext);
    const [errorMessages, setErrorMessages] = useState(null);
    const [successMessage, setSuccessMessage] = useState(null);
    const [teacher, setTeacher] = useState(false);
    const [company, setCompany] = useState('');
    const [location, setLocation] = useState('');
    const [privacyTrigger, setPrivacyTrigger] = useState(false);
    const [termsTrigger, setTermsTrigger] = useState(false);
    const navigate = useNavigate();

    if (isAuthenticated) {
      navigate('/chat')
    }

    // const submitRegistration = async (e) => {
    //   const requestbody = {
    //     email: email,
    //     first_name: firstName,
    //     last_name: lastName,
    //     company_name: company,
    //     location: location,
    //     is_teacher: teacher,
    //     password: password,
    //     re_password: confirmPassword
    //   }
    //   try {
    //     const response = await axios.post(`${process.env.REACT_APP_AUTH_URL}/auth/users/`, requestbody);
    //     const status = response.status;
    //     if (status === 201) {
    //       setSuccessMessage('Registration successful. Please check your email for a verification link.');
    //     } else if (status === 400) {
    //       setErrorMessages('Registration failed. Please check your details and try again.');
    //     }
    //   } catch (error) {
    //     setErrorMessages('Registration failed. Please check your details and try again.');
    //   }
    // }


    const handleSubmit = (e) => {
      e.preventDefault();
      if (password === confirmPassword && password.length > 5) {
        try {
          register({ email, firstName, lastName, company, location, teacher, password, confirmPassword })
          setSuccessMessage('Registration successful. Please check your email for a verification link.');
        } catch (error) {
          setErrorMessages('Registration failed. Please check your details and try again.');
        }
      } else {
        setErrorMessages('Passwords do not match or are less than 6 characters');
      }
    }

  return (
    <main className="form-signin m-auto pt-5 mt-5">
  {successMessage? <SuccessMessage message={successMessage} />: null}
  {errorMessages ? <ErrorMessage message={errorMessages} />: null}
  <form onSubmit={handleSubmit} className="pt-5 d-md-flex flex-md-wrap flex-column">
    <h1 className="h3 mb-3 fw-normal">Please Register</h1>
    <div className="row">
      <div className="col-md-6">
        <div className="form-group">
          <label htmlFor="firstName" className="control-label">First Name</label>
          <input type="text" className="form-control rounded-2" value={firstName} onChange={(e) => setFirstName(e.target.value)} id="firstName" placeholder="First Name" required/>
        </div>
        <div className="form-group">
          <label htmlFor="lastName">Last Name</label>
          <input type="text" className="form-control rounded-2" value={lastName} onChange={(e) => setLastName(e.target.value)} id="lastName" placeholder="Last Name" />
        </div>
        <div className="form-group">
          <label htmlFor="company">Institute</label>
          <input type="text" className="form-control rounded-2" value={company} onChange={(e) => setCompany(e.target.value)} id="company" placeholder="Institute" />
        </div>
        <div className="form-group">
          <label htmlFor="location">Country</label>
          <input type="text" className="form-control rounded-2" value={location} onChange={(e) => setLocation(e.target.value)} id="location" placeholder="Country" />
        </div>
      </div>
      <div className="col-md-6">
      <div className="form-group">
          <label htmlFor="email">Email address</label>
          <input type="email" className="form-control rounded-2" value={email} onChange={(e) => setEmail(e.target.value)} id="email" placeholder="Email address" required/>
        </div>
        <div className="form-group">
          <label htmlFor="password">Password</label>
          <input type="password" className="form-control rounded-2" value={password} onChange={(e) => setPassword(e.target.value)} id="password" placeholder="Password" required/>
        </div>
        <div className="form-group">
          <label htmlFor="confirmPassword">Confirm Password</label>
          <input type="password" className="form-control rounded-2" value={confirmPassword} onChange={(e) => setConfirmPassword(e.target.value)} id="confirmPassword" placeholder="Confirm Password" required/>
        </div>
        <div className="checkbox mb-3">
          <label className="form-radio-label">Are you a Teacher?</label>
          <input type="radio" className="form-radio-input m-2" value={teacher} onChange={(e) => setTeacher(true)} id="teacherTrue" name="teacher" />
          <label className="form-radio-label">Yes</label>
          <input type="radio" className="form-radio-input m-2" value={teacher} onChange={(e) => setTeacher(false)} id="teacherFalse" name="teacher" />
          <label className="form-radio-label">No</label>
        </div>
      </div>
    </div>
    <div className="checkbox mb-3">
      <label className="checkbox-label">By clicking Register, you agree to the <span onClick={() => setTermsTrigger(true)} className="text-primary">terms and conditions</span> and <span onClick={() => setPrivacyTrigger(true)} className="text-primary">privacy policy</span>.</label>
    </div>
    <TermAndConditions termsTrigger={termsTrigger} setTermsTrigger={setTermsTrigger} />
    <PrivacyPolicy privacyTrigger={privacyTrigger} setPrivacyTrigger={setPrivacyTrigger} />
    <button className="w-100 btn btn-lg btn-success" type="submit">Register</button>
  </form>
</main>
  )
}

const mapStateToProps = (state) => {
  return {
    isAuthenticated: state.auth.isAuthenticated,
  }
}
export default connect(mapStateToProps, { register })(Register);