import React from 'react'

const TermAndConditions = (props) => {
    return (props.termsTrigger) ? (
        <div className="popup">
            <div className="popup-inner">
                <button className="btn btn-danger btn-close" onClick={() => props.setTermsTrigger(false)}></button>
                <h2>Terms and Conditions</h2>
                <p>Effective date: March 01, 2023</p>
                <div className='serviceTerms'>
                    Welcome to AalimGPT, a chatbot service that provides Islamic Scholar advice based on Quran, Sunnah, and Fiqh. These Terms and Conditions ("Terms") govern your use of our service, so please read them carefully. By using our service, you agree to these Terms.

                    <h4>Service description</h4>
                    Our service provides a chatbot that can answer questions related to Islamic Scholar advice. Our chatbot is based on a machine learning model that has been trained on a dataset of Quran, Sunnah, and Fiqh. Our service is free, but we require donations to keep the service running. We also require users to sign up and provide some personal information, including email address, religious affiliation, and location. We keep a record of all the chats that happen on our platform and human Islamic scholars look through the chats that are marked as not correct and provide corrected answers. This dataset is further used to fine-tune the model. We do not sell this data to any third party or expose user information to any 3rd party.

                    <h4>User obligations</h4>
                    You agree to use our service only for lawful purposes and in a manner consistent with all applicable laws and regulations. You may not use our service to harass, threaten, or harm others, or to violate the privacy or intellectual property rights of others. You are solely responsible for the content of your interactions with our chatbot.

                    <h4>Intellectual property</h4>
                    Our service and its contents are protected by copyright, trademark, and other laws. You may not modify, reproduce, distribute, or display any part of our service without our prior written consent. You may not use our service for any commercial purpose without our prior written consent.

                    <h4>Disclaimer of warranties</h4>
                    Our service is provided "as is" and "as available" without warranties of any kind, express or implied, including but not limited to, implied warranties of merchantability, fitness for a particular purpose, and non-infringement. We do not guarantee the accuracy, timeliness, completeness, or reliability of our service. We do not guarantee that our service will be uninterrupted or error-free, or that any defects will be corrected.

                    <h4>Limitation of liability</h4>
                    To the fullest extent permitted by law, we will not be liable for any direct, indirect, incidental, special, consequential, or punitive damages arising out of or in connection with your use of our service, even if we have been advised of the possibility of such damages. You agree to indemnify and hold us harmless from any claims arising out of or in connection with your use of our service.

                    <h4>Termination</h4>
                    We reserve the right to terminate your access to our service at any time for any reason, without prior notice. We also reserve the right to modify or discontinue our service at any time without prior notice.

                    <h4>General</h4>
                    These Terms and your use of our service will be governed by and construed in accordance with the laws of Islamic Republic of Pakistan. Any dispute arising out of or in connection with these Terms or your use of our service will be submitted to the exclusive jurisdiction of the courts of Islamic Republic of Pakistan.

                    <h4>Changes to these Terms</h4>
                    We may update these Terms from time to time by posting a new version on our website. You should review these Terms periodically for changes.

                    <h4>Contact us</h4>
                    If you have any questions or concerns about these Terms or our service, please <a href="mailto:admin@aalimgpt.app">contact us</a>.
                </div>
            </div>
        </div>
    ) : "";
}

export { TermAndConditions }