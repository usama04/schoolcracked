import React, { useEffect, useState } from 'react';
import { connect } from 'react-redux';
import { checkAuthenticated, load_user } from './actions/auth';
import Nav from './components/Nav'
import Sidemenu from './components/Sidemenu';
import { ChangePassword } from './components/ChangePassword';

const Layout = ({ checkAuthenticated, load_user, children }) => {
    const [passTrigger, setPassTrigger] = useState(false);
    useEffect(() => {
        checkAuthenticated();
        load_user();
    }, [checkAuthenticated, load_user]);

    return (
        <div className='App'>
            {/* <Sidemenu /> */}
            <Nav passTrigger={passTrigger} setPassTrigger={setPassTrigger} />
            
            <ChangePassword passTrigger={passTrigger} setPassTrigger={setPassTrigger} />
            {children}
        </div>
    );
};

export default connect(null, { checkAuthenticated, load_user })(Layout);