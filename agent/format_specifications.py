DEFAULT_FORMAT_SPECIFICATIONS = {
    # TODO: Add speicifcations
}

DEFAULT_GRANT_PROPOSAL_SPECIFICATIONS = {
    "structure": [
        "Executive Summary",
        "Organization Background",
        "Problem Statement",
        "Program Description",
        "Goals and Objectives",
        "Implementation Timeline",
        "Budget",
        "Evaluation Plan"
    ],
    "style_guide": "Formal, evidence-based writing with emphasis on impact and outcomes",
    "length_requirements": "5-10 pages",
    "special_sections": ["Capital Area Food Bank (CAFB) Leadership in Food Medicine"]
}

DEFAULT_BLOG_POST_SPECIFICATIONS = {
    "structure": [
        "Attention-grabbing headline",
        "Introduction",
        "Main body (4 paragraphs)",
        "Conclusion with call to action"
    ],
    "style_guide": "Conversational tone, with personal stories and quotes",
    "length_requirements": "500-800 words",
    "special_sections": ["Client Quotes", "Barriers to SNAP Access"]
}

DEFAULT_PRESENTATION_SPECIFICATIONS = {
    "structure": [
        "Title Slide",
        "Agenda",
        "Introduction / Background",
        "Problem Statement",
        "Proposed Solution / Program Overview",
        "Key Data and Insights",
        "Implementation Plan",
        "Expected Outcomes / Community Impact",
        "Budget Overview",
        "Conclusion and Next Steps",
        "Q&A Slide",
        "Acknowledgments / Contact Information"
    ],
    "style_guide": (
        "Follow the Capital Area Food Bank presentation template. Use minimal text per slide, "
        "prefer bullet points over paragraphs, and maintain consistent formatting. Include quotes, key stats, and visuals where applicable."
    ),
    "length_requirements": "12–15 slides",
    "special_sections": [
        "Community Partnerships",
        "Data-Driven Impact Metrics"
    ],
    "formatting_notes": (
        "Each slide should follow the predefined layout in the template. Replace placeholders with slide-specific content. "
        "Ensure all fonts, colors, and alignments remain consistent with the CAFB theme."
    )
}

CAFB_GRANT_PROPOSAL_SPECIFICATIONS = {
    "structure": [
        "Cover Page",
        "Executive Summary",
        "Statement of Need",
        "Program Description",
        "Goals & Objectives",
        "Implementation Timeline",
        "Budget + Justification",
        "Evaluation Plan",
        "Staff & Organizational Background",
        "Appendices"
    ],
    "style_guide": {
        "tone": "Formal, evidence-based, equity-aware",
        "font": "Assistant",
        "headings": "Bold or Extra-Bold, Primary Green",
        "body": "Regular or Semi-Bold, Gray",
        "colors": {
            "headings": "Primary Green",
            "sections": ["White", "Light Taupe", "Dark Green"]
        },
        "visuals": "Use charts, tables, infographics with brand style (halftones, monoline, contrast rules)"
    },
    "length_requirements": "6–10 pages (excluding appendices)",
    "special_sections": [
        "Capital Area Food Bank Leadership in Food Medicine",
        "Equity and Inclusion Narrative",
        "Partnership Impact Statement"
    ]
}

CAFB_BLOG_POST_SPECIFICATIONS = {
    "structure": [
        "Headline",
        "Introduction",
        "Main Body (3–5 sections)",
        "Conclusion with Call to Action"
    ],
    "style_guide": {
        "tone": "Warm, hopeful, community-driven",
        "font": "Assistant",
        "headings": "Primary Green",
        "body": "Gray, Regular",
        "accents": ["Orange (pull quotes)", "Dark Green"],
        "images": "Use authentic, bright, natural-light photography with emotional context",
        "icons": "Use monoline-style icons only"
    },
    "length_requirements": "500–800 words",
    "special_sections": [
        "Client Stories or Volunteer Quotes",
        "Barriers to Access or Policy Context"
    ]
}

CAFB_PRESENTATION_SPECIFICATIONS = {
    "structure": [
        "Title Slide",
        "Agenda",
        "Introduction / Background",
        "Problem Statement",
        "Program Overview / Proposed Solution",
        "Key Data and Insights",
        "Implementation Plan",
        "Expected Outcomes / Community Impact",
        "Budget Summary",
        "Call to Action / Next Steps",
        "Q&A Slide",
        "Acknowledgments & Contact Info"
    ],
    "style_guide": {
        "font": "Assistant",
        "heading_style": "Extra-Bold, 44 pts, Primary Green",
        "subhead_style": "Bold, All Caps, Gray",
        "body_style": "Regular or Semi-Bold, Gray",
        "colors": {
            "background": ["White", "Light Taupe"],
            "accents": ["Primary Green", "Dark Green", "Orange (sparingly)"]
        },
        "logo_use": "Follow holding shape/pill for contrast, never distort or recolor logos",
        "visuals": "Use monoline icons, brand photography, charts styled with CAFB theme"
    },
    "length_requirements": "12–15 slides",
    "special_sections": ["Community Partnerships", "Data-Driven Impact Metrics"]
}

FORMAT_SPECIFICATIONS = {
    "Grant Proposal": CAFB_GRANT_PROPOSAL_SPECIFICATIONS,
    "Blog Post": CAFB_BLOG_POST_SPECIFICATIONS,
    "Presentation": CAFB_PRESENTATION_SPECIFICATIONS
    # TODO: Add specifications for remaining formats
}