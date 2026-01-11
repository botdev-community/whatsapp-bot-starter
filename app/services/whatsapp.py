"""
WhatsApp Service
Handles all WhatsApp API interactions for sending messages
"""

import aiohttp
from typing import List, Dict, Optional
from app.config import settings, get_whatsapp_api_url
from app.utils.logger import logger


class WhatsAppService:
    """Service for interacting with WhatsApp Cloud API"""
    
    def __init__(self):
        self.api_url = get_whatsapp_api_url()
        self.headers = {
            "Authorization": f"Bearer {settings.WHATSAPP_API_TOKEN}",
            "Content-Type": "application/json"
        }
    
    async def send_text_message(self, to: str, message: str, preview_url: bool = False) -> dict:
        """
        Send a text message
        
        Args:
            to: Recipient phone number (with country code, without +)
            message: Text message content
            preview_url: Enable URL preview
            
        Returns:
            dict: API response
        """
        url = f"{self.api_url}/messages"
        
        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": to,
            "type": "text",
            "text": {
                "preview_url": preview_url,
                "body": message
            }
        }
        
        return await self._send_request(url, payload)
    
    async def send_image(
        self, 
        to: str, 
        image_url: Optional[str] = None,
        image_id: Optional[str] = None,
        caption: Optional[str] = None
    ) -> dict:
        """
        Send an image message
        
        Args:
            to: Recipient phone number
            image_url: URL of the image (or use image_id)
            image_id: Media ID from WhatsApp (or use image_url)
            caption: Optional image caption
            
        Returns:
            dict: API response
        """
        url = f"{self.api_url}/messages"
        
        image_data = {}
        if image_url:
            image_data["link"] = image_url
        elif image_id:
            image_data["id"] = image_id
        else:
            raise ValueError("Either image_url or image_id must be provided")
        
        if caption:
            image_data["caption"] = caption
        
        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": to,
            "type": "image",
            "image": image_data
        }
        
        return await self._send_request(url, payload)
    
    async def send_document(
        self,
        to: str,
        document_url: Optional[str] = None,
        document_id: Optional[str] = None,
        filename: Optional[str] = None,
        caption: Optional[str] = None
    ) -> dict:
        """
        Send a document message
        
        Args:
            to: Recipient phone number
            document_url: URL of the document
            document_id: Media ID from WhatsApp
            filename: Document filename
            caption: Optional caption
            
        Returns:
            dict: API response
        """
        url = f"{self.api_url}/messages"
        
        document_data = {}
        if document_url:
            document_data["link"] = document_url
        elif document_id:
            document_data["id"] = document_id
        else:
            raise ValueError("Either document_url or document_id must be provided")
        
        if filename:
            document_data["filename"] = filename
        if caption:
            document_data["caption"] = caption
        
        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": to,
            "type": "document",
            "document": document_data
        }
        
        return await self._send_request(url, payload)
    
    async def send_buttons(
        self,
        to: str,
        body_text: str,
        buttons: List[Dict[str, str]],
        header_text: Optional[str] = None,
        footer_text: Optional[str] = None
    ) -> dict:
        """
        Send interactive button message
        
        Args:
            to: Recipient phone number
            body_text: Main message text
            buttons: List of buttons (max 3)
                     Each button: {"id": "unique_id", "title": "Button Text"}
            header_text: Optional header
            footer_text: Optional footer
            
        Returns:
            dict: API response
        """
        if len(buttons) > 3:
            raise ValueError("Maximum 3 buttons allowed")
        
        url = f"{self.api_url}/messages"
        
        interactive_data = {
            "type": "button",
            "body": {"text": body_text},
            "action": {
                "buttons": [
                    {
                        "type": "reply",
                        "reply": {
                            "id": btn["id"],
                            "title": btn["title"]
                        }
                    }
                    for btn in buttons
                ]
            }
        }
        
        if header_text:
            interactive_data["header"] = {"type": "text", "text": header_text}
        if footer_text:
            interactive_data["footer"] = {"text": footer_text}
        
        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": to,
            "type": "interactive",
            "interactive": interactive_data
        }
        
        return await self._send_request(url, payload)
    
    async def send_list(
        self,
        to: str,
        body_text: str,
        button_text: str,
        sections: List[Dict],
        header_text: Optional[str] = None,
        footer_text: Optional[str] = None
    ) -> dict:
        """
        Send interactive list message
        
        Args:
            to: Recipient phone number
            body_text: Main message text
            button_text: Text for the list button
            sections: List of sections with rows
                     [{"title": "Section", "rows": [{"id": "1", "title": "Item", "description": "Desc"}]}]
            header_text: Optional header
            footer_text: Optional footer
            
        Returns:
            dict: API response
        """
        url = f"{self.api_url}/messages"
        
        interactive_data = {
            "type": "list",
            "body": {"text": body_text},
            "action": {
                "button": button_text,
                "sections": sections
            }
        }
        
        if header_text:
            interactive_data["header"] = {"type": "text", "text": header_text}
        if footer_text:
            interactive_data["footer"] = {"text": footer_text}
        
        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": to,
            "type": "interactive",
            "interactive": interactive_data
        }
        
        return await self._send_request(url, payload)
    
    async def send_template(
        self,
        to: str,
        template_name: str,
        language_code: str = "en_US",
        components: Optional[List[Dict]] = None
    ) -> dict:
        """
        Send a template message
        
        Args:
            to: Recipient phone number
            template_name: Name of the approved template
            language_code: Template language
            components: Template components (parameters, etc.)
            
        Returns:
            dict: API response
        """
        url = f"{self.api_url}/messages"
        
        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": to,
            "type": "template",
            "template": {
                "name": template_name,
                "language": {"code": language_code}
            }
        }
        
        if components:
            payload["template"]["components"] = components
        
        return await self._send_request(url, payload)
    
    async def mark_as_read(self, message_id: str) -> dict:
        """
        Mark a message as read
        
        Args:
            message_id: WhatsApp message ID
            
        Returns:
            dict: API response
        """
        url = f"{self.api_url}/messages"
        
        payload = {
            "messaging_product": "whatsapp",
            "status": "read",
            "message_id": message_id
        }
        
        return await self._send_request(url, payload)
    
    async def _send_request(self, url: str, payload: dict) -> dict:
        """
        Send HTTP request to WhatsApp API
        
        Args:
            url: API endpoint URL
            payload: Request payload
            
        Returns:
            dict: API response
        """
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=payload, headers=self.headers) as response:
                    response_data = await response.json()
                    
                    if response.status != 200:
                        logger.error(f"WhatsApp API error: {response_data}")
                        raise Exception(f"API error: {response_data}")
                    
                    logger.info(f"Message sent successfully: {response_data}")
                    return response_data
                    
        except Exception as e:
            logger.error(f"Error sending WhatsApp message: {e}", exc_info=True)
            raise
