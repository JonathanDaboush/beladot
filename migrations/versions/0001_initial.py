"""
Initial Alembic migration script.
"""
from alembic import op
import sqlalchemy as sa
# revision identifiers, used by Alembic.
revision = '0001_initial'
down_revision = None
branch_labels = None
depends_on = None
def upgrade():
    # Example: create a users table (replace with your actual models)
    op.create_table(
        'users',
        sa.Column('user_id', sa.Integer, primary_key=True),
        sa.Column('full_name', sa.String(255)),
        sa.Column('email', sa.String(255), unique=True, nullable=False),
        sa.Column('password', sa.String(255), nullable=False),
        sa.Column('created_at', sa.DateTime),
        sa.Column('account_status', sa.Boolean, default=True),
    )
    # Add more tables as needed based on your models

def downgrade():
    op.drop_table('users')
