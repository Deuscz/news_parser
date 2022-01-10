import {createStore, applyMiddleware} from 'redux'
import {put, call, takeEvery} from 'redux-saga/effects';
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

// sagaMiddleware.run(watchFetchStatistics);

export const ConnectedApp = connect((state) => {
    console.log(state);
    return state;
})(App);
sagaMiddleware.run(watchAll);
// import { createStore,applyMiddleware } from 'redux'
// import thunk from 'redux-thunk';
// import {rootReducer} from '../Reducer'
// export default function configureStore(initialState) {
//     const createStoreWithMiddleware = applyMiddleware(
//         thunk
//     )(createStore);
//     const store = createStoreWithMiddleware(rootReducer);
//     return store;
// }