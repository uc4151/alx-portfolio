from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '08108704791'
down_revision = '297efc24f565'
branch_labels = None
depends_on = None

def upgrade():
    # Drop the img_url column from the posts table
    op.drop_column('posts', 'img_url')

def downgrade():
    # Add the img_url column back to the posts table
    op.add_column('posts', sa.Column('img_url', sa.String(), nullable=False))