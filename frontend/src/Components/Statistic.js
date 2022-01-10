import React, {useEffect} from 'react';
import {useSelector, useDispatch} from 'react-redux';
import {loadStatistics} from '../Actions'
import {Table} from "react-bootstrap";


export function Statistics(props) {
    const statistics = useSelector(state => state.statisticsReducer.statistics);
    const loading = useSelector(state => state.statisticsReducer.loading);
    const dispatch = useDispatch();
    let dbStatistics, sportArticlesRecords;
    let loadData = () => {
        dispatch(loadStatistics());
    }
    useEffect(() => {
        loadData();
    }, []);
    if (typeof statistics.db_statistics !== 'undefined') {
        dbStatistics = statistics.db_statistics.map((statistic, index) => {
            return <DbStatisticComponent statistic={statistic} history={props.history} key={index}/>
        });
    }
    if (typeof statistics.file_statistics !== 'undefined') {
        sportArticlesRecords = [statistics.file_statistics].map((statistic, index) => {
            return <FileStatisticComponent statistic={statistic} history={props.history} key={index}/>
        });
    }
    if (typeof dbStatistics !== 'undefined' || typeof sportArticlesRecords !== 'undefined') {
        return (<>
                <div style={{margin: 5}}>
                    <div><h3>Database sources statistics</h3></div>
                    <Table variant="striped">
                        <thead>
                        <tr>
                            <th scope="col">URL</th>
                            <th scope="col">Health articles</th>
                            <th scope="col">Politics articles</th>
                            <th scope="col">Last news date</th>
                        </tr>
                        </thead>
                        <tbody>
                        {dbStatistics}
                        </tbody>
                    </Table>
                    <h3>{"There is no records in database" ? !dbStatistics : ""}</h3>
                    <div><h3>Sport files statistics</h3></div>
                    <Table>
                        <thead>
                        <tr>
                            <th scope="col">Number of files</th>
                            <th scope="col">Start Date</th>
                            <th scope="col">End Date</th>
                        </tr>
                        </thead>
                        <tbody>
                        {sportArticlesRecords}
                        </tbody>
                    </Table>
                    <h3>{"There is no records in files" ? !sportArticlesRecords : ""}</h3>
                </div>
            </>
        );
    } else {
        return (<div style={{width: 300, height: 300, padding: 20}}>Loading...</div>);
    }
}


function DbStatisticComponent({statistic, history}) {
    return (
        <tr>
            <td>{statistic.source_url}</td>
            <td>{statistic.health_articles}</td>
            <td>{statistic.politics_articles}</td>
            <td>{statistic.last_news_date}</td>
        </tr>
    );
}

function FileStatisticComponent({statistic, history}) {
    return (
        <tr>
            <td>{statistic.number_of_files}</td>
            <td>{statistic.min_date}</td>
            <td>{statistic.max_date}</td>
        </tr>

    );
}