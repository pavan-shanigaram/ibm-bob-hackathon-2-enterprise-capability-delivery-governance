"""project hub - team phases and dependencies

Revision ID: 002
Revises: 001
Create Date: 2024-01-02 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


revision = '002'
down_revision = '001'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # project_team_phases
    op.create_table(
        'project_team_phases',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('project_id', sa.Integer(), nullable=False),
        sa.Column('team_id', sa.Integer(), nullable=False),
        sa.Column('phase_name', sa.String(200), nullable=False),
        sa.Column('planned_start', sa.Date(), nullable=True),
        sa.Column('planned_end', sa.Date(), nullable=True),
        sa.Column('status', sa.Enum(
            'NotStarted', 'InProgress', 'Done', 'Blocked',
            name='phasestatus'
        ), nullable=False, server_default='NotStarted'),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(['project_id'], ['projects.id']),
        sa.ForeignKeyConstraint(['team_id'], ['teams.id']),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_project_team_phases_id', 'project_team_phases', ['id'])

    # project_team_dependencies
    op.create_table(
        'project_team_dependencies',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('project_id', sa.Integer(), nullable=False),
        sa.Column('from_team_id', sa.Integer(), nullable=False),
        sa.Column('to_team_id', sa.Integer(), nullable=False),
        sa.Column('dependency_type', sa.Enum(
            'Blocker', 'Parallel', 'Sequential',
            name='dependencytype'
        ), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('status', sa.Enum(
            'Pending', 'Resolved',
            name='dependencystatus'
        ), nullable=False, server_default='Pending'),
        sa.Column('due_date', sa.Date(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(['project_id'], ['projects.id']),
        sa.ForeignKeyConstraint(['from_team_id'], ['teams.id'], name='fk_dep_from_team'),
        sa.ForeignKeyConstraint(['to_team_id'], ['teams.id'], name='fk_dep_to_team'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_project_team_dependencies_id', 'project_team_dependencies', ['id'])


def downgrade() -> None:
    op.drop_index('ix_project_team_dependencies_id', table_name='project_team_dependencies')
    op.drop_table('project_team_dependencies')
    op.drop_index('ix_project_team_phases_id', table_name='project_team_phases')
    op.drop_table('project_team_phases')
