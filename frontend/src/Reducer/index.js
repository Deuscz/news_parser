import { combineReducers } from 'redux'
import * as types from "../Constants";

let articlesState = {
    articles: [],
    loading: false,
    error: false,
};
let statisticsState = {
    statistics: [],
    loading: false,
    error: false,
};
let parsingState = {
    loading: false,
    error: false,
};
let formState = {
    status: "OK",
    errors: [],
}


const articlesReducer = (state = articlesState, action) => {
    switch (action.type) {
        case types.ARTICLES_LOADING:
            return {
                articles: [],
                loading: true,
                error: false,
            };
        case types.ARTICLES_LOADING_SUCCEEDED:
            return {
                articles: action.payload,
                loading: false,
                error: false,
            };
        case types.ARTICLES_LOADING_FAILED:
            return {
                articles: [],
                loading: false,
                error: true,
            };
        default:
            return state;
    }
}

const statisticsReducer = (state = statisticsState, action) => {
    switch (action.type) {
        case types.STATISTICS_LOADING:
            return {
                statistics: [],
                loading: true,
                error: false,
            };
        case types.STATISTICS_LOADING_SUCCEEDED:
            return {
                statistics: action.payload,
                loading: false,
                error: false,
            };
        case types.STATISTICS_LOADING_FAILED:
            return {
                statistics: [],
                loading: false,
                error: true,
            };
        default:
            return state;
    }
}


const parsingReducer = (state = parsingState, action) => {
    switch (action.type) {
        case types.ARTICLES_START_PARSING:
            return {
                loading: true,
                error: false,
            };
        case types.ARTICLES_PARSING_SUCCEEDED:
            return {
                loading: false,
                error: false,
            };
        case types.ARTICLES_PARSING_FAILED:
            return {
                loading: false,
                error: true,
            };

        default:
            return state;
    }
}

const formReducer = (state = formState, action) => {
    switch(action.type){
        case types.START_SUBMIT:
            return {
                status: "OK",
                errors: [],
            };
        case types.STOP_SUBMIT:
            return {status: "FAILED", errors: action.payload.errors};
        case types.SUBMIT_SUCCEDED:
            return {...state, status: "SUCCEDED"}
        default:
            return {
                status: "OK",
                errors: [],
            };
    }
}

export const rootReducer = combineReducers({
    articlesReducer,
    statisticsReducer,
    parsingReducer,
    formReducer
})