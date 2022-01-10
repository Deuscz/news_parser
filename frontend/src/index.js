import React from 'react';
import ReactDOM from 'react-dom';
import { Provider } from 'react-redux';
import './index.css';
import reportWebVitals from './reportWebVitals';
import {BrowserRouter} from "react-router-dom";
import {store, ConnectedApp} from "./Store";

ReactDOM.render(
    <React.StrictMode>
        <Provider store={store}><BrowserRouter><ConnectedApp/></BrowserRouter></Provider>
    </React.StrictMode>,
    document.getElementById('root')
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
//
// import React from 'react';
// import { Provider } from 'react-redux';
// import configureStore from './Store/index';
// import ReactDOM from 'react-dom';
// import './index.css';
// import App from './Containers/App';
// import reportWebVitals from './reportWebVitals';
// import 'bootstrap/dist/css/bootstrap.min.css';
// import {BrowserRouter} from "react-router-dom";
// const store = configureStore();
//
// ReactDOM.render(
//     <React.StrictMode>
//         <Provider store={store}><BrowserRouter><App /></BrowserRouter></Provider>
//     </React.StrictMode>,
//     document.getElementById('root')
// );
//
// // If you want to start measuring performance in your app, pass a function
// // to log results (for example: reportWebVitals(console.log))
// // or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
// reportWebVitals();
