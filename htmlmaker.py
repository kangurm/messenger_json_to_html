import json
from datetime import datetime

file_name = "messages.json"

# Load the JSON file
with open(file_name, "r", encoding="utf-8") as file:
    data = json.load(file)

# Extract participants
participants = data.get("participants", [])

# Define colors for participants
colors = ["#DCF8C6", "#f0f0f0"]  # Light green for one user, white for the other
participant_styles = {participants[i]: colors[i % len(colors)] for i in range(len(participants))}

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
                background-color: #f0f0f0;
            }
            .chat-container {
                max-width: 600px;
                margin: 20px auto;
                background-color: #fff;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
                overflow: hidden;
                padding: 10px;
            }
            .message {
                margin: 10px 0;
                padding: 10px;
                border-radius: 8px;
                width: fit-content;
                max-width: 80%;
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
            .media {
                margin-top: 5px;
            }
        </style>
    </head>
    <body>
        <div class="chat-container">
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

        # Write the message block
        output.write(f"""
        <div class="message {alignment}" style="background-color: {style}">
            <div class="sender">{sender}</div>
        """)

        if text:
            output.write(f"<div>{text}</div>")

        if media:
            for m in media:
                output.write(f"<div class='media'><a href='{m['uri']}' target='_blank'>[Media file]</a></div>")

        if reactions:
            reaction_text = ", ".join(f"{r['actor']}: {r['reaction']}" for r in reactions)
            output.write(f"<div class='reactions'><em>Reactions:</em> {reaction_text}</div>")

        output.write(f"<div class='timestamp'>{formatted_time}</div>")
        output.write("</div>")  # Close message div

    # Close HTML
    output.write("""
        </div>
    </body>
    </html>
    """)

print("Chat transcript has been saved to output.html")
