import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
import time

# Replace these with your credentials
TELEGRAM_BOT_TOKEN = '7945635558:AAH7GblGydFLIl0kzrHWklt1jiZBGjqKc7U'
TUTOR_LMS_API_KEY = 'key_fb1052e71173b6d6a0ec5ea71f284273'
TUTOR_LMS_SECRET_KEY = 'secret_1aa8f54ad934258cc3b4ac4db499cddcc1faf7da7b93381fa88bdcf546e6f202'
TUTOR_LMS_BASE_URL = 'https://dynamiwebtraining.com/wp-json/tutor/v1/courses'

# Function to fetch courses from Tutor LMS with retries
def fetch_courses_with_retries(retries=3, delay=5):
    auth = (TUTOR_LMS_API_KEY, TUTOR_LMS_SECRET_KEY)  # Basic Auth credentials
    headers = {
        'Accept': 'application/json'
    }
    
    for attempt in range(1, retries + 1):
        try:
            print(f"Attempting to fetch courses (Attempt {attempt}/{retries})...")
            response = requests.get(TUTOR_LMS_BASE_URL, headers=headers, auth=auth, timeout=30)
            
            # Debugging: Print the response status and content
            print(f"Response status code: {response.status_code}")
            print(f"Response content: {response.text}")
            
            response.raise_for_status()
            data = response.json()
            if isinstance(data, dict) and 'data' in data:
                return data['data']  # Assuming courses are in 'data' key
            return []
        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt} failed: {e}")
            if attempt < retries:
                time.sleep(delay)
            else:
                print("Max retries reached. Could not fetch courses.")
                return []


# Command handler for /courses
async def list_courses(update: Update, context: CallbackContext):
    courses = fetch_courses_with_retries()
    if not courses:
        await update.message.reply_text("No courses found or an error occurred.")
        return

    message = "Available Courses:\n"
    for course in courses:
        title = course.get('title', 'No Title')
        permalink = course.get('permalink', 'No Link Available')
        message += f"\n• {title}\nLink: {permalink}\n"

    await update.message.reply_text(message)

# Main function to run the bot
def main():
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Command to list courses
    application.add_handler(CommandHandler("courses", list_courses))

    # Start the bot
    print("Bot is running...")
    application.run_polling()

if __name__ == "__main__":
    main()
