"""
Portfolio-related API endpoints
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from typing import List, Optional
import logging

# ✅ Import SendGrid-based email functions ONLY
from utils.email_service import send_contact_email, send_acknowledgement_email

router = APIRouter()
logger = logging.getLogger("uvicorn")


# =========================
# Models
# =========================

class ContactRequest(BaseModel):
    name: str
    email: EmailStr
    message: str
    subject: Optional[str] = None


class Project(BaseModel):
    id: int
    title: str
    description: str
    technologies: List[str]
    github_url: Optional[str] = None
    live_url: Optional[str] = None
    image_url: Optional[str] = None


class Skill(BaseModel):
    name: str
    level: str
    category: str


# =========================
# Sample Data
# =========================

PROJECTS = [
    {
        "id": 1,
        "title": "CANDOR DATA PLATFORM",
        "description": "Automated end-to-end data warehouse lifecycle using AI-assisted workflows.",
        "technologies": ["Python", "React", "AWS Bedrock"],
    },
    {
        "id": 2,
        "title": "Sales Inquiry Automation",
        "description": "AI-powered email classification and response system.",
        "technologies": ["FastAPI", "React", "SQLite"],
    },
]

SKILLS = [
    # Programming Languages
    {"name": "Python", "level": "expert", "category": "Programming Languages"},
    {"name": "C", "level": "advanced", "category": "Programming Languages"},

    # Frameworks
    {"name": "FastAPI", "level": "advanced", "category": "Frameworks"},
    {"name": "React", "level": "intermediate", "category": "Frameworks"},
    {"name": "Flask", "level": "advanced", "category": "Frameworks"},

    # Database Systems
    {"name": "MySQL", "level": "advanced", "category": "Database Systems"},
    {"name": "SQL", "level": "advanced", "category": "Database Systems"},
    {"name": "SQLite", "level": "basic", "category": "Database Systems"},

    # Technical Libraries
    {"name": "NumPy", "level": "advanced", "category": "Technical Libraries"},
    {"name": "Pandas", "level": "advanced", "category": "Technical Libraries"},
    {"name": "Scikit-learn", "level": "intermediate", "category": "Technical Libraries"},
    {"name": "OpenCV", "level": "intermediate", "category": "Technical Libraries"},

    # Web Development
    {"name": "HTML", "level": "advanced", "category": "Web Development"},
    {"name": "CSS", "level": "advanced", "category": "Web Development"},
    {"name": "JavaScript", "level": "advanced", "category": "Web Development"},

    # Domain Expertise
    {"name": "Cybersecurity", "level": "intermediate", "category": "Domain Expertise"},
    {"name": "REST APIs", "level": "advanced", "category": "Domain Expertise"},
    {"name": "OOP", "level": "advanced", "category": "Domain Expertise"},

    # Tools & Platforms
    {"name": "Git", "level": "intermediate", "category": "Tools & Platforms"},
    {"name": "WordPress", "level": "intermediate", "category": "Tools & Platforms"},
]


# =========================
# Routes
# =========================

@router.get("/projects", response_model=List[Project])
async def get_projects():
    return PROJECTS


@router.get("/skills", response_model=List[Skill])
async def get_skills():
    return SKILLS


@router.post("/contact")
async def submit_contact(contact: ContactRequest):
    """
    Handle contact form submission
    """

    name = contact.name
    email = contact.email
    subject = contact.subject or "Portfolio Contact"
    message = contact.message

    logger.info("📩 Contact form submitted")
    logger.info(f"Name: {name}")
    logger.info(f"Email: {email}")
    logger.info(f"Subject: {subject}")

    # -------------------------
    # Send submission email
    # -------------------------
    try:
        sent = send_contact_email(
            name=name,
            sender_email=email,
            subject=subject,
            message=message,
        )
        if sent:
            logger.info("✅ Submission email sent via SendGrid")
        else:
            logger.error("❌ Submission email failed")
    except Exception as e:
        logger.exception("❌ Error sending submission email")

    # -------------------------
    # Send acknowledgement email
    # -------------------------
    try:
        ack = send_acknowledgement_email(
            name=name,
            recipient_email=email,
            subject=subject,
        )
        if ack:
            logger.info("✅ Acknowledgement email sent via SendGrid")
        else:
            logger.error("❌ Acknowledgement email failed")
    except Exception as e:
        logger.exception("❌ Error sending acknowledgement email")

    # -------------------------
    # Always return success
    # -------------------------
    return {
        "success": True,
        "message": "Thank you for your message! I'll get back to you soon.",
        "data": {
            "name": name,
            "email": email,
            "subject": subject,
        },
    }

