mkdir -p app/services
cat > app/services/analyzer_service.py << 'EOF'
from langchain_community.document_loaders import PyPDFLoader
from crewai import Crew, Process
from app.agents.agents import financial_analyst, verifier, investment_advisor, risk_assessor
from app.tasks.tasks import verify_task, analyze_task, investment_task, risk_task
from app.utils.openai_retry import call_with_retry

async def analyze_pdf(file_path: str, query: str) -> str:
    loader = PyPDFLoader(file_path)
    pages = loader.load()
    full_text = "\n\n".join([p.page_content for p in pages])
    full_text = full_text.replace("\n\n\n", "\n\n").strip()[:90000]

    crew = Crew(
        agents=[financial_analyst, verifier, investment_advisor, risk_assessor],
        tasks=[verify_task, analyze_task, risk_task, investment_task],
        process=Process.sequential,
        verbose=1,
    )

    result = await call_with_retry(
        crew.kickoff,
        inputs={"query": query, "document_text": full_text}
    )
    return str(result)
EOF
