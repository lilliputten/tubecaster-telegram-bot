# import telebot
# from telebot import custom_filters, types
from telebot.states import State, StatesGroup

# from telebot.states.sync.context import StateContext
# from telebot.storage import StateMemoryStorage
# from telebot.types import ReplyParameters

# state_storage = StateMemoryStorage()  # don't use this in production; switch to redis
# bot = telebot.TeleBot("TOKEN", state_storage=state_storage, use_class_middlewares=True)


# Define states
class BotStates(StatesGroup):
    waitForCastUrl = State()
    waitForInfoUrl = State()
    waitForRegistrationInfo = State()
