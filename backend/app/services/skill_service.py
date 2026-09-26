from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import HTTPException
from app.models.skill import Skill
from app.models.employee_skill import EmployeeSkill
from app.models.employee import Employee
from app.models.capability_requirement import CapabilityRequirement
from app.models.project import Project, ProjectStatus
from app.models.project_assignment import ProjectEmployeeAssignment
from app.schemas.skill import SkillCreate


def get_skills(db: Session) -> List[Skill]:
    return db.query(Skill).all()


def create_skill(db: Session, data: SkillCreate) -> Skill:
    existing = db.query(Skill).filter(Skill.name == data.name).first()
    if existing:
        raise HTTPException(status_code=409, detail="Skill already exists")
    skill = Skill(**data.model_dump())
    db.add(skill)
    db.commit()
    db.refresh(skill)
    return skill


def get_capability_matrix(db: Session) -> List[dict]:
    employees = db.query(Employee).filter(Employee.is_active == True).all()
    skills = db.query(Skill).all()
    result = []
    for emp in employees:
        emp_skills = db.query(EmployeeSkill).filter(EmployeeSkill.employee_id == emp.id).all()
        skill_map = {es.skill_id: es.proficiency_level for es in emp_skills}
        result.append({
            "employee_id": emp.id,
            "employee_name": emp.name,
            "skills": [
                {
                    "skill_id": s.id,
                    "skill_name": s.name,
                    "skill_category": s.category,
                    "proficiency_level": skill_map.get(s.id),
                }
                for s in skills
            ],
        })
    return result


def get_skill_gaps(db: Session) -> List[dict]:
    """Return projects with capability requirements that have insufficient coverage."""
    active_projects = db.query(Project).filter(Project.status == ProjectStatus.Active).all()
    gaps = []
    for project in active_projects:
        reqs = db.query(CapabilityRequirement).filter(CapabilityRequirement.project_id == project.id).all()
        project_gaps = []
        for req in reqs:
            skill = db.query(Skill).filter(Skill.id == req.skill_id).first()
            # Count assigned employees on project who have required skill at required proficiency
            assigned_emp_ids = db.query(ProjectEmployeeAssignment.employee_id).filter(
                ProjectEmployeeAssignment.project_id == project.id
            ).subquery()
            qualified_count = db.query(func.count(EmployeeSkill.id)).filter(
                EmployeeSkill.employee_id.in_(assigned_emp_ids),
                EmployeeSkill.skill_id == req.skill_id,
            ).scalar() or 0
            if qualified_count < req.headcount_needed:
                project_gaps.append({
                    "skill_id": req.skill_id,
                    "skill_name": skill.name if skill else "Unknown",
                    "required_proficiency": req.required_proficiency,
                    "headcount_needed": req.headcount_needed,
                    "headcount_available": qualified_count,
                    "gap": req.headcount_needed - qualified_count,
                })
        if project_gaps:
            gaps.append({
                "project_id": project.id,
                "project_name": project.name,
                "gaps": project_gaps,
            })
    return gaps
