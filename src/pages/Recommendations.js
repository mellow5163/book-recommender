import React from 'react'
import './Recommendations.css'
import { useNavigate } from 'react-router-dom';
import { useLocation } from 'react-router-dom';

function Recommendations() {

    const location = useLocation();
    const { results } = location.state || { results: [] };

    const navigate = useNavigate();

    const handleNavigate = () => {
    navigate('/');
    };

    return (
        <div className='recs'>
            <h1>Recommendations</h1>
            {results.length > 0 ? (
                <ul>
                    {results.map((result, index) => (
                        <li key={index}>{result}</li>
                    ))}
                </ul>
            ) : (
            <p>No results</p>
            )}
            
            <button className='navigate-button' onClick={handleNavigate}>Go to Home</button>
        </div>
    )
}

export default Recommendations
