import streamlit as st
import time  # For simulating updates
import os
from datetime import datetime
from PIL import Image  # For handling images

# --- Global Variables (for simplicity - avoid in real apps!) ---
MESSAGES = []  # In-memory list to store messages
USER_NAME = ""
IMAGE_DIR = "images"  # Directory to store uploaded images
os.makedirs(IMAGE_DIR, exist_ok=True)  # Ensure the directory exists

# --- Helper Functions ---
def format_message(message):
    return f"{message['timestamp']} - {message['user']}: {message['text']}"

# Load existing messages.  Using st.cache_data for optimization
# In real code, load from database at app start
@st.cache_data(ttl=60)  # Cache messages for 60 seconds
def get_messages():
    return MESSAGES

def add_message(user, text, image=None):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    message = {"timestamp": timestamp, "user": user, "text": text, "image": image}
    MESSAGES.append(message)
    # Clear cache, so the new message will display.
    get_messages.clear() # Clear cache to force update.

# --- Streamlit App ---

def main():
    global USER_NAME  # Use the global variable

    st.title("Simple WhatsApp Clone (Streamlit)")

    # --- User Authentication ---
    if not USER_NAME:
        USER_NAME = st.text_input("Enter your name:", "")
        if USER_NAME:
            st.success(f"Logged in as {USER_NAME}")
        else:
            st.warning("Please enter your name to start chatting.")
            return  # Stop execution until the user enters a name

    # --- Message Input ---
    message_text = st.text_input("Your message:", "")
    uploaded_image = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

    if st.button("Send"):
        if message_text or uploaded_image:
            image_path = None
            if uploaded_image:
                # Save the image locally (for demonstration purposes)
                image_filename = f"{int(time.time())}_{uploaded_image.name}"  # Unique filename
                image_path = os.path.join(IMAGE_DIR, image_filename)
                with open(image_path, "wb") as f:
                    f.write(uploaded_image.read())

            add_message(USER_NAME, message_text, image=image_path)
            message_text = ""  # Clear the input field

    # --- Message Display ---
    st.subheader("Messages")

    # Get messages from cache (faster)
    messages_to_display = get_messages()

    for message in messages_to_display:
        st.write(format_message(message))
        if message["image"]:
            try:
                image = Image.open(message["image"])
                st.image(image, width=200)
            except FileNotFoundError:
                st.error("Image not found.")

    # --- Simulate Real-Time Updates (Polling) ---
    time.sleep(1)  # Wait for 1 second
    st.rerun()  # Refresh the app to check for new messages

if __name__ == "__main__":
    main()