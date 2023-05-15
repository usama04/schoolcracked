import { logout } from '../actions/auth'
import { useNavigate } from 'react-router-dom'
import '../styles/Sidemenu.css'
import { connect } from 'react-redux'


const Logout = ({ logout, isAuthenticated }) => {
    const navigate = useNavigate();

    const logoutfunc = () => {
        logout();
        navigate('/');
    }

    if (!isAuthenticated) {
        navigate('/')
    }

    return (
        <div className='sidemenu__button mb-3' onClick={logoutfunc}>Logout</div>
    )
}

const mapStateToProps = state => ({
    isAuthenticated: state.auth.isAuthenticated
});

export default connect(mapStateToProps, { logout })(Logout)