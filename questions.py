sheet1_fields = [
    "ALTITUDE",
    "ORBITAL LIFE YEARS",
    "Launch Orbit Classification (ISRO)",
    "No. of payloads",
    "Type of Satellite",
    "Satellite Application Description",
    "Sensor Specifications",
    "Spectral Bands",
    "Spatial Resolution",
    "Technological breakthroughs",
    "Max Launch Mass of Vehicle to LEO (Kg)",
    "Actual Launch Mass Carried by the Vehicle (Kg)",
    "LAUNCH SUCCESS (1) / FAILURE (0)",
    "VEHICLE RESUABILITY (0/1)",
    "Vehicle Resubaility Details"
]

sheet2_fields = [
    "User",
    "User Category Number",
    "User Description",
    "Purpose",
    "Purpose Category Number",
    "Purpose Description",
    "SDG Category",
    "SDG Category Identification Number",
    "SDG Description",
    "Frugal",
    "Development Cost Efficiency (0/1)",
    "Development Cost Efficiency Description",
    "Operational Cost Efficiency (0/1)",
    "Operational Cost Efficiency Description",
    "Labour Cost Efficiency (0/1)",
    "Labour Cost Efficiency Description",
    "Frugal Innovation Design (0/1)",
    "Frugal Innovation Design Description",
    "Return on Investment",
    "Return on Investment Description"
]

# Mappings
user_category_map = {
    "Military": 1,
    "Civil": 2,
    "Commercial": 3,
    "Government": 4,
    "Mix": 5
}

purpose_category_map = {
    "Communications": 1,
    "Earth Observation": 2,
    "Navigation": 3,
    "Space Science": 4,
    "Technology Development": 5
}

sdg_category_map = {
    "Economic": [1, 2, 8, 10],
    "Social": [3, 4, 5, 12, 16, 17],
    "Environmental": [6, 7, 11, 13, 14, 15],
    "Innovation": [9]
}

sdg_category_number_map = {
    "Economic": 1,
    "Social": 2,
    "Environmental": 3,
    "Innovation": 4
}

sdg_number_to_category = {}
for category, sdgs in sdg_category_map.items():
    for sdg in sdgs:
        sdg_number_to_category[sdg] = category 