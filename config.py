import os

# ==========================================
# Flask Configuration
# ==========================================

SECRET_KEY = "xxxxxxx"

# ==========================================
# Upload Configuration
# ==========================================

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")

ALLOWED_EXTENSIONS = {"pdf"}

MAX_CONTENT_LENGTH = 16 * 1024 * 1024   # 16 MB

# Create uploads folder automatically
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ==========================================
# Groq API Configuration
# ==========================================

GROQ_API_KEY = "API_KEY"

# Recommended Model
GROQ_MODEL = "llama-3.3-70b-versatile"

# Optional AI Settings
AI_TEMPERATURE = 0.3
AI_MAX_TOKENS = 4096

# ==========================================
# PDF Configuration
# ==========================================

REPORT_FOLDER = os.path.join(BASE_DIR, "reports")

os.makedirs(REPORT_FOLDER, exist_ok=True)