import yaml

daytime = ("Morning", "Day", "Evening", "Night")
characters = yaml.load(open("static/scripts/characters.yml", "r", encoding="utf-8"), Loader=yaml.FullLoader)