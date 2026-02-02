import os
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi import FastAPI, HTTPException, Depends


from llm.prompt import SYSTEM_PROMPT, build_user_prompt
from llm.llm_client import call_llm
from validators.validator import validate_llm_output
from fusion.fusion_client import get_supply_plan
from fusion.response_mapper import map_supply_plan
from utils.formatter import format_plan_for_user
from config import SUPPLY_PLAN_ID


app = FastAPI()

# ---------------- AUTH ----------------
security = HTTPBasic()

def authenticate_user(credentials: HTTPBasicCredentials = Depends(security)):
    if (
        credentials.username == os.getenv("GETPLAN_USERNAME")
        and credentials.password == os.getenv("GETPLAN_PASSWORD")
    ):
        return credentials.username
    raise HTTPException(status_code=401, detail="Unauthorized")


class SupplyPlanRequest(BaseModel):
    query: str

def run_supply_plan_agent(user_input: str) -> str:
    llm_output = call_llm(
        build_user_prompt(user_input)
    )

    print("LLM OUTPUT:", llm_output)

    validation = validate_llm_output(llm_output)

    if validation["status"] != "PROCEED":
        return validation["message"]

    fusion_response = get_supply_plan(SUPPLY_PLAN_ID)

    if "error" in fusion_response:
        return fusion_response["error"]

    mapped = map_supply_plan(fusion_response)

    return format_plan_for_user(mapped)
import asyncio

async def run_supply_plan_agent_async(user_input: str) -> dict:
    # wrap blocking code in thread executor if needed
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, run_supply_plan_agent, user_input)


@app.get("/")
def root():
    return {"message": "Supply Plan Agent is running."}


@app.post("/supply-plan")
async def supply_plan_agent(request: SupplyPlanRequest, username: str = Depends(authenticate_user)):
    user_input = request.query
    response = await run_supply_plan_agent_async(user_input)
    return {"response": response}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("agent_pipeline:app", host="0.0.0.0", port=8003, reload=True)
