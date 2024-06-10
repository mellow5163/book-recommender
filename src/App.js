/* eslint-disable no-unused-vars */
//import logo from './logo.svg';
import './App.css';
import Title from './title';
import AddBook from './addBook';
import React, { useState, useEffect } from 'react'
//import axios from "axios"
//import { useNavigate } from 'react-router-dom';

function App() {
// eslint-disable-next-line no-unused-vars
  const [data, setData] = useState([{}])

  /*

  const navigate = useNavigate();

  const handleNavigate = () => {
    navigate('/about');
  };

  */



// eslint-disable-next-line no-unused-vars
  return (
    <div className="App">
      <Title></Title>
      <AddBook></AddBook>
    </div>
  );
}

export default App;
