# Codex Rules for This Project

## General Coding Rules
- Use Python 3.14 
- Always include type hints
- Follow PEP 8 and PEP257, except for indentation: use 4 spaces TABS indentation

- Use Black formatting style
- Use descriptive variable names
- Avoid side effects in module-level code
- Prefer functional style when possible: I don't want a mess of classes. Use classes when it makes sense.
- Itertools and functools are great. Let's use them.


## FastAPI Rules
- Organize endpoints using APIRouter
- Split code into modules: routers/, models/, schemas/, services/
- Never write database logic in route handlers
- Use Pydantic models for request/response schemas

## Docker Rules
- Pin base images to exact versions
- Never hard-code credentials; always use environment variables
- Ensure containers run as non-root where possible

## Documentation Rules
- Add docstrings to all functions and classes (again, follow PEP 257)
- Add a top level docstring with an overview of the module 
- Document every new endpoint in README.md

