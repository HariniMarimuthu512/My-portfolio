"""
Portfolio-related API endpoints
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from typing import List, Optional
import os
import sys
import logging
from pathlib import Path

# Add project root to path for utils import
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Initialize defaults first
RECIPIENT_EMAIL = "hariniportfolio.contact@gmail.com"

def send_contact_email(*args, **kwargs):
    """Default fallback function"""
    print("Email service not available. Install dependencies and configure .env file.")
    return False

# Try to import email service
send_acknowledgement_email = None
try:
    from utils.email_service import send_contact_email as _send_email, RECIPIENT_EMAIL as _recipient, send_acknowledgement_email as _send_ack
    send_contact_email = _send_email
    send_acknowledgement_email = _send_ack
    if _recipient:
        RECIPIENT_EMAIL = _recipient
except ImportError as e:
    # Fallback if utils not found
    print(f"Warning: Could not import email service: {e}")
except AttributeError as e:
    # Handle case where RECIPIENT_EMAIL doesn't exist in module
    print(f"Warning: RECIPIENT_EMAIL not found in email_service: {e}")
    try:
        from utils.email_service import send_contact_email as _send_email, send_acknowledgement_email as _send_ack
        send_contact_email = _send_email
        send_acknowledgement_email = _send_ack
    except:
        pass
except Exception as e:
    # Handle any other errors during import
    print(f"Warning: Error importing email service: {e}")
    import traceback
    traceback.print_exc()

router = APIRouter()


class ContactRequest(BaseModel):
    """
    Contact form request model
    """
    name: str
    email: EmailStr
    message: str
    subject: Optional[str] = None


class Project(BaseModel):
    """
    Project model
    """
    id: int
    title: str
    description: str
    technologies: List[str]
    github_url: Optional[str] = None
    live_url: Optional[str] = None
    image_url: Optional[str] = None


class Skill(BaseModel):
    """
    Skill model
    """
    name: str
    level: str  # beginner, intermediate, advanced, expert
    category: str  # language, framework, tool, etc.


# Sample data - in production, this would come from a database
PROJECTS = [
    {
        "id": 1,
        "title": "CANDOR DATA PLATFORM",
        "description": "Automated the end-to-end data-warehouse lifecycle by ingesting, transforming, modeling, and deploying data from heterogeneous sources using an AI-assisted \"vibe coding\" environment, significantly reducing manual scripting and accelerating delivery.",
        "technologies": ["Python", "React", "JavaScript", "TypeScript", "AWS Bedrock", "Claude"],
        "github_url": None,
        "live_url": None,
        "image_url": None
    },
    {
        "id": 2,
        "title": "SALES INQUIRY Automation System",
        "description": "Managed the inquiry processing workflow by scanning, classifying, and routing large volumes of emails for hotels and travel agencies. Built scheduled email processing with escalation flows and AI-driven classification to reduce manual effort. Developed a React + FastAPI solution with an optimized SQLite backend to enable real-time AI-generated responses.",
        "technologies": ["Python", "FastAPI", "React.js", "SQLite", "AI/ML Models", "Task Scheduling", "Batch Processing"],
        "github_url": None,
        "live_url": None,
        "image_url": None
    },
    {
        "id": 3,
        "title": "Leveraging Object Detection for Enhanced Security in Theatre Seating Arrangements under Low-Light Conditions",
        "description": "Developed a low-light image enhancement and object-detection system for analyzing theatre seating arrangements. Enhanced dark frames using MIRNet and applied YOLOv3 for accurate, real-time detection under challenging lighting.",
        "technologies": ["Python", "YOLOv3", "MIRNet", "OpenCV", "Deep Learning"],
        "github_url": None,
        "live_url": None,
        "image_url": None
    },
    {
        "id": 4,
        "title": "Mitigating Distributed Denial of Service (DDoS) Attacks for Web Security",
        "description": "Collaborated with the security team to optimize firewall configurations, tune intrusion detection systems, and deploy protection plugins. Implemented Wordfence for enhanced DDoS protection and threat visibility across WordPress environments.",
        "technologies": ["Kali Linux", "WordPress", "Python", "Pentmenu", "Wordfence Plugin"],
        "github_url": None,
        "live_url": None,
        "image_url": None
    }
]

SKILLS = [
    # Programming Languages
    {"name": "Python", "level": "expert", "category": "Programming Languages"},
    {"name": "C", "level": "advanced", "category": "Programming Languages"},
    # Web Development
    {"name": "HTML", "level": "advanced", "category": "Web Development"},
    {"name": "CSS", "level": "advanced", "category": "Web Development"},
    {"name": "JavaScript", "level": "advanced", "category": "Web Development"},
    # Frameworks
    {"name": "Flask", "level": "advanced", "category": "Frameworks"},
    {"name": "React.js", "level": "intermediate", "category": "Frameworks"},
    # Database Systems
    {"name": "MySQL", "level": "advanced", "category": "Database Systems"},
    {"name": "SQL", "level": "advanced", "category": "Database Systems"},
    {"name": "SQLite", "level": "basic", "category": "Database Systems"},
    # Development Environment
    {"name": "Visual Studio Code", "level": "advanced", "category": "Development Environment"},
    # Technical Libraries
    {"name": "NumPy", "level": "advanced", "category": "Technical Libraries"},
    {"name": "Pandas", "level": "advanced", "category": "Technical Libraries"},
    {"name": "Scikit-learn", "level": "advanced", "category": "Technical Libraries"},
    {"name": "OpenCV", "level": "advanced", "category": "Technical Libraries"},
    {"name": "YOLOv3", "level": "basic", "category": "Technical Libraries"},
    # Domain Expertise
    {"name": "Cybersecurity", "level": "advanced", "category": "Domain Expertise"},
    {"name": "OOP", "level": "advanced", "category": "Domain Expertise"},
    {"name": "Data Structures", "level": "advanced", "category": "Domain Expertise"},
    {"name": "REST APIs", "level": "advanced", "category": "Domain Expertise"},
    # Tools & Platforms
    {"name": "Kali Linux", "level": "intermediate", "category": "Tools & Platforms"},
    {"name": "Pentmenu", "level": "intermediate", "category": "Tools & Platforms"},
    {"name": "Wordfence", "level": "intermediate", "category": "Tools & Platforms"},
    {"name": "WordPress", "level": "intermediate", "category": "Tools & Platforms"}
]


@router.get("/projects", response_model=List[Project])
async def get_projects():
    """
    Get all portfolio projects
    """
    return PROJECTS


@router.get("/projects/{project_id}", response_model=Project)
async def get_project(project_id: int):
    """
    Get a specific project by ID
    """
    project = next((p for p in PROJECTS if p["id"] == project_id), None)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@router.get("/skills", response_model=List[Skill])
async def get_skills():
    """
    Get all skills
    """
    return SKILLS


@router.get("/test")
async def test_endpoint():
    """Test endpoint to verify server is working"""
    import sys
    print("=" * 60, flush=True)
    print("TEST ENDPOINT CALLED - Portfolio router is working!", flush=True)
    print("=" * 60, flush=True)
    sys.stdout.flush()
    return {"status": "ok", "message": "Server is working"}


@router.post("/contact")
async def submit_contact(contact: ContactRequest):
    """
    Handle contact form submission and send email notification
    Always returns success, even if email fails
    """
    import sys
    import os
    import logging
    
    # CRITICAL: Write to a file to verify endpoint is called
    try:
        with open("contact_log.txt", "a", encoding="utf-8") as f:
            f.write(f"\n{'='*80}\n")
            f.write(f"ENDPOINT CALLED at {__import__('datetime').datetime.now()}\n")
            f.write(f"{'='*80}\n")
            f.flush()
    except:
        pass
    
    # Use Python's logging module which works better with uvicorn
    logger = logging.getLogger("uvicorn")
    
    # Log immediately when endpoint is called - use both print and logger
    logger.error("=" * 80)  # Use error level to ensure it shows
    logger.error("*** ENDPOINT CALLED - STARTING PROCESSING ***")
    logger.error("=" * 80)
    
    # Also use print statements
    print("\n\n" + "=" * 80, flush=True)
    print("=" * 80, flush=True)
    print("*** ENDPOINT CALLED - STARTING PROCESSING ***", flush=True)
    print("=" * 80, flush=True)
    print(f"Contact object type: {type(contact)}", flush=True)
    print(f"Contact object: {contact}", flush=True)
    sys.stdout.flush()
    sys.stderr.flush()
    
    # Wrap everything in try/except to ensure we always return a response
    try:
        # Extract contact data directly - Pydantic models guarantee these attributes exist
        print("Attempting to extract name...", flush=True)
        name = contact.name
        print(f"Name extracted: {name}", flush=True)
        
        print("Attempting to extract email...", flush=True)
        email = contact.email
        print(f"Email extracted: {email}", flush=True)
        
        print("Attempting to extract subject...", flush=True)
        subject = contact.subject if contact.subject else "Portfolio Contact"
        print(f"Subject extracted: {subject}", flush=True)
        
        print("Attempting to extract message...", flush=True)
        message = contact.message
        print(f"Message extracted (length: {len(str(message))})", flush=True)
        
        # VERY VISIBLE LOGGING - This MUST appear in server terminal
        logger = logging.getLogger("uvicorn")
        logger.error("=" * 80)
        logger.error("*** CONTACT FORM SUBMITTED - ENDPOINT CALLED ***")
        logger.error(f"  Name: {name}")
        logger.error(f"  Email: {email}")
        logger.error(f"  Subject: {subject}")
        logger.error(f"  Message length: {len(str(message))} chars")
        logger.error("=" * 80)
        
        print("\n\n" + "=" * 80, flush=True)
        print("=" * 80, flush=True)
        print("*** CONTACT FORM SUBMITTED - ENDPOINT CALLED ***", flush=True)
        print("=" * 80, flush=True)
        print(f"  Name: {name}", flush=True)
        print(f"  Email: {email}", flush=True)
        print(f"  Subject: {subject}", flush=True)
        print(f"  Message length: {len(str(message))} chars", flush=True)
        print("=" * 80 + "\n", flush=True)
        sys.stdout.flush()
        
        # Try to send notification email to portfolio owner (but don't fail if it doesn't work)
        email_sent = False
        try:
            email_sent = send_contact_email(
                name=name,
                sender_email=email,
                subject=subject,
                message=message
            )
            if email_sent:
                print(f"✓ Notification email sent successfully to {RECIPIENT_EMAIL}", flush=True)
            else:
                print(f"✗ Notification email NOT sent (check EMAIL_PASSWORD in .env file)", flush=True)
        except Exception as email_error:
            print(f"✗ Notification email sending failed: {str(email_error)}", flush=True)
            import traceback
            traceback.print_exc()
            email_sent = False
        
        # Send acknowledgement email to the person who submitted the form
        # CRITICAL: Log to file to verify this code runs
        try:
            with open("contact_log.txt", "a", encoding="utf-8") as f:
                f.write(f"\n{'='*60}\n")
                f.write(f"ACKNOWLEDGEMENT EMAIL CHECK:\n")
                f.write(f"  send_acknowledgement_email function: {send_acknowledgement_email}\n")
                f.write(f"  email: {email}\n")
                f.write(f"  email != 'Unknown': {email != 'Unknown'}\n")
                f.write(f"{'='*60}\n")
                f.flush()
        except Exception as log_err:
            pass
        
        logger = logging.getLogger("uvicorn")
        logger.error("=" * 60)
        logger.error("ACKNOWLEDGEMENT EMAIL CHECK:")
        logger.error(f"  send_acknowledgement_email function: {send_acknowledgement_email}")
        logger.error(f"  email: {email}")
        logger.error(f"  email != 'Unknown': {email != 'Unknown'}")
        logger.error("=" * 60)
        
        print(f"\n{'='*60}", flush=True)
        print(f"ACKNOWLEDGEMENT EMAIL CHECK:", flush=True)
        print(f"  send_acknowledgement_email function: {send_acknowledgement_email}", flush=True)
        print(f"  email: {email}", flush=True)
        print(f"  email != 'Unknown': {email != 'Unknown'}", flush=True)
        print(f"{'='*60}\n", flush=True)
        
        # ALWAYS try to send acknowledgement email
        ack_sent = False
        try:
            if send_acknowledgement_email and email and email != "Unknown":
                print(f"Attempting to send acknowledgement email to {email}...", flush=True)
                sys.stdout.flush()
                
                # Log to file
                try:
                    with open("contact_log.txt", "a", encoding="utf-8") as f:
                        f.write(f"Calling send_acknowledgement_email with:\n")
                        f.write(f"  name={name}\n")
                        f.write(f"  recipient_email={email}\n")
                        f.write(f"  subject={subject}\n")
                        f.flush()
                except:
                    pass
                
                ack_sent = send_acknowledgement_email(
                    name=name,
                    recipient_email=email,
                    subject=subject
                )
                
                # Log result to file
                try:
                    with open("contact_log.txt", "a", encoding="utf-8") as f:
                        f.write(f"send_acknowledgement_email returned: {ack_sent}\n")
                        f.flush()
                except:
                    pass
                
                if ack_sent:
                    print(f"✓ Acknowledgement email sent successfully to {email}", flush=True)
                else:
                    print(f"✗ Acknowledgement email NOT sent to {email} (check EMAIL_PASSWORD in .env)", flush=True)
            else:
                reason = "function not available" if not send_acknowledgement_email else f"invalid email: {email}"
                print(f"✗ Cannot send acknowledgement - {reason}", flush=True)
                try:
                    with open("contact_log.txt", "a", encoding="utf-8") as f:
                        f.write(f"Cannot send acknowledgement - {reason}\n")
                        f.flush()
                except:
                    pass
        except Exception as ack_error:
            print(f"✗ Acknowledgement email sending failed: {str(ack_error)}", flush=True)
            import traceback
            traceback.print_exc()
            try:
                with open("contact_log.txt", "a", encoding="utf-8") as f:
                    f.write(f"ERROR sending acknowledgement: {str(ack_error)}\n")
                    f.write(traceback.format_exc())
                    f.flush()
            except:
                pass
            # Don't fail the request if acknowledgement fails
        
        # ALWAYS return success response with actual data
        print("=" * 60, flush=True)
        print("RETURNING SUCCESS RESPONSE", flush=True)
        print(f"Returning: name={name}, email={email}, subject={subject}", flush=True)
        print("=" * 60 + "\n", flush=True)
        sys.stdout.flush()
        
        return {
            "success": True,
            "message": "Thank you for your message! I'll get back to you soon.",
            "data": {
                "name": name,
                "email": email,
                "subject": subject
            }
        }
    except Exception as e:
        # If anything fails, try to extract data from contact object if possible
        print(f"ERROR in endpoint: {e}", flush=True)
        import traceback
        traceback.print_exc()
        sys.stdout.flush()
        
        # Try to extract data even if there was an error
        name = "Unknown"
        email = "Unknown"
        subject = "Portfolio Contact"
        
        try:
            # Try to get data from contact object using different methods
            if hasattr(contact, 'name'):
                name = getattr(contact, 'name', 'Unknown')
            if hasattr(contact, 'email'):
                email = getattr(contact, 'email', 'Unknown')
            if hasattr(contact, 'subject'):
                subject = getattr(contact, 'subject', 'Portfolio Contact') or "Portfolio Contact"
            
            # Try dict() method as fallback
            if hasattr(contact, 'dict'):
                contact_dict = contact.dict()
                name = contact_dict.get('name', name)
                email = contact_dict.get('email', email)
                subject = contact_dict.get('subject', subject) or subject
            elif hasattr(contact, 'model_dump'):
                contact_dict = contact.model_dump()
                name = contact_dict.get('name', name)
                email = contact_dict.get('email', email)
                subject = contact_dict.get('subject', subject) or subject
        except Exception as extract_error:
            print(f"Could not extract data from contact object: {extract_error}", flush=True)
        
        print(f"Returning with extracted values: name={name}, email={email}, subject={subject}", flush=True)
        sys.stdout.flush()
        
        return {
            "success": True,
            "message": "Thank you for your message! I'll get back to you soon.",
            "data": {
                "name": name,
                "email": email,
                "subject": subject
            }
        }

