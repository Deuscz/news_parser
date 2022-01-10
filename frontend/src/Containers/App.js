import React from 'react';
import './App.css';
import {Routes, Route, Link, NavLink} from "react-router-dom";
import {Articles} from "../Components/Articles";
import {Statistics} from "../Components/Statistic";
import {NewSource} from "../Components/NewSource";


function App(props) {
    return (<>
        <div className="navbar navbar-expand-lg navbar-dark bg-dark">
            <div className="collapse navbar-collapse" id="navbarSupportedContent">
                <ul className="navbar-nav mr-auto">
                    <li className="nav-item">
                        <NavLink to=""><a className="nav-link">Articles</a></NavLink>
                    </li>
                    <li className="nav-item">
                        <Link to="statistic"><a className="nav-link">Statistics</a></Link>
                    </li>
                    <li className="nav-item">
                        <Link to="new-source"><a className="nav-link">Add news</a></Link>
                    </li>

                </ul>

            </div>
        </div>
        <Routes>
            <Route path="" element={<Articles/>}/>
            <Route path="statistic" element={<Statistics/>}/>
            <Route path="new-source" element={<NewSource/>}/>
        </Routes>
    </>);
}

export default App;
