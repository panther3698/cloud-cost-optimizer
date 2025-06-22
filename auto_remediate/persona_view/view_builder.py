from kpi_mapper.kpi_translator import KPI_TRANSLATION_MAP

ROLE_KPI_MAP = {
    'FinOps': ['PreTaxCost'],
    'CloudOps': [
        'CPUUtilization', 'MemoryUtilization',
        'DiskReadOps', 'DiskWriteOps', 'NetworkIn', 'NetworkOut'
    ],
    'CIO': ['PreTaxCost'],  # Add more as needed for summary
}

def build_persona_view(role: str, data: dict) -> dict:
    """
    Filters and structures KPI data based on the user's role.
    Args:
        role (str): The persona role (FinOps, CloudOps, CIO).
        data (dict): Raw KPI data with metric keys matching KPI_TRANSLATION_MAP.
    Returns:
        dict: Structured dictionary with user-friendly labels and values.
    """
    role = role.strip()
    kpis = ROLE_KPI_MAP.get(role, [])
    result = {}
    for kpi in kpis:
        if kpi in data and kpi in KPI_TRANSLATION_MAP:
            label = KPI_TRANSLATION_MAP[kpi]['label']
            value = data[kpi]
            result[label] = value
    return result
