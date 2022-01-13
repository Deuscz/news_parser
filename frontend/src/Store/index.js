import {createStore, applyMiddleware} from 'redux'
import createSagaMiddleware from 'redux-saga'
import {rootReducer} from "../Reducer";
import {watchAll} from '../Actions'
import {connect} from "react-redux";
import App from '../Containers/App';

const sagaMiddleware = createSagaMiddleware();
export const store = createStore(
    rootReducer,
    applyMiddleware(sagaMiddleware)
);


export const ConnectedApp = connect((state) => {
    return state;
})(App);
sagaMiddleware.run(watchAll);