CAFB_TEMPLATE = """You are a specialized content extraction assistant for the Capital Area Food Bank (CAFB).
Your task is to carefully analyze text and extract specific information based on the request.
Always provide your response as a numbered list of distinct items.
Do not generate information not present in the original text.
Focus on information relevant to CAFB's mission of addressing food insecurity.
"""

DEFAULT_EXTRACTION_TEMPLATE = """Extract all {extraction_type} from the following text about CAFB.
Format your response as a numbered list with each item capturing a distinct piece of information.
Be comprehensive and include all relevant information related to {extraction_type}.

TEXT:
{text}

{extraction_type}:
1.
"""

EXTRACTION_CATEGORY_TEMPLATES = {
    "Key Points": """
        Extract all important points from the following text for CAFB program.
        Format your response as a numbered list of distinct important points.
        Each point should be a complete sentence or phrase capturing a single important idea.
        Focus on information about food insecurity, programs, initiatives, and impact.
        Include only factual information present in the text, not inferences.

        TEXT:
        {text}

        KEY POINTS:
    """,

    "Quotes": """
        Extract all direct quotes from the following text.
        Format each quote as a separate list item with attribution if available.
        Ensure quotes are exact and enclosed in quotation marks.
        Include who said the quote if mentioned in the text.
        For quotes from Capital Area Food Bank (CAFB) clients or stakeholders, note their relationship to CAFB.

        TEXT:
        {text}

        QUOTES:
    """,

    "Statistics": """Extract all numerical data, statistics, and metrics from the following text about CAFB program.
        Format your response as a numbered list where each item contains:
        - The specific statistic or measurement
        - Context or meaning of the statistic
        - Time period or date if mentioned
        - Source of the statistic if available

        Focus on statistics related to food insecurity, program impact, funding, or client demographics.
        Convert all written numbers to numerals (e.g., "three million" to "3 million").

        TEXT:
        {text}

        STATISTICS:
    """,

    "Program Impacts": """
        Extract all information about CAFB program impacts and outcomes from the text.
        Format as a numbered list with each item containing:
        - The specific program or initiative name
        - The impact or outcome described
        - Population served or benefiting
        - Time frame if mentioned

        Include both quantitative impacts (numbers) and qualitative impacts (descriptions).

        TEXT:
        {text}

        PROGRAM IMPACTS:
    """,

    "Food Medicine Leadership": """
        Extract all information about CAFB's role and leadership in food as medicine initiatives.
        Format as a numbered list capturing:
        - Specific food as medicine programs or initiatives
        - Partnerships with healthcare organizations
        - Innovation in connecting nutrition to health outcomes
        - Evidence of CAFB's leadership in this space
        - Impact of these initiatives

        TEXT:
        {text}

        FOOD MEDICINE LEADERSHIP:
    """,

    "Barriers Identified": """
        Extract all information about barriers CAFB program clients face in accessing SNAP and food assistance.
        Format as a numbered list where each item:
        - Identifies a specific barrier
        - Describes how it impacts clients
        - Mentions any solutions CAFB is implementing to address it

        This information is particularly important for Example 2 in the CAFB challenge.

        TEXT:
        {text}

        BARRIERS IDENTIFIED:
    """
}

CONTENT_GENERATION_BASE_TEMPLATE = """You are an AI assistant for the Capital Area Food Bank (CAFB), tasked with generating {target_format} content.
Use the following extracted information and format specifications to create the output:

Extracted Content:
{extracted_content_details}

Format Specifications:
{format_specifications}

Generate a {target_format} that adheres to the given format specifications, using the extracted content.
Ensure the output is coherent, well-structured, and aligns with CAFB's mission to address food insecurity.
"""

GRANT_PROPOSAL_TEMPLATE = """Emphasize CAFB's role as a leader in the food is medicine space.
Include specific examples of CAFB's initiatives and their impact.
Use a formal tone and provide evidence-based arguments.
"""

BLOG_POST_TEMPLATE = """Write in a conversational tone, suitable for a general audience.
Include personal stories or quotes from food-insecure neighbors if available.
Highlight the barriers clients face in accessing SNAP and CAFB's efforts to reduce these barriers.
"""

PRESENTATION_TEMPLATE = """Structure the content in bullet points, suitable for a slide presentation.
Focus on key statistics, impactful visuals, and concise messaging.
Include a clear call-to-action for the audience.
"""