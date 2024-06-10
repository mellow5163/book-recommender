import React from 'react'
import './title.css'
import { useNavigate } from 'react-router-dom';




export const Title = () => {

    const navigate = useNavigate();

    const handleNavigate = () => {
    navigate('/about');
    };



    return(
        <div className='title'>
            <button className="button" onClick={handleNavigate}>More Information</button>
            <h1>Book Recommender</h1>
            <h2>Through machine learning, this website recommends books based on titles that the user has previously enjoyed. This project leverages book ratings from the Goodbooks-10k dataset. If you are looking for some good books to read, feel free to give this recommendation system a try!</h2>
        </div>
    )
}

export default Title
