# SKILL.md — YouTube Channel Tracker

**Purpose:** Fetch latest videos from a configured list of YouTube channels

## Triggers

Use this skill when the user asks to:
- Check latest videos from their YouTube channels
- `/yt-tracker` or `/yt-tracker fetch` — Fetch all channels
- `/yt-tracker list` — Show configured channels
- "What's new on my channels?"
- "Show me the latest videos from my YouTube channels"
- "Check my YouTube subscriptions"

## API

- **Provider:** ScrapeCreators
- **Base URL:** `https://api.scrapecreators.com/v1/youtube/channel-videos`
- **Auth:** `x-api-key` header

## Functions

### `fetch_all_channels()`
Main function: Loop through all configured channels → output to stdout

### `fetch_channel_videos(channel_id, limit)`
Fetch latest N videos from a single channel

**Parameters:**
- `channelId`: YouTube channel ID (starts with `UC...`)
- `limit`: Max videos to return (default: 3)

**Returns:**
```json
{
  "success": true,
  "videos": [...],
  "credits_remaining": 4572
}
```

### `list_channels()`
Show configured channels from config.json

---

## Output Format

```
=== Octogone ===
1. Pourquoi Donald Trump se remet à parler des extraterrestres ? (1h 10m) — 138K views
   https://youtube.com/watch?v=KDV4Q35rPT0
2. Des dossiers Epstein aux marchés financiers... (1h 07m) — 424K views
   https://youtube.com/watch?v=bo9tLr3KV2M
3. La Bank of England parle d'Aliens... (1h 07m) — 217K views
   https://youtube.com/watch?v=WJXM8g-kB30

───
API credits remaining: 4572

Errors: 0
```

---

## Config Schema

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

---

## Usage

```bash
# Fetch all channels
python app.py fetch

# List configured channels
python app.py list
```

---

## Adding Channels

To add a new channel, ask Claw to edit `config.json`:
- Provide channel name and YouTube channel ID (starts with `UC...`)
- Or provide the channel URL/handle and Claw will resolve it

---

## Error Handling

- Failed channels: Skip and report at end
- API errors: Display error code and continue
- Timeout: 30 seconds per request

---

## Credits

Monitor `credits_remaining` in output. Current balance shown after each fetch.