import nox
import toml

nox.options.default_venv_backend = "venv"
nox.options.reuse_existing_virtualenvs = True

# automatically identify optional dependencies from pyproject.toml
optional_dependencies = toml.load("pyproject.toml")["project"][
    "optional-dependencies"
].keys()


@nox.session(python="3.13")
@nox.parametrize("extras", [None, *optional_dependencies])
def generate_requirements(session: nox.Session, extras: list[str]):
    """Generate requirements[-optional].txt file(s)"""
    command = ["pip-compile", "--output-file"]

    # Suffix `requirements.txt` file with optional dependency names
    # ex. `requirements.txt` -> `requirements-dev.txt`
    command += [f"requirements-{extras}.txt"] if extras else ["requirements.txt"]
    if extras:
        command += ["--extra", extras]

    command += ["pyproject.toml"]
    session.run(*command)
