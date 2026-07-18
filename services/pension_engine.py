def calculate_pension_projection(
    current_age,
    retirement_age,
    current_pension,
    monthly_contribution,
    annual_return,
):

    years_remaining = retirement_age - current_age

    projected_value = current_pension

    yearly_contribution = monthly_contribution * 12

    yearly_data = []

    for year in range(1, years_remaining + 1):

        projected_value += yearly_contribution

        projected_value *= (1 + annual_return / 100)

        yearly_data.append({
            "Year": year,
            "Age": current_age + year,
            "Projected Pension": round(projected_value, 2)
        })

    return yearly_data