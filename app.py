#!/usr/bin/env python3
"""
YouTube Channel Tracker - Fetch latest videos from configured channels
Usage:
    python app.py fetch           - Fetch all channels
    python app.py list            - List configured channels
"""

import json
import sys
from pathlib import Path
from datetime import datetime

import requests

# Load config
SKILL_DIR = Path(__file__).parent
with open(SKILL_DIR / "config.json") as f:
    CONFIG = json.load(f)


def format_duration(seconds: int) -> str:
    """Format seconds to human-readable duration (e.g., 2h 33m or 45m)."""
    if seconds is None:
        return ""
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    if hours > 0:
        return f"{hours}h {minutes}m"
    return f"{minutes}m"


def format_views(count: int) -> str:
    """Format view count to human-readable (e.g., 1.2M)."""
    if count is None:
        return ""
    if count >= 1_000_000:
        return f"{count / 1_000_000:.1f}M"
    elif count >= 1_000:
        return f"{count / 1_000:.0f}K"
    return str(count)


def fetch_channel_videos(channel_id: str, limit: int = 3) -> dict:
    """
    Fetch latest videos from a YouTube channel.
    
    Args:
        channel_id: YouTube channel ID (starts with UC...)
        limit: Maximum number of videos to fetch
        
    Returns:
        dict with 'success', 'videos', 'credits_remaining', or 'error'
    """
    try:
        response = requests.get(
            f"{CONFIG['api']['base_url']}/youtube/channel-videos",
            params={"channelId": channel_id, "limit": limit},
            headers={"x-api-key": CONFIG["api"]["key"]},
            timeout=30
        )
        
        if response.status_code != 200:
            return {
                "success": False,
                "error": f"API error: {response.status_code}",
                "details": response.text[:200] if response.text else ""
            }
        
        data = response.json()
        
        if not data.get("success"):
            return {
                "success": False,
                "error": data.get("message", "Unknown error")
            }
        
        return {
            "success": True,
            "videos": data.get("videos", [])[:limit],
            "credits_remaining": data.get("credits_remaining", "unknown")
        }
        
    except requests.Timeout:
        return {"success": False, "error": "Request timeout"}
    except requests.RequestException as e:
        return {"success": False, "error": f"Request failed: {e}"}
    except json.JSONDecodeError:
        return {"success": False, "error": "Invalid JSON response"}


def fetch_all_channels():
    """Fetch latest videos from all configured channels."""
    channels = CONFIG.get("channels", [])
    default_limit = CONFIG.get("defaults", {}).get("videos_per_channel", 3)
    
    if not channels:
        print("No channels configured. Add channels to config.json")
        return
    
    errors = []
    total_credits = None
    
    for channel in channels:
        name = channel.get("name", "Unknown")
        channel_id = channel.get("channelId")
        limit = channel.get("limit", default_limit)
        
        print(f"\n=== {name} ===\n")
        
        if not channel_id:
            print(f"⚠️  Error: No channelId configured\n")
            errors.append({"name": name, "error": "No channelId configured"})
            continue
        
        result = fetch_channel_videos(channel_id, limit)
        
        if not result.get("success"):
            print(f"⚠️  Error: {result.get('error', 'Unknown error')}")
            if result.get("details"):
                print(f"   Details: {result['details']}")
            print()
            errors.append({"name": name, "error": result.get("error", "Unknown error")})
            continue
        
        videos = result.get("videos", [])
        
        if total_credits is None:
            total_credits = result.get("credits_remaining")
        
        for i, video in enumerate(videos, 1):
            title = video.get("title", "Untitled")
            url = video.get("url", "")
            duration = format_duration(video.get("lengthSeconds"))
            views = format_views(video.get("viewCountInt"))
            
            duration_str = f" ({duration})" if duration else ""
            views_str = f" — {views} views" if views else ""
            
            print(f"{i}. {title}{duration_str}{views_str}")
            print(f"   {url}\n")
    
    # Summary
    print("─" * 50)
    if total_credits is not None:
        print(f"API credits remaining: {total_credits}\n")
    
    if errors:
        print(f"Errors: {len(errors)}")
        for err in errors:
            print(f"  - {err['name']}: {err['error']}")
    else:
        print("Errors: 0")


def list_channels():
    """List all configured channels."""
    channels = CONFIG.get("channels", [])
    default_limit = CONFIG.get("defaults", {}).get("videos_per_channel", 3)
    
    if not channels:
        print("No channels configured.")
        return
    
    print(f"\nConfigured channels ({len(channels)}):\n")
    for i, ch in enumerate(channels, 1):
        name = ch.get("name", "Unknown")
        channel_id = ch.get("channelId", "N/A")
        limit = ch.get("limit", default_limit)
        print(f"{i}. {name}")
        print(f"   ID: {channel_id}")
        print(f"   Limit: {limit} videos\n")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(0)
    
    action = sys.argv[1].lower()
    
    if action == "fetch":
        fetch_all_channels()
    elif action == "list":
        list_channels()
    else:
        print(f"Unknown action: {action}")
        print("Usage: python app.py [fetch|list]")
        sys.exit(1)