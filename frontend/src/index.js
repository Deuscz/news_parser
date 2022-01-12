import React from 'react';
import ReactDOM from 'react-dom';
import { Provider } from 'react-redux';
import './index.css';
import reportWebVitals from './reportWebVitals';
import { BrowserRouter } from "react-router-dom";
import { store, ConnectedApp } from "./Store";

ReactDOM.render(
    <React.StrictMode>
        <BrowserRouter><Provider store={store}><ConnectedApp /></Provider></BrowserRouter>
    </React.StrictMode>,
    document.getElementById('root')
);

reportWebVitals();
