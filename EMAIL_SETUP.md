# Email Setup Instructions

To enable email notifications for contact form submissions, you need to configure Gmail App Password.

## Steps to Set Up Gmail App Password

1. **Enable 2-Step Verification** (if not already enabled):
   - Go to https://myaccount.google.com/security
   - Enable 2-Step Verification

2. **Generate App Password**:
   - Go to https://myaccount.google.com/apppasswords
   - Select "Mail" as the app
   - Select "Other (Custom name)" as the device
   - Enter "Portfolio Website" as the name
   - Click "Generate"
   - Copy the 16-character password (it will look like: xxxx xxxx xxxx xxxx)

3. **Create .env file**:
   - Copy `.env.example` to `.env`
   - Replace `your_app_password_here` with the 16-character app password (remove spaces)
   - The .env file should look like:
     ```
     SMTP_SERVER=smtp.gmail.com
     SMTP_PORT=587
     EMAIL_USER=hariniportfolio.contact@gmail.com
     EMAIL_PASSWORD=xxxxxxxxxxxxxxxx
     RECIPIENT_EMAIL=hariniportfolio.contact@gmail.com
     ```

4. **Test the Setup**:
   - Restart your FastAPI server
   - Submit a test message through the contact form
   - Check your email inbox for the notification

## Important Notes

- **Never commit .env file to git** - it contains sensitive information
- Use App Password, NOT your regular Gmail password
- The .env file is already in .gitignore (if you have one)

## Troubleshooting

- If emails don't send, check the server console for error messages
- Make sure 2-Step Verification is enabled
- Verify the app password is correct (no spaces)
- Check that .env file is in the project root directory

