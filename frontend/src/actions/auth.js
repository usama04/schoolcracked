import {
    LOGIN_SUCCESS,
    LOGIN_FAIL,
    USER_LOADED_SUCCESS,
    USER_LOADED_FAIL,
    AUTHENTICATED_SUCCESS,
    AUTHENTICATED_FAIL,
    LOGOUT,
    REGISTER_SUCCESS,
    REGISTER_FAIL,
    ACTIVATION_SUCCESS,
    ACTIVATION_FAIL
} from './types';
import axios from 'axios';

export const checkAuthenticated = () => async dispatch => {
    if (localStorage.getItem("access")){
        const config = {
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
        };
        const body = JSON.stringify({'token': localStorage.getItem("access")});
        try {
            const res = await axios.post(`${process.env.REACT_APP_AUTH_URL}/auth/jwt/verify/`, body, config);
            if (res.data.code !== "token_not_valid") {
                dispatch({
                    type: AUTHENTICATED_SUCCESS
                });
            } else {
                dispatch({
                    type: AUTHENTICATED_FAIL
                });
            }
        } catch (err) {
            dispatch({
                type: AUTHENTICATED_FAIL
            });
        }
    } else {
        dispatch({
            type: AUTHENTICATED_FAIL
        });
    }
};


export const load_user = () => async dispatch => {
    if (localStorage.getItem("access")){
        const config = {
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `JWT ${localStorage.getItem("access")}`,
                'Accept': 'application/json'
            }
        };

        try {
            const res = await axios.get(`${process.env.REACT_APP_AUTH_URL}/auth/users/me/`, config);
            dispatch({
                type: USER_LOADED_SUCCESS,
                payload: res.data
            });
        } catch (err) {
            dispatch({
                type: USER_LOADED_FAIL
            });
        }
    } else {
        dispatch({
            type: USER_LOADED_FAIL
        });
    }
};

export const login = (email, password) => async dispatch => {
    const config = {
        headers: {
            'Content-Type': 'application/json'
        }
    };

    const body = JSON.stringify({'email': email, 'password': password});
    try {
        const res = await axios.post(`${process.env.REACT_APP_AUTH_URL}/auth/jwt/create/`, body, config);
        dispatch({
            type: LOGIN_SUCCESS,
            payload: res.data
        });
        dispatch(load_user());
        return "success"
    } catch (err) {
        dispatch({
            type: LOGIN_FAIL
        });
        return "error"
    }
};

export const logout = () => dispatch => {
    dispatch({
        type: LOGOUT
    });
}

export const register = (data) => async dispatch => {
    const email = data.email;
    const first_name = data.firstName;
    const last_name = data.lastName;
    const company = data.company;
    const location = data.location;
    const is_teacher = data.teacher;
    const password = data.password;
    const re_password = data.confirmPassword;
    const config = {
        headers: {
            'Content-Type': 'application/json'
        }
    };
    const body = JSON.stringify({'first_name': first_name, 'last_name': last_name, 'email': email, 'password': password, 're_password': re_password, 'company_name': company, 'location': location, 'is_teacher': is_teacher});
    try {
        const res = await axios.post(`${process.env.REACT_APP_AUTH_URL}/auth/users/`, body, config);
        dispatch({
            type: REGISTER_SUCCESS,
            payload: res.data
        });
        return "success"
    } catch (err) {
        dispatch({
            type: REGISTER_FAIL
        });
        return "error"
    }
}

export const verify = (uid, token) => async dispatch => {
    console.log(uid, token)
    const config = {
        headers: {
            'Content-Type': 'application/json'
        }
    };
    const body = JSON.stringify({'uid': uid, 'token': token});
    try {
        await axios.post(`${process.env.REACT_APP_AUTH_URL}/auth/users/activation/`, body, config);
        dispatch({
            type: ACTIVATION_SUCCESS
        });
    } catch (err) {
        dispatch({
            type: ACTIVATION_FAIL
        });
    }
}