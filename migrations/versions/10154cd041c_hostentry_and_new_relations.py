"""Hostentry and new relations

Revision ID: 10154cd041c
Revises: 3d7620e463c
Create Date: 2015-05-05 18:49:49.481740

"""

# revision identifiers, used by Alembic.
revision = '10154cd041c'
down_revision = '3d7620e463c'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('hostentries',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('hostname', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('created_by_user_id', sa.Integer(), nullable=True),
    sa.Column('updated_by_user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['created_by_user_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['updated_by_user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('ipaddresses', sa.Column('hostentry_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'ipaddresses', 'hostentries', ['hostentry_id'], ['id'])
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'ipaddresses', type_='foreignkey')
    op.drop_column('ipaddresses', 'hostentry_id')
    op.drop_table('hostentries')
    ### end Alembic commands ###
