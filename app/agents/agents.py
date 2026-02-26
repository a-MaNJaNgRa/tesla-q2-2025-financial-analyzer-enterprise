mkdir -p app/agents
cat > app/agents/agents.py << 'EOF'
from dotenv import load_dotenv
from crewai import Agent
from langchain_openai import ChatOpenAI

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.1)

financial_analyst = Agent(
    role="Senior Tesla Financial Analyst",
    goal="Analyze the provided Tesla Q2 2025 document text and give accurate insights.",
    backstory="You are a top-tier Tesla analyst. Use only the provided document text.",
    llm=llm,
    verbose=True,
    max_iter=12,
    allow_delegation=True
)

verifier = Agent(
    role="Financial Document Verifier",
    goal="Confirm the document is Tesla's official Q2 2025 Update.",
    backstory="You verify corporate financial filings.",
    llm=llm,
    verbose=True,
    max_iter=4
)

investment_advisor = Agent(
    role="Institutional Investment Advisor",
    goal="Give a clear Buy/Hold/Sell recommendation for TSLA.",
    backstory="You manage a large Tesla-focused fund.",
    llm=llm,
    verbose=True
)

risk_assessor = Agent(
    role="Risk Assessment Expert",
    goal="Identify all material risks from the Q2 2025 document.",
    backstory="Former SEC filing examiner.",
    llm=llm,
    verbose=True
)
EOF
