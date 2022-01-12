import React from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { startSubmit } from '../Actions'
import { Alert, Button, TextField, FormControl, Paper, Select, MenuItem, Box, InputLabel, Grid } from '@mui/material';
import { CATEGORIES } from '../Constants';


export function NewSource(props) {
    const dispatch = useDispatch();
    const errors = useSelector((state) => state.formReducer.errors);
    const status = useSelector((state) => state.formReducer.status)

    let onSubmitHandler = (e) => {
        e.preventDefault();
        dispatch(startSubmit({
            name: e.target.name.value,
            url: e.target.url.value,
            source_link: e.target.source_link.value,
            category: e.target.category.value,
        }));
    }



    return (<Paper sx={{ width: '99%', margin: '10px' }}>
        {status === "SUCCEDED" ? <Alert severity="success">Form was submited successfully!</Alert> : null}
        {status === "FAILED" ? <Alert severity="error">Form has some errors!</Alert> : null}
        {status === "OK" ? <Alert severity="info">Use this form to add news source!</Alert> : null}
        <FormControl fullWidth sx={{ m: 2 }}>
            <form onSubmit={onSubmitHandler}>
                <Grid container>
                    <TextField required label="Source name" name="name" placeholder="name" sx={{ m: 2 }}></TextField>
                    {(errors.name !== undefined) ? <Alert sx={{ m: 2, width: 600 }} severity="error" id='errors'>{errors.name}</Alert> : null}
                </Grid>
                <Grid container>
                    <TextField required label="Link to source" name="url" placeholder="link" sx={{ m: 2 }}></TextField>
                    {(errors.url !== undefined) ? <Alert sx={{ m: 2, width: 600 }} severity="error" id='errors'>{errors.url}</Alert> : null}

                </Grid>
                <Grid container>
                    <TextField required label="Link to rss feed" name="source_link" placeholder="source link" sx={{ m: 2 }}></TextField>
                    {(errors.source_link !== undefined) ? <Alert sx={{ m: 2, width: 600 }} severity="error" id='errors'>{errors.source_link}</Alert> : null}
                </Grid>

                <Grid container>
                    <CategoryComponent />
                    {(errors.category !== undefined) ? <Alert sx={{ m: 2, width: 600 }} severity="error" id='errors'>{errors.category}</Alert> : null}
                </Grid>
                <Button sx={{ m: 2, width: 200 }} type='submit' variant="outlined">Confirm</Button>
            </form>
        </FormControl>
    </Paper>);
}


export function CategoryComponent() {
    const [category, setCategory] = React.useState('');

    const handleChange = (event) => {
        setCategory(event.target.value);
    };
    return (
        <Box sx={{ minWidth: 120, m: 2, width: 600 }}>
            <FormControl fullWidth>
                <InputLabel id="demo-simple-select-label">Category</InputLabel>
                <Select
                    labelId="category"
                    name="category"
                    value={category}
                    onChange={handleChange}
                >
                    {CATEGORIES.map((category, index) => {
                        return <MenuItem value={category} key={index}>{category}</MenuItem>
                    })}
                </Select>
            </FormControl>
        </Box>
    );
}