def map_supply_plan(data: dict) -> dict:
    return {
        "plan_name": data.get("PlanName"),
        "plan_id": data.get("PlanId"),
        "plan_type": data.get("PlanType"),
        "plan_status": data.get("PlanStatus"),
        "start_date": data.get("PlanHorizonStartDate"),
        "end_date": data.get("CutoffDate"),
        "assignment_set": data.get("AssignmentSetName")
    }
