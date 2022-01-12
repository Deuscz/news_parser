import React, { useEffect } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { loadArticles, startParsing } from '../Actions';
import { Table, TableHead, TableBody, Alert, Paper, Button, ButtonGroup, } from '@mui/material';
import { StyledTableCell, StyledTableRow } from './Tables';

export function Articles(props) {
    const articles = useSelector(state => state.articlesReducer.articles);
    const loading = useSelector(state => state.parsingReducer.loading);
    const dispatch = useDispatch();
    let articlesRecords, sportArticlesRecords, component;
    let ifparsing = (loading && (articles.articles || articles.sport_articles)) ? <Alert severity="info">Loading new articles...</Alert> : <Alert severity="success">Articles were successfully loaded!</Alert>;
    useEffect(() => {
        let loadData = () => {
            dispatch(loadArticles());
        };
        loadData();
    }, []);
    if (articles.articles !== undefined) {
        articlesRecords = articles.articles.map((article, index) => {
            return <ArticleComponent article={article} key={index} />
        });
    }
    if (articles.sport_articles !== undefined) {
        sportArticlesRecords = articles.sport_articles.map((article, index) => {
            return <ArticleComponent article={article} key={index} />
        });
    }
    let check = (articles.sport_articles !== undefined) || (articles.articles !== undefined) ? ((articles.sport_articles.length !== 0) || (articles.articles.length !== 0)) : false;
    if (check) {
        component = (<>
            <Paper sx={{ width: '99%', margin: '10px' }}>
                <ButtonsComponent />
                <h3>{ifparsing}</h3>
                <Table stickyHeader aria-label="sticky table" >
                    <TableHead sx={{ backgroundColor: 'red' }}>
                        <StyledTableRow>
                            <StyledTableCell scope="col">Name, url</StyledTableCell>
                            <StyledTableCell scope="col">Category</StyledTableCell>
                            <StyledTableCell scope="col">Title</StyledTableCell>
                            <StyledTableCell scope="col">Published</StyledTableCell>
                        </StyledTableRow>
                    </TableHead>
                    <TableBody>
                        {articlesRecords}
                        {sportArticlesRecords}
                    </TableBody>
                </Table>
            </Paper>
        </>
        );
    } else {
        component = (<>
            <Paper sx={{ width: '99%', margin: '10px' }}>
                <ButtonsComponent />
                <h3>{ifparsing}</h3>
                <div style={{ width: 300, height: 300, padding: 20 }}>There are no articles for today yet</div>
            </Paper>
        </>);
    }

    return component;
}

export function ArticleComponent({ article }) {
    return (
        <StyledTableRow>
            <StyledTableCell><a href={article.url}>{article.source_name}</a></StyledTableCell>
            <StyledTableCell>{article.category}</StyledTableCell>
            <StyledTableCell>{article.title}</StyledTableCell>
            <StyledTableCell>{article.published_date}</StyledTableCell>
        </StyledTableRow>

    );
}

export function ButtonsComponent() {
    const dispatch = useDispatch();
    return (
        <ButtonGroup variant="contained" aria-label="outlined">
            <Button color="info" size="medium" onClick={() => dispatch(startParsing())}>Parse Articles</Button>
            <Button color="success" onClick={() => dispatch(loadArticles())}>Refresh News</Button>
        </ButtonGroup>
    )
}