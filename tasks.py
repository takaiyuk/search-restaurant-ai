from invoke import task

PACKAGE_NAME = "search_restaurant_ai"


@task
def run(c):
    """Run streamlit app"""
    cmd = f"poetry run streamlit run {PACKAGE_NAME}/main.py"
    c.run(cmd)


@task
def format(c):
    """Format"""
    c.run(
        """
        poetry run black .
        poetry run isort --case-sensitive .
    """
    )


@task
def lint(ctx):
    """Lint"""
    ctx.run(
        f"""
        poetry run black --check .
        poetry run isort --check-only --case-sensitive .
        poetry run pflake8 .
        poetry run mypy {PACKAGE_NAME} --install-types --non-interactive
    """
    )
