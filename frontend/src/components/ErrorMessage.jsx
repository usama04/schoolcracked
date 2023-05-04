import { React } from 'react';

const ErrorMessage = (props) => {
    return (
        <div className="alert alert-danger" role="alert">
            {props.message}
        </div>
    )
}

export { ErrorMessage }