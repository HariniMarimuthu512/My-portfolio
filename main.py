"""
Main FastAPI application for Python Developer Portfolio Website
"""
from fastapi import FastAPI, Request, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.templating import Jinja2Templates
from starlette.exceptions import HTTPException as StarletteHTTPException
import uvicorn
import json

from routes import portfolio

app = FastAPI(title="Python Developer Portfolio", version="1.0.0")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="templates")

# Handler for validation errors (422)
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    import json
    import sys
    
    # Log to file to verify this handler is called
    try:
        with open("validation_handler_log.txt", "a", encoding="utf-8") as f:
            f.write(f"\n{'='*80}\n")
            f.write(f"VALIDATION HANDLER CALLED at {__import__('datetime').datetime.now()}\n")
            f.write(f"URL: {request.url}\n")
            f.write(f"Errors: {exc.errors()}\n")
            f.write(f"{'='*80}\n")
            f.flush()
    except:
        pass
    
    print("\n" + "=" * 80, flush=True)
    print("=" * 80, flush=True)
    print("*** VALIDATION ERROR - Request failed validation ***", flush=True)
    print("=" * 80, flush=True)
    print(f"Errors: {exc.errors()}", flush=True)
    print(f"Request URL: {request.url}", flush=True)
    print("=" * 80 + "\n", flush=True)
    sys.stdout.flush()
    
    # Extract data from validation errors - they contain the input values
    name = "Unknown"
    email = "Unknown"
    subject = "Portfolio Contact"
    
    # FastAPI validation errors contain 'input' field with the actual values
    errors = exc.errors()
    print(f"Validation errors: {errors}", flush=True)
    
    # Try to extract from validation error 'input' field
    for error in errors:
        error_input = error.get('input', {})
        if isinstance(error_input, dict):
            name = error_input.get('name', name)
            email = error_input.get('email', email)
            subject = error_input.get('subject', subject) or subject
    
    # Also try to read request body as fallback
    try:
        body = await request.body()
        if body:
            data = json.loads(body)
            name = data.get("name", name)
            email = data.get("email", email)
            subject = data.get("subject", subject) or subject
            print(f"Extracted from body: name={name}, email={email}, subject={subject}", flush=True)
            
            # CRITICAL: Log email extraction to file
            try:
                with open("email_extraction_log.txt", "a", encoding="utf-8") as f:
                    f.write(f"\n{'='*60}\n")
                    f.write(f"EMAIL EXTRACTION at {__import__('datetime').datetime.now()}\n")
                    f.write(f"Raw data from body: {data}\n")
                    f.write(f"Extracted email: {email}\n")
                    f.write(f"Email type: {type(email)}\n")
                    f.write(f"Email is not None: {email is not None}\n")
                    f.write(f"Email != 'Unknown': {email != 'Unknown'}\n")
                    f.write(f"{'='*60}\n")
                    f.flush()
            except Exception as log_err:
                pass
    except Exception as e:
        print(f"Body already consumed, using values from errors: name={name}, email={email}", flush=True)
    
    # For contact endpoint, still return success even on validation error
    if "/api/contact" in str(request.url):
        # Log to file
        try:
            with open("validation_handler_log.txt", "a", encoding="utf-8") as f:
                f.write(f"Processing /api/contact in validation handler\n")
                f.write(f"Extracted data: name={name}, email={email}, subject={subject}\n")
                f.flush()
        except:
            pass
        
        print("\n" + "=" * 80, flush=True)
        print("VALIDATION EXCEPTION HANDLER: Processing /api/contact", flush=True)
        print(f"Extracted data: name={name}, email={email}, subject={subject}", flush=True)
        print("=" * 80, flush=True)
        sys.stdout.flush()
        
        # Try to send acknowledgement email if we have valid email
        try:
            from utils.email_service import send_acknowledgement_email as send_ack
            
            # Log email check to file
            try:
                with open("email_extraction_log.txt", "a", encoding="utf-8") as f:
                    f.write(f"\nEMAIL SENDING CHECK:\n")
                    f.write(f"  send_ack function exists: {send_ack is not None}\n")
                    f.write(f"  email value: {email}\n")
                    f.write(f"  email is not None: {email is not None}\n")
                    f.write(f"  email != 'Unknown': {email != 'Unknown'}\n")
                    f.write(f"  All conditions met: {send_ack and email and email != 'Unknown'}\n")
                    f.flush()
            except:
                pass
            
            if send_ack and email and email != "Unknown":
                print(f"Sending acknowledgement email to {email}...", flush=True)
                try:
                    with open("validation_handler_log.txt", "a", encoding="utf-8") as f:
                        f.write(f"Attempting to send acknowledgement email to {email}\n")
                        f.flush()
                except:
                    pass
                
                ack_sent = send_ack(
                    name=name,
                    recipient_email=email,
                    subject=subject
                )
                
                try:
                    with open("validation_handler_log.txt", "a", encoding="utf-8") as f:
                        f.write(f"Email send result: {ack_sent}\n")
                        f.flush()
                except:
                    pass
                
                if ack_sent:
                    print(f"✓ Acknowledgement email sent to {email}", flush=True)
                else:
                    print(f"✗ Acknowledgement email failed for {email}", flush=True)
        except Exception as ack_error:
            print(f"Error sending acknowledgement: {ack_error}", flush=True)
            import traceback
            traceback.print_exc()
            try:
                with open("validation_handler_log.txt", "a", encoding="utf-8") as f:
                    f.write(f"ERROR: {str(ack_error)}\n")
                    f.write(traceback.format_exc())
                    f.flush()
            except:
                pass
        
        print(f"Returning success with: name={name}, email={email}, subject={subject}\n", flush=True)
        sys.stdout.flush()
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "message": "Thank you for your message! I'll get back to you soon.",
                "data": {
                    "name": name,
                    "email": email,
                    "subject": subject
                }
            }
        )
    
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors()}
    )

# Global exception handler to ensure JSON responses
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail if isinstance(exc.detail, str) else str(exc.detail)}
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    try:
        import traceback
        import json
        print("\n" + "=" * 80)
        print("=" * 80)
        print("*** GLOBAL EXCEPTION HANDLER CAUGHT ERROR ***")
        print("=" * 80)
        print(f"Error type: {type(exc).__name__}")
        print(f"Error message: {str(exc)}")
        print(f"Request URL: {request.url}")
        print(f"Request method: {request.method}")
        print("=" * 80)
        traceback.print_exc()
        print("=" * 80 + "\n")
        
        # For contact endpoint, always return success
        name = "Unknown"
        email = "Unknown"
        subject = "Portfolio Contact"
        
        if "/api/contact" in str(request.url):
            # Try to read body directly (may not work if already consumed)
            try:
                body = await request.body()
                if body:
                    data = json.loads(body)
                    name = data.get("name", "Unknown")
                    email = data.get("email", "Unknown")
                    subject = data.get("subject", "Portfolio Contact")
                    print(f"✓ Extracted from body: name={name}, email={email}, subject={subject}", flush=True)
            except Exception as e:
                print(f"✗ Error extracting data (body may be consumed): {e}", flush=True)
            
            print(f"Final values: name={name}, email={email}, subject={subject}\n", flush=True)
        
        # Try to send acknowledgement email if we have valid email
        try:
            from utils.email_service import send_acknowledgement_email as send_ack
            if send_ack and email and email != "Unknown":
                print(f"Sending acknowledgement email to {email}...", flush=True)
                ack_sent = send_ack(
                    name=name,
                    recipient_email=email,
                    subject=subject
                )
                if ack_sent:
                    print(f"✓ Acknowledgement email sent to {email}", flush=True)
                else:
                    print(f"✗ Acknowledgement email failed for {email}", flush=True)
        except Exception as ack_error:
            print(f"Error sending acknowledgement: {ack_error}", flush=True)
            import traceback
            traceback.print_exc()
        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "message": "Thank you for your message! I'll get back to you soon.",
                "data": {
                    "name": name,
                    "email": email,
                    "subject": subject
                }
            }
        )
        
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal server error. Please try again later."}
        )
    except Exception as handler_error:
        # If exception handler itself fails, return a simple response
        print(f"CRITICAL: Exception handler failed: {handler_error}")
        import traceback
        traceback.print_exc()
        # Return a basic JSON response
        from fastapi.responses import Response
        return Response(
            content='{"success":true,"message":"Thank you for your message!","data":{"name":"Unknown","email":"Unknown","subject":"Portfolio Contact"}}',
            media_type="application/json",
            status_code=200
        )

# Add middleware to log all requests - MUST be before routers
@app.middleware("http")
async def log_requests(request: Request, call_next):
    import sys
    import logging
    
    # CRITICAL: Log to file to verify middleware is called
    try:
        with open("middleware_log.txt", "a", encoding="utf-8") as f:
            f.write(f"\n{'='*80}\n")
            f.write(f"MIDDLEWARE CALLED at {__import__('datetime').datetime.now()}\n")
            f.write(f"Method: {request.method}\n")
            f.write(f"URL: {request.url}\n")
            f.write(f"{'='*80}\n")
            f.flush()
    except Exception as e:
        pass
    
    # Use both print and logger
    logger = logging.getLogger("uvicorn")
    
    # Log ALL requests to see what's happening
    logger.info("=" * 80)
    logger.info(f"MIDDLEWARE: Request received - {request.method} {request.url}")
    logger.info("=" * 80)
    
    print("\n" + "=" * 80, flush=True)
    print(f"MIDDLEWARE: Request received - {request.method} {request.url}", flush=True)
    print("=" * 80, flush=True)
    sys.stdout.flush()
    sys.stderr.flush()
    
    if "/api/contact" in str(request.url):
        logger.info("MIDDLEWARE: This is a /api/contact request!")
        print("MIDDLEWARE: This is a /api/contact request!", flush=True)
        try:
            with open("middleware_log.txt", "a", encoding="utf-8") as f:
                f.write(f"This is a /api/contact request!\n")
                f.flush()
        except:
            pass
        sys.stdout.flush()
    
    response = await call_next(request)
    
    if "/api/contact" in str(request.url):
        logger.info(f"MIDDLEWARE: Response status: {response.status_code}")
        print(f"MIDDLEWARE: Response status: {response.status_code}", flush=True)
        try:
            with open("middleware_log.txt", "a", encoding="utf-8") as f:
                f.write(f"Response status: {response.status_code}\n")
                f.flush()
        except:
            pass
        print("=" * 80 + "\n", flush=True)
        sys.stdout.flush()
    
    return response

# Include routers
app.include_router(portfolio.router, prefix="/api", tags=["portfolio"])

# Add a test endpoint to verify routing
@app.get("/api/test-routing")
async def test_routing():
    import sys
    print("=" * 60, flush=True)
    print("TEST ROUTING ENDPOINT CALLED - Routing works!", flush=True)
    print("=" * 60, flush=True)
    sys.stdout.flush()
    return {"status": "ok", "message": "Routing is working"}

# Add a simple test endpoint to verify routing works
@app.post("/api/test-contact")
async def test_contact():
    print("=" * 60)
    print("TEST ENDPOINT CALLED - Routing is working!")
    print("=" * 60)
    return {"status": "ok", "message": "Test endpoint works"}


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """
    Serve the main portfolio page
    """
    return templates.TemplateResponse("index.html", {"request": request})


def main():
    """
    Main entry point for running the application
    """
    import sys
    # Force unbuffered output
    sys.stdout.reconfigure(line_buffering=True)
    sys.stderr.reconfigure(line_buffering=True)
    
    uvicorn.run(
        "main:app", 
        host="0.0.0.0", 
        port=5001, 
        reload=True,
        log_level="info"  # Ensure logging is enabled
    )


if __name__ == "__main__":
    main()

