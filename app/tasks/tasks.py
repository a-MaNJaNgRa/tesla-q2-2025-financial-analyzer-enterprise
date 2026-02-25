from crewai import Task

verify_task = Task(
    description=(
        "Review the provided Tesla Q2 2025 financial document text. "
        "Verify the correctness and consistency of revenue, net income, "
        "EPS, margins, cash flow, and guidance figures."
    ),
    expected_output=(
        "A structured verification summary highlighting confirmed values "
        "and any inconsistencies found."
    ),
)

analyze_task = Task(
    description=(
        "Perform a comprehensive financial analysis of Tesla Q2 2025 results. "
        "Analyze revenue growth, profitability trends, operating margins, "
        "cash flow health, and forward guidance."
    ),
    expected_output=(
        "A structured financial analysis including key metrics, trend insights, "
        "and strategic interpretation."
    ),
)

risk_task = Task(
    description=(
        "Identify and evaluate financial, operational, regulatory, "
        "and macroeconomic risks in Tesla Q2 2025 results."
    ),
    expected_output=(
        "A structured risk assessment listing major and minor risk factors "
        "with severity evaluation."
    ),
)

investment_task = Task(
    description=(
        "Provide an investment recommendation based on the financial analysis "
        "and risk assessment. Consider valuation context and long-term outlook."
    ),
    expected_output=(
        "A professional investment summary including bullish factors, bearish "
        "factors, and a balanced conclusion."
    ),
)