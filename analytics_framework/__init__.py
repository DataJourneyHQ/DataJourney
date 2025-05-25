from pathlib import Path

PACKAGE_LOC = Path(__file__).parent.resolve()
INTAKE_LOC = Path.joinpath(PACKAGE_LOC, "intake")
LANGCHAIN_LOC = Path.joinpath(PACKAGE_LOC, "langchain")
