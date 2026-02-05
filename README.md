# Engineering Team Crew

A multi-agent engineering crew built with [crewAI](https://crewai.com). This project wires together specialized agents (lead, backend, frontend, testing) to turn a set of requirements into code and artifacts in a repeatable workflow.

## What’s Included

- **Multi-agent workflow** orchestrated by crewAI.
- **Config-driven roles and tasks** in YAML.
- **Pluggable tools** (e.g., a write-file tool for code output).
- **Simple entry points** to run, train, replay, or test the crew.

## Project Structure

```
.
├── README.md
├── pyproject.toml
├── src/
│   └── engineering_team/
│       ├── config/
│       │   ├── agents.yaml
│       │   └── tasks.yaml
│       ├── tools/
│       ├── crew.py
│       └── main.py
└── uv.lock
```

## Requirements

- **Python**: `>=3.10,<3.14`
- **Dependency manager**: [uv](https://docs.astral.sh/uv/) (recommended)
- **API key**: `OPENAI_API_KEY` in your environment or `.env`

## Setup

1. Install `uv` if you don’t have it:

   ```bash
   pip install uv
   ```

2. Install dependencies:

   ```bash
   uv sync
   ```

3. (Optional) Create a `.env` file with your API key:

   ```bash
   echo "OPENAI_API_KEY=your_key_here" > .env
   ```

## Running the Project

You can run the crew using the `crewai` CLI or the script entry points defined in `pyproject.toml`.

### Option A: crewAI CLI

```bash
crewai run
```

### Option B: Script entry points

```bash
uv run engineering_team
```

Other available commands:

```bash
uv run run_crew
uv run train
uv run replay
uv run test
uv run run_with_trigger
```

## How It Works

- The main entry point is `src/engineering_team/main.py`.
- The crew definition and orchestration live in `src/engineering_team/crew.py`.
- Agents and tasks are configured in:
  - `src/engineering_team/config/agents.yaml`
  - `src/engineering_team/config/tasks.yaml`

When you run the crew, it uses the requirements defined in `main.py` and produces outputs in the `output/` directory.

## Customization

- **Agents**: edit `config/agents.yaml`
- **Tasks**: edit `config/tasks.yaml`
- **Crew logic and tools**: update `crew.py` and `tools/`
- **Input requirements**: adjust `main.py`

## Support & Resources

- [crewAI Documentation](https://docs.crewai.com)
- [crewAI GitHub](https://github.com/joaomdmoura/crewai)
- [crewAI Discord](https://discord.com/invite/X4JWnZnxPb)

---

If you want a more specialized workflow (e.g., different agents or task pipelines), update the YAML configs and the `EngineeringTeam` class in `crew.py`.
