import * as types from "../Constants";
import { call, put, takeEvery, all } from "redux-saga/effects";


export const loadArticles = () => {
    return { type: types.ARTICLES_LOADING };
};

const loadArticlesSuccess = (data) => {
    return { type: types.ARTICLES_LOADING_SUCCEEDED, payload: data };
};

const loadArticlesError = () => {
    return { type: types.ARTICLES_LOADING_FAILED };
};

export const loadStatistics = () => {
    return { type: types.STATISTICS_LOADING };
};

const loadStatisticsSuccess = (data) => {
    return { type: types.STATISTICS_LOADING_SUCCEEDED, payload: data };
};

const loadStatisticsError = () => {
    return { type: types.STATISTICS_LOADING_FAILED };
};

export const startParsing = () => {
    return { type: types.ARTICLES_START_PARSING };
}

const stopParsingSuccess = () => {
    return { type: types.ARTICLES_PARSING_SUCCEEDED };
}


const stopParsingFail = () => {
    return { type: types.ARTICLES_PARSING_FAILED };
}

export const startSubmit = (data) => {
    return { type: types.START_SUBMIT, payload: data }
}

const stopSubmit = (data) => {
    return { type: types.STOP_SUBMIT, payload: data }
}
const successSubmit = () => {
    return { type: types.SUBMIT_SUCCEDED}
}

export function* watchAll() {
    yield all([
        takeEvery(types.ARTICLES_LOADING, fetchArticlesAsync),
        takeEvery(types.STATISTICS_LOADING, fetchStatisticsAsync),
        takeEvery(types.ARTICLES_START_PARSING, fetchStartParsingAsync),
        takeEvery(types.START_SUBMIT, submitFormAsync)
    ])
}

function* fetchArticlesAsync() {
    try {
        const data = yield call(() => {
            return fetch('/api/v1/articles-list', {
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                }
            }).then(res => res.json())
        });
        yield put(loadArticlesSuccess(data));
    } catch (error) {
        yield put(loadArticlesError());
    }
}

function* fetchStatisticsAsync() {
    try {
        const data = yield call(() => {
            return fetch('/api/v1/statistics', {
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                }
            }).then(res => res.json())
        });
        yield put(loadStatisticsSuccess(data));
    } catch (error) {
        yield put(loadStatisticsError());
    }
}

function* fetchStartParsingAsync() {
    try {
        yield call(() => {
            return fetch('/api/v1/articles-list', {
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                },
                method: 'POST'
            }).then(res => res.json())
        });
        yield put(stopParsingSuccess());
    } catch (error) {
        yield put(stopParsingFail());
    }
}

function* submitFormAsync(data) {
    try {
        const result = yield call(() => {
            return fetch('/api/v1/add_news', {
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                },
                method: 'POST',
                body: JSON.stringify(data.payload)
            }).then(res => res.json())
        });
        console.log(result);
        if (result.errors){
            yield put(stopSubmit(result));
        }else{
            yield put(successSubmit());
        }
    } catch (error) {
        console.log(error)
    }
}