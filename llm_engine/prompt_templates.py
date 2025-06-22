prompt_templates = {
    "explain_cost_spikes": {
        "persona": "{persona}",
        "template": (
            "As a {persona}, analyze the recent cost spike in the cloud bill. "
            "Provide a clear explanation of the main drivers and suggest possible causes."
        )
    },
    "identify_idle_resources": {
        "persona": "{persona}",
        "template": (
            "As a {persona}, review the current cloud environment and identify any idle or underutilized resources. "
            "List them with reasons why they are considered idle."
        )
    },
    "recommend_savings": {
        "persona": "{persona}",
        "template": (
            "As a {persona}, recommend actionable steps to optimize cloud costs and maximize savings. "
            "Prioritize recommendations based on impact and feasibility."
        )
    }
}