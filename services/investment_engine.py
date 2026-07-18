def simulate_investment(
    initial_investment,
    monthly_investment,
    annual_return,
    years,
):

    portfolio = initial_investment

    results = []

    for year in range(1, years + 1):

        portfolio += monthly_investment * 12
        portfolio *= (1 + annual_return / 100)

        results.append({
            "Year": year,
            "Portfolio Value": round(portfolio, 2)
        })

    return results