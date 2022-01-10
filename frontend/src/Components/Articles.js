import React, { useEffect } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { loadArticles, startParsing } from '../Actions'
import { Button, Row, Col, Table } from "react-bootstrap";


export function Articles(props) {
    const articles = useSelector(state => state.articlesReducer.articles);
    const loading = useSelector(state => state.parsingReducer.loading);
    const dispatch = useDispatch();
    let articlesRecords, sportArticlesRecords;
    let ifparsing = loading ? "Loading new articles..." : "";
    let loadData = () => {
        dispatch(loadArticles());
    }
    useEffect(() => {
        loadData();
    }, []);
    if (typeof articles.articles !== 'undefined') {
        articlesRecords = articles.articles.map((article, index) => {
            return <ArticleComponent article={article} key={index} />
        });
    }
    if (typeof articles.sport_articles !== 'undefined') {
        sportArticlesRecords = articles.sport_articles.map((article, index) => {
            return <SportArticleComponent article={article} key={index} />
        });
    }
    if (typeof articlesRecords !== 'undefined' || typeof sportArticlesRecords !== 'undefined') {
        return (<>
            <Row>
                <Button as={Col} variant="primary" onClick={() => dispatch(startParsing())}>Parse Articles</Button>
                <Button as={Col} variant="info" onClick={() => dispatch(loadArticles())}>Refresh News</Button>
            </Row>
            <h3>{ifparsing}</h3>
            <div>
                <Table className="table table-striped">
                    <thead>
                        <tr>
                            <th scope="col">Name, url</th>
                            <th scope="col">Category</th>
                            <th scope="col">Title</th>
                            <th scope="col">Published</th>
                        </tr>
                    </thead>
                    <tbody>
                        {articlesRecords}
                        {sportArticlesRecords}
                    </tbody>
                </Table>
            </div>
            <h3>{!(articlesRecords || sportArticlesRecords) ? "There are no articles for today yet" : ""}</h3>
        </>
        );
    } else {
        return (<div style={{ width: 300, height: 300, padding: 20 }}>Loading...</div>);
    }
}


function SportArticleComponent({ article }) {
    return (
        <tr>
            <td><a href={article.url}>{article.source_name}</a></td>
            <td>{article.category}</td>
            <td>{article.title}</td>
            <td>{article.published_date}</td>
        </tr>

    );
}

function ArticleComponent({ article }) {
    return (
        <tr>
            <td><a href={article.url}>{article.source_name}</a></td>
            <td>{article.category}</td>
            <td>{article.title}</td>
            <td>{article.published_date}</td>
        </tr>

    );
}