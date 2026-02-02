import requests
from config import FUSION_BASE_URL, FUSION_USERNAME, FUSION_PASSWORD

def get_supply_plan(plan_id: int) -> dict:
    url = f"{FUSION_BASE_URL}/fscmRestApi/resources/11.13.18.05/supplyPlans/{plan_id}"

    response = requests.get(
        url,
        auth=(FUSION_USERNAME, FUSION_PASSWORD),
        headers={"Accept": "application/json"}
    )

    if response.status_code == 404:
        return {"error": "Plan not found"}

    if response.status_code in (401, 403):
        return {"error": "Authorization error"}

    if response.status_code >= 500:
        return {"error": "Fusion service unavailable"}

    return response.json()
