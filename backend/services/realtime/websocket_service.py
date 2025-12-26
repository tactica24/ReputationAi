"""
Real-time WebSocket Service for Live Updates
Provides instant notifications and dashboard updates
"""

from fastapi import WebSocket, WebSocketDisconnect
from typing import Dict, Set, Any, List
import json
import asyncio
from datetime import datetime
from enum import Enum


class EventType(Enum):
    """WebSocket event types"""
    NEW_MENTION = "new_mention"
    ALERT_CREATED = "alert_created"
    REPUTATION_UPDATE = "reputation_update"
    SENTIMENT_CHANGE = "sentiment_change"
    TREND_DETECTED = "trend_detected"
    SYSTEM_NOTIFICATION = "system_notification"
    HEARTBEAT = "heartbeat"


class ConnectionManager:
    """Manage WebSocket connections for real-time updates"""
    
    def __init__(self):
        # Store active connections by user_id
        self.active_connections: Dict[int, Set[WebSocket]] = {}
        
        # Store connections by entity_id for targeted updates
        self.entity_subscriptions: Dict[int, Set[WebSocket]] = {}
        
        # Connection metadata
        self.connection_metadata: Dict[WebSocket, Dict[str, Any]] = {}
    
    async def connect(
        self, 
        websocket: WebSocket, 
        user_id: int,
        entity_ids: List[int] = None
    ):
        """
        Accept new WebSocket connection
        
        Args:
            websocket: WebSocket connection
            user_id: User ID
            entity_ids: List of entity IDs to subscribe to
        """
        await websocket.accept()
        
        # Add to user connections
        if user_id not in self.active_connections:
            self.active_connections[user_id] = set()
        self.active_connections[user_id].add(websocket)
        
        # Subscribe to entities
        if entity_ids:
            for entity_id in entity_ids:
                if entity_id not in self.entity_subscriptions:
                    self.entity_subscriptions[entity_id] = set()
                self.entity_subscriptions[entity_id].add(websocket)
        
        # Store metadata
        self.connection_metadata[websocket] = {
            "user_id": user_id,
            "entity_ids": entity_ids or [],
            "connected_at": datetime.utcnow(),
            "last_heartbeat": datetime.utcnow()
        }
        
        # Send welcome message
        await self.send_personal_message({
            "type": "connection_established",
            "user_id": user_id,
            "timestamp": datetime.utcnow().isoformat()
        }, websocket)
    
    def disconnect(self, websocket: WebSocket):
        """Remove WebSocket connection"""
        # Get metadata
        metadata = self.connection_metadata.get(websocket)
        if not metadata:
            return
        
        user_id = metadata["user_id"]
        entity_ids = metadata["entity_ids"]
        
        # Remove from user connections
        if user_id in self.active_connections:
            self.active_connections[user_id].discard(websocket)
            if not self.active_connections[user_id]:
                del self.active_connections[user_id]
        
        # Remove from entity subscriptions
        for entity_id in entity_ids:
            if entity_id in self.entity_subscriptions:
                self.entity_subscriptions[entity_id].discard(websocket)
                if not self.entity_subscriptions[entity_id]:
                    del self.entity_subscriptions[entity_id]
        
        # Remove metadata
        if websocket in self.connection_metadata:
            del self.connection_metadata[websocket]
    
    async def send_personal_message(self, message: dict, websocket: WebSocket):
        """Send message to specific connection"""
        try:
            await websocket.send_json(message)
        except Exception as e:
            print(f"Error sending message: {e}")
            self.disconnect(websocket)
    
    async def broadcast_to_user(self, user_id: int, message: dict):
        """Broadcast message to all connections of a user"""
        if user_id in self.active_connections:
            disconnected = []
            
            for connection in self.active_connections[user_id]:
                try:
                    await connection.send_json(message)
                except Exception:
                    disconnected.append(connection)
            
            # Clean up disconnected
            for conn in disconnected:
                self.disconnect(conn)
    
    async def broadcast_to_entity_subscribers(
        self, 
        entity_id: int, 
        message: dict
    ):
        """Broadcast message to all subscribers of an entity"""
        if entity_id in self.entity_subscriptions:
            disconnected = []
            
            for connection in self.entity_subscriptions[entity_id]:
                try:
                    await connection.send_json(message)
                except Exception:
                    disconnected.append(connection)
            
            # Clean up disconnected
            for conn in disconnected:
                self.disconnect(conn)
    
    async def broadcast_all(self, message: dict):
        """Broadcast message to all connected clients"""
        all_connections = set()
        for connections in self.active_connections.values():
            all_connections.update(connections)
        
        disconnected = []
        for connection in all_connections:
            try:
                await connection.send_json(message)
            except Exception:
                disconnected.append(connection)
        
        # Clean up disconnected
        for conn in disconnected:
            self.disconnect(conn)
    
    def get_active_users_count(self) -> int:
        """Get number of active users"""
        return len(self.active_connections)
    
    def get_active_connections_count(self) -> int:
        """Get total number of active connections"""
        return sum(len(conns) for conns in self.active_connections.values())


# Global connection manager instance
manager = ConnectionManager()


class RealtimeEventPublisher:
    """Publish real-time events to connected clients"""
    
    def __init__(self, connection_manager: ConnectionManager):
        self.manager = connection_manager
    
    async def publish_new_mention(
        self, 
        entity_id: int, 
        mention_data: Dict[str, Any]
    ):
        """Publish new mention event"""
        event = {
            "type": EventType.NEW_MENTION.value,
            "entity_id": entity_id,
            "data": mention_data,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        await self.manager.broadcast_to_entity_subscribers(entity_id, event)
    
    async def publish_alert(
        self, 
        user_id: int, 
        entity_id: int,
        alert_data: Dict[str, Any]
    ):
        """Publish alert event"""
        event = {
            "type": EventType.ALERT_CREATED.value,
            "entity_id": entity_id,
            "data": alert_data,
            "timestamp": datetime.utcnow().isoformat(),
            "severity": alert_data.get("severity", "medium")
        }
        
        # Send to user
        await self.manager.broadcast_to_user(user_id, event)
        
        # Also send to entity subscribers
        await self.manager.broadcast_to_entity_subscribers(entity_id, event)
    
    async def publish_reputation_update(
        self, 
        entity_id: int,
        old_score: float,
        new_score: float,
        trend: str
    ):
        """Publish reputation score update"""
        event = {
            "type": EventType.REPUTATION_UPDATE.value,
            "entity_id": entity_id,
            "data": {
                "old_score": old_score,
                "new_score": new_score,
                "change": new_score - old_score,
                "trend": trend
            },
            "timestamp": datetime.utcnow().isoformat()
        }
        
        await self.manager.broadcast_to_entity_subscribers(entity_id, event)
    
    async def publish_sentiment_change(
        self, 
        entity_id: int,
        sentiment_data: Dict[str, Any]
    ):
        """Publish significant sentiment change"""
        event = {
            "type": EventType.SENTIMENT_CHANGE.value,
            "entity_id": entity_id,
            "data": sentiment_data,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        await self.manager.broadcast_to_entity_subscribers(entity_id, event)
    
    async def publish_trend_detection(
        self, 
        entity_id: int,
        trend_data: Dict[str, Any]
    ):
        """Publish trend detection event"""
        event = {
            "type": EventType.TREND_DETECTED.value,
            "entity_id": entity_id,
            "data": trend_data,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        await self.manager.broadcast_to_entity_subscribers(entity_id, event)
    
    async def publish_system_notification(
        self, 
        user_id: int,
        notification: Dict[str, Any]
    ):
        """Publish system notification"""
        event = {
            "type": EventType.SYSTEM_NOTIFICATION.value,
            "data": notification,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        await self.manager.broadcast_to_user(user_id, event)


class HeartbeatService:
    """Maintain WebSocket connections with periodic heartbeats"""
    
    def __init__(self, connection_manager: ConnectionManager):
        self.manager = connection_manager
        self.heartbeat_interval = 30  # seconds
        self.running = False
    
    async def start(self):
        """Start heartbeat service"""
        self.running = True
        while self.running:
            await self._send_heartbeats()
            await asyncio.sleep(self.heartbeat_interval)
    
    def stop(self):
        """Stop heartbeat service"""
        self.running = False
    
    async def _send_heartbeats(self):
        """Send heartbeat to all connections"""
        heartbeat_message = {
            "type": EventType.HEARTBEAT.value,
            "timestamp": datetime.utcnow().isoformat(),
            "active_users": self.manager.get_active_users_count(),
            "active_connections": self.manager.get_active_connections_count()
        }
        
        await self.manager.broadcast_all(heartbeat_message)


# Initialize services
event_publisher = RealtimeEventPublisher(manager)
heartbeat_service = HeartbeatService(manager)
