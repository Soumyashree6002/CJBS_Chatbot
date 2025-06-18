FIELD_CONTEXTS = {
    "user": """Please answer the following based only on trusted sources:
- "User" refers to the **type of entity using the satellite**, such as Government, Military, Civil, Commercial, or a mix.
- Do **not** confuse with terms like 'user beams' or 'user base'. We are looking for institutional or stakeholder type.
- Give short, precise answers. Avoid repeating long descriptions.
- If info is unavailable, return: Data not available.""",

    "purpose": """Provide the **primary purpose** of the satellite based on trusted sources.
- This refers to whether the satellite is used for Communications, Earth Observation, Navigation, Space Science, or Technology Development.
- Avoid technical jargon or function-level details like transponders or sensors.
- Only mention the **broad category** of purpose (e.g., Earth Observation).""",

    "sdg": """Based on the real-world use cases and social or environmental impacts of the satellite, which UN Sustainable Development Goals (SDGs) does it support?
- Give 1-3 relevant SDG numbers and explain briefly.
- Then infer the corresponding SDG category from:
  - Economic (SDG 1, 2, 8, 10)
  - Social (SDG 3, 4, 5, 12, 16, 17)
  - Environmental (SDG 6, 7, 11, 13, 14, 15)
  - Innovation (SDG 9)
- Only include SDGs actually supported by the satellite's impact or technology.""",

    "user category number": """Return the corresponding numeric code for the user type:
- Military: 1
- Civil: 2
- Commercial: 3
- Government: 4
- Mix: 5
If unsure, return: Data not available.""",

    "purpose category number": """Return the corresponding numeric code for the satellite's purpose:
- Communications: 1
- Earth Observation: 2
- Navigation: 3
- Space Science: 4
- Technology Development: 5
If unsure, return: Data not available.""",

    "sdg category": "Return only the SDG **category** (e.g., Economic, Social, Environmental, Innovation) based on supported SDG numbers.",
    "sdg category identification number": "Return the SDG **category number** (1: Economic, 2: Social, 3: Environmental, 4: Innovation).",
}

# Field-specific query overrides for better search results
FIELD_QUERY_OVERRIDES = {
    "sdg category": "how {satellite} supports sustainable development goals",
    "sdg category identification number": "which SDGs are supported by {satellite}",
    "sdg description": "what sustainable or developmental benefits does {satellite} provide",
    "frugal": "was {satellite} developed using frugal innovation",
    "development cost efficiency (0/1)": "was {satellite} developed cost-effectively",
    "operational cost efficiency (0/1)": "does {satellite} have low operational costs",
    "labour cost efficiency (0/1)": "was {satellite} developed using low labour costs",
    "frugal innovation design (0/1)": "is there frugal innovation in the design of {satellite}",
    "return on investment": "what value did {satellite} generate for its cost",
    "return on investment description": "describe the return on investment of {satellite}",
}
