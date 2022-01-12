import React from "react";
import { render, unmountComponentAtNode } from "react-dom";
import { act } from "react-dom/test-utils";
import { CategoryComponent, NewSource } from './NewSource'
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



it("renders category selector", () => {
    act(() => {
        render(<CategoryComponent />, container);
    });
    expect(container.textContent).toBe(`Category​​`);
});

it("renders form", () => {
    act(() => {
        render(<Provider store={store}><NewSource /></Provider>, container);
    });
    let textFields = container.querySelectorAll("span");
    expect(textFields[1].textContent).toBe("Source name *");
    expect(textFields[3].textContent).toBe("Link to source *");
    expect(textFields[5].textContent).toBe("Link to rss feed *");
});