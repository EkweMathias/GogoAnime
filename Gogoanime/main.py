from gogoanime_script.search import Anime

with Anime() as bot:
    bot.load_main_page()
    bot.search()