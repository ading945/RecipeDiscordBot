
import recipes
import discord
import os
import requests
import json
import random
from discord.ext import commands

client = commands.Bot(command_prefix="$")
#client = discord.Client()
@client.event
async def on_ready():
    print('ladies and geltamninnn we have logged in as {0.user}'.format(client))

class SearchRecipe():
  def __init__(self):
    self.uinput = ""
    self.flag = 0
    self.datafound = []

  def recipename(self):
    #self.uinput = simpledialog.askstring(title="Recipe grabber", prompt="Input a recipe name keyword")
   
    with open('JamieOliver.txt', "r") as fh:
      recipes = json.load(fh)
      #for key, values in recipes.items():
      for recipe in recipes:
        name = recipe.get("recipe_name", [])
        ingredients = "\n".join(recipe.get("ingredients"))
        if self.uinput.lower() in name.lower():
          self.datafound.append(f"{name}: \n {ingredients} \n")
          
    self.flag = 1 

  def search_for_recipe(self, uinput):
    with open('JamieOliver.txt', "r") as fh:
      recipes = json.load(fh)
      #for key, values in recipes.items():
      for recipe in recipes:
        ingredients = recipe.get("ingredients", [])
        for ingredient in ingredients:
          if uinput in ingredient:
            self.datafound.append(recipe.get("link"))
            break
    self.flag = 1
    #self.window.quit()
    



def main():
  do_download = input("Should I download recipes fromn the website again? THIS WILL TAKE AT LEAST \n5 MINUTES (This is not neccassary for the project to run) Y/N: ")
  if do_download.lower() == "y":
    with open('JamieOliver.txt', "w") as fh:
      fh.write("")
    recipes.write_data_file()
 
  @client.event
  async def on_message(message):
    author = message.author
    content = message.content
    print('{}:{}'.format(author,content))

    if message.author == client.user:
        return
    if message.content.startswith('$recipe'):    
        x = SearchRecipe()
       
        channel = message.channel
        await channel.send('Input an ingredient')

        def check(m):
            return m.content != None and m.channel == channel

        msg = await client.wait_for('message', check=check)
        x.search_for_recipe(msg.content)
        if x.flag == 1:
          embed=discord.Embed(title="Recipe", description="Here is a random list of recipes with " + msg.content, color=0xFF5733)
          for i in range(10):
            embed.add_field(name="Recipe link", value= f"{(x.datafound[random.randrange(0,(len(x.datafound)))])}")
          await message.channel.send(embed=embed)
@client.command()
async def message(ctx, user:discord.Member, *, message=None):
  message = "test"
  embed = discord.Embed(title=message)
  await user.send(embed=embed)  

client.run('ODIyOTI3NDY3NjIyNDMyODE5.YFZY7Q.xVqmptE0RLOtfFzZWA2772xV8yE')

if __name__=="__main__":
 
  main()
