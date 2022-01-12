import React from 'react';
import './App.css';
import { Routes, Route, Link, NavLink } from "react-router-dom";
import { Articles } from "../Components/Articles";
import { Statistics } from "../Components/Statistic";
import { NewSource } from "../Components/NewSource";
import Box from '@mui/material/Box';
import Tabs from '@mui/material/Tabs';
import Tab from '@mui/material/Tab';

export default function App() {
    const [value, setValue] = React.useState(0);

    const handleChange = (event, newValue) => {
        setValue(newValue);
    };

    return (
        <Box sx={{ width: '100%', bgcolor: 'background.paper' }}>
            <Tabs value={value} onChange={handleChange} centered>
                <Tab component={Link} to={""} label="Articles" />
                <Tab component={Link} to={"statistic"} label="Statistics" />
                <Tab component={Link} to={"new-source"} label="Add news" />
            </Tabs>
            <Routes>
                <Route path="" element={<Articles />} />
                <Route path="statistic" element={<Statistics />} />
                <Route path="new-source" element={<NewSource />} />
            </Routes>
        </Box>
    );
}