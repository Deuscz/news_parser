import React, { useEffect } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { startSubmit } from '../Actions'
import { Table, Form, input, label, Alert } from "react-bootstrap";
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



    return (<div style={{ margin: 5 }}>
            {status=="SUCCEDED" ? <Alert variant="success">Form was submited successfully!</Alert>: null}
            {status=="FAILED" ? <Alert variant="danger">Form has some errors!</Alert>: null}
            {status=="OK" ? <Alert variant="info">Use this form to add news source!</Alert>: null}
        <Form onSubmit={onSubmitHandler}>
            <div class="form-group mb-2">
                <label>Name of source</label>
                <input type="text" className="form-control" name="name" placeholder="name" required="True"></input>
                {(errors.name !== undefined) ? <Alert variant="danger" id='errors'>{errors.name}</Alert> : null }
            </div>
            <div class="form-group mb-2">
                <label>Link to RSS feed</label>
                <input type="text" className="form-control" name="url" placeholder="link" required="True"></input>
                {(errors.url !== undefined)? <Alert variant="danger" id='errors'>{errors.url}</Alert> : null }
            </div>
            <div class="form-group mb-2">
                <label>Link to source</label>
                <input type="text" className="form-control" name="source_link" placeholder="source link" required="True"></input>
                {(errors.source_link !== undefined) ? <Alert variant="danger" id='errors'>{errors.source_link}</Alert> : null }
            </div>
            <div class="form-group mb-2">
                <label>Category</label>
                <select className="form-control" name="category">
                    {CATEGORIES.map((category, index) => {
                        return <CategoryComponent category={category} key={index} />
                    })}
                </select>
                {(errors.category !== undefined) ? <Alert variant="danger" id='errors'>{errors.category}</Alert> : null }
            </div>
            <button type="submit" className="btn btn-primary mb-2">Confirm</button>
        </Form>
    </div>);
}


function CategoryComponent({ category }) {
    return (
        <option>{category}</option>
    )
}