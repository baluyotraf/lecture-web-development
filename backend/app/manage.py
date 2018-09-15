import click
from flask.cli import FlaskGroup
from app.models import db


def create_web_app(info):
    from app.application import create_application
    return create_application()


@click.group(cls=FlaskGroup, create_app=create_web_app)
def web_cli():
    """
    Tool for managing the web application
    """


@web_cli.command()
def create_db():
    """
    Creates database tables
    """
    db.create_all()
    print('Database tables successfully created')


if __name__ == '__main__':
    web_cli()
