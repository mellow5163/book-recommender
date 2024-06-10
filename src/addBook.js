/* eslint-disable no-unused-vars */
import React, { useState, useEffect }  from 'react'
import './addBook.css'
import { useNavigate } from 'react-router-dom';

export const AddBook= ()=> {

    const navigate = useNavigate();

    // eslint-disable-next-line no-unused-vars
    const handleNavigate = () => {
    navigate('/recommendations')
    }


    const [book1, setBook1] = useState('')
    const [book2, setBook2] = useState('')
    const [book3, setBook3] = useState('')
    const [error1, setError] = useState('')
    //const [results, setResults] = useState([]);

    //check if book is in dataset and incorporate fuzzy searching, need to connect with backend for this
    const handleBook1Change = (e) => setBook1(e.target.value);
    const handleBook2Change = (e) => setBook2(e.target.value);
    const handleBook3Change = (e) => setBook3(e.target.value);

    // eslint-disable-next-line no-unused-vars
    const handleSubmit=(e)=> { 
        e.preventDefault();
        //logs books to the console
        console.log('Book 1: ', book1)
        console.log('Book 2: ', book2)
        console.log('Book 3: ', book3)

        //send books to backend

        fetch('http://127.0.0.1:4000/register_books', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ books_received: [book1, book2, book3]})
        })
        .then(response => {
            if (response.ok) {
                setError('')
            }
            return response.json()
        })
        .then(data => {
            if (data.error) {
                setError(data.error)
            }
            else {
                console.log('Success', data)
                //setResults(data)
                navigate('/recommendations', { state: { results: data } });
                setError('')
            }
        })
        .catch(error => {
            console.error('error');
            setError('')
        })

    }

    return (
        <div className='name'>
            <form onSubmit={handleSubmit}>
                <label>Please enter the titles of 3 books that you rate highly:</label>
                <input required value={book1} onChange={handleBook1Change} placeholder="book 1"></input>
                <input required value={book2} onChange={handleBook2Change} placeholder="book 2"></input>
                <input required value={book3} onChange={handleBook3Change} placeholder="book 3"></input>
                <button type="submit"> Get Recommendations</button>
            </form>
            {error1 && <div className='error_message'>{error1}</div>}
        </div>
    )
    
}

export default AddBook
