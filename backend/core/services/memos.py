import json

from django.conf import settings
from openai import OpenAI

client = OpenAI()


MEMO_SCHEMA = {
    "type": "object",
    "properties": {
        "summary": {
            "type": "object",
            "properties": {
                "text": {
                    "type": "string"
                },
                "claim_ids": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    }
                },
            },
            "required": [
                "text",
                "claim_ids",
            ],
            "additionalProperties": False,
        },
        "recommendation": {
            "type": "object",
            "properties": {
                "text": {
                    "type": "string"
                },
                "claim_ids": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    }
                },
            },
            "required": [
                "text",
                "claim_ids",
            ],
            "additionalProperties": False,
        },
        "key_risks": {
            "type": "object",
            "properties": {
                "text": {
                    "type": "string"
                },
                "claim_ids": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    }
                },
            },
            "required": [
                "text",
                "claim_ids",
            ],
            "additionalProperties": False,
        },
        "data_appendix": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "label": {
                        "type": "string"
                    },
                    "value": {
                        "type": "string"
                    },
                    "claim_ids": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        }
                    },
                },
                "required": [
                    "label",
                    "value",
                    "claim_ids",
                ],
                "additionalProperties": False,
            }
        },
    },
    "required": [
        "summary",
        "recommendation",
        "key_risks",
        "data_appendix",
    ],

    "additionalProperties": False,
}


def generate_ic_memo(claims):
    """
    Use the LLM only to turn deterministic claims
    into a short IC-style memo.
    """

    instructions = """
        You are drafting a very short institutional
        investment committee memo.

        The backend has already calculated all metrics,
        evaluated mandate eligibility, scored the fund,
        and ranked the fund.

        Use ONLY the supplied claims.

        Do NOT:
        - calculate new metrics
        - invent facts
        - invent investment performance
        - invent manager information
        - invent risks
        - change the ranking
        - make a final investment approval decision

        The memo must have exactly these sections:

        1. Summary
        2. Recommendation
        3. Key Risks
        4. Data Appendix

        Keep the memo concise.

        The recommendation should be framed as
        "advance for further diligence" rather than
        final investment approval.

        Every factual statement must reference the
        claim IDs that support it.

        Pay particular attention to claims describing
        the number of observations.

        If the analysis is based on only a small number
        of observations, explicitly state that the
        results should be considered preliminary.
    """
    payload = {
        "claims": claims
    }
    response = client.responses.create(
        model=settings.OPENAI_MODEL,
        instructions=instructions,
        input=json.dumps(
            payload,
            indent=2,
        ),
        text={
            "format": {
                "type": "json_schema",
                "name": "ic_memo",
                "strict": True,
                "schema": MEMO_SCHEMA,
            }
        },
    )
    return json.loads(
        response.output_text
    )


def validate_memo_claims(
    memo,
    claims,
):
    """
    Ensure the LLM did not invent claim IDs.
    """
    valid_claim_ids = {
        claim["claim_id"]
        for claim in claims
    }
    invalid_claim_ids = []
    sections = [
        memo["summary"],
        memo["recommendation"],
        memo["key_risks"],
    ]
    sections.extend(
        memo["data_appendix"]
    )
    for section in sections:
        for claim_id in section[
            "claim_ids"
        ]:
            if (
                claim_id
                not in valid_claim_ids
            ):
                invalid_claim_ids.append(
                    claim_id
                )
    return list(
        set(invalid_claim_ids)
    )


def build_audit_view(
    memo,
    claims,
):
    """
    Connect memo statements to the backend
    claims that support them.

    For this demo:
    memo -> claim -> computed metric/value
    """
    claim_map = {
        claim["claim_id"]: claim
        for claim in claims
    }

    audit = []

    # Main memo sections
    main_sections = [
        "summary",
        "recommendation",
        "key_risks",
    ]
    for section_name in main_sections:
        section = memo[
            section_name
        ]

        supporting_claims = []
        for claim_id in section[
            "claim_ids"
        ]:
            claim = claim_map.get(
                claim_id
            )
            if claim:
                supporting_claims.append(
                    claim
                )
        audit.append({
            "section": section_name,
            "memo_text": (
                section["text"]
            ),
            "claim_ids": (
                section["claim_ids"]
            ),
            "claims": supporting_claims,
        })
    # Data appendix
    for item in memo[
        "data_appendix"
    ]:
        supporting_claims = []
        for claim_id in item[
            "claim_ids"
        ]:
            claim = claim_map.get(
                claim_id
            )
            if claim:
                supporting_claims.append(
                    claim
                )
        audit.append({
            "section": "data_appendix",
            "memo_text": (
                f"{item['label']}: "
                f"{item['value']}"
            ),
            "claim_ids": (
                item["claim_ids"]
            ),
            "claims": supporting_claims,
        })
    return audit
