def validate_llm_output(llm_output: dict) -> dict:
    if "error" in llm_output:
        return {"status": "STOP", "message": "Unable to understand request"}

    if llm_output.get("intent") != "GET_SUPPLY_PLAN":
        return {"status": "STOP", "message": "Unsupported request"}

    return {"status": "PROCEED"}

    # plan_id = llm_output.get("planId")

    # if not isinstance(plan_id, int) or plan_id <= 0:
    #     return {"status": "ASK_USER", "message": "Invalid Plan ID"}

    # return {"status": "PROCEED", "planId": plan_id}
