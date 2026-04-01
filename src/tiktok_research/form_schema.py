from __future__ import annotations

from copy import deepcopy
from typing import Any


YES_NO_OPTIONS = [
    {"value": "1", "label": "Yes"},
    {"value": "0", "label": "No"},
]

YES_NO_UNCLEAR_OPTIONS = [
    {"value": "yes", "label": "Yes"},
    {"value": "no", "label": "No"},
    {"value": "unclear", "label": "Unclear"},
]

PREWATCH_OPTIONS = [
    {"value": "0", "label": "Expect accurate / appropriate"},
    {"value": "1", "label": "Expect misinformation"},
    {"value": "2", "label": "Unclear from thumbnail alone"},
]

CREATOR_TYPE_OPTIONS = [
    {"value": "healthcare_professional", "label": "Healthcare professional"},
    {"value": "fitness_wellness_influencer", "label": "Fitness / wellness influencer"},
    {"value": "patient_personal", "label": "Patient / personal account"},
    {"value": "brand_commercial", "label": "Brand / commercial"},
    {"value": "other_unclear", "label": "Other / unclear"},
]

MISINFO_SCORE_OPTIONS = [
    {"value": "1", "label": "1 Accurate"},
    {"value": "2", "label": "2 Mostly accurate"},
    {"value": "3", "label": "3 Mixed"},
    {"value": "4", "label": "4 Mostly inaccurate"},
    {"value": "5", "label": "5 Misinformation"},
]

DISCERN_OPTIONS = [{"value": str(score), "label": str(score)} for score in range(1, 6)]

MISINFO_TYPE_OPTIONS = [
    {"value": "TREAT-WRONG", "label": "Wrong treatment"},
    {"value": "TREAT-CONTRA", "label": "Contraindicated treatment"},
    {"value": "TREAT-DURATION", "label": "Wrong duration"},
    {"value": "TREAT-ROUTE", "label": "Wrong method"},
    {"value": "DX-WRONG", "label": "Wrong diagnosis criteria"},
    {"value": "SX-WRONG", "label": "Wrong symptom description"},
    {"value": "CAUSE-WRONG", "label": "Wrong cause or etiology"},
    {"value": "PROG-WRONG", "label": "Wrong prognosis"},
    {"value": "EXAG", "label": "Exaggeration / overclaim"},
    {"value": "OMIT", "label": "Dangerous omission"},
    {"value": "OTHER", "label": "Other"},
]

CLINICAL_DOMAIN_OPTIONS = [
    {"value": "SUI", "label": "Stress UI"},
    {"value": "UUI_OAB", "label": "Urge / OAB"},
    {"value": "mixed", "label": "Mixed UI"},
    {"value": "pelvic_floor", "label": "Pelvic floor"},
    {"value": "postpartum", "label": "Postpartum"},
    {"value": "pediatric", "label": "Pediatric"},
    {"value": "other", "label": "Other"},
]

MISINFO_SCORE_GUIDE = [
    {
        "score": "1",
        "label": "Accurate",
        "definition": "Claims align with current clinical guidance and do not appear misleading.",
        "example": "Encourages pelvic floor therapy with no unrealistic promises.",
    },
    {
        "score": "2",
        "label": "Mostly accurate",
        "definition": "Core message is sound, though details are somewhat simplified.",
        "example": "General bladder training advice without nuance on when to seek care.",
    },
    {
        "score": "3",
        "label": "Mixed",
        "definition": "Contains both useful and questionable claims, or lacks enough nuance to fully trust.",
        "example": "Shares one evidence-based tip but overstates how broadly it applies.",
    },
    {
        "score": "4",
        "label": "Mostly inaccurate",
        "definition": "Makes major unsupported claims that could delay appropriate care.",
        "example": "Presents one device or routine as a cure for every kind of incontinence.",
    },
    {
        "score": "5",
        "label": "Misinformation",
        "definition": "Directly contradicts guidelines or makes clearly dangerous claims.",
        "example": "Tells viewers to avoid clinicians and rely only on a commercial product.",
    },
]

BASE_FIELD_SECTIONS = [
    {
        "key": "prewatch",
        "title": "Before You Watch",
        "description": "Capture the coder's first impression before pressing play.",
        "fields": [
            {
                "id": "Pre_Watch_Prediction",
                "label": "Based on the thumbnail, username, and description, do you expect misinformation?",
                "description": "Lock this in before playback starts.",
                "type": "choice",
                "options": PREWATCH_OPTIONS,
                "required": True,
                "help_text": "Choose 0, 1, or 2 before watching. 2 = Unclear from thumbnail alone.",
                "entry_hint": "0 / 1 / 2",
            }
        ],
    },
    {
        "key": "thumbnail",
        "title": "Thumbnail Snapshot",
        "description": "Quick visual cues from the thumbnail or opening frame.",
        "fields": [
            {
                "id": "Thumbnail_White_Coat",
                "label": "White coat or scrubs visible?",
                "type": "choice",
                "options": YES_NO_UNCLEAR_OPTIONS,
                "required": True,
                "help_text": "Answer from the thumbnail or first frame only.",
                "entry_hint": "yes / no / unclear",
            },
            {
                "id": "Thumbnail_Clinical_Setting",
                "label": "Clinical setting visible?",
                "type": "choice",
                "options": YES_NO_UNCLEAR_OPTIONS,
                "required": True,
                "help_text": "Answer from the thumbnail or first frame only.",
                "entry_hint": "yes / no / unclear",
            },
            {
                "id": "Thumbnail_Text_Overlay",
                "label": "Text or claim overlay on the thumbnail?",
                "type": "choice",
                "options": YES_NO_OPTIONS,
                "required": True,
                "help_text": "Mark yes if the thumbnail or opening frame includes text that frames the claim.",
                "entry_hint": "0 / 1",
            },
            {
                "id": "Thumbnail_Creator_Visible",
                "label": "Creator visible in the thumbnail?",
                "type": "choice",
                "options": YES_NO_OPTIONS,
                "required": True,
                "help_text": "Mark yes when the creator is visibly present in the opening visual.",
                "entry_hint": "0 / 1",
            },
        ],
    },
    {
        "key": "content",
        "title": "Creator and Content Tags",
        "description": "These tags make downstream filtering and analysis much easier.",
        "fields": [
            {
                "id": "B1_Creator_Type",
                "label": "Creator type",
                "type": "choice",
                "options": CREATOR_TYPE_OPTIONS,
                "required": True,
                "help_text": "Infer from the account, narration, and context. Do not verify credentials externally.",
                "entry_hint": "Pick one",
            },
            {
                "id": "B2_Definition",
                "label": "Discusses definition or general description of urinary incontinence",
                "type": "choice",
                "options": YES_NO_OPTIONS,
                "required": True,
            },
            {
                "id": "B2_Causes",
                "label": "Discusses causes or risk factors",
                "type": "choice",
                "options": YES_NO_OPTIONS,
                "required": True,
            },
            {
                "id": "B2_PelvicFloor",
                "label": "Discusses pelvic floor exercises or PT",
                "type": "choice",
                "options": YES_NO_OPTIONS,
                "required": True,
            },
            {
                "id": "B2_Behavioral",
                "label": "Discusses behavioral modifications",
                "type": "choice",
                "options": YES_NO_OPTIONS,
                "required": True,
            },
            {
                "id": "B2_Medical",
                "label": "Discusses medications or medical treatments",
                "type": "choice",
                "options": YES_NO_OPTIONS,
                "required": True,
            },
            {
                "id": "B2_Surgical",
                "label": "Discusses surgical treatments",
                "type": "choice",
                "options": YES_NO_OPTIONS,
                "required": True,
            },
            {
                "id": "B2_Products",
                "label": "Promotes a specific product, device, or supplement",
                "type": "choice",
                "options": YES_NO_OPTIONS,
                "required": True,
            },
            {
                "id": "B2_SeeDr",
                "label": "Explicitly advises viewers to see a clinician",
                "type": "choice",
                "options": YES_NO_OPTIONS,
                "required": True,
            },
            {
                "id": "B2_Other",
                "label": "Covers other content not listed above",
                "type": "choice",
                "options": YES_NO_OPTIONS,
                "required": True,
            },
        ],
    },
    {
        "key": "misinfo",
        "title": "Misinformation Assessment",
        "description": "Use your clinical reference materials when a claim feels uncertain.",
        "fields": [
            {
                "id": "B3_Misinfo_Score",
                "label": "Overall misinformation score",
                "type": "choice",
                "options": MISINFO_SCORE_OPTIONS,
                "required": True,
                "help_text": "1 = Accurate, 5 = Misinformation. Use the guide below when deciding.",
                "entry_hint": "1 / 2 / 3 / 4 / 5",
            },
            {
                "id": "B4_Misinfo_Details",
                "label": "Brief details on inaccurate claims",
                "description": "Required when the score is 4 or 5.",
                "type": "textarea",
                "required_when": {"field": "B3_Misinfo_Score", "values": ["4", "5"]},
                "help_text": "Describe the unsupported or risky claim in plain language.",
                "entry_hint": "Free text",
            },
            {
                "id": "Misinfo_Types",
                "label": "Misinformation type codes",
                "description": "Select every code that applies when the score is 4 or 5.",
                "type": "multi",
                "options": MISINFO_TYPE_OPTIONS,
                "required_when": {"field": "B3_Misinfo_Score", "values": ["4", "5"]},
            },
            {
                "id": "Clinical_Domain",
                "label": "Clinical domain",
                "description": "Select every domain that applies when the score is 4 or 5.",
                "type": "multi",
                "options": CLINICAL_DOMAIN_OPTIONS,
                "required_when": {"field": "B3_Misinfo_Score", "values": ["4", "5"]},
            },
        ],
    },
    {
        "key": "discern_core",
        "title": "DISCERN 1 to 8",
        "description": "Rate each item from 1 to 5.",
        "fields": [
            {"id": "DQ1_Aims", "label": "Q1. Are the aims clear?", "type": "choice", "options": DISCERN_OPTIONS, "required": True, "help_text": "1=Not at all, 5=Fully. Consider whether the video clearly states what the video is about.", "reference_note": "Focus on whether the video clearly states what the video is about."},
            {"id": "DQ2_Achieves", "label": "Q2. Does it achieve its aims?", "type": "choice", "options": DISCERN_OPTIONS, "required": True, "help_text": "1=Not at all, 5=Fully. Consider whether the stated purpose is actually met."},
            {"id": "DQ3_Relevant", "label": "Q3. Is it relevant to patients?", "type": "choice", "options": DISCERN_OPTIONS, "required": True, "help_text": "1=Not at all, 5=Fully. Consider whether the content is relevant to people with UI concerns."},
            {"id": "DQ4_Sources", "label": "Q4. Are sources clear?", "type": "choice", "options": DISCERN_OPTIONS, "required": True, "help_text": "1=Not at all, 5=Fully. Consider whether the speaker identifies evidence or source material."},
            {"id": "DQ5_Date", "label": "Q5. Is it current or clearly dated?", "type": "choice", "options": DISCERN_OPTIONS, "required": True, "help_text": "1=Not at all, 5=Fully. Consider whether timing or currency is clear."},
            {"id": "DQ6_Balanced", "label": "Q6. Is it balanced and unbiased?", "type": "choice", "options": DISCERN_OPTIONS, "required": True, "help_text": "1=Not at all, 5=Fully. Consider whether risks and limits are acknowledged."},
            {"id": "DQ7_AddlSources", "label": "Q7. Does it point to other resources?", "type": "choice", "options": DISCERN_OPTIONS, "required": True, "help_text": "1=Not at all, 5=Fully. Consider whether viewers are directed to other help or resources."},
            {"id": "DQ8_Uncertainty", "label": "Q8. Does it acknowledge uncertainty?", "type": "choice", "options": DISCERN_OPTIONS, "required": True, "help_text": "1=Not at all, 5=Fully. Consider whether unknowns or limitations are admitted."},
        ],
    },
    {
        "key": "discern_treatment",
        "title": "DISCERN 9 to 16",
        "description": "Continue the same 1 to 5 scale for treatment and overall quality.",
        "fields": [
            {"id": "DQ9_HowWorks", "label": "Q9. Does it describe how treatments work?", "type": "choice", "options": DISCERN_OPTIONS, "required": True},
            {"id": "DQ10_Benefits", "label": "Q10. Does it describe benefits?", "type": "choice", "options": DISCERN_OPTIONS, "required": True},
            {"id": "DQ11_Risks", "label": "Q11. Does it describe risks or side effects?", "type": "choice", "options": DISCERN_OPTIONS, "required": True},
            {"id": "DQ12_NoTreat", "label": "Q12. Does it discuss no treatment?", "type": "choice", "options": DISCERN_OPTIONS, "required": True},
            {"id": "DQ13_QoL", "label": "Q13. Does it address quality of life?", "type": "choice", "options": DISCERN_OPTIONS, "required": True},
            {"id": "DQ14_Options", "label": "Q14. Does it present multiple options?", "type": "choice", "options": DISCERN_OPTIONS, "required": True},
            {"id": "DQ15_SharedDec", "label": "Q15. Does it support shared decision-making?", "type": "choice", "options": DISCERN_OPTIONS, "required": True},
            {"id": "DQ16_Overall", "label": "Q16. Overall quality", "type": "choice", "options": DISCERN_OPTIONS, "required": True, "help_text": "1=Very poor, 5=Excellent. Give your overall impression as a health information source."},
        ],
    },
    {
        "key": "notes",
        "title": "Notes and Review Flags",
        "description": "Use notes to help later reconciliation and adjudication.",
        "fields": [
            {
                "id": "B6_Notes",
                "label": "Coder notes",
                "description": "Required when the misinformation score is 4 or 5.",
                "type": "textarea",
                "required_when": {"field": "B3_Misinfo_Score", "values": ["4", "5"]},
                "help_text": "Note the reasoning or uncertainty that another reviewer should see.",
                "entry_hint": "Free text",
            },
            {
                "id": "Flag_For_Review",
                "label": "Flag for reviewer follow-up?",
                "type": "choice",
                "options": YES_NO_OPTIONS,
                "required": False,
                "help_text": "Use this when the video needs adjudication or discussion.",
                "entry_hint": "0 / 1",
            },
        ],
    },
]

EXPORT_METADATA_FIELDS = [
    "Video_ID",
    "TikTok_URL",
    "Views",
    "Likes",
    "Comments",
    "Shares",
    "Post_Date",
    "Creator_Handle",
]


def build_field_registry() -> tuple[list[dict[str, Any]], dict[str, dict[str, Any]], list[str]]:
    sections = deepcopy(BASE_FIELD_SECTIONS)
    field_index: dict[str, dict[str, Any]] = {}
    field_order: list[str] = []
    for section in sections:
        if section["key"] == "misinfo":
            section["score_reference"] = deepcopy(MISINFO_SCORE_GUIDE)
        if section["key"] == "discern_core":
            section["scale_hint"] = "Workbook scale for Q1-Q8: 1 = Not at all, 5 = Fully."
            section["scale_note"] = "Use Help on each item for the exact coding guidance."
        if section["key"] == "discern_treatment":
            section["scale_hint"] = "Workbook scale for Q9-Q15: 1 = Not at all, 5 = Fully."
            section["scale_note"] = "Q16 overall uses 1 = Very poor and 5 = Excellent."

        for field in section["fields"]:
            if field["id"].startswith("DQ"):
                if field["id"] == "DQ16_Overall":
                    field["scale_hint"] = "Workbook scale: 1 = Very poor, 5 = Excellent."
                else:
                    field["scale_hint"] = "Workbook scale: 1 = Not at all, 5 = Fully."
            field_index[field["id"]] = field
            field_order.append(field["id"])

    field_index["B3_Misinfo_Score"]["followup_note"] = (
        "If you choose 4 or 5, the sheet also requires details, type codes, clinical domain, and notes."
    )
    return sections, field_index, field_order


FIELD_SECTIONS, FIELD_INDEX, FIELD_ORDER = build_field_registry()
DISCERN_FIELDS = [field_id for field_id in FIELD_ORDER if field_id.startswith("DQ")]
DISCERN_FIELD_IDS = {f"Q{index}": field_id for index, field_id in enumerate(DISCERN_FIELDS, start=1)}
EXPORT_FIELD_ORDER = EXPORT_METADATA_FIELDS + FIELD_ORDER + ["DISCERN_Total"]
