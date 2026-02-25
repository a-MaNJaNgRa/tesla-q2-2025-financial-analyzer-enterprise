from crewai import Agent
from langchain_openai import ChatOpenAI
from app.core.config import get_settings

settings = get_settings()

llm = ChatOpenAI(
    api_key=settings.OPENAI_API_KEY,
    model="gpt-4o-mini",
    temperature=0.2,
)


financial_analyst = Agent(
    role="Senior Financial Analyst",
    goal="Analyze financial documents and extract meaningful insights",
    backstory=(
        "You are an experienced Wall Street financial analyst "
        "with deep expertise in quarterly earnings reports."
    ),
    llm=llm,
    verbose=True,
)

verifier = Agent(
    role="Financial Data Verifier",
    goal="Verify correctness of extracted financial information",
    backstory="You double-check financial statements for accuracy and consistency.",
    llm=llm,
    verbose=True,
)

investment_advisor = Agent(
    role="Investment Advisor",
    goal="Provide strategic investment insights",
    backstory="You provide professional investment-grade insights based on financial data.",
    llm=llm,
    verbose=True,
)

risk_assessor = Agent(
    role="Risk Analyst",
    goal="Identify risks and red flags in financial reports",
    backstory="You specialize in detecting financial, operational, and macroeconomic risks.",
    llm=llm,
    verbose=True,
)