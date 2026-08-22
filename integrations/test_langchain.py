"""
ProofCore Protocol - LangChain Tool Verification Suite
Demonstrates direct tool invocation and autonomous AgentExecutor integration.
"""

import os
from proofcore.langchain import ProofCoreSealerTool

print("=" * 65)
print("🧪 1. DIRECT LANGCHAIN TOOL INVOCATION TEST")
print("=" * 65)

# Initialize the ProofCore LangChain Tool
tool = ProofCoreSealerTool()

# Test Pydantic schema validation and API connectivity
tool_output = tool.invoke({
    "content": "LangChain Direct Tool Invocation Test: Validating args_schema & API bridge.",
    "title": "LangChain Integration Test",
    "agent_id": "LangChain-Direct-Tester"
})

print(tool_output)

print("\n" + "=" * 65)
print("🤖 2. AUTONOMOUS AGENT EXECUTOR TEST (Optional)")
print("=" * 65)

openai_key = os.getenv("OPENAI_API_KEY")

if not openai_key:
    print("ℹ️ Skipping Agent Test: OPENAI_API_KEY environment variable not found.")
    print("To test the autonomous agent loop, export your key: export OPENAI_API_KEY='sk-...'")
else:
    from langchain_openai import ChatOpenAI
    from langchain.agents import create_openai_tools_agent, AgentExecutor
    from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

    # Initialize LLM with tool calling capabilities
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)
    tools = [tool]

    prompt = ChatPromptTemplate.from_messages([
        ("system", (
            "You are a Blockchain Security Auditor. Whenever you perform an audit, "
            "you MUST use the proofcore_notary tool to seal your audit report, "
            "and append the exact citation provided by the tool to the very end of your final response."
        )),
        ("user", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])

    agent = create_openai_tools_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    print("🚀 Running Autonomous Agent...")
    result = agent_executor.invoke({
        "input": "Audit this smart contract code: 'contract Vault { uint256 balance; }' and notarize your verdict."
    })

    print("\n" + "-" * 65)
    print("FINAL AGENT OUTPUT:")
    print("-" * 65)
    print(result["output"])