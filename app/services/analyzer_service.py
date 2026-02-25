from langchain_community.document_loaders import PyPDFLoader
from crewai import Crew, Process

from app.agents.agents import (
    financial_analyst,
    verifier,
    investment_advisor,
    risk_assessor,
)

from app.tasks.tasks import (
    verify_task,
    analyze_task,
    risk_task,
    investment_task,
)

from app.utils.openai_retry import call_with_retry


async def analyze_pdf(file_path: str, query: str) -> str:
    """
    Enterprise-grade PDF analysis pipeline.
    - Deterministic text extraction
    - Token-safe trimming
    - Sequential multi-agent workflow
    - Retry-protected execution
    """

    # Load PDF
    loader = PyPDFLoader(file_path)
    pages = loader.load()

    # Combine all pages
    full_text = "\n\n".join([page.page_content for page in pages])

    # Clean excessive whitespace
    full_text = full_text.replace("\n\n\n", "\n\n").strip()

    # Token safety (prevent huge prompts)
    full_text = full_text[:90000]

    # Define Crew workflow
    crew = Crew(
        agents=[
            financial_analyst,
            verifier,
            risk_assessor,
            investment_advisor,
        ],
        tasks=[
            verify_task,
            analyze_task,
            risk_task,
            investment_task,
        ],
        process=Process.sequential,
        verbose=True,
    )

    # Run with retry protection
    result = await call_with_retry(
        crew.kickoff,
        inputs={
            "query": query,
            "document_text": full_text,
        },
    )

    return str(result)