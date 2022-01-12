import React from "react";
import { render, unmountComponentAtNode } from "react-dom";
import { act } from "react-dom/test-utils";
import App from './App'
import { BrowserRouter } from "react-router-dom";
import { Provider } from 'react-redux';
import { store } from "../Store";

let container = null;
beforeEach(() => {
    container = document.createElement("div");
    document.body.appendChild(container);
});

afterEach(() => {
    unmountComponentAtNode(container);
    container.remove();
    container = null;
});



it("renders app", () => {
    act(() => {
        render(<BrowserRouter><Provider store={store}><App /></Provider></BrowserRouter>, container);
    });
    let navs = container.querySelectorAll('a');
    expect(navs[0].textContent).toBe("Articles");
    expect(navs[1].textContent).toBe("Statistics");
    expect(navs[2].textContent).toBe("Add news");

});
