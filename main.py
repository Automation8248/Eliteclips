import os
import json
import random
import requests
import datetime

# --- CONFIGURATION ---
VIDEO_FOLDER = "videos"
HISTORY_FILE = "history.json"
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")

# Yahan maine image se dekh kar aapka exact Repo Name daal diya hai
GITHUB_REPO = "Automation8248/Eliteclips"
BRANCH_NAME = "main"

# --- DATA GRID (Pre-saved Titles & Captions) ---

# List 1: Titles (Har bar inme se koi ek randomly select hoga)
TITLES_GRID = [
    "You Won’t Believe This Scene 😱",
    "This Movie Moment Changed Everything",
    "Wait for the Plot Twist!",
    "Best Scene in the Whole Movie?",
    "This Scene Gave Me Chills",
    "Hollywood at Its Finest 🎬",
    "That One Scene Everyone Talks About",
    "This Hit Different 🔥",
    "POV: You’re Watching a Masterpiece",
    "The Most Savage Comeback Ever",
    "This Actor Deserves an Oscar",
    "Legendary Movie Moment",
    "This Scene Broke the Internet",
    "When the Hero Finally Snaps 😤",
    "Villain Stole the Show",
    "This Is Why We Love Movies",
    "That Twist Nobody Saw Coming",
    "Top Tier Acting Right Here",
    "This Scene Is Pure Gold",
    "You Missed This Detail!",
    "The Ending Was Insane 🤯",
    "This Gave Me Goosebumps",
    "The Most Emotional Scene Ever",
    "This Scene Lives Rent Free in My Head",
    "Peak Cinema 🎥",
    "When Karma Hits Back",
    "This Scene Deserved More Hype",
    "Hollywood Magic in 60 Seconds",
    "That Dialogue Was Cold 🥶",
    "This Is Cinema!",
    "Instant Classic Scene",
    "You Need to Watch This",
    "The Most Underrated Movie Moment",
    "This Scene = Perfection",
    "Wait Till the End 👀",
    "This Is Why He’s the GOAT",
    "The Most Powerful Speech Ever",
    "This Scene Went Too Hard 🔥",
    "Unforgettable Movie Moment",
    "The Scene That Made History",
    "This Was Next Level",
    "When the Plot Gets Real",
    "The Most Satisfying Scene Ever",
    "This Scene Still Gives Chills",
    "One of the Best Scenes Ever Filmed",
    "This Deserved an Award",
    "The Most Intense 60 Seconds",
    "This Scene Is Iconic",
    "That Reaction Was Priceless",
    "Movie Fans Know This One",
    "This Scene Never Gets Old",
    "Straight Out of a Blockbuster",
    "This Is Why It’s a Classic",
    "When the Truth Comes Out",
    "This Scene Was Legendary"
]


# List 2: Captions (Har bar inme se koi ek randomly select hoga)
CAPTIONS_GRID = [
    "This scene deserves an Oscar 🏆🔥",
    "Wait till the end… trust me 😳",
    "Hollywood never disappoints 🎬",
    "This moment gave me chills 🥶",
    "POV: You found the best scene today",
    "Tag someone who loves movies 🎥",
    "This is why we love cinema ❤️",
    "That plot twist though 😱",
    "Instant classic. No debate.",
    "This actor nailed it 💯",
    "One of the best scenes ever made",
    "You missed this detail… watch again 👀",
    "Pure cinematic masterpiece ✨",
    "This scene hits different",
    "Villain stole the whole movie 😈",
    "When the hero finally snaps 🔥",
    "This deserves more hype 🚀",
    "The dialogue was cold 🥶",
    "Movie fans know what this is 🎬",
    "This scene lives rent free in my head",
    "Goosebumps every single time 😮‍💨",
    "That reaction was priceless 😂",
    "This is cinema. Period.",
    "Underrated but legendary scene",
    "You won’t believe what happens next 😳",
    "This part broke the internet 🌎",
    "Straight out of a blockbuster 💥",
    "The most intense 60 seconds ever",
    "Watch this twice. Trust me.",
    "When karma hits back 😤",
    "This scene never gets old",
    "Peak Hollywood energy ⚡",
    "Tell me this isn’t iconic 😏",
    "This is why he’s the GOAT 🐐",
    "That ending was insane 🤯",
    "Comment your favorite movie below 🎥",
    "If you know, you know 😌",
    "This scene = perfection 💎",
    "Top tier acting right here",
    "The most powerful speech ever",
    "This hit harder than expected",
    "Absolute masterpiece moment",
    "When the truth comes out 👀",
    "This scene deserved an award 🏆",
    "Unforgettable movie vibes ✨",
    "Press like if you felt this ❤️",
    "This scene went too hard 🔥",
    "Real movie lovers will understand",
    "This is what great storytelling looks like",
    "Drop a 🎬 if you want more scenes like this"
]


# List 3: Fixed Hashtags (Ye har video me SAME rahega)
FIXED_HASHTAGS = """
.
.
.
.
.
#viral #trending #fyp #foryou #reels #short #shorts #ytshorts #explore #explorepage #viralvideo #trend #newvideo #content #creator #dailycontent #entertainment #fun #interesting #watchtillend #mustwatch #reality #real #moment #life #daily #people #reaction #vibes #share #support"""

# Isse AFFILIATE_HASHTAGS se badal kar INSTA_HASHTAGS kar diya hai
INSTA_HASHTAGS = """
.
.
.
.
"#viral #fyp #trending #explorepage #ytshorts"
"""
YOUTUBE_HASHTAGS = """
.
.
.
"#youtubeshorts #youtube #shorts #subscribe #viralshorts"
"""

FACEBOOK_HASHTAGS = """
.
.
.
"#facebookreels #fb #reelsvideo #viralreels #viral-video #trending-now #facebook-reels #reels-viral #must-watch #share-this #explore-page #for-you #social-media-growth #digital-marketing #content-creator #video-marketing #online-earning #internet-famous #watch-till-end #like-and-share #tag-a-friend #daily-content #short-video #brand-building #seo-boost #fbreels"
"""

# --- HELPER FUNCTIONS ---

def load_history():
    if not os.path.exists(HISTORY_FILE):
        return []
    with open(HISTORY_FILE, 'r') as f:
        return json.load(f)

def save_history(data):
    with open(HISTORY_FILE, 'w') as f:
        json.dump(data, f, indent=4)

# --- MAIN LOGIC ---

def run_automation():
    # 1. DELETE OLD FILES (15 Days Logic)
    history = load_history()
    today = datetime.date.today()
    new_history = []
    
    print("Checking for expired videos...")
    for entry in history:
        sent_date = datetime.date.fromisoformat(entry['date_sent'])
        days_diff = (today - sent_date).days
        
        file_path = os.path.join(VIDEO_FOLDER, entry['filename'])
        
        if days_diff >= 15:
            if os.path.exists(file_path):
                os.remove(file_path)
                print(f"DELETED EXPIRED: {entry['filename']}")
        else:
            new_history.append(entry)
    
    save_history(new_history)
    history = new_history 

    # 2. PICK NEW VIDEO
    if not os.path.exists(VIDEO_FOLDER):
        os.makedirs(VIDEO_FOLDER)
        
    all_videos = [f for f in os.listdir(VIDEO_FOLDER) if f.lower().endswith(('.mp4', '.mov', '.mkv'))]
    sent_filenames = [entry['filename'] for entry in history]
    
    available_videos = [v for v in all_videos if v not in sent_filenames]
    
    if not available_videos:
        print("No new videos to send.")
        return

    video_to_send = random.choice(available_videos)
    video_path = os.path.join(VIDEO_FOLDER, video_to_send)
    
    print(f"Selected Video File: {video_to_send}")

    # 3. RANDOM SELECTION (Grid System)
    selected_title = random.choice(TITLES_GRID)
    selected_caption = random.choice(CAPTIONS_GRID)
    
    # Combine content
    full_telegram_caption = f"{selected_title}\n\n{selected_caption}\n{FIXED_HASHTAGS}"
    
    print(f"Generated Title: {selected_title}")
    print(f"Generated Caption: {selected_caption}")

    # 4. SEND TO TELEGRAM
    if TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID:
        print("Sending to Telegram...")
        
        # Server time ko automatically Indian Standard Time (IST) mein convert karna
        ist_now = datetime.datetime.utcnow() + datetime.timedelta(hours=5, minutes=30)
        
        # Format: DD MONTH HH:MM:SS AM/PM YYYY aur sabko CAPITAL karna
        time_string = ist_now.strftime("%d %b %I:%M:%S %p %Y").upper()
        
        # Sirf bold date aur time, koi title/hashtag nahi
        telegram_caption = f"<b>{time_string}</b>"

        with open(video_path, 'rb') as video_file:
            url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendVideo"
            payload = {
                'chat_id': TELEGRAM_CHAT_ID, 
                'caption': telegram_caption,
                'parse_mode': 'HTML' # <b> tag se text ko bold karne ke liye zaroori hai
            }
            files = {'video': video_file}
            try:
                requests.post(url, data=payload, files=files)
            except Exception as e:
                print(f"Telegram Error: {e}")

    # 5. SEND TO WEBHOOK
    if WEBHOOK_URL:
        print("Sending to Webhook...")
        # URL construction with your specific repo name
        raw_video_url = f"https://raw.githubusercontent.com/{GITHUB_REPO}/{BRANCH_NAME}/{VIDEO_FOLDER}/{video_to_send}"
        # Encode spaces if any
        raw_video_url = raw_video_url.replace(" ", "%20")
        
        webhook_data = {
            "video_url": raw_video_url,
            "title": selected_title,
            "caption": selected_caption,
            "hashtags": FIXED_HASHTAGS,
            "insta_hashtags": INSTA_HASHTAGS,
            "youtube_hashtags": YOUTUBE_HASHTAGS, # Naya add kiya gaya
            "facebook_hashtags": FACEBOOK_HASHTAGS, # Naya add kiya gaya
            "source": "AffiliateBot"
        }
        try:
            requests.post(WEBHOOK_URL, json=webhook_data)
            print(f"Webhook Sent: {raw_video_url}")
        except Exception as e:
            print(f"Webhook Error: {e}")

    # 6. UPDATE HISTORY
    new_history.append({
        "filename": video_to_send,
        "date_sent": today.isoformat()
    })
    save_history(new_history)
    print("Automation Complete.")

if __name__ == "__main__":
    run_automation()
