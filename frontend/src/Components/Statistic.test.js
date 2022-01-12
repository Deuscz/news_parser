import React from "react";
import { render, unmountComponentAtNode } from "react-dom";
import { act } from "react-dom/test-utils";
import { DbStatisticComponent, FileStatisticComponent } from './Statistic'

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



it("renders database statistic", () => {
    act(() => {
        const testStatistic = {
            source_url: "https://www.google.com/",
            health_articles: 5,
            politics_articles: 5,
            last_news_date: "2022.01.01",
        }
        render(<DbStatisticComponent statistic={testStatistic} />, container);
    });
    let tds = container.querySelectorAll("td")
    expect(tds[0].innerHTML).toBe("https://www.google.com/");
    expect(tds[1].innerHTML).toBe("5");
    expect(tds[2].innerHTML).toBe("5");
    expect(tds[3].innerHTML).toBe("2022.01.01");

});

it("renders file statistic", () => {
    act(() => {
        const testStatistic = {
            number_of_files: 2,
            min_date: "2022.01.01",
            max_date: "2022.01.02",
        }
        render(<FileStatisticComponent statistic={testStatistic} />, container);
    });
    let tds = container.querySelectorAll("td")
    expect(tds[0].innerHTML).toBe("2");
    expect(tds[1].innerHTML).toBe("2022.01.01");
    expect(tds[2].innerHTML).toBe("2022.01.02");

});