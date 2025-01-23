from alembic import command
from alembic.config import Config
import os

def upgrade_db():
    """Upgrade the database to the latest revision."""
    alembic_cfg = Config(os.path.join(os.path.dirname(__file__), "alembic.ini"))
    command.upgrade(alembic_cfg, "head")
    print("Database upgraded to the latest revision.")
