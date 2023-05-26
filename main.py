import os
import telebot
import datetime
import pytz
from telebot import types
from telebot.types import Poll

# Define secret information
API_KEY = os.getenv('API_KEY')
SSReview_id = os.getenv('SSREVIEW_ID')
SSPoll_id = os.getenv('SSPOLL_ID')
SSPoll_link = os.getenv('SSPOLL_LINK')
SSChat_id = os.getenv('SSCHAT_ID')
SSChat_link = os.getenv('SSCHAT_LINK')
IGNORED_CHAT_ID = os.getenv('SSCHAT_ID')

# Create bot
bot = telebot.TeleBot(API_KEY)

# Define the approval keyboard with an approve and reject button
approval_keyboard = types.InlineKeyboardMarkup(row_width=2)
approve_button = types.InlineKeyboardButton(text='👍 Approve', callback_data='approve')
reject_button = types.InlineKeyboardButton(text='👎 Reject', callback_data='reject')
approval_keyboard.add(approve_button, reject_button)

# Define the user persistent keyboard with three buttons
SSPoll_invite = "Invite me to Survey Squad: Polls"
SSChat_invite = "Invite me to Survey Squad: Chat"
Help_text = "How do I create a poll?"
SSPoll_button = types.KeyboardButton(SSPoll_invite)
SSChat_button = types.KeyboardButton(SSChat_invite)
Help_button = types.KeyboardButton(Help_text)

# Define time zone and time format
timezone = pytz.timezone('US/Central')
now = datetime.datetime.now(timezone)
time_string = now.strftime("%Y-%m-%d %I:%M:%S %p %Z")

# Create the user persistent keyboard
keyboard_all = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
keyboard_all.add(SSPoll_button, SSChat_button, Help_button)

SSPoll_value = 0
SSChat_value = 0

# Define dictionaries for pending poll approvals
pending_polls = {}
pending_messages = {}
pending_polls_id = {}
pending_user = {}

# Define start command handler
# It will tell the user what the bot does and what type of polls should be submitted
@bot.message_handler(commands=['start'])
def start(message):
  from_user_name = message.from_user.username
  from_first_name = message.from_user.first_name
  from_last_name = message.from_user.last_name
  from_full_name = f'{from_first_name} {from_last_name}'
  print(f'@{from_user_name}, {from_full_name} has used the start command. time: {time_string}')
  SSPoll_value = 0
  SSChat_value = 0
  if message.chat.type == 'private':
    SSPoll_member = bot.get_chat_member(SSPoll_id, message.chat.id)
    SSChat_member = bot.get_chat_member(SSChat_id, message.chat.id)
    if SSPoll_member.status == 'member':
      SSPoll_value = 1
    if SSChat_member.status == 'member':
      SSChat_value = 2
    member_value = SSPoll_value+SSChat_value
    if member_value == 0:
      keyboard_all = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
      keyboard_all.add(SSPoll_button, SSChat_button, Help_button)
    elif member_value == 1:
      keyboard_all = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
      keyboard_all.add(SSChat_button, Help_button)
    elif member_value == 2:
      keyboard_all = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
      keyboard_all.add(SSPoll_button, Help_button)
    elif member_value == 3:
      keyboard_all = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
      keyboard_all.add(Help_button)
    else:
      keyboard_all = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
      keyboard_all.add(SSPoll_button, SSChat_button, Help_button)
      
  welcome_text = 'Hello! I’m the Survey Squad Bot 😊\nPlease send me a poll and I’ll handle the rest!'
  explain_text = 'I’m specifically looking for polls that stem from real-life discussions in which there are differing opinions without a way to figure out what the majority opinion is.'
  bot.send_message(message.chat.id, welcome_text, reply_markup=keyboard_all, disable_notification=True)
  bot.send_message(message.chat.id, explain_text, reply_markup=keyboard_all, disable_notification=True)

# Define message handler
# It will respond to text that matches what is sent by the user persistent keyboard
@bot.message_handler(func=lambda message:True)
def send_links(message):
  from_user_name = message.from_user.username
  from_first_name = message.from_user.first_name
  from_last_name = message.from_user.last_name
  from_full_name = f'{from_first_name} {from_last_name}'
  SSPoll_value = 0
  SSChat_value = 0
  
  if message.chat.type == 'private':
    SSPoll_member = bot.get_chat_member(SSPoll_id, message.chat.id)
    SSChat_member = bot.get_chat_member(SSChat_id, message.chat.id)
    if SSPoll_member.status == 'member':
      SSPoll_value = 1
    if SSChat_member.status == 'member':
      SSChat_value = 2
    member_value = SSPoll_value+SSChat_value
    if member_value == 0:
      keyboard_all = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
      keyboard_all.add(SSPoll_button, SSChat_button, Help_button)
    elif member_value == 1:
      keyboard_all = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
      keyboard_all.add(SSChat_button, Help_button)
    elif member_value == 2:
      keyboard_all = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
      keyboard_all.add(SSPoll_button, Help_button)
    elif member_value == 3:
      keyboard_all = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
      keyboard_all.add(Help_button)
    else:
      keyboard_all = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
      keyboard_all.add(SSPoll_button, SSChat_button, Help_button)
      
  if message.text == SSPoll_invite:
    if message.chat.type == 'private':
      chat_member = bot.get_chat_member(SSPoll_id, message.chat.id)
      if chat_member.status == 'member':
        bot.send_message(message.chat.id, 'You are already a member of Survey Squad: Polls.', reply_markup=keyboard_all, disable_notification=True)
        print(f'@{from_user_name}, {from_full_name} has asked for the SSPoll link but is already a member. time: {time_string}')
      else:
        bot.send_message(message.chat.id, "Here is the invite link you requested: https://t.me/+W9PboT-LL4pkOWEx", reply_markup=keyboard_all, disable_notification=True)
        print(f'@{from_user_name}, {from_full_name} has asked for the SSPoll link. time: {time_string}')
  elif message.text == SSChat_invite:
    if message.chat.type == 'private':
      chat_member = bot.get_chat_member(SSChat_id, message.chat.id)
      if chat_member.status == 'member':
        bot.send_message(message.chat.id, "You are already a member of Survey Squad: Chat.", reply_markup=keyboard_all, disable_notification=True)
        print(f'@{from_user_name}, {from_full_name} has asked for the SSChat link but is already a member. time: {time_string}')
      else:
        bot.send_message(message.chat.id, "Here is the invite link you requested: https://t.me/+cMuAaHhP7jo3MjFh", reply_markup=keyboard_all, disable_notification=True)
        print(f'@{from_user_name}, {from_full_name} has asked for the SSChat link. time: {time_string}')
  elif message.text == Help_text:
    help_reply = 'You’ll need to create the poll right here in the chat with me.\n\nTo begin creating a poll on a mobile device, tap the paperclip icon next to the message bar then tap "Poll".\n\nOn the desktop client, click the kebab (vertical dots) menu at the top right then click "create poll".\n\nPolls are anonymous by default but it’s usually more fun to have the votes be publicly visible. You can set the votes to public by toggling "Anonymous Voting", which is located below your answer options when creating a poll.'
    bot.send_message(message.chat.id, help_reply, reply_markup=keyboard_all, disable_notification=True)
    print(f'@{from_user_name}, {from_full_name} has asked for help sending a poll. time: {time_string}')
  else:
    # rejects every other text message
    bot.reply_to(message, "My apologies, I don’t understand. Please send me a poll or use one of buttons below.", reply_markup=keyboard_all, disable_notification=True)
    print(f'@{from_user_name}, {from_full_name} typed something that wasn’t understood. time: {time_string}')


# Define photo handler
# It will reject all messages that are photos
@bot.message_handler(content_types=['photo'])
def handle_photos(message):
  from_user_name = message.from_user.username
  from_first_name = message.from_user.first_name
  from_last_name = message.from_user.last_name
  from_full_name = f'{from_first_name} {from_last_name}'
  SSPoll_value = 0
  SSChat_value = 0
  
  if message.chat.type == 'private':
    SSPoll_member = bot.get_chat_member(SSPoll_id, message.chat.id)
    SSChat_member = bot.get_chat_member(SSChat_id, message.chat.id)
    if SSPoll_member.status == 'member':
      SSPoll_value = 1
    if SSChat_member.status == 'member':
      SSChat_value = 2
    member_value = SSPoll_value+SSChat_value
    if member_value == 0:
      keyboard_all = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
      keyboard_all.add(SSPoll_button, SSChat_button, Help_button)
    elif member_value == 1:
      keyboard_all = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
      keyboard_all.add(SSChat_button, Help_button)
    elif member_value == 2:
      keyboard_all = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
      keyboard_all.add(SSPoll_button, Help_button)
    elif member_value == 3:
      keyboard_all = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
      keyboard_all.add(Help_button)
    else:
      keyboard_all = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
      keyboard_all.add(SSPoll_button, SSChat_button, Help_button)

  bot.reply_to(message, "My apologies, I don’t accept images. Please send me a poll or use one of buttons below.", reply_markup=keyboard_all, disable_notification=True)
  print(f'@{from_user_name}, {from_full_name} sent an image. time: {time_string}')


# Define poll message handler
@bot.message_handler(content_types=['poll'])
def handle_poll(message):
  # Get user information
  from_user_name = message.from_user.username
  from_first_name = message.from_user.first_name
  from_last_name = message.from_user.last_name
  from_full_name = f'{from_first_name} {from_last_name}'
  from_chatid = message.chat.id
  SSPoll_value = 0
  SSChat_value = 0
  if message.chat.type == 'private':
    SSPoll_member = bot.get_chat_member(SSPoll_id, message.chat.id)
    SSChat_member = bot.get_chat_member(SSChat_id, message.chat.id)
    if SSPoll_member.status == 'member':
      SSPoll_value = 1
    if SSChat_member.status == 'member':
      SSChat_value = 2
    member_value = SSPoll_value+SSChat_value
    if member_value == 0:
      keyboard_all = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
      keyboard_all.add(SSPoll_button, SSChat_button, Help_button)
    elif member_value == 1:
      keyboard_all = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
      keyboard_all.add(SSChat_button, Help_button)
    elif member_value == 2:
      keyboard_all = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
      keyboard_all.add(SSPoll_button, Help_button)
    elif member_value == 3:
      keyboard_all = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
      keyboard_all.add(Help_button)
    else:
      keyboard_all = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
      keyboard_all.add(SSPoll_button, SSChat_button, Help_button)
      
    # Extract the poll from the message
    poll = message.poll
  
    # Create a new poll object with the same settings as the original poll
    new_poll = Poll(id=poll.id, question=poll.question, options=poll.options, allows_multiple_answers=poll.allows_multiple_answers, is_anonymous=poll.is_anonymous, type=poll.type, correct_option_id=poll.correct_option_id, explanation=poll.explanation)

    # Forward poll to admin chat for approval
    sent_poll = bot.forward_message(SSReview_id, from_chatid, message.message_id)

    # Check if they are part of the "Survey Squad: Polls" group
    if message.chat.type == 'private':
      chat_member = bot.get_chat_member(SSPoll_id, from_chatid)
      if chat_member.status == 'member':
        # user is in "Survey Squad: Polls" group, let them know the admins are reviewing the poll
        bot.send_message(from_chatid, "Thank you for your submission, your poll has been sent to the admins for review. I’ll get back to you when a decision has been made.", reply_markup=keyboard_all, disable_notification=True)
      else:
        bot.send_message(from_chatid, "Thank you for your submission, your poll has been sent to the admins for review. I’ll get back to you when a decision has been made.\n\nIn the mean time, you’ll need to join the group *Survey Squad: Polls* so you can can see your poll and participate in voting. Here is the invite link to that group: https://t.me/+W9PboT-LL4pkOWEx", parse_mode='Markdown', reply_markup=keyboard_all, disable_notification=True)
    
    # Send an message to the admin chat that will actually handle the approval
    approval_message = f'Poll from @{from_user_name}, {from_full_name}\n\n{new_poll.question}'
    sent_message = bot.send_message(chat_id=SSReview_id, text=approval_message, reply_markup=approval_keyboard)

    # Store information about these messages in the dictionary
    pending_user[sent_message.message_id] = {'original_user': from_chatid, 'original_username': from_full_name}
    pending_messages[sent_message.message_id] = {'original_message': message}
    pending_polls[sent_message.message_id] = {'original_poll': new_poll}
    pending_polls_id[sent_message.message_id] = {'original_id': sent_poll.message_id}



# Define callback query handler
@bot.callback_query_handler(func=lambda query: True)
def handle_callback_query(query):
  # Get the message ID and callback data from the callback query
  message_id = query.message.message_id
  admin_poll_id = pending_polls_id[message_id]['original_id']
  userchat_id = pending_user[message_id]['original_user']
  userchat_name = pending_user[message_id]['original_username']
  poll_id = pending_polls[message_id]['original_poll']
  callback_data = query.data
  SSPoll_value = 0
  SSChat_value = 0
  
  SSPoll_member = bot.get_chat_member(SSPoll_id, userchat_id)
  SSChat_member = bot.get_chat_member(SSChat_id, userchat_id)
  if SSPoll_member.status == 'member':
    SSPoll_value = 1
  else:
    pass
  if SSChat_member.status == 'member':
    SSChat_value = 2
  else:
    pass
  member_value = SSPoll_value+SSChat_value
  if member_value == 0:
    keyboard_all = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    keyboard_all.add(SSPoll_button, SSChat_button, Help_button)
  elif member_value == 1:
    keyboard_all = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    keyboard_all.add(SSChat_button, Help_button)
  elif member_value == 2:
    keyboard_all = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    keyboard_all.add(SSPoll_button, Help_button)
  elif member_value == 3:
    keyboard_all = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    keyboard_all.add(Help_button)
  else:
    keyboard_all = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    keyboard_all.add(SSPoll_button, SSChat_button, Help_button)
  
    
    # If the callback data is 'approve', send the original message to the channel and delete the approval message
  if callback_data == 'approve':
        bot.answer_callback_query(callback_query_id=query.id, text='You’ve approved the poll')

        # Create poll in SSPolls
        final_poll = bot.send_poll(SSPoll_id, question=poll_id.question, options=poll_id.options, allows_multiple_answers=poll_id.allows_multiple_answers, is_anonymous=poll_id.is_anonymous, type=poll_id.type, correct_option_id=poll_id.correct_option_id, explanation=poll_id.explanation)

        # Forward poll from SSPolls to SSChat
        # Disabled for now as I didn't end up liking it being sent in two places at once
        # bot.forward_message(SSChat_id, SSPoll_id, final_poll.message_id, disable_notification=True)

        # Create a link to the message
        poll_link = f"https://t.me/c/{SSPoll_link}/{final_poll.message_id}"

        # Send link to the SSChat
        #bot.send_message(SSPoll_id, f'Chat for the above poll is here:\n{chat_link}')
      
        # Send the link to the user and admins
        bot.send_message(userchat_id, f'Congratulations! Your poll "{poll_id.question}" was approved and is available here:\n{poll_link}', reply_markup=keyboard_all, disable_notification=True)
        bot.send_message(SSReview_id, f'{userchat_name}’s poll "{poll_id.question}" was approved and is available here:\n{poll_link}', disable_notification=True)

        # Delete messages in admin approval channel
        bot.delete_message(chat_id=query.message.chat.id, message_id=query.message.message_id)
        bot.delete_message(SSReview_id, admin_poll_id)
        del pending_polls[message_id]
        del pending_messages[message_id]
        del pending_polls_id[message_id]
        del pending_user[message_id]
      
    # If the callback data is 'reject', delete the approval message and notify the user that their message was rejected
  elif callback_data == 'reject':
        
        bot.answer_callback_query(callback_query_id=query.id, text='You\'ve rejected the poll')
      
        # Let the user know their poll was rejected
        bot.send_message(userchat_id, f'Unfortunately, your poll "{poll_id.question}" has been rejected.\n\nI don’t know the reason, but you can reach out to @SuspiciousYouth for details.', reply_markup=keyboard_all, disable_notification=True)

        # Mark it in the review chat that it was rejected
        bot.send_message(SSReview_id, text=f'{userchat_name}’s poll "{poll_id.question}" was rejected', disable_notification=True)

        # Delete messages in admin approval channel
        bot.delete_message(query.message.chat.id, query.message.message_id)
        del pending_polls[message_id]
        del pending_messages[message_id]
        del pending_polls_id[message_id]
        del pending_user[message_id]

# start the bot
bot.polling()
