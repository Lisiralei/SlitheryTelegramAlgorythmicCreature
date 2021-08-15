import telebot
import Asta
import Alg17
import bottoken

slitherbot = telebot.TeleBot(bottoken.telegramtoken)


def check_user_input_for_two_ints(input):
    try:
        # Convert it into integer
        val1, val2 = (int(s) for s in input.split())
        return True
    except ValueError:
        return False


@slitherbot.message_handler(content_types=['text'])
def start(message):
    if message.text == "/start":
        slitherbot.send_message(message.from_user.id, "Welcome.\nPlease, select a width and length for the playing field (the messages only fit about 10 units wide)")
        slitherbot.register_next_step_handler(message, getfieldparam)
    else:
        slitherbot.send_message(message.from_user.id, "To start the algorhythm, write /start")
        slitherbot.register_next_step_handler(message, start)

def getfieldparam(message):
    global n
    global m
    global field
    if check_user_input_for_two_ints(message.text):
        n, m = (int(s) for s in message.text.split())
        field = Alg17.rookmechanics(n, m)
    else:
        slitherbot.send_message(message.from_user.id, "Please input 2 numbers")
        slitherbot.register_next_step_handler(message, getfieldparam)
        return
    slitherbot.send_message(message.from_user.id, Asta.draw_grid(field))
    slitherbot.send_message(message.from_user.id, "Now please input the X and Y coordinates of the start point")
    slitherbot.register_next_step_handler(message, getstartpoint)

def getstartpoint(message):
    global strt
    strt = [0, 0]
    if check_user_input_for_two_ints(message.text):
        strt[0], strt[1] = (int(s) for s in message.text.split())
        strt = tuple(strt)
    else:
        slitherbot.send_message(message.from_user.id, "Please input 2 numbers")
        slitherbot.register_next_step_handler(message, getstartpoint)
        return
    if strt in field.walls:
        field.walls.remove(strt)
    slitherbot.send_message(message.from_user.id, "Now please input the X and Y coordinates of the end point")
    slitherbot.register_next_step_handler(message, getendpoint)


def getendpoint(message):
    global endpt
    endpt = [0, 0]
    if check_user_input_for_two_ints(message.text):
        endpt[0], endpt[1] = (int(s) for s in message.text.split())
        endpt = tuple(endpt)
    else:
        slitherbot.send_message(message.from_user.id, "Please input 2 numbers")
        slitherbot.register_next_step_handler(message, getendpoint)
        return
    if endpt in field.walls:
        field.walls.remove(endpt)
    slitherbot.send_message(message.from_user.id, Asta.draw_grid(field, start = strt, goal = endpt))
    slitherbot.send_message(message.from_user.id, "Building a path...")
    came_from, cost_so = Asta.a_star_search(field, strt, endpt)
    thispath = Asta.reconstruct_path(came_from, strt, endpt)
    astraightpath = Asta.reconstruct_path(came_from, strt, endpt)
    astraightpath = Alg17.straightener(astraightpath)
    slitherbot.send_message(message.from_user.id, Asta.draw_grid(field, path = thispath, start = strt, goal = endpt) + Alg17.pathteller(astraightpath))
    slitherbot.register_next_step_handler(message, start)


slitherbot.polling(none_stop=True, interval=0)
