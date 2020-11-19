import droit, logging, json
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler


# Get configuration from config.json
with open("data/config.json") as f:
	config = json.load(f)

if(config["logging"]):
	logging.basicConfig(filename="data/telepyd.log", format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
	logger = logging.getLogger(__name__)


# Initialize database object
db = droit.Database(multiSession=True)
db.loadPlugins()									# Load native plugins
db.loadPlugins(location="droit-plugins-telegram")	# Load telegram plugins
db.parseScript(config["database"])					# Parse Droit Database Script file

db.sessions.path = "data/sessions.json"
db.sessions.loadSessions()
db.sessions.droitname = config["botname"]

db.temp["cmd"] = False
db.temp["inline"] = None
db.temp["callback"] = False


def cmdCallback(update, context):
	db.temp["cmd"] = True
	echo(update, context)

def cbCallback(update, context):
	db.temp["callback"] = update.callback_query.data
	echo(update, context)

def echo(update, context):
	rawText = ""
	if not(db.temp["callback"]):
		rawText = update.message.text
	userinput = droit.models.DroitUserinput(rawText)

	if(db.temp["callback"]):
		userFirstName = update.callback_query.message.chat.first_name
		userId = update.callback_query.message.chat.id
	else:
		userFirstName = update.message.from_user.first_name
		userId = update.message.from_user.id

	# Activate previous session / create new session
	if(db.sessions.activateById(userId)):
		if not("customUsername" in db.sessions.getActive().userData.keys()):
			db.sessions.sessions[db.sessions.active].username = userFirstName
		elif not(db.sessions.getActive().userData["customUsername"]):
			db.sessions.sessions[db.sessions.active].username = userFirstName
	else:
		newUser = droit.models.DroitSession(userFirstName, ident=userId)
		db.sessions.sessions.append(newUser)
		db.sessions.activateById(userId)

	hits = db.useRules(userinput)				# Search matching rules for userinput

	if(hits):
		hit = hits[0]
		
		output = db.formatOut(hit, userinput)
		if(db.temp["inline"]):
			update.message.reply_text(output, reply_markup=db.temp["inline"])
		elif(db.temp["callback"]):
			update.callback_query.bot.send_message(chat_id=update.callback_query.message.chat.id, text=output)
			update.callback_query.answer()
		else:
			update.message.reply_text(output)
		db.sessions.active = -1
		db.sessions.saveSessions()

	db.temp["cmd"] = False
	db.temp["inline"] = None
	db.temp["callback"] = False


def error(update, context):
	"""Log errors."""
	if(config["logging"]):
		logger.warning('Update "%s" caused error "%s"', update, context.error)


def registerHandlers(dp, rules):
	handlers = []
	for rule in rules:
		for subrule in rule.input:
			if(subrule.tag == "TELE"):
				if(subrule.attrib["option"] == "cmd"):
					chld = " ".join(subrule.children)
					if not(chld in handlers):
						handlers.append(chld)
						dp.add_handler(CommandHandler(chld, cmdCallback))
	return dp



def main():
	"""Start the bot."""
	updater = Updater(token=config["token"], use_context=True)
	
	dp = updater.dispatcher

	dp = registerHandlers(dp, db.rules)
	dp.add_handler(CallbackQueryHandler(cbCallback))
	dp.add_handler(MessageHandler(Filters.text, echo))
	dp.add_error_handler(error)

	updater.start_polling()

	updater.idle()


if __name__ == '__main__':
	main()