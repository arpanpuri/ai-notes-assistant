# AI Notes Assistant

A small Python project that turns a local LLM into a command-line note-taking assistant. The app lets the user chat naturally, save notes into SQLite, and search through earlier notes using tool calling.

## Project goal

This project demonstrates how to build a practical AI workflow with:

- a local LLM via Ollama
- tool calling for saving and searching notes
- structured JSON output with Pydantic
- SQLite persistence for long-term storage
- retry logic and logging for stable interactions

## How it works

The assistant runs in a loop in [app.py](app.py). A user enters a message, the model decides whether it should use a tool, and the app handles the tool call.

There are two main tools:

- `save_note(content, tags)`
  - extracts metadata from the note
  - stores the content and metadata in SQLite
- `search_notes(query)`
  - searches previously saved notes by keyword

The app uses LLM tool-calling in a simple but realistic pattern:

1. Send a user message to the model.
2. If the model decides to call a tool, parse the arguments.
3. Validate them with Pydantic schemas.
4. Execute the tool.
5. Send the tool result back to the model.
6. Ask the model to provide the final response.

## Files

- [app.py](app.py) — main chat loop and tool orchestration
- [llm.py](llm.py) — Ollama wrapper and retry logic
- [metadata.py](metadata.py) — metadata extraction prompt and schema validation
- [models.py](models.py) — metadata model definition
- [schemas.py](schemas.py) — tool argument schemas
- [tools.py](tools.py) — SQLite storage and retrieval logic

## Example flow

```python
response = llm.llm_call(
    model="qwen3:8b",
    messages=messages,
    tools=[save_note, search_notes]
)
```

This is the core idea: the model can decide whether it needs to remember information or look up past notes instead of just generating text.

## Setup

1. Install Ollama.
2. Pull a model such as `qwen3:8b`.
3. Start the local Ollama service.
4. Install Python dependencies:

```bash
pip install ollama tenacity pydantic
```

5. Run the app:

```bash
python app.py
```

## What I learned

This project taught me several important concepts about building AI-powered applications:

### 1. Tool calling makes LLMs useful in the real world

A pure chatbot can answer questions, but a tool-enabled model can actually take actions. In this project, the model can save notes and search past memories instead of only producing text. That is a big step toward building practical assistants.

### 2. Structured outputs are essential

Using Pydantic models made the app much more reliable. Instead of hoping the model returns a clean JSON object, the app validates the output against a schema before using it. This reduces errors when extracting metadata like title, tags, sentiment, and key entities.

### 3. LLM systems need strong prompt design

The metadata extraction prompt had to be specific. It was not enough to say "extract metadata"; the model needed a clear format and a clear list of fields to produce. This showed me that good prompting is part design, part engineering, and part iteration.

### 4. Persistent memory is a core AI feature

The notes database demonstrated how an assistant can keep context beyond the current conversation. Storing content, metadata, and searchable tags is an important pattern for memory in AI apps.

### 5. Reliability requires retries and logging

The retry wrapper in [llm.py](llm.py) made the LLM calls more resilient. In real AI systems, network issues, temporary model failures, and malformed responses are common. Logging and retry policies are simple but important safeguards.

### 6. Small projects can teach real architecture

Even a lightweight tool-based app introduces patterns that scale to larger systems: schema validation, model orchestration, database persistence, and response chaining. This project helped me understand how larger AI products are structured, even when the code is still compact.

### 7. Local-first AI is practical and useful

Using Ollama with a local model made the project easy to run without depending on a cloud API. That was a valuable lesson: local AI workflows can be fast, private, and accessible for learning and experimentation.

## Future improvements

Some ideas for extending the project:

- add note editing and deletion
- support categories and timestamps
- improve search with semantic matching
- add a web interface using Flask or FastAPI
- create dashboards for note statistics and sentiment trends

## License

This project is intended for learning and experimentation.
