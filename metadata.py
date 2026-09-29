import llm
from models import NoteMetadata


def extract_metadata(content: str) -> NoteMetadata:

    messages = [
        {
            "role": "user",
            "content": f"""
Extract metadata from this note.

Note:
{content}

Return:
- a short title
- relevant tags
- sentiment
- key entities
"""
        }
    ]

    response = llm.llm_call(
        model="qwen3:8b",
        messages=messages,
        output_schema=NoteMetadata.model_json_schema()
    )

    return NoteMetadata.model_validate_json(
        response.message.content
    )

if __name__ == "__main__":
    metadata = extract_metadata(
        "My DSA exam is on Monday."
    )

    print(metadata)