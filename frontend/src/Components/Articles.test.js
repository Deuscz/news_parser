import React from "react";
import { render, unmountComponentAtNode } from "react-dom";
import { act } from "react-dom/test-utils";
import { ArticleComponent } from './Articles'

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



it("renders article", () => {
    act(() => {
        const testArticle = {
            url: "https://www.google.com/",
            source_name: "Test",
            category: "Test",
            title: "Test",
            published_date: "2022.01.01",
        }
        render(<ArticleComponent article={testArticle} />, container);
    });
    let tds = container.querySelectorAll("td")
    expect(tds[0].innerHTML).toBe("<a href=\"https://www.google.com/\">Test</a>");
    expect(tds[1].innerHTML).toBe("Test");
    expect(tds[2].innerHTML).toBe("Test");
    expect(tds[3].innerHTML).toBe("2022.01.01");

});