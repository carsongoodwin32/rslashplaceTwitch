from twitchAPI import Twitch
from twitchAPI.oauth import UserAuthenticator
from twitchAPI.types import AuthScope, ChatEvent
from twitchAPI.chat import Chat, EventData, ChatMessage, ChatSub, ChatCommand
import asyncio, csv

APP_ID = ''
APP_SECRET = ''
USER_SCOPE = [AuthScope.CHAT_READ, AuthScope.CHAT_EDIT]
TARGET_CHANNEL = ''
CSV_FILENAME = "commandstream.csv"


# this will be called when the event READY is triggered, which will be on bot start
async def on_ready(ready_event: EventData):
    print('Bot is ready for work, joining channels')
    # join our target channel, if you want to join multiple, either call join for each individually
    # or even better pass a list of channels as the argument
    await ready_event.chat.join_room(TARGET_CHANNEL)
    # you can do other bot initialization things in here


# # this will be called whenever a message in a channel was send by either the bot OR another user
# async def on_message(msg: ChatMessage):
#     print(f'in {msg.room.name}, {msg.user.name} said: {msg.text}')


# # this will be called whenever someone subscribes to a channel
# async def on_sub(sub: ChatSub):
#     print(f'New subscription in {sub.room.name}:\\n'
#           f'  Type: {sub.sub_plan}\\n'
#           f'  Message: {sub.sub_message}')


# this will be called whenever the !reply command is issued
async def test_command(cmd: ChatCommand):
    if len(cmd.parameter) == 0:
        await cmd.reply('you did not tell me what to reply with')
    else:
        await cmd.reply(f'{cmd.user.name}: {cmd.parameter}')

async def test_command2(cmd: ChatCommand):
    try:
        # Split the command into x, y, r, g, and b values
        x, y, r, g, b = map(int, cmd.parameter.split(','))

        # Check if x and y are within the valid range (0-100)
        if 0 <= x <= 100 and 0 <= y <= 100:
            # Check if r, g, and b are within the valid range (0-255)
            if 0 <= r <= 255 and 0 <= g <= 255 and 0 <= b <= 255:
                # Append the new color data to the CSV file
                with open(CSV_FILENAME, mode="a", newline="") as csv_file:
                    csv_writer = csv.writer(csv_file)
                    csv_writer.writerow([x, y, r, g, b])
                await cmd.reply(f"Added ({x},{y}): ({r},{g},{b}) to {CSV_FILENAME}")
            else:
                await cmd.reply("Invalid color values. Use values between 0 and 255.")
        else:
            await cmd.reply("Invalid x or y values. Use values between 0 and 100.")
    except ValueError:
        await cmd.reply("Invalid command format. Use 'x,y,r,g,b' (e.g., '10,20,255,0,0').")




# this is where we set up the bot
async def run():
    # set up twitch api instance and add user authentication with some scopes
    twitch = await Twitch(APP_ID, APP_SECRET)
    auth = UserAuthenticator(twitch, USER_SCOPE)
    token, refresh_token = await auth.authenticate()
    await twitch.set_user_authentication(token, USER_SCOPE, refresh_token)

    # create chat instance
    chat = await Chat(twitch)

    # register the handlers for the events you want

    # listen to when the bot is done starting up and ready to join channels
    chat.register_event(ChatEvent.READY, on_ready)
    # # listen to chat messages
    # chat.register_event(ChatEvent.MESSAGE, on_message)
    # # listen to channel subscriptions
    # chat.register_event(ChatEvent.SUB, on_sub)
    # there are more events, you can view them all in this documentation

    # you can directly register commands and their handlers, this will register the !reply command
    chat.register_command('reply', test_command)
    chat.register_command('place', test_command2)


    # we are done with our setup, lets start this bot up!
    chat.start()

    # lets run till we press enter in the console
    try:
        input('press ENTER to stop\\n')
    finally:
        # now we can close the chat bot and the twitch api client
        chat.stop()
        await twitch.close()


# lets run our setup
asyncio.run(run())