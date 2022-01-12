import React, { useEffect } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { loadStatistics } from '../Actions'
import { Table, Paper, TableHead, TableBody, TableRow, Alert } from '@mui/material';
import { StyledTableCell, StyledTableRow } from './Tables';

export function Statistics(props) {
    const statistics = useSelector(state => state.statisticsReducer.statistics);
    let dbStatistics, sportArticlesRecords;
    const dispatch = useDispatch();
    useEffect(() => {
        let loadData = () => {
            dispatch(loadStatistics());
        };
        loadData();
    }, []);
    if (statistics.db_statistics !== undefined) {
        dbStatistics = statistics.db_statistics.map((statistic, index) => {
            return <DbStatisticComponent statistic={statistic} history={props.history} key={index} />
        });
    }
    if (statistics.file_statistics !== undefined) {
        sportArticlesRecords = [statistics.file_statistics].map((statistic, index) => {
            return <FileStatisticComponent statistic={statistic} history={props.history} key={index} />
        });
    }
    if (typeof dbStatistics !== 'undefined' || typeof sportArticlesRecords !== 'undefined') {
        return (<>
            <Paper sx={{ width: '99%', overflow: 'hidden', margin: '10px' }}>
                <div><h3>Database sources statistics</h3></div>
                <Table variant="striped">
                    <TableHead>
                        <TableRow sx={{}}>
                            <StyledTableCell scope="col">URL</StyledTableCell>
                            <StyledTableCell scope="col">Health articles</StyledTableCell>
                            <StyledTableCell scope="col">Politics articles</StyledTableCell>
                            <StyledTableCell scope="col">Last news date</StyledTableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {dbStatistics}
                    </TableBody>
                </Table>
                <h3>{!dbStatistics ? <Alert severity="info">There is no records in database</Alert> : ""}</h3>
                <div><h3>Sport files statistics</h3></div>
                <Table>
                    <TableHead>
                        <TableRow>
                            <StyledTableCell scope="col">Number of files</StyledTableCell>
                            <StyledTableCell scope="col">Start Date</StyledTableCell>
                            <StyledTableCell scope="col">End Date</StyledTableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {sportArticlesRecords}
                    </TableBody>
                </Table>
                <h3>{!sportArticlesRecords ? <Alert severity="info">There is no records in files</Alert> : ""}</h3>
            </Paper>
        </>
        );
    } else {
        return (<div style={{ width: 300, height: 300, padding: 20 }}>Loading...</div>);
    }
}


export function DbStatisticComponent({ statistic, history }) {
    return (
        <StyledTableRow>
            <StyledTableCell>{statistic.source_url}</StyledTableCell>
            <StyledTableCell>{statistic.health_articles}</StyledTableCell>
            <StyledTableCell>{statistic.politics_articles}</StyledTableCell>
            <StyledTableCell>{statistic.last_news_date}</StyledTableCell>
        </StyledTableRow>
    );
}

export function FileStatisticComponent({ statistic, history }) {
    return (
        <StyledTableRow>
            <StyledTableCell>{statistic.number_of_files}</StyledTableCell>
            <StyledTableCell>{statistic.min_date}</StyledTableCell>
            <StyledTableCell>{statistic.max_date}</StyledTableCell>
        </StyledTableRow>

    );
}