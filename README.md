# AirBot - Airline Chatbot Assistant

An intelligent airline chatbot application that helps users with flight bookings, cancellations, seat availability, and airline policy queries using RAG (Retrieval-Augmented Generation) technology.

## 📋 Project Overview

AirBot is a full-stack web application consisting of:
- **Backend**: Django REST API with LangChain/LangGraph integration for conversational AI
- **Frontend**: Vanilla JavaScript SPA with authentication and chat interface
- **AI Features**: RAG-based policy querying using ChromaDB and Groq LLM
- **Database**: MongoDB for flight/ticket data, SQLite for Django auth

## ✨ Features

- **User Authentication**: Sign up and sign in functionality
- **Conversational AI**: Natural language interaction for airline queries
- **Flight Management**: 
  - Search seat availability by PNR, Flight ID, route, or airline
  - Cancel trips
  - View booking details
- **Policy Queries**: Ask questions about airline policies (baggage, cancellation, etc.)
- **Real-time Chat Interface**: Interactive messaging with the AI assistant

## 🛠️ Tech Stack

### Backend
- **Framework**: Django 5.2.7 with Django REST Framework
- **AI/ML**: 
  - LangChain & LangGraph for conversational workflows
  - Groq API for LLM inference
  - ChromaDB for vector storage
  - Sentence Transformers for embeddings
- **Databases**: 
  - MongoDB (flight/ticket data)
  - SQLite (user authentication)
- **Web Scraping**: Selenium, BeautifulSoup4

### Frontend
- **Pure JavaScript** (ES6+)
- **HTML5/CSS3**
- **Fetch API** for backend communication

## 📁 Project Structure

```
Airline-Chatbot/
├── Backend/
│   ├── airbot/              # Django project settings
│   ├── core/                # Main application
│   │   ├── auth.py          # Authentication logic
│   │   ├── views_chat.py    # Chat API endpoints
│   │   ├── models.py        # Database models
│   │   ├── mongo.py         # MongoDB integration
│   │   └── rag/             # RAG agent implementation
│   ├── chroma_store/        # Vector database storage
│   ├── manage.py            # Django management script
│   └── requirements.txt     # Python dependencies
├── Frontend/
│   ├── index.html           # Login/signup page
│   ├── chat.html            # Chat interface
│   ├── app.js               # Authentication logic
│   └── style.css            # Styling
└── .env                     # Environment variables
```

## 🚀 Installation & Setup

### Prerequisites

- **Python 3.8+**
- **MongoDB** (local or cloud instance)
- **Groq API Key** (for LLM access)

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd Airline-Chatbot
```

### Step 2: Configure Environment Variables

Edit the `.env` file in the root directory with your credentials:

```env
# API Keys
GROQ_API_KEY=your_groq_api_key_here
PINECONE_API_KEY=your_pinecone_key_here  # Optional
PINECONE_INDEX_NAME=medicobot
PINECONE_ENV=us-east-1

# Django Settings
DEBUG=1
DJANGO_SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=127.0.0.1,localhost

# Database
MONGO_URL=mongodb://localhost:27017
MONGO_DB=airbot

# Storage
CHROMA_DB_DIR=./chroma_store
UPLOAD_DIR=./uploaded_dir
```

### Step 3: Backend Setup

1. **Navigate to Backend directory**:
   ```bash
   cd Backend
   ```

2. **Create and activate virtual environment**:
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run Django migrations**:
   ```bash
   python manage.py migrate
   ```

5. **Start the Django development server**:
   ```bash
   python manage.py runserver
   ```

   The backend will be available at `http://127.0.0.1:8000`

### Step 4: Frontend Setup

1. **Navigate to Frontend directory** (in a new terminal):
   ```bash
   cd Frontend
   ```

2. **Serve the frontend** using any static file server:

   **Option A - Using Python's built-in server**:
   ```bash
   python -m http.server 8080
   ```

   **Option B - Using Node.js http-server** (if installed):
   ```bash
   npx http-server -p 8080
   ```

   **Option C - Using VS Code Live Server extension**:
   - Right-click on `index.html` and select "Open with Live Server"

3. **Access the application**:
   - Open your browser and navigate to `http://localhost:8080` (or the port shown by your server)

### Step 5: MongoDB Setup

Ensure MongoDB is running:

**Local MongoDB**:
```bash
mongod
```

**Or use MongoDB Atlas** (cloud):
- Update `MONGO_URL` in `.env` with your Atlas connection string

## 🎯 Usage

### 1. Authentication
- Open the application in your browser
- **Sign Up**: Create a new account with username and password
- **Sign In**: Log in with your credentials

### 2. Chat Interface
Once logged in, you can interact with AirBot:

**Example Queries**:
- "Show me seat availability"
- "Cancel my trip with PNR ABC123"
- "What is the baggage allowance policy?"
- "Tell me about cancellation charges"

### 3. Seat Availability Flow
When you request seat availability, the bot will guide you through:
1. PNR (optional)
2. Flight ID (optional)
3. Source airport (optional)
4. Destination airport (optional)
5. Airline name (optional)

You can skip any field by typing "skip" or provide at least one parameter.

## 🔌 API Endpoints

### Authentication
- `POST /auth/signup/` - Create new user account
- `POST /auth/login/` - User login

### Chat Operations
- `POST /ask-policy/` - Query airline policies using RAG
- `POST /chat/` - General chat interactions
- `GET /seat-availability/` - Search available seats
- `POST /cancel-trip/` - Cancel a booking

## 🧪 Testing

To test the application:

1. **Backend API tests**:
   ```bash
   cd Backend
   python manage.py test
   ```

2. **Manual testing**:
   - Create a test user account
   - Try various chat queries
   - Test seat availability search
   - Test policy questions

## 🔒 Security Notes

- **Never commit** the `.env` file with real API keys to version control
- Change the `DJANGO_SECRET_KEY` in production
- Set `DEBUG=0` in production environments
- Use HTTPS in production
- Implement rate limiting for API endpoints

## 🐛 Troubleshooting

### Backend won't start
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Check if MongoDB is running
- Verify `.env` file exists and has correct values

### Frontend can't connect to backend
- Ensure backend is running on `http://127.0.0.1:8000`
- Check CORS settings in `Backend/airbot/settings.py`
- Verify `API_BASE` in frontend JavaScript files

### MongoDB connection errors
- Check if MongoDB service is running
- Verify `MONGO_URL` in `.env` file
- For Atlas, ensure IP whitelist is configured

### Groq API errors
- Verify your `GROQ_API_KEY` is valid
- Check API rate limits
- Ensure you have credits/quota available

## 📝 Development Notes

- The backend uses Django's development server (not for production)
- Frontend uses vanilla JavaScript (no build process required)
- ChromaDB stores vector embeddings locally in `chroma_store/`
- User sessions are stored in localStorage

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

[Add your license information here]

## 👥 Authors

[Add author information here]

## 🙏 Acknowledgments

- LangChain for conversational AI framework
- Groq for LLM API
- ChromaDB for vector storage
- Django community

---

**Note**: This is a development setup. For production deployment, consider:
- Using a production WSGI server (Gunicorn, uWSGI)
- Setting up proper environment variables
- Implementing proper logging and monitoring
- Using a production-grade database setup
- Adding SSL/TLS certificates
- Implementing proper error handling and validation
