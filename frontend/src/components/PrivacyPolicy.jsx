import React from 'react'

const PrivacyPolicy = (props) => {
    return (props.privacyTrigger) ? (
        <div className="popup">
            <div className="popup-inner">
                <button className="btn btn-danger btn-close" onClick={() => props.setPrivacyTrigger(false)}></button>
                <h2>Privacy Policy</h2>
                <p>Effective date: March 01, 2023</p>
                <div className='serviceTerms'>

                    This Privacy Policy explains how we collect, use, and protect your personal information when you use our AalimGPT chatbot service. By using our service, you consent to the collection, use, and disclosure of your personal information as described in this Privacy Policy.

                    <h4>Information we collect</h4>
                    When you sign up for our service, we collect personal information such as your name, email address, religious affiliation, and location. We may also collect information about your interactions with our chatbot service, including the questions you ask and the answers you receive. We use cookies and other similar technologies to collect information about your device and your use of our service.

                    <h4>How we use your information</h4>
                    We use your personal information to provide our chatbot service to you, to communicate with you, and to improve our service. We may use your information to send you marketing or promotional materials, but you may opt out of receiving such materials at any time. We may also use your information to conduct research and analysis to improve our service.

                    <h4>Sharing of information</h4>
                    We do not sell, trade, or otherwise transfer your personal information to third parties. However, we may share your information with our human Islamic scholars who review and correct the answers provided by our chatbot. We may also share your information with our service providers who assist us in operating our service.

                    <h4>Security of information</h4>
                    We take reasonable measures to protect your personal information from unauthorized access, use, or disclosure. However, no method of transmission over the internet or method of electronic storage is 100% secure. Therefore, while we strive to use commercially acceptable means to protect your personal information, we cannot guarantee its absolute security.

                    <h4>Retention of information</h4>
                    We retain your personal information for as long as necessary to provide our service to you and to fulfill the purposes described in this Privacy Policy. We may also retain and use your information as necessary to comply with our legal obligations, resolve disputes, and enforce our agreements.

                    <h4>Changes to this Privacy Policy</h4>
                    We may update this Privacy Policy from time to time by posting a new version on our website. You should review this Privacy Policy periodically for changes.

                    <h4>Contact us</h4>
                    If you have any questions or concerns about our Privacy Policy, please <a href="mailto:admin@aalimgpt.app">contact us</a>.
                </div>
            </div>
        </div>
            ) : "";
}

export  { PrivacyPolicy }