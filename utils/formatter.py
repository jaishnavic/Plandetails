def format_plan_for_user(plan: dict) -> str:
    return f"""
Supply Plan Details

Plan Name: {plan.get('plan_name', 'N/A')}
Plan ID: {plan.get('plan_id', 'N/A')}
Plan Type: {plan.get('plan_type', 'N/A')}
Status: {plan.get('plan_status', 'N/A')}
Assignment Set: {plan.get('assignment_set', 'N/A')}
Duration: {plan.get('start_date', 'N/A')} to {plan.get('end_date', 'N/A')}
"""
