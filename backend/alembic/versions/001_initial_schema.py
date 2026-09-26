"""initial schema

Revision ID: 001
Revises: 
Create Date: 2024-01-01 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # teams table
    op.create_table(
        'teams',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('lead_employee_id', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name'),
    )
    op.create_index('ix_teams_id', 'teams', ['id'])

    # employees table (no FK to squads yet — added after squads)
    op.create_table(
        'employees',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(150), nullable=False),
        sa.Column('email', sa.String(200), nullable=False),
        sa.Column('job_title', sa.String(150), nullable=True),
        sa.Column('role', sa.Enum(
            'Designer', 'Developer', 'BusinessAnalyst', 'ScrumMaster',
            'PlatformEngineer', 'OperationsEngineer', 'QAEngineer', 'Architect',
            name='employeerole'
        ), nullable=False),
        sa.Column('team_id', sa.Integer(), nullable=True),
        sa.Column('auth0_user_id', sa.String(200), nullable=True),
        sa.Column('allocation_percentage', sa.Numeric(5, 2), nullable=False, server_default='0'),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='1'),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(['team_id'], ['teams.id']),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email'),
        sa.UniqueConstraint('auth0_user_id'),
    )
    op.create_index('ix_employees_id', 'employees', ['id'])
    op.create_index('ix_employees_email', 'employees', ['email'])

    # squads table
    op.create_table(
        'squads',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('team_id', sa.Integer(), nullable=False),
        sa.Column('scrum_master_id', sa.Integer(), nullable=True),
        sa.Column('capacity_points', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(['team_id'], ['teams.id']),
        sa.ForeignKeyConstraint(['scrum_master_id'], ['employees.id'], name='fk_squad_scrum_master'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_squads_id', 'squads', ['id'])

    # squad_members
    op.create_table(
        'squad_members',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('squad_id', sa.Integer(), nullable=False),
        sa.Column('employee_id', sa.Integer(), nullable=False),
        sa.Column('role_in_squad', sa.Enum(
            'Designer', 'Developer', 'BusinessAnalyst', 'ScrumMaster',
            'PlatformEngineer', 'OperationsEngineer', 'QAEngineer', 'Architect', 'Lead',
            name='squadroleenum'
        ), nullable=False),
        sa.Column('allocation_percentage', sa.Numeric(5, 2), nullable=False, server_default='100'),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(['squad_id'], ['squads.id']),
        sa.ForeignKeyConstraint(['employee_id'], ['employees.id']),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_squad_members_id', 'squad_members', ['id'])

    # skills
    op.create_table(
        'skills',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('category', sa.String(100), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name'),
    )
    op.create_index('ix_skills_id', 'skills', ['id'])

    # employee_skills
    op.create_table(
        'employee_skills',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('employee_id', sa.Integer(), nullable=False),
        sa.Column('skill_id', sa.Integer(), nullable=False),
        sa.Column('proficiency_level', sa.Enum(
            'Beginner', 'Intermediate', 'Expert', 'Lead',
            name='proficiencylevel'
        ), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(['employee_id'], ['employees.id']),
        sa.ForeignKeyConstraint(['skill_id'], ['skills.id']),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_employee_skills_id', 'employee_skills', ['id'])

    # projects
    op.create_table(
        'projects',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(200), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('status', sa.Enum('Draft', 'Active', 'OnHold', 'Completed', 'Cancelled', name='projectstatus'), nullable=False, server_default='Draft'),
        sa.Column('priority', sa.Enum('Low', 'Medium', 'High', 'Critical', name='projectpriority'), nullable=False, server_default='Medium'),
        sa.Column('start_date', sa.Date(), nullable=True),
        sa.Column('end_date', sa.Date(), nullable=True),
        sa.Column('owner_team_id', sa.Integer(), nullable=True),
        sa.Column('owner_squad_id', sa.Integer(), nullable=True),
        sa.Column('health_indicator', sa.Enum('Green', 'Amber', 'Red', name='healthindicator'), nullable=False, server_default='Green'),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(['owner_team_id'], ['teams.id']),
        sa.ForeignKeyConstraint(['owner_squad_id'], ['squads.id']),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_projects_id', 'projects', ['id'])

    # project_squad_assignments
    op.create_table(
        'project_squad_assignments',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('project_id', sa.Integer(), nullable=False),
        sa.Column('squad_id', sa.Integer(), nullable=False),
        sa.Column('assigned_at', sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(['project_id'], ['projects.id']),
        sa.ForeignKeyConstraint(['squad_id'], ['squads.id']),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_project_squad_assignments_id', 'project_squad_assignments', ['id'])

    # project_employee_assignments
    op.create_table(
        'project_employee_assignments',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('project_id', sa.Integer(), nullable=False),
        sa.Column('employee_id', sa.Integer(), nullable=False),
        sa.Column('allocation_percentage', sa.Numeric(5, 2), nullable=False, server_default='100'),
        sa.Column('role_on_project', sa.String(100), nullable=True),
        sa.Column('assigned_at', sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(['project_id'], ['projects.id']),
        sa.ForeignKeyConstraint(['employee_id'], ['employees.id']),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_project_employee_assignments_id', 'project_employee_assignments', ['id'])

    # authorizations
    op.create_table(
        'authorizations',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('employee_id', sa.Integer(), nullable=False),
        sa.Column('system', sa.Enum('GitHub', 'AzureDevOps', 'SAP', 'Salesforce', 'Production', name='authorizedsystem'), nullable=False),
        sa.Column('access_level', sa.String(100), nullable=False, server_default='ReadOnly'),
        sa.Column('granted_at', sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column('expires_at', sa.DateTime(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='1'),
        sa.Column('compliance_status', sa.Enum('Compliant', 'Expired', 'PendingReview', 'Revoked', name='compliancestatus'), nullable=False, server_default='Compliant'),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(['employee_id'], ['employees.id']),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_authorizations_id', 'authorizations', ['id'])

    # delivery_metrics
    op.create_table(
        'delivery_metrics',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('squad_id', sa.Integer(), nullable=False),
        sa.Column('project_id', sa.Integer(), nullable=True),
        sa.Column('sprint_name', sa.String(100), nullable=False),
        sa.Column('sprint_start', sa.Date(), nullable=True),
        sa.Column('sprint_end', sa.Date(), nullable=True),
        sa.Column('velocity', sa.Numeric(8, 2), nullable=False, server_default='0'),
        sa.Column('story_points_planned', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('story_points_delivered', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('cycle_time_days', sa.Numeric(6, 2), nullable=True),
        sa.Column('lead_time_days', sa.Numeric(6, 2), nullable=True),
        sa.Column('defect_leakage_count', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('release_success', sa.Boolean(), nullable=False, server_default='1'),
        sa.Column('delivery_score', sa.Numeric(5, 2), nullable=False, server_default='0'),
        sa.Column('recorded_at', sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(['squad_id'], ['squads.id']),
        sa.ForeignKeyConstraint(['project_id'], ['projects.id']),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_delivery_metrics_id', 'delivery_metrics', ['id'])

    # resource_allocations
    op.create_table(
        'resource_allocations',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('employee_id', sa.Integer(), nullable=False),
        sa.Column('project_id', sa.Integer(), nullable=True),
        sa.Column('squad_id', sa.Integer(), nullable=True),
        sa.Column('allocation_percentage', sa.Numeric(5, 2), nullable=False, server_default='0'),
        sa.Column('period_start', sa.Date(), nullable=False),
        sa.Column('period_end', sa.Date(), nullable=False),
        sa.Column('is_over_allocated', sa.Boolean(), nullable=False, server_default='0'),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(['employee_id'], ['employees.id']),
        sa.ForeignKeyConstraint(['project_id'], ['projects.id']),
        sa.ForeignKeyConstraint(['squad_id'], ['squads.id']),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_resource_allocations_id', 'resource_allocations', ['id'])

    # capability_requirements
    op.create_table(
        'capability_requirements',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('project_id', sa.Integer(), nullable=False),
        sa.Column('skill_id', sa.Integer(), nullable=False),
        sa.Column('required_proficiency', sa.Enum(
            'Beginner', 'Intermediate', 'Expert', 'Lead',
            name='proficiencylevel'
        ), nullable=False),
        sa.Column('headcount_needed', sa.Integer(), nullable=False, server_default='1'),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(['project_id'], ['projects.id']),
        sa.ForeignKeyConstraint(['skill_id'], ['skills.id']),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_capability_requirements_id', 'capability_requirements', ['id'])


def downgrade() -> None:
    op.drop_table('capability_requirements')
    op.drop_table('resource_allocations')
    op.drop_table('delivery_metrics')
    op.drop_table('authorizations')
    op.drop_table('project_employee_assignments')
    op.drop_table('project_squad_assignments')
    op.drop_table('projects')
    op.drop_table('employee_skills')
    op.drop_table('skills')
    op.drop_table('squad_members')
    op.drop_table('squads')
    op.drop_table('employees')
    op.drop_table('teams')
