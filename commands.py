import datetime
import discord
import json
import sys
import urllib
from search import search
from tcgplayerinfo import Item

async def bot_help(msg, cmd):
    await msg.channel.send("**tcg.search <search term> --optional arguments**" +
                           "\n`tcg.search Gulpin" +
                           "\ntcg.search 37mm ATG --category Axis & Allies" +
                           "\ntcg.search The Scarab God --category Magic`" +
                           "\noptional arguments:" +
                           "\n\tcategory: What is the item from? Makes the search much faster. Ex:" +
                           "\n\t\t`--category Magic` `--category Pokemon` `--category Funko`")

async def bot_die(msg, cmd):
    if msg.author.id == 498241529304055818:
        sys.exit(0)

async def bot_search(msg, cmd):
    # Hackathons aren't about good code, they're about having a working presentation.
    # Therefore, this code is good.
    if len(cmd) == 1:
        await msg.channel.send("{0.author.mention} You must provite a valid search term!")
        return

    search_term = cmd[1]
    if search_term.startswith("--"):
        await msg.channel.send("{0.author.mention} You must provide a valid search term"
                               + " before adding optional arguments!")
        return

    end_of_search_term = False
    search_term = ""
    filter = ""
    filters = dict()
    for c in cmd[1:]:
        if c.startswith("--"):
            end_of_search_term = True

            filter = c[2:]
            filters[filter] = ""
        else:
            if not end_of_search_term:
                search_term += c + " "
            else:
                filters[filter] += c + " "
    for key in filters:
        filters[key] = filters[key].rstrip()
    search_term = search_term.rstrip()
    if "category" in filters.keys():
        category = filters["category"]
    else:
        category = ""

    with open("./keys.json") as f:
        keys = json.load(f)

    ids, found_in_cat = search(keys["tcgplayer"]["bearer"], search_term, category)
    items = []
    for id in ids:
        items.append(Item(keys["tcgplayer"]["bearer"], id))

    if len(items) == 0:
        await msg.channel.send("{0.author.mention} Nothing was found for your search!".format(msg))
        return


    catalog_url = "https://shop.tcgplayer.com/{0}/product/show?ProductName={1}"
    url_search = urllib.parse.quote_plus(search_term)
    if not found_in_cat:
        url_category = "productcatalog"
    else:
        url_category = category.replace(" ", "-")
        url_category = url_category.replace("&", "and")
        url_category = url_category.lower()
    tcgp_url = catalog_url.format(url_category, url_search)

    url_template = "[{0.product_name}]({0.product_URL})"
    related = ""
    if len(items) > 1:
        for i in items[1:]:
            if len(related + url_template.format(i) + "\n") > 1024:
                break
            related += url_template.format(i) + "\n"
    else:
        related = "Sorry, but this was all that we could find!"

    embed = discord.Embed(colour=discord.Colour(0xA9A9A9),
                          timestamp=items[0].modified_date)

    embed.set_image(url=items[0].image_url)
    embed.set_thumbnail(url="https://www.tcgplayer.com/Content/images/tcgplayer-logo-color_320x120.png")
    embed.set_footer(text="Last modified on:")

    embed.add_field(name="First Result", value=url_template.format(items[0]), inline=True)
    embed.add_field(name="Input", value="`{0}\n{1}`".format(search_term, filters), inline=True)
    embed.add_field(name="Other Results", value=related, inline=True)
    embed.add_field(name="TCGPlayer", value="[More results!]({0})".format(tcgp_url))

    await msg.channel.send(embed=embed)

async def bot_categories(msg, cmd):
    cat_array = []
    with open('cats.json') as cat_file:
        categories = json.loads(cat_file.read())
        cat_array = [key for key in categories]
    reply = "`{0}`".format("\n".join(cat_array))
    await msg.channel.send(reply)

commands = {"help":bot_help, "die":bot_die, "search":bot_search, "categories":bot_categories}
