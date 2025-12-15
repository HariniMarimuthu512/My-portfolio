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
    {"name": "Python", "level": "expert", "category": "Programming Languages"},
    {"name": "FastAPI", "level": "advanced", "category": "Frameworks"},
    {"name": "React", "level": "intermediate", "category": "Frameworks"},
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
