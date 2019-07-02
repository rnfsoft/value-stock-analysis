
Tutorial:
    https://towardsdatascience.com/value-investing-dashboard-with-python-beautiful-soup-and-dash-python-43002f6a97ca

    
    Stock Evaluation
        Have the track records (EPS per year)
        Have efficiency (ROE > 15%) — Net income / shareholder equity
        Determine manipulation (ROA > 7%) — Net income / Total Asset
        Have small long term debt (Long term debt < 5 * total income)
        Low Debt to Equity
        Ability to pay interest: (Interest Coverage Ratio > 3) — EBIT / Interest expenses

    Future/Current Value and Recommendation
        Find EPS Annual Compounded Growth Rate
        Estimate EPS 5 years from now
        Estimate stock price 5 years from now (Stock Price EPS * Average PE)
        Determine target by price today based on returns(discount rate 15%/20%)
        Add margin of safety (Safety net 15%)
        Buy if market price is lower than the marginal price
        Sell if market price is higher than the marginal price

Reference URL:
    https://sladkovm.github.io/webdev/2017/10/16/Deploying-Plotly-Dash-in-a-Docker-Container-on-Digitital-Ocean.html
    https://github.com/sladkovm/docker-flask-gunicorn-nginx
    https://www.learndatasci.com/tutorials/python-finance-part-3-moving-average-trading-strategy/
    https://stackoverflow.com/questions/159720/what-is-the-naming-convention-in-python-for-variable-and-function-names
    https://github.com/plotly/dash/pull/406 # How to change favicon from Dash to custom

Depolyment:

    docker-machine ls
    docker-compose rm -fs
    docker-compose up --build -d
    docker-machine create -d digitalocean --digitalocean-access-token xxxx production


Demo:
    http://www.lostininvestment.com/