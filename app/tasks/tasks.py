mkdir -p app/tasks
cat > app/tasks/tasks.py << 'EOF'
from crewai import Task
from app.agents.agents import financial_analyst, verifier, investment_advisor, risk_assessor

verify_task = Task(
    description="Document text provided. Confirm this is Tesla's official Q2 2025 Update and summarize structure.",
    expected_output="Confirmation + major sections summary.",
    agent=verifier,
)

analyze_task = Task(
    description="Full document text:\n{document_text}\n\nUser query: {query}\nExtract key metrics, YoY changes, highlight Robotaxi, Energy storage, affordable model.",
    expected_output="5-part professional report.",
    agent=financial_analyst,
)

investment_task = Task(
    description="Based on analysis, give clear TSLA Buy/Hold/Sell recommendation.",
    expected_output="Recommendation with supporting metrics.",
    agent=investment_advisor,
)

risk_task = Task(
    description="List top 8 material risks for Tesla investors.",
    expected_output="Numbered list with severity.",
    agent=risk_assessor,
)
EOF
