import json
from datetime import datetime
from math import ceil

file_name = "messages.json"

# Load the JSON file
with open(file_name, "r", encoding="utf-8") as file:
    data = json.load(file)

# Extract participants
participants = data.get("participants", [])

# Define colors for participants
colors = ["#DCF8C6", "#f0f0f0"]  # Light green for one user, white for the other
participant_styles = {participants[i]: colors[i % len(colors)] for i in range(len(participants))}

# Define pagination settings
PAGE_HEIGHT_CM = 29.7  # A4 height in cm
PAGE_WIDTH_CM = 21     # A4 width in cm
MARGIN_CM = 1          # Page margin
LINE_HEIGHT_CM = 0.6   # Approx height for each message line
FOOTER_HEIGHT_CM = 1.0  # Footer height in cm
MAX_PAGE_HEIGHT_CM = PAGE_HEIGHT_CM - 2 * MARGIN_CM - FOOTER_HEIGHT_CM  # Max height for messages

# Initialize variables for page tracking
page_count = 1
current_height = 0  # Track the height of messages on the current page
current_page_messages = []

# Open the output file
with open("output.html", "w", encoding="utf-8") as output:
    # Write HTML header with inline CSS for styling
    output.write("""
    <html>
    <head>
        <title>Chat Transcript</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                line-height: 1.6;
                margin: 0;
                padding: 0;
                background-color: #ffffff;
            }
            .page {
                width: 21cm;
                height: 29.7cm;
                margin: 0 auto;
                padding: 0cm 1cm 0cm 1cm;
                box-sizing: border-box;
                page-break-after: always;
                display: flex;
                flex-direction: column;
                justify-content: space-between;
                border: 1px solid #ddd;
            }
            .messages {
                flex-grow: 1;
                overflow: hidden;
                word-wrap: break-word;
            }
            .message {
                margin: 10px 0;
                padding: 10px;
                border-radius: 8px;
                width: fit-content;
                max-width: 80%;
                word-wrap: break-word;
                box-sizing: border-box;
                overflow-wrap: break-word;
                z-index: 1;
            }
            .message-left {
                background-color: #DCF8C6;
                margin-right: auto;
            }
            .message-right {
                background-color: #FFF;
                margin-left: auto;
            }
            .sender {
                font-weight: bold;
                margin-bottom: 5px;
                font-size: 0.9em;
            }
            .timestamp {
                font-size: 0.8em;
                color: #888;
                margin-top: 5px;
            }
            .footer {
                text-align: center;
                font-size: 12px;
                margin-top: 10px;
                padding: 5px;
                background-color: transparent;
            }
            @media print {
                .page {
                    border: none;
                    box-shadow: none;
                }
                .footer {
                    position: absolute;
                    bottom: 1cm;
                    left: 50%;
                    transform: translateX(-50%);
                }
            }
        </style>
    </head>
    <body>
    """)

    # Loop through messages
    for message in data.get("messages", []):
        sender = message.get("senderName", "Unknown")
        timestamp = message.get("timestamp")
        text = message.get("text", "")
        media = message.get("media", [])
        reactions = message.get("reactions", [])

        # Format timestamp
        formatted_time = datetime.fromtimestamp(timestamp / 1000).strftime("%d-%m-%y %H:%M:%S")

        # Determine message alignment and style
        alignment = "message-right" if sender == participants[0] else "message-left"
        style = participant_styles.get(sender, "#FFF")

        # Approximate the height of the message
        sender_height = 1.0  # Sender's name takes ~1 line
        timestamp_height = 1.0  # Timestamp takes ~1 line
        text_height = ceil(len(text) / 80) * LINE_HEIGHT_CM  # Text height based on content
        media_height = len(media) * 1.0  # Media files take ~1 line each
        reactions_height = len(reactions) * 1.0  # Reactions take ~1 line each

        total_message_height = sender_height + timestamp_height + text_height + media_height + reactions_height
        current_height += total_message_height

        # Check if the message fits on the current page
        if current_height > MAX_PAGE_HEIGHT_CM:
            # Write the current page and reset for next page
            output.write(f"""
            <div class="page">
                <div class="messages">
                    {''.join(current_page_messages)}
                </div>
                <div class="footer">Page {page_count}</div>
            </div>
            """)
            # Reset for the next page
            page_count += 1
            current_height = total_message_height  # Reset height for the new page
            current_page_messages = []

        # Add the message block to the current page
        current_page_messages.append(f"""
        <div class="message {alignment}" style="background-color: {style}">
            <div class="sender">{sender}</div>
            <div class="timestamp">{formatted_time}</div>
        """)

        if text:
            current_page_messages.append(f"<div>{text}</div>")

        if media:
            for m in media:
                current_page_messages.append(f"<div class='media'><a href='{m['uri']}' target='_blank'>[Media file]</a></div>")

        if reactions:
            reaction_text = ", ".join(f"{r['actor']}: {r['reaction']}" for r in reactions)
            current_page_messages.append(f"<div class='reactions'><em>Reactions:</em> {reaction_text}</div>")

        current_page_messages.append("</div>")  # Close message div

    # Add the last page if there are remaining messages
    if current_page_messages:
        output.write(f"""
        <div class="page">
            <div class="messages">
                {''.join(current_page_messages)}
            </div>
            <div class="footer">Page {page_count}</div>
        </div>
        """)

    # Close HTML
    output.write("""
    </body>
    </html>
    """)

print("Chat transcript has been saved to output.html")
