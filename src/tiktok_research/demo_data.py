from __future__ import annotations

from .models import Researcher


DEMO_RESEARCHERS = (
    Researcher(slug="reviewer-a", display_name="Reviewer A"),
    Researcher(slug="reviewer-b", display_name="Reviewer B"),
)


DEMO_MAIN_VIDEOS = [
    {
        "video_id": "VID001",
        "id": "9000000000000000001",
        "username": "pelvicfloorlab",
        "view_count": 18234,
        "like_count": 1311,
        "comment_count": 122,
        "share_count": 88,
        "create_time": 1735689600,
        "post_date": "2025-01-01",
        "video_description": "Three signs it is time to talk to a clinician about leaking urine after exercise.",
        "transcript": "If you leak urine when you exercise, coughing and running are useful patterns to note, but they are not a diagnosis by themselves. A pelvic floor evaluation, symptom diary, and personalized plan matter more than chasing quick fixes.",
    },
    {
        "video_id": "VID002",
        "id": "9000000000000000002",
        "username": "movementmyths",
        "view_count": 25601,
        "like_count": 2444,
        "comment_count": 301,
        "share_count": 199,
        "create_time": 1735948800,
        "post_date": "2025-01-04",
        "video_description": "Not every pelvic floor symptom needs the same exercise. Here is why breath, pressure, and movement patterns matter.",
        "transcript": "A lot of short videos tell you to squeeze harder, but not every symptom improves with more gripping. Sometimes urgency, pain, or pressure symptoms get worse when you stay clenched all day. Start with assessment, then choose the right progression.",
    },
    {
        "video_id": "VID003",
        "id": "9000000000000000003",
        "username": "clinicrounds",
        "view_count": 30220,
        "like_count": 2760,
        "comment_count": 244,
        "share_count": 178,
        "create_time": 1736294400,
        "post_date": "2025-01-08",
        "video_description": "A urogynecology fellow explains why pads can help with symptoms but do not treat the underlying condition.",
        "transcript": "Pads can reduce disruption while you work through symptoms, but pads are not treatment. Depending on the type of incontinence, options include pelvic floor therapy, bladder training, medications, devices, or procedures. The right plan depends on the pattern.",
    },
    {
        "video_id": "VID004",
        "id": "9000000000000000004",
        "username": "postpartumcoachdemo",
        "view_count": 14550,
        "like_count": 911,
        "comment_count": 90,
        "share_count": 66,
        "create_time": 1736726400,
        "post_date": "2025-01-13",
        "video_description": "A postpartum coach shares common mistakes people make when they rush back into impact workouts too quickly.",
        "transcript": "If you are newly postpartum and leaking with jumping, your body may need a slower progression than social media suggests. Start with breathing, pressure management, and symptom tracking, then build back to impact with guidance if symptoms persist.",
    },
    {
        "video_id": "VID005",
        "id": "9000000000000000005",
        "username": "bladderdiarybasics",
        "view_count": 11802,
        "like_count": 799,
        "comment_count": 61,
        "share_count": 44,
        "create_time": 1737244800,
        "post_date": "2025-01-19",
        "video_description": "How to start a simple bladder diary before your appointment.",
        "transcript": "A bladder diary can help you notice how often you void, when urgency happens, what you drink, and what activities trigger leakage. Bring two or three days of notes to your visit so you and your clinician can see patterns instead of guessing.",
    },
]


DEMO_REPLACEMENT_CANDIDATES = [
    {
        "id": f"91000000000000000{index:02d}",
        "username": f"candidate{index:02d}",
        "view_count": 8000 + (index * 550),
        "like_count": 700 + (index * 44),
        "comment_count": 40 + index,
        "share_count": 20 + index,
        "create_time": 1738368000 + (index * 86400),
        "region_code": "US",
        "video_description": description,
    }
    for index, description in enumerate(
        [
            "Urinary incontinence myths in endurance athletes and why assessment matters.",
            "Stress incontinence after coughing or laughing does not always mean weak muscles only.",
            "Overactive bladder tips that focus on bladder training instead of panic and shame.",
            "Pelvic floor relaxation basics for people who feel urgency and constant gripping.",
            "Postpartum bladder leakage questions to ask at your follow-up visit.",
            "Pediatric bedwetting myths and why family-friendly evaluation matters.",
            "Mixed incontinence signs that suggest more than one pattern is present.",
            "Kegel device advertising claims versus what evidence-based care usually looks like.",
            "Behavioral strategies for bladder leakage that complement pelvic floor therapy.",
            "When pelvic floor pain and urgency need a clinician instead of more squeezing.",
            "Bladder leakage at the gym and how symptom diaries help shape treatment.",
            "Urgency, prolapse, and pelvic floor symptoms explained without miracle cures.",
        ],
        start=1,
    )
]

