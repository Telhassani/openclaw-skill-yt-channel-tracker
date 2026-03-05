# YouTube Channel Tracker

An OpenClaw skill that fetches the latest videos from a configured list of YouTube channels.

## Features

- Fetch latest N videos from each configured channel
- Per-channel configurable video limits
- Video title, URL, duration, and view count
- Error handling with skip-and-continue
- API credit tracking

## Installation

```bash
cd /data/.openclaw/workspace/skills/youtube-channel-tracker
pip install -r requirements.txt
```

## Configuration

Edit `config.json` to add your channels:

```json
{
  "api": {
    "provider": "scrapecreators",
    "key": "YOUR_API_KEY",
    "base_url": "https://api.scrapecreators.com/v1"
  },
  "channels": [
    {"name": "Channel Name", "channelId": "UC...", "limit": 3}
  ],
  "defaults": {
    "videos_per_channel": 3
  }
}
```

### Getting Channel IDs

YouTube channel IDs start with `UC` and can be found in:
- Channel URL: `youtube.com/channel/UCxxxxxxxxxxxxxxxxxxxxxx`
- Channel page source: search for `channelId`

## Usage

### CLI

```bash
# Fetch all channels
python app.py fetch

# List configured channels
python app.py list
```

### OpenClaw Triggers

```
/yt-tracker         → Fetch all channels
/yt-tracker list    → Show configured channels
```

Or use natural language:
- "What's new on my channels?"
- "Show me the latest videos from my YouTube channels"

## Output Example

```
=== Octogone ===
1. Pourquoi Donald Trump se remet à parler des extraterrestres ? (1h 10m) — 139K views
   https://www.youtube.com/watch?v=KDV4Q35rPT0
2. Des dossiers Epstein aux marchés financiers... (1h 7m) — 424K views
   https://www.youtube.com/watch?v=bo9tLr3KV2M
3. La Bank of England parle d'Aliens... (1h 7m) — 217K views
   https://www.youtube.com/watch?v=WJXM8g-kB30

──────────────────────────────────────────────────
API credits remaining: 4563

Errors: 0
```

## API

This skill uses [ScrapeCreators](https://scrapecreators.com) API.

**Endpoint:** `GET /youtube/channel-videos`

**Parameters:**
- `channelId` — YouTube channel ID (required)
- `limit` — Max videos to return (optional)

**Headers:**
- `x-api-key: YOUR_API_KEY`

## Adding Channels

Ask Claw to add channels:
```
"Add Lex Fridman to my tracker, limit 5"
"Add https://www.youtube.com/@lexfridman"
```

Claw will validate the channel and update `config.json`.

## License

MIT