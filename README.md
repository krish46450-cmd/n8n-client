# Windows Dump Analyzer - Client App

A comprehensive Flask-based web application for analyzing Windows dump files, managing support tickets, and providing AI-powered assistance.

## Features

### Core Features
- 🔐 **User Authentication**: Secure registration and login system
- 🎫 **Support Ticket System**: Create and track support requests
- 💬 **AI Chatbot**: Google Gemini-powered assistant for troubleshooting
- 📊 **Dashboard**: Analytics and system overview
- 📧 **Email Notifications**: Automated email alerts for tickets
- 📤 **Export Functions**: Export tickets and conversations to CSV

### Advanced Features
- 🖼️ **Image Upload**: Upload screenshots to chatbot and tickets
- 📚 **Knowledge Base**: Store and retrieve solutions
- 🔄 **Support Dashboard Integration**: Connect with support team dashboard
- 🎨 **Responsive Design**: Works on desktop and mobile

## Quick Start

### Prerequisites

- Python 3.8+
- pip
- Google Gemini API key ([Get one here](https://makersuite.google.com/app/apikey))

### Local Development Setup

1. **Clone the repository**
   ```bash
   cd Client_App
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**

   Create a `.env` file:
   ```env
   SECRET_KEY=your-secret-key-here
   FLASK_ENV=development
   GEMINI_API_KEY=your-gemini-api-key-here
   DATABASE_URL=sqlite:///dump_analyzer.db
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Access the app**
   - Open browser to: `http://127.0.0.1:5000`
   - Register a new account
   - Start using the app!

## Deployment

See [DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md) for detailed deployment instructions.

**Quick Deploy to Render**:
1. Push code to Git
2. Connect to Render
3. Use Blueprint deployment (render.yaml)
4. Set environment variables
5. Deploy!

## Project Structure

```
Client_App/
├── app.py                  # Main Flask application
├── models.py              # Database models (User, Ticket, Conversation, etc.)
├── forms.py               # WTForms for user input
├── config.py              # Configuration settings
├── requirements.txt       # Python dependencies
├── render.yaml           # Render deployment config
├── .env                  # Environment variables (local)
├── .env.production       # Production environment template
│
├── templates/            # Jinja2 HTML templates
│   ├── auth/            # Login, registration
│   ├── dashboard/       # Main dashboard
│   ├── support/         # Ticket management
│   ├── chatbot/         # AI assistant
│   └── base.html        # Base template
│
├── static/              # Static assets
│   ├── css/
│   ├── js/
│   └── images/
│
├── utils/               # Utility modules
│   ├── dump_analyzer.py      # Windows dump analysis
│   ├── file_scanner.py       # File system scanner
│   ├── knowledge_base.py     # Solution storage
│   ├── gemini_assistant.py   # AI integration
│   └── email_notifier.py     # Email service
│
├── uploads/             # User uploads (gitignored)
├── logs/               # Application logs (gitignored)
└── migrations/         # Database migrations
```

## Technology Stack

### Backend
- **Flask 2.3.3**: Web framework
- **SQLAlchemy**: ORM for database
- **Flask-Login**: User session management
- **Flask-Migrate**: Database migrations
- **Flask-WTF**: Form handling and validation

### AI & Services
- **Google Gemini**: AI chatbot and analysis
- **Email**: SMTP notifications
- **Gunicorn**: Production WSGI server

### Database
- **SQLite**: Local development
- **PostgreSQL**: Production (Render)

### Frontend
- **Jinja2**: Templating
- **Bootstrap**: UI framework
- **JavaScript**: Interactive features

## Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `SECRET_KEY` | Flask secret key | Yes |
| `FLASK_ENV` | Environment (development/production) | Yes |
| `DATABASE_URL` | Database connection string | Yes |
| `GEMINI_API_KEY` | Google Gemini API key | Yes |
| `SUPPORT_API_URL` | Support Dashboard URL | No |
| `MAIL_USERNAME` | Email for notifications | No |
| `MAIL_PASSWORD` | Email password | No |

### Database Models

- **User**: User accounts and profiles
- **Ticket**: Support ticket records
- **TicketMessage**: Messages within tickets
- **Conversation**: Chatbot conversations
- **ConversationMessage**: Individual chat messages
- **DumpAnalysis**: Analysis results (if applicable)
- **KnowledgeBaseSolution**: Stored solutions
- **SolutionFeedback**: User feedback on solutions

## API Endpoints

### Authentication
- `GET/POST /register` - User registration
- `GET/POST /login` - User login
- `GET /logout` - User logout

### Dashboard
- `GET /` - Main dashboard
- `GET /profile` - User profile
- `POST /profile/update` - Update profile

### Support Tickets
- `GET /support` - Ticket list
- `POST /support/submit` - Create ticket
- `GET /support/ticket/<id>` - View ticket
- `POST /support/ticket/<id>/message` - Add message

### Chatbot
- `GET /chatbot` - Chat interface
- `POST /chatbot/send` - Send message
- `POST /chatbot/upload-image` - Upload image

### Export
- `GET /export/tickets` - Export tickets to CSV
- `GET /export/conversations` - Export chats to CSV

## Development

### Running Tests

```bash
# Install test dependencies
pip install pytest pytest-flask

# Run tests
pytest
```

### Database Migrations

```bash
# Create migration
flask db migrate -m "Description"

# Apply migration
flask db upgrade

# Rollback migration
flask db downgrade
```

### Adding New Features

1. Update models in `models.py`
2. Create migration: `flask db migrate`
3. Add routes in `app.py`
4. Create templates in `templates/`
5. Test locally
6. Deploy

## Limitations

### Windows-Specific Features

Some features only work on Windows:
- **WinDbg integration**: Requires Windows debugger tools
- **Minidump analysis**: Windows-specific file format
- **System paths**: C:\ drive paths

These features are gracefully disabled on non-Windows systems (like Render's Linux servers).

### File Storage

- **Local**: Uses `uploads/` folder
- **Production (Render Free)**: Ephemeral storage (files deleted on restart)
- **Production (Recommended)**: Use AWS S3 or Render Disks

## Troubleshooting

### Common Issues

**Issue**: Gemini AI not responding
- Check API key is set correctly
- Verify API quota at Google AI Studio
- Check logs for error messages

**Issue**: Database errors
- Ensure database migrations are applied
- Check DATABASE_URL is correct
- Verify database is accessible

**Issue**: Email not sending
- Use Gmail App Password, not regular password
- Enable 2FA on Gmail account
- Check SMTP settings

**Issue**: Uploads not persisting
- Expected on Render free tier (ephemeral storage)
- Solution: Use S3 or upgrade to Render Disk

## Security

### Best Practices

1. **Never commit secrets**
   - Use `.env` for local secrets
   - Use environment variables in production
   - `.gitignore` excludes sensitive files

2. **Use strong passwords**
   - Generate random SECRET_KEY
   - Use password hashing (implemented)
   - Enable CSRF protection (enabled)

3. **API Security**
   - Keep Gemini API key private
   - Rotate keys if exposed
   - Monitor API usage

4. **Production**
   - Use HTTPS (automatic on Render)
   - Set `FLASK_ENV=production`
   - Disable debug mode

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

MIT License - See LICENSE file for details

## Support

- **Deployment Issues**: See [DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md)
- **Application Issues**: Check logs at `logs/app.log`
- **Render Issues**: Check [Render Documentation](https://render.com/docs)

## Roadmap

- [ ] AWS S3 integration for persistent storage
- [ ] Real-time chat with WebSockets
- [ ] Mobile app (React Native)
- [ ] Advanced analytics dashboard
- [ ] Multi-language support
- [ ] Docker containerization
- [ ] Kubernetes deployment

---

**Version**: 1.0.0
**Last Updated**: January 2026
