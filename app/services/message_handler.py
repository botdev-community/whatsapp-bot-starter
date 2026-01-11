"""
Message Handler Service
Processes incoming WhatsApp messages and implements bot logic
"""

from typing import Dict
from app.services.whatsapp import WhatsAppService
from app.services.database import Database
from app.utils.logger import logger


class MessageHandler:
    """Handles incoming WhatsApp messages and implements bot logic"""
    
    def __init__(self):
        self.whatsapp = WhatsAppService()
        self.db = Database()
    
    async def process_message(self, message: Dict, value: Dict):
        """
        Process an incoming message
        
        Args:
            message: Message object from webhook
            value: Value object containing metadata
        """
        try:
            message_type = message.get("type")
            from_number = message.get("from")
            message_id = message.get("id")
            timestamp = message.get("timestamp")
            
            logger.info(f"Processing {message_type} message from {from_number}")
            
            # Mark message as read
            await self.whatsapp.mark_as_read(message_id)
            
            # Save message to database
            await self.db.save_message({
                "message_id": message_id,
                "from": from_number,
                "type": message_type,
                "timestamp": timestamp,
                "data": message
            })
            
            # Route to appropriate handler based on message type
            if message_type == "text":
                await self.handle_text_message(message, from_number)
            elif message_type == "image":
                await self.handle_image_message(message, from_number)
            elif message_type == "document":
                await self.handle_document_message(message, from_number)
            elif message_type == "audio":
                await self.handle_audio_message(message, from_number)
            elif message_type == "video":
                await self.handle_video_message(message, from_number)
            elif message_type == "location":
                await self.handle_location_message(message, from_number)
            elif message_type == "interactive":
                await self.handle_interactive_message(message, from_number)
            else:
                logger.warning(f"Unsupported message type: {message_type}")
            
        except Exception as e:
            logger.error(f"Error processing message: {e}", exc_info=True)
    
    async def handle_text_message(self, message: Dict, from_number: str):
        """
        Handle text messages - Implement your bot logic here
        
        Args:
            message: Message object
            from_number: Sender's phone number
        """
        text = message.get("text", {}).get("body", "").strip()
        text_lower = text.lower()
        
        logger.info(f"Received text: {text}")
        
        # Example command handlers
        if text_lower in ["hello", "hi", "hey"]:
            await self.whatsapp.send_text_message(
                to=from_number,
                message="👋 Hello! Welcome to WhatsApp Bot Starter.\n\nType 'help' to see available commands."
            )
        
        elif text_lower == "help":
            help_message = """
🤖 *WhatsApp Bot Commands*

• hello - Greet the bot
• help - Show this help message
• menu - Show interactive menu
• buttons - Demo button message
• info - Get bot information

Type any command to get started!
            """
            await self.whatsapp.send_text_message(
                to=from_number,
                message=help_message
            )
        
        elif text_lower == "menu":
            await self.whatsapp.send_list(
                to=from_number,
                body_text="Select an option from the menu:",
                button_text="View Options",
                sections=[
                    {
                        "title": "Main Menu",
                        "rows": [
                            {
                                "id": "option_1",
                                "title": "Option 1",
                                "description": "Description for option 1"
                            },
                            {
                                "id": "option_2",
                                "title": "Option 2",
                                "description": "Description for option 2"
                            },
                            {
                                "id": "option_3",
                                "title": "Option 3",
                                "description": "Description for option 3"
                            }
                        ]
                    }
                ]
            )
        
        elif text_lower == "buttons":
            await self.whatsapp.send_buttons(
                to=from_number,
                body_text="Choose an action:",
                buttons=[
                    {"id": "btn_1", "title": "Button 1"},
                    {"id": "btn_2", "title": "Button 2"},
                    {"id": "btn_3", "title": "Button 3"}
                ],
                header_text="Demo Buttons",
                footer_text="Select one option"
            )
        
        elif text_lower == "info":
            info_message = """
ℹ️ *Bot Information*

Name: WhatsApp Bot Starter
Version: 1.0.0
Built by: BotDev Community

This is a production-ready template for building WhatsApp bots using FastAPI and WhatsApp Cloud API.

GitHub: github.com/botdev-community
            """
            await self.whatsapp.send_text_message(
                to=from_number,
                message=info_message
            )
        
        else:
            # Default response for unknown commands
            await self.whatsapp.send_text_message(
                to=from_number,
                message=f"I received your message: '{text}'\n\nType 'help' to see available commands."
            )
    
    async def handle_image_message(self, message: Dict, from_number: str):
        """Handle image messages"""
        image = message.get("image", {})
        caption = image.get("caption", "")
        
        logger.info(f"Received image with caption: {caption}")
        
        await self.whatsapp.send_text_message(
            to=from_number,
            message="📸 I received your image! Image processing is not implemented yet."
        )
    
    async def handle_document_message(self, message: Dict, from_number: str):
        """Handle document messages"""
        document = message.get("document", {})
        filename = document.get("filename", "unknown")
        
        logger.info(f"Received document: {filename}")
        
        await self.whatsapp.send_text_message(
            to=from_number,
            message=f"📄 I received your document: {filename}"
        )
    
    async def handle_audio_message(self, message: Dict, from_number: str):
        """Handle audio messages"""
        logger.info("Received audio message")
        
        await self.whatsapp.send_text_message(
            to=from_number,
            message="🎵 I received your audio message!"
        )
    
    async def handle_video_message(self, message: Dict, from_number: str):
        """Handle video messages"""
        logger.info("Received video message")
        
        await self.whatsapp.send_text_message(
            to=from_number,
            message="🎥 I received your video!"
        )
    
    async def handle_location_message(self, message: Dict, from_number: str):
        """Handle location messages"""
        location = message.get("location", {})
        latitude = location.get("latitude")
        longitude = location.get("longitude")
        
        logger.info(f"Received location: {latitude}, {longitude}")
        
        await self.whatsapp.send_text_message(
            to=from_number,
            message=f"📍 I received your location:\nLat: {latitude}\nLon: {longitude}"
        )
    
    async def handle_interactive_message(self, message: Dict, from_number: str):
        """Handle interactive message responses (buttons, lists)"""
        interactive = message.get("interactive", {})
        interactive_type = interactive.get("type")
        
        if interactive_type == "button_reply":
            button_reply = interactive.get("button_reply", {})
            button_id = button_reply.get("id")
            button_title = button_reply.get("title")
            
            logger.info(f"Button clicked: {button_id} - {button_title}")
            
            await self.whatsapp.send_text_message(
                to=from_number,
                message=f"You clicked: {button_title}"
            )
        
        elif interactive_type == "list_reply":
            list_reply = interactive.get("list_reply", {})
            list_id = list_reply.get("id")
            list_title = list_reply.get("title")
            
            logger.info(f"List item selected: {list_id} - {list_title}")
            
            await self.whatsapp.send_text_message(
                to=from_number,
                message=f"You selected: {list_title}"
            )
    
    async def process_status(self, status: Dict):
        """
        Process message status updates
        
        Args:
            status: Status object from webhook
        """
        try:
            message_id = status.get("id")
            status_type = status.get("status")
            timestamp = status.get("timestamp")
            
            logger.info(f"Message {message_id} status: {status_type}")
            
            # Update message status in database
            await self.db.update_message_status(message_id, status_type, timestamp)
            
        except Exception as e:
            logger.error(f"Error processing status: {e}", exc_info=True)
