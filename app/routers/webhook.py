"""
Webhook Router
Handles WhatsApp webhook verification and incoming messages
"""

from fastapi import APIRouter, Request, HTTPException, Query
from fastapi.responses import PlainTextResponse, JSONResponse
import hmac
import hashlib

from app.config import settings
from app.services.message_handler import MessageHandler
from app.utils.logger import logger

router = APIRouter()
message_handler = MessageHandler()


@router.get("")
async def verify_webhook(
    hub_mode: str = Query(alias="hub.mode"),
    hub_verify_token: str = Query(alias="hub.verify_token"),
    hub_challenge: str = Query(alias="hub.challenge")
):
    """
    Webhook verification endpoint
    WhatsApp sends a GET request to verify the webhook
    """
    logger.info(f"Webhook verification request received: mode={hub_mode}")
    
    # Verify the mode is 'subscribe'
    if hub_mode != "subscribe":
        logger.warning(f"Invalid hub.mode: {hub_mode}")
        raise HTTPException(status_code=400, detail="Invalid hub.mode")
    
    # Verify the token matches
    if hub_verify_token != settings.WEBHOOK_VERIFY_TOKEN:
        logger.warning("Webhook verification failed: Invalid token")
        raise HTTPException(status_code=403, detail="Invalid verify token")
    
    # Return the challenge to complete verification
    logger.info("Webhook verified successfully")
    return PlainTextResponse(content=hub_challenge, status_code=200)


@router.post("")
async def receive_message(request: Request):
    """
    Receive and process incoming WhatsApp messages
    """
    try:
        # Get request body
        body = await request.json()
        logger.info(f"Received webhook: {body}")
        
        # Verify webhook signature (optional but recommended for production)
        # signature = request.headers.get("X-Hub-Signature-256")
        # if not verify_signature(await request.body(), signature):
        #     raise HTTPException(status_code=403, detail="Invalid signature")
        
        # Extract messages from webhook payload
        if "entry" not in body:
            logger.warning("No entry in webhook body")
            return JSONResponse(content={"status": "ok"}, status_code=200)
        
        for entry in body.get("entry", []):
            for change in entry.get("changes", []):
                value = change.get("value", {})
                
                # Process messages
                if "messages" in value:
                    for message in value.get("messages", []):
                        await message_handler.process_message(message, value)
                
                # Process message status updates
                if "statuses" in value:
                    for status in value.get("statuses", []):
                        await message_handler.process_status(status)
        
        return JSONResponse(content={"status": "ok"}, status_code=200)
        
    except Exception as e:
        logger.error(f"Error processing webhook: {e}", exc_info=True)
        # Return 200 even on error to prevent WhatsApp from retrying
        return JSONResponse(content={"status": "error"}, status_code=200)


def verify_signature(payload: bytes, signature: str) -> bool:
    """
    Verify webhook signature from WhatsApp
    
    Args:
        payload: Request body as bytes
        signature: X-Hub-Signature-256 header value
        
    Returns:
        bool: True if signature is valid
    """
    if not signature:
        return False
    
    try:
        # Extract the signature hash
        hash_type, hash_value = signature.split("=")
        if hash_type != "sha256":
            return False
        
        # Calculate expected signature
        expected_signature = hmac.new(
            settings.WHATSAPP_API_TOKEN.encode(),
            payload,
            hashlib.sha256
        ).hexdigest()
        
        # Compare signatures
        return hmac.compare_digest(expected_signature, hash_value)
        
    except Exception as e:
        logger.error(f"Error verifying signature: {e}")
        return False
