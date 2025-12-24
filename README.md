# TechElevate - Career Development Platform

A comprehensive platform for job seekers to enhance their technical skills, prepare for interviews, and optimize their resumes.

## Features

- 🎯 **ATS Resume Ranker** - AI-powered resume analysis
- 📝 **Resume Builder** - Create professional resumes
- 💼 **Mock Interviews** - Practice with AI-driven interviews
- 🧠 **Skill Assessment** - Aptitude and technical tests
- 📊 **Career Roadmaps** - Personalized learning paths
- 👥 **Soft Skills Training** - Communication and interpersonal skills
- 💎 **Subscription Tiers** - Free, Basic, Pro, and Premium plans

## Prerequisites

- Python 3.8 or higher
- MongoDB (local or cloud instance)
- pip (Python package manager)

## Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd TechElevate
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Download spaCy language model**
   ```bash
   python -m spacy download en_core_web_sm
   ```

5. **Set up environment variables**
   ```bash
   # Copy the example file
   cp .env.example .env
   
   # Edit .env and update the values
   ```

6. **Configure MongoDB**
   - Install MongoDB locally or use MongoDB Atlas
   - Update `MONGO_URI` in your `.env` file
   - Default: `mongodb://localhost:27017/techelevate`

7. **Run the application**
   ```bash
   # Development
   python app.py
   
   # Production (using gunicorn)
   gunicorn app:app
   ```

8. **Access the application**
   Open your browser and navigate to `http://localhost:5000`

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `FLASK_ENV` | Environment mode | `development` |
| `SECRET_KEY` | Session encryption key | `dev-secret-key-here-change-this` |
| `MONGO_URI` | MongoDB connection string | `mongodb://localhost:27017/techelevate` |
| `PORT` | Server port | `5000` |
| `SESSION_COOKIE_SECURE` | Enable secure cookies (HTTPS only) | `false` |

## Project Structure

```
TechElevate/
├── app.py                 # Main Flask application
├── ai_ranker.py          # Resume ranking AI module
├── requirements.txt      # Python dependencies
├── Procfile             # Deployment configuration
├── runtime.txt          # Python version specification
├── .env.example         # Environment variables template
├── static/              # CSS, JS, images
├── templates/           # HTML templates
│   ├── home.html
│   ├── dashboard.html
│   ├── profile.html
│   ├── resume_builder.html
│   ├── aptitude/       # Aptitude test pages
│   ├── technical/      # Technical test pages
│   └── softskills/     # Soft skills training
└── uploads/            # User-uploaded files

```

## Features in Detail

### Authentication
- User registration and login
- Session-based authentication
- Password hashing with Werkzeug

### Subscription System
- **Free**: 3 resumes, 5 job matches, 3 cover letters
- **Basic**: 10 resumes, 25 job matches, 15 cover letters
- **Pro**: 50 resumes, 100 job matches, 75 cover letters
- **Premium**: Unlimited access

### ATS Resume Ranker
- PDF and image resume parsing
- AI-powered keyword extraction
- Semantic similarity analysis
- Skills matching and recommendations

### Resume Builder
- Interactive resume creation
- Multiple templates
- LinkedIn profile import
- AI-powered suggestions

### Assessment Tests
- Quantitative aptitude
- Logical reasoning
- Data interpretation
- Technical skills (Python, Java, C++, Web Development)
- Soft skills evaluation

## Security Features

- ✅ Password hashing
- ✅ Session management
- ✅ CORS protection
- ✅ Input validation
- ✅ File upload restrictions (16MB limit)
- ✅ Secure cookie configuration
- ✅ Environment variable protection

## Deployment

### Heroku
```bash
heroku create your-app-name
git push heroku main
heroku config:set SECRET_KEY=your-secret-key
heroku config:set MONGO_URI=your-mongodb-uri
```

### Render
1. Connect your GitHub repository
2. Set environment variables in dashboard
3. Deploy automatically from main branch

## Development

### Running Tests
```bash
# Add your test command here
pytest
```

### Code Style
```bash
# Format code
black .

# Lint
flake8 .
```

## Troubleshooting

### MongoDB Connection Issues
- Ensure MongoDB is running: `mongod` (Windows) or `sudo service mongod start` (Linux)
- Check connection string in `.env`
- For MongoDB Atlas, whitelist your IP address

### Module Import Errors
```bash
# Reinstall dependencies
pip install -r requirements.txt --upgrade

# Download spaCy model
python -m spacy download en_core_web_sm
```

### Port Already in Use
```bash
# Change PORT in .env file or use:
python app.py --port 8000
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License.

## Support

For issues and questions:
- Create an issue on GitHub
- Contact: support@techelevate.com

## Acknowledgments

- Flask framework
- MongoDB database
- spaCy NLP library
- Sentence Transformers
- PyMongo
