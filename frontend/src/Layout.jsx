import React, { useEffect } from 'react';
import { connect } from 'react-redux';
import { checkAuthenticated, load_user } from './actions/auth';
import Nav from './components/Nav'
import Sidemenu from './components/Sidemenu';

const Layout = ({ checkAuthenticated, load_user, children }) => {
    useEffect(() => {
        checkAuthenticated();
        load_user();
    }, [checkAuthenticated, load_user]);

    return (
        <div className='App'>
            <Nav />
            <Sidemenu />
            {children}
        </div>
    );
};

export default connect(null, { checkAuthenticated, load_user })(Layout);