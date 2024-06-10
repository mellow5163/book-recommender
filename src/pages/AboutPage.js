import React from 'react'
import './AboutPage.css'
import { useNavigate } from 'react-router-dom';

function AboutPage() {

    const navigate = useNavigate();

    const handleNavigate = () => {
    navigate('/');
    };

    return (
        <div className='about'>
            <button className='navigate-button' onClick={handleNavigate}>Go to Recommender</button>
            <h1>Additional Information</h1>
            <h2>Overview</h2>
            <p2>Our final project is a book recommendation system, developed as a web application that allows users to input three books that they like and receive personalized book recommendations based on those inputs. With the vast number of books available today, finding the right book to read can be overwhelming for readers. This recommender aims to simplify this process by helping users discover new books that match their preferences, making their reading experience more enjoyable and efficient.</p2>
            <h3>Key AI methodologies</h3>
            <p3>This website employs a hybrid model that combines collaborative filtering and content-based filtering. This model utilizes the K-Nearest Neighbor algorithm in the content-based filtering portion, and utilizes cosine similarity in the collaborative filtering portion.  was a Neural Network. The Accuracy of this model was determined using F-1 scores, Precision, Recall, Root Mean Squared Error, and Mean Absolute Error.</p3>
            <h4>Challenges</h4>
            <p4> We faced three primary challenges throughout this project. Firstly, we struggled to find example recommendation models online that do not rely on user data. Most existing recommendation systems are user-centric, making it difficult to find references for a book-based approach. The second primary challenge was addressing the cold start problem for less-reviewed books. Generating recommendations for such books required the integration of content-based methods effectively. The last primary challenge we faced was finding the right balance between diversity and relevance in recommendations. Careful model tuning and evaluation are needed to ensure that the recommendations are both relevant and varied to avoid a monotonous user experience. </p4>

        </div>
    )
}

export default AboutPage
