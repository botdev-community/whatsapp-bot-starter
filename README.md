# WhatsApp Bot Starter 🚀

[![BotDev Community](https://img.shields.io/badge/Part%20of-BotDev%20Community-blue)](https://github.com/botdev-community)
[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-green.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> Production-ready WhatsApp bot template using FastAPI and WhatsApp Cloud API

A complete, production-ready starter template for building WhatsApp bots using the official WhatsApp Cloud API. Built with FastAPI, this template includes webhook handling, message processing, and deployment configurations.

## ✨ Features

- ✅ **WhatsApp Cloud API Integration** - Official Meta API support
- ✅ **FastAPI Backend** - Modern, fast, async web framework
- ✅ **Webhook Handling** - Automatic message processing
- ✅ **Text & Media Support** - Handle text, images, documents, and more
- ✅ **Template Messages** - Send WhatsApp template messages
- ✅ **Interactive Messages** - Buttons and lists support
- ✅ **MongoDB Integration** - Store conversations and user data
- ✅ **Environment Variables** - Secure configuration management
- ✅ **Docker Support** - Easy deployment with Docker
- ✅ **Production Ready** - Includes logging, error handling, and validation

## 📋 Prerequisites

- Python 3.9 or higher
- WhatsApp Business Account
- Meta Developer Account
- MongoDB (local or cloud)

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/botdev-community/whatsapp-bot-starter.git
cd whatsapp-bot-starter
```

### 2. Install Dependencies

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Setup WhatsApp Cloud API

1. **Create a Meta Developer Account:**
   - Go to [Meta for Developers](https://developers.facebook.com/)
   - Create an app and select "Business" type
   - Add WhatsApp product

2. **Get Your Credentials:**
   - Phone Number ID
   - WhatsApp Business Account ID
   - Access Token (Temporary or Permanent)
   - Webhook Verify Token (you create this)

3. **Setup Webhook:**
   - Set webhook URL: `https://your-domain.com/webhook`
   - Set verify token (same as in your `.env`)
   - Subscribe to `messages` field

### 4. Configure Environment Variables

Create a `.env` file in the root directory:

```env
# WhatsApp API Configuration
WHATSAPP_API_TOKEN=your_access_token_here
WHATSAPP_PHONE_NUMBER_ID=your_phone_number_id
WHATSAPP_BUSINESS_ACCOUNT_ID=your_business_account_id
WEBHOOK_VERIFY_TOKEN=your_custom_verify_token

# MongoDB Configuration
MONGODB_URL=mongodb://localhost:27017
MONGODB_DB_NAME=whatsapp_bot

# Application Configuration
APP_HOST=0.0.0.0
APP_PORT=8000
ENVIRONMENT=development
LOG_LEVEL=INFO
```

### 5. Run the Application

```bash
# Development mode
uvicorn app.main:app --reload

# Production mode
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

The server will start at `http://localhost:8000`

### 6. Test the Webhook

```bash
# Test webhook verification
curl "http://localhost:8000/webhook?hub.mode=subscribe&hub.verify_token=your_verify_token&hub.challenge=test123"

# Should return: test123
```

## 📁 Project Structure

```
whatsapp-bot-starter/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application entry point
│   ├── config.py               # Configuration management
│   ├── models/
│   │   ├── __init__.py
│   │   ├── message.py          # Message data models
│   │   └── user.py             # User data models
│   ├── services/
│   │   ├── __init__.py
│   │   ├── whatsapp.py         # WhatsApp API service
│   │   ├── message_handler.py  # Message processing logic
│   │   └── database.py         # Database operations
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── logger.py           # Logging configuration
│   │   └── validators.py       # Input validation
│   └── routers/
│       ├── __init__.py
│       └── webhook.py          # Webhook endpoints
├── tests/
│   ├── __init__.py
│   ├── test_webhook.py
│   └── test_message_handler.py
├── deployment/
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── railway.json
├── .env.example
├── .gitignore
├── requirements.txt
├── README.md
└── LICENSE
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `WHATSAPP_API_TOKEN` | WhatsApp API access token | Yes | - |
| `WHATSAPP_PHONE_NUMBER_ID` | Your phone number ID | Yes | - |
| `WHATSAPP_BUSINESS_ACCOUNT_ID` | Business account ID | Yes | - |
| `WEBHOOK_VERIFY_TOKEN` | Custom verify token | Yes | - |
| `MONGODB_URL` | MongoDB connection URL | No | `mongodb://localhost:27017` |
| `MONGODB_DB_NAME` | Database name | No | `whatsapp_bot` |
| `APP_HOST` | Application host | No | `0.0.0.0` |
| `APP_PORT` | Application port | No | `8000` |
| `ENVIRONMENT` | Environment (dev/prod) | No | `development` |
| `LOG_LEVEL` | Logging level | No | `INFO` |

## 📱 Usage Examples

### Sending Text Messages

```python
from app.services.whatsapp import WhatsAppService

whatsapp = WhatsAppService()

# Send a simple text message
await whatsapp.send_text_message(
    to="1234567890",
    message="Hello from WhatsApp Bot!"
)
```

### Sending Media Messages

```python
# Send an image
await whatsapp.send_image(
    to="1234567890",
    image_url="https://example.com/image.jpg",
    caption="Check out this image!"
)

# Send a document
await whatsapp.send_document(
    to="1234567890",
    document_url="https://example.com/doc.pdf",
    filename="document.pdf"
)
```

### Sending Interactive Messages

```python
# Send buttons
await whatsapp.send_buttons(
    to="1234567890",
    body_text="Choose an option:",
    buttons=[
        {"id": "1", "title": "Option 1"},
        {"id": "2", "title": "Option 2"},
        {"id": "3", "title": "Option 3"}
    ]
)

# Send list message
await whatsapp.send_list(
    to="1234567890",
    body_text="Select from the menu:",
    button_text="View Menu",
    sections=[
        {
            "title": "Section 1",
            "rows": [
                {"id": "1", "title": "Item 1", "description": "Description 1"},
                {"id": "2", "title": "Item 2", "description": "Description 2"}
            ]
        }
    ]
)
```

## 🐳 Docker Deployment

### Using Docker Compose

```bash
# Build and run
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

### Using Docker Only

```bash
# Build image
docker build -t whatsapp-bot .

# Run container
docker run -d \
  --name whatsapp-bot \
  -p 8000:8000 \
  --env-file .env \
  whatsapp-bot
```

## ☁️ Deployment Options

### Railway

1. Install Railway CLI:
```bash
npm install -g @railway/cli
```

2. Deploy:
```bash
railway login
railway init
railway up
```

3. Set environment variables in Railway dashboard

### Heroku

```bash
# Login to Heroku
heroku login

# Create app
heroku create your-app-name

# Set environment variables
heroku config:set WHATSAPP_API_TOKEN=your_token

# Deploy
git push heroku main
```

### Render

1. Create a new Web Service
2. Connect your GitHub repository
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Add environment variables in dashboard

### DigitalOcean App Platform

1. Create a new app
2. Select your repository
3. Configure:
   - Build Command: `pip install -r requirements.txt`
   - Run Command: `uvicorn app.main:app --host 0.0.0.0 --port 8080`
4. Add environment variables

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app tests/

# Run specific test
pytest tests/test_webhook.py
```

## 📚 Documentation

### API Endpoints

#### Webhook Verification (GET)
```
GET /webhook?hub.mode=subscribe&hub.verify_token=TOKEN&hub.challenge=CHALLENGE
```

#### Receive Messages (POST)
```
POST /webhook
Content-Type: application/json
```

#### Health Check
```
GET /health
```

### Message Types Supported

- ✅ Text messages
- ✅ Image messages
- ✅ Video messages
- ✅ Audio messages
- ✅ Document messages
- ✅ Location messages
- ✅ Interactive messages (buttons, lists)
- ✅ Template messages
- ✅ Reactions

## 🛠️ Customization

### Adding Custom Message Handlers

Edit `app/services/message_handler.py`:

```python
async def handle_message(self, message: dict):
    message_type = message.get("type")
    
    if message_type == "text":
        text = message.get("text", {}).get("body", "")
        
        # Add your custom logic here
        if text.lower() == "hello":
            await self.whatsapp.send_text_message(
                to=message.get("from"),
                message="Hi! How can I help you?"
            )
```

### Adding Database Models

Create models in `app/models/`:

```python
from pydantic import BaseModel
from datetime import datetime

class Conversation(BaseModel):
    user_id: str
    message: str
    timestamp: datetime
    direction: str  # "incoming" or "outgoing"
```

## 🔒 Security Best Practices

1. **Never commit `.env` files** - Always use `.env.example`
2. **Use environment variables** - Never hardcode credentials
3. **Validate webhook signatures** - Verify requests from WhatsApp
4. **Use HTTPS** - Always use SSL certificates in production
5. **Rate limiting** - Implement rate limiting to prevent abuse
6. **Input validation** - Sanitize all user inputs
7. **Rotate tokens** - Regularly rotate API tokens

## 🐛 Troubleshooting

### Webhook Not Receiving Messages

1. Check webhook URL is publicly accessible
2. Verify webhook token matches
3. Check subscribed webhook fields
4. Review application logs

### Messages Not Sending

1. Verify API token is valid
2. Check phone number ID is correct
3. Ensure recipient has opted in
4. Check API rate limits

### Database Connection Issues

1. Verify MongoDB is running
2. Check connection string
3. Ensure database user has permissions

## 📖 Resources

### Official Documentation
- [WhatsApp Cloud API Docs](https://developers.facebook.com/docs/whatsapp/cloud-api)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [MongoDB Documentation](https://docs.mongodb.com/)

### Tutorials
- [WhatsApp Cloud API Getting Started](https://developers.facebook.com/docs/whatsapp/cloud-api/get-started)
- [FastAPI Tutorial](https://fastapi.tiangolo.com/tutorial/)

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

Read our [Contributing Guidelines](CONTRIBUTING.md) for more details.

## 💬 Community

This project is maintained by [BotDev Community](https://github.com/botdev-community).

- 💬 [Discussions](https://github.com/botdev-community/community/discussions)
- 🐛 [Issues](https://github.com/botdev-community/whatsapp-bot-starter/issues)
- 🤝 [Join the Community](https://github.com/botdev-community/community/issues/new?template=join-request.yml)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- WhatsApp Cloud API by Meta
- FastAPI by Sebastián Ramírez
- BotDev Community contributors

---

<div align="center">

**Built with ❤️ by [BotDev Community](https://github.com/botdev-community)**

[⭐ Star this repo](https://github.com/botdev-community/whatsapp-bot-starter) • 
[🐛 Report Bug](https://github.com/botdev-community/whatsapp-bot-starter/issues) • 
[💡 Request Feature](https://github.com/botdev-community/whatsapp-bot-starter/issues)

</div>
