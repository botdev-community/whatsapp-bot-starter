"""
Database Service
Handles MongoDB operations for storing messages and user data
"""

from motor.motor_asyncio import AsyncIOMotorClient
from typing import Dict, Optional, List
from datetime import datetime

from app.config import settings
from app.utils.logger import logger


class Database:
    """MongoDB database service"""
    
    _client: Optional[AsyncIOMotorClient] = None
    _db = None
    
    def __init__(self):
        """Initialize database connection"""
        if Database._client is None:
            Database._client = AsyncIOMotorClient(settings.MONGODB_URL)
            Database._db = Database._client[settings.MONGODB_DB_NAME]
            logger.info(f"Database client initialized: {settings.MONGODB_DB_NAME}")
    
    async def connect(self):
        """Establish database connection"""
        try:
            # Verify connection
            await Database._client.admin.command('ping')
            logger.info("Database connection established")
        except Exception as e:
            logger.error(f"Database connection failed: {e}")
            raise
    
    async def close(self):
        """Close database connection"""
        if Database._client:
            Database._client.close()
            logger.info("Database connection closed")
    
    async def ping(self) -> bool:
        """Check database connection"""
        try:
            await Database._client.admin.command('ping')
            return True
        except Exception:
            return False
    
    # Messages Collection Operations
    
    async def save_message(self, message_data: Dict) -> str:
        """
        Save a message to the database
        
        Args:
            message_data: Message data to save
            
        Returns:
            str: Inserted document ID
        """
        try:
            collection = Database._db.messages
            message_data["created_at"] = datetime.utcnow()
            message_data["updated_at"] = datetime.utcnow()
            
            result = await collection.insert_one(message_data)
            logger.info(f"Message saved: {result.inserted_id}")
            return str(result.inserted_id)
            
        except Exception as e:
            logger.error(f"Error saving message: {e}")
            raise
    
    async def get_message(self, message_id: str) -> Optional[Dict]:
        """
        Retrieve a message by message_id
        
        Args:
            message_id: WhatsApp message ID
            
        Returns:
            dict: Message data or None
        """
        try:
            collection = Database._db.messages
            message = await collection.find_one({"message_id": message_id})
            return message
            
        except Exception as e:
            logger.error(f"Error retrieving message: {e}")
            return None
    
    async def update_message_status(
        self, 
        message_id: str, 
        status: str, 
        timestamp: str
    ) -> bool:
        """
        Update message status
        
        Args:
            message_id: WhatsApp message ID
            status: New status (sent, delivered, read, failed)
            timestamp: Status timestamp
            
        Returns:
            bool: True if updated successfully
        """
        try:
            collection = Database._db.messages
            result = await collection.update_one(
                {"message_id": message_id},
                {
                    "$set": {
                        "status": status,
                        "status_timestamp": timestamp,
                        "updated_at": datetime.utcnow()
                    }
                }
            )
            
            if result.modified_count > 0:
                logger.info(f"Message {message_id} status updated to {status}")
                return True
            return False
            
        except Exception as e:
            logger.error(f"Error updating message status: {e}")
            return False
    
    async def get_user_messages(
        self, 
        phone_number: str, 
        limit: int = 50
    ) -> List[Dict]:
        """
        Get messages for a specific user
        
        Args:
            phone_number: User's phone number
            limit: Maximum number of messages to retrieve
            
        Returns:
            list: List of messages
        """
        try:
            collection = Database._db.messages
            cursor = collection.find(
                {"from": phone_number}
            ).sort("created_at", -1).limit(limit)
            
            messages = await cursor.to_list(length=limit)
            return messages
            
        except Exception as e:
            logger.error(f"Error retrieving user messages: {e}")
            return []
    
    # Users Collection Operations
    
    async def save_user(self, user_data: Dict) -> str:
        """
        Save or update user data
        
        Args:
            user_data: User data to save
            
        Returns:
            str: User document ID
        """
        try:
            collection = Database._db.users
            phone_number = user_data.get("phone_number")
            
            # Check if user exists
            existing_user = await collection.find_one({"phone_number": phone_number})
            
            if existing_user:
                # Update existing user
                user_data["updated_at"] = datetime.utcnow()
                await collection.update_one(
                    {"phone_number": phone_number},
                    {"$set": user_data}
                )
                logger.info(f"User updated: {phone_number}")
                return str(existing_user["_id"])
            else:
                # Insert new user
                user_data["created_at"] = datetime.utcnow()
                user_data["updated_at"] = datetime.utcnow()
                result = await collection.insert_one(user_data)
                logger.info(f"User created: {phone_number}")
                return str(result.inserted_id)
                
        except Exception as e:
            logger.error(f"Error saving user: {e}")
            raise
    
    async def get_user(self, phone_number: str) -> Optional[Dict]:
        """
        Get user by phone number
        
        Args:
            phone_number: User's phone number
            
        Returns:
            dict: User data or None
        """
        try:
            collection = Database._db.users
            user = await collection.find_one({"phone_number": phone_number})
            return user
            
        except Exception as e:
            logger.error(f"Error retrieving user: {e}")
            return None
    
    async def update_user_session(
        self,
        phone_number: str,
        session_data: Dict
    ) -> bool:
        """
        Update user session data
        
        Args:
            phone_number: User's phone number
            session_data: Session data to update
            
        Returns:
            bool: True if updated successfully
        """
        try:
            collection = Database._db.users
            result = await collection.update_one(
                {"phone_number": phone_number},
                {
                    "$set": {
                        "session": session_data,
                        "last_active": datetime.utcnow(),
                        "updated_at": datetime.utcnow()
                    }
                }
            )
            
            return result.modified_count > 0
            
        except Exception as e:
            logger.error(f"Error updating user session: {e}")
            return False
    
    # Analytics Operations
    
    async def get_message_stats(self) -> Dict:
        """
        Get message statistics
        
        Returns:
            dict: Message statistics
        """
        try:
            collection = Database._db.messages
            
            total_messages = await collection.count_documents({})
            text_messages = await collection.count_documents({"type": "text"})
            image_messages = await collection.count_documents({"type": "image"})
            
            return {
                "total_messages": total_messages,
                "text_messages": text_messages,
                "image_messages": image_messages
            }
            
        except Exception as e:
            logger.error(f"Error getting message stats: {e}")
            return {}
