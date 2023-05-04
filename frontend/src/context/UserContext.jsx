import React, {createContext, useContext, useEffect, useState} from 'react';

export const UserContext = createContext();
export const UserProvider = (props) => {
    const [token, setToken] = useState(
        localStorage.getItem('usertoken') || ''
    );
    useEffect(() => {
        const fetchUser = async () => {
            const requestOptions = {
                method: 'GET',
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${token}`
                }
            };
            const response = await fetch(`${process.env.REACT_APP_API_URL}/api/users/me`, requestOptions);

            if (!response.ok) {
                setToken(null);
                localStorage.removeItem('usertoken');
            }
            localStorage.setItem('usertoken', token);
        };
        fetchUser();
    }, [token]);
    return (
        <UserContext.Provider value={{token, setToken}}>
            {props.children}
        </UserContext.Provider>
    );
};
