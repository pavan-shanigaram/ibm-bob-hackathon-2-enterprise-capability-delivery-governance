"""
Enterprise Governance Platform — Seed Data Script
Populates all tables with realistic sample data for demonstration.
Run: python seed/seed_data.py
"""
import sys
import os
import random
from datetime import date, datetime, timedelta

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.core.database import SessionLocal, engine
from app.core.config import settings
from app.models import (
    Team, Employee, Squad, SquadMember, Skill, EmployeeSkill,
    Project, ProjectSquadAssignment, ProjectEmployeeAssignment,
    Authorization, DeliveryMetric, ResourceAllocation, CapabilityRequirement,
)
from app.models.employee import EmployeeRole
from app.models.squad_member import SquadRoleEnum
from app.models.employee_skill import ProficiencyLevel
from app.models.project import ProjectStatus, ProjectPriority, HealthIndicator
from app.models.authorization import AuthorizedSystem, ComplianceStatus

random.seed(42)

# ─── Data Definitions ───────────────────────────────────────────────────────

TEAMS = [
    {"name": "Enterprise UI",   "description": "Frontend experiences across all enterprise applications"},
    {"name": "SAP",             "description": "SAP ERP implementation and support"},
    {"name": "Salesforce",      "description": "CRM platform development and administration"},
    {"name": "Platform",        "description": "Cloud infrastructure and DevOps platform engineering"},
    {"name": "Integration",     "description": "API and middleware integration services"},
    {"name": "Security",        "description": "Cybersecurity, IAM and compliance"},
    {"name": "Network",         "description": "Network infrastructure and connectivity"},
    {"name": "BAU",             "description": "Business As Usual — operations and support"},
]

SKILLS = [
    # Frontend
    ("React", "Frontend"), ("Angular", "Frontend"), ("TypeScript", "Frontend"),
    ("CSS/Tailwind", "Frontend"), ("Next.js", "Frontend"),
    # Backend
    ("Python", "Backend"), ("Java", "Backend"), ("Node.js", "Backend"),
    ("FastAPI", "Backend"), ("Spring Boot", "Backend"),
    # Cloud
    ("AWS", "Cloud"), ("Azure", "Cloud"), ("GCP", "Cloud"),
    ("Kubernetes", "Cloud"), ("Terraform", "Cloud"), ("Docker", "Cloud"),
    # SAP
    ("SAP ABAP", "SAP"), ("SAP BTP", "SAP"), ("SAP S4HANA", "SAP"), ("SAP Fiori", "SAP"),
    # Salesforce
    ("Salesforce Admin", "Salesforce"), ("Apex", "Salesforce"),
    ("Salesforce LWC", "Salesforce"), ("Salesforce CPQ", "Salesforce"),
    # Integration
    ("MuleSoft", "Integration"), ("Apache Kafka", "Integration"),
    ("REST API Design", "Integration"), ("GraphQL", "Integration"),
    # Security
    ("Penetration Testing", "Security"), ("IAM", "Security"),
    ("SIEM", "Security"), ("Zero Trust", "Security"),
    # Data
    ("SQL", "Data"), ("Power BI", "Data"), ("Databricks", "Data"),
]

FIRST_NAMES = [
    "Alice", "Bob", "Carol", "David", "Emma", "Frank", "Grace", "Henry",
    "Isabella", "James", "Katherine", "Liam", "Mia", "Nathan", "Olivia",
    "Patrick", "Quinn", "Rachel", "Samuel", "Taylor", "Uma", "Victor",
    "Wendy", "Xavier", "Yasmine", "Zachary", "Aisha", "Bruno", "Chloe",
    "Derek", "Elena", "Felix", "Gina", "Hugo", "Iris", "Jack",
]
LAST_NAMES = [
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller",
    "Davis", "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez",
    "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin",
    "Lee", "Perez", "Thompson", "White", "Harris", "Sanchez", "Clark",
    "Ramirez", "Lewis", "Robinson", "Walker", "Young", "Allen", "King",
]

PROJECTS = [
    {"name": "Digital Portal Modernisation",    "status": ProjectStatus.Active,    "priority": ProjectPriority.High,     "owner_team": "Enterprise UI"},
    {"name": "SAP S/4HANA Migration",           "status": ProjectStatus.Active,    "priority": ProjectPriority.Critical, "owner_team": "SAP"},
    {"name": "Salesforce CPQ Implementation",   "status": ProjectStatus.Active,    "priority": ProjectPriority.High,     "owner_team": "Salesforce"},
    {"name": "Cloud Platform Uplift",           "status": ProjectStatus.Active,    "priority": ProjectPriority.Critical, "owner_team": "Platform"},
    {"name": "API Gateway Consolidation",       "status": ProjectStatus.Active,    "priority": ProjectPriority.Medium,   "owner_team": "Integration"},
    {"name": "Zero Trust Security Programme",   "status": ProjectStatus.Active,    "priority": ProjectPriority.Critical, "owner_team": "Security"},
    {"name": "Network SD-WAN Rollout",          "status": ProjectStatus.Active,    "priority": ProjectPriority.High,     "owner_team": "Network"},
    {"name": "BAU Automation Initiative",       "status": ProjectStatus.Active,    "priority": ProjectPriority.Medium,   "owner_team": "BAU"},
    {"name": "Employee Self-Service Portal",    "status": ProjectStatus.Active,    "priority": ProjectPriority.Medium,   "owner_team": "Enterprise UI"},
    {"name": "Real-time Data Integration",      "status": ProjectStatus.Active,    "priority": ProjectPriority.High,     "owner_team": "Integration"},
    {"name": "SAP Analytics Cloud",             "status": ProjectStatus.OnHold,    "priority": ProjectPriority.Low,      "owner_team": "SAP"},
    {"name": "Salesforce Service Cloud",        "status": ProjectStatus.Completed, "priority": ProjectPriority.Medium,   "owner_team": "Salesforce"},
    {"name": "Identity Access Management",      "status": ProjectStatus.Active,    "priority": ProjectPriority.Critical, "owner_team": "Security"},
    {"name": "Kubernetes Migration",            "status": ProjectStatus.Active,    "priority": ProjectPriority.High,     "owner_team": "Platform"},
]

SQUAD_NAME_PATTERNS = [
    "Alpha Squad", "Beta Squad", "Gamma Squad",
]

PROFICIENCY_LEVELS = list(ProficiencyLevel)
EMPLOYEE_ROLES = list(EmployeeRole)
SQUAD_ROLES = list(SquadRoleEnum)


# ─── Seed Functions ──────────────────────────────────────────────────────────

def seed_teams(db):
    teams = []
    for t in TEAMS:
        team = Team(name=t["name"], description=t["description"])
        db.add(team)
        teams.append(team)
    db.flush()
    print(f"  Seeded {len(teams)} teams")
    return {t.name: t for t in teams}


def seed_skills(db):
    skills = []
    for name, category in SKILLS:
        skill = Skill(name=name, category=category)
        db.add(skill)
        skills.append(skill)
    db.flush()
    print(f"  Seeded {len(skills)} skills")
    return skills


def seed_employees_and_squads(db, team_map, skills):
    all_employees = []
    all_squads = []
    used_emails = set()
    emp_counter = [0]

    for team_name, team in team_map.items():
        # 3 squads per team
        for sq_idx in range(3):
            squad = Squad(
                name=f"{team_name} — {SQUAD_NAME_PATTERNS[sq_idx]}",
                team_id=team.id,
                capacity_points=random.randint(60, 120),
                description=f"Scrum squad {sq_idx + 1} for {team_name}",
            )
            db.add(squad)
            db.flush()
            all_squads.append(squad)

            # 5–7 employees per squad
            num_employees = random.randint(5, 7)
            squad_members_added = []
            for _ in range(num_employees):
                fn = random.choice(FIRST_NAMES)
                ln = random.choice(LAST_NAMES)
                email_base = f"{fn.lower()}.{ln.lower()}"
                emp_counter[0] += 1
                email = f"{email_base}.{emp_counter[0]}@enterprise.com"
                while email in used_emails:
                    emp_counter[0] += 1
                    email = f"{email_base}.{emp_counter[0]}@enterprise.com"
                used_emails.add(email)

                role = random.choice(EMPLOYEE_ROLES)
                emp = Employee(
                    name=f"{fn} {ln}",
                    email=email,
                    job_title=role.value.replace("Engineer", " Engineer"),
                    role=role,
                    team_id=team.id,
                    is_active=True,
                    allocation_percentage=random.choice([50.0, 75.0, 100.0]),
                )
                db.add(emp)
                db.flush()
                all_employees.append(emp)
                squad_members_added.append(emp)

                # Squad membership
                squad_role = random.choice(SQUAD_ROLES)
                sm = SquadMember(
                    squad_id=squad.id,
                    employee_id=emp.id,
                    role_in_squad=squad_role,
                    allocation_percentage=random.choice([50.0, 75.0, 100.0]),
                )
                db.add(sm)

                # Assign 3–6 random skills
                skill_sample = random.sample(skills, random.randint(3, 6))
                used_skill_ids = set()
                for skill in skill_sample:
                    if skill.id in used_skill_ids:
                        continue
                    used_skill_ids.add(skill.id)
                    es = EmployeeSkill(
                        employee_id=emp.id,
                        skill_id=skill.id,
                        proficiency_level=random.choice(PROFICIENCY_LEVELS),
                    )
                    db.add(es)

            # Assign first employee as scrum master
            if squad_members_added:
                squad.scrum_master_id = squad_members_added[0].id

        db.flush()
        # Set team lead to first employee in first squad of team
        team_employees = [e for e in all_employees if e.team_id == team.id]
        if team_employees:
            team.lead_employee_id = team_employees[0].id

    db.flush()
    print(f"  Seeded {len(all_employees)} employees, {len(all_squads)} squads")
    return all_employees, all_squads


def seed_projects(db, team_map, all_squads, all_employees):
    projects = []
    today = date.today()
    for pd in PROJECTS:
        owner_team = team_map.get(pd["owner_team"])
        start = today - timedelta(days=random.randint(30, 180))
        end = today + timedelta(days=random.randint(30, 180))
        p = Project(
            name=pd["name"],
            description=f"Strategic initiative: {pd['name']}",
            status=pd["status"],
            priority=pd["priority"],
            start_date=start,
            end_date=end,
            owner_team_id=owner_team.id if owner_team else None,
            health_indicator=random.choice([HealthIndicator.Green, HealthIndicator.Green, HealthIndicator.Amber, HealthIndicator.Red]),
        )
        db.add(p)
        db.flush()
        projects.append(p)

        # Assign 2–3 squads from owner team
        team_squads = [s for s in all_squads if s.team_id == (owner_team.id if owner_team else -1)]
        for squad in random.sample(team_squads, min(2, len(team_squads))):
            db.add(ProjectSquadAssignment(project_id=p.id, squad_id=squad.id))

        # Assign 4–8 employees from owner team
        team_emps = [e for e in all_employees if e.team_id == (owner_team.id if owner_team else -1)]
        for emp in random.sample(team_emps, min(random.randint(4, 8), len(team_emps))):
            db.add(ProjectEmployeeAssignment(
                project_id=p.id,
                employee_id=emp.id,
                allocation_percentage=random.choice([25.0, 50.0, 75.0, 100.0]),
                role_on_project=random.choice(["Developer", "Lead", "Architect", "QA", "BA"]),
            ))

        # Add capability requirements for active projects
        if pd["status"] == ProjectStatus.Active:
            from app.models.skill import Skill as SkillModel
            all_skills = db.query(SkillModel).limit(5).all()
            for skill in random.sample(all_skills, min(2, len(all_skills))):
                db.add(CapabilityRequirement(
                    project_id=p.id,
                    skill_id=skill.id,
                    required_proficiency=random.choice([ProficiencyLevel.Intermediate, ProficiencyLevel.Expert]),
                    headcount_needed=random.randint(1, 3),
                ))

    db.flush()
    print(f"  Seeded {len(projects)} projects")
    return projects


def seed_authorizations(db, all_employees):
    systems = list(AuthorizedSystem)
    count = 0
    today = date.today()
    for emp in all_employees:
        # Each employee gets 3–5 system authorizations
        for system in random.sample(systems, random.randint(3, 5)):
            days_granted = random.randint(30, 365)
            days_expiry = random.randint(-30, 365)  # negative = already expired
            granted_at = datetime.utcnow() - timedelta(days=days_granted)
            expires_at = datetime.utcnow() + timedelta(days=days_expiry)
            is_active = days_expiry > 0
            compliance_status = (
                ComplianceStatus.Compliant if is_active and days_expiry > 30
                else ComplianceStatus.Expired if not is_active
                else ComplianceStatus.PendingReview
            )
            db.add(Authorization(
                employee_id=emp.id,
                system=system,
                access_level=random.choice(["ReadOnly", "ReadWrite", "Admin"]),
                granted_at=granted_at,
                expires_at=expires_at,
                is_active=is_active,
                compliance_status=compliance_status,
            ))
            count += 1
    db.flush()
    print(f"  Seeded {count} authorization records")


def seed_delivery_metrics(db, all_squads, projects):
    today = date.today()
    count = 0
    for squad in all_squads:
        # 3 sprints of data per squad
        for sprint_num in range(1, 4):
            sprint_start = today - timedelta(weeks=(4 - sprint_num) * 2)
            sprint_end = sprint_start + timedelta(weeks=2)
            planned = random.randint(30, 80)
            delivered = random.randint(int(planned * 0.6), planned)
            defects = random.randint(0, 5)
            release_ok = random.random() > 0.2
            velocity = float(delivered)
            score_raw = (delivered / planned * 50) + (float(release_ok) * 30) + (max(0, 1 - defects / max(delivered, 1)) * 20)
            score = round(min(max(score_raw, 0), 100), 2)
            project = random.choice(projects) if projects else None
            db.add(DeliveryMetric(
                squad_id=squad.id,
                project_id=project.id if project else None,
                sprint_name=f"Sprint {sprint_num}",
                sprint_start=sprint_start,
                sprint_end=sprint_end,
                velocity=velocity,
                story_points_planned=planned,
                story_points_delivered=delivered,
                cycle_time_days=round(random.uniform(1, 5), 1),
                lead_time_days=round(random.uniform(3, 10), 1),
                defect_leakage_count=defects,
                release_success=release_ok,
                delivery_score=score,
            ))
            count += 1
    db.flush()
    print(f"  Seeded {count} delivery metric records")


def seed_allocations(db, all_employees, projects):
    today = date.today()
    count = 0
    for emp in random.sample(all_employees, min(50, len(all_employees))):
        period_start = today - timedelta(days=30)
        period_end = today + timedelta(days=60)
        alloc_pct = random.choice([25.0, 50.0, 75.0, 100.0])
        project = random.choice(projects) if projects else None
        db.add(ResourceAllocation(
            employee_id=emp.id,
            project_id=project.id if project else None,
            allocation_percentage=alloc_pct,
            period_start=period_start,
            period_end=period_end,
            is_over_allocated=alloc_pct > 100,
        ))
        count += 1
    db.flush()
    print(f"  Seeded {count} resource allocation records")


# ─── Main ─────────────────────────────────────────────────────────────────────

def run():
    print("Starting seed...")
    db = SessionLocal()
    try:
        # Check if already seeded
        existing = db.query(Team).first()
        if existing:
            print("Database already seeded. Skipping.")
            return

        print("Seeding teams...")
        team_map = seed_teams(db)

        print("Seeding skills...")
        skills = seed_skills(db)

        print("Seeding employees and squads...")
        all_employees, all_squads = seed_employees_and_squads(db, team_map, skills)

        print("Seeding projects...")
        projects = seed_projects(db, team_map, all_squads, all_employees)

        print("Seeding authorizations...")
        seed_authorizations(db, all_employees)

        print("Seeding delivery metrics...")
        seed_delivery_metrics(db, all_squads, projects)

        print("Seeding resource allocations...")
        seed_allocations(db, all_employees, projects)

        db.commit()
        print("\nSeed completed successfully!")
        print(f"  Teams: {len(team_map)}")
        print(f"  Squads: {len(all_squads)}")
        print(f"  Employees: {len(all_employees)}")
        print(f"  Projects: {len(projects)}")
        print(f"  Skills: {len(skills)}")

    except Exception as e:
        db.rollback()
        print(f"Seed failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    finally:
        db.close()


if __name__ == "__main__":
    run()
