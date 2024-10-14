import chainlit as cl
import random

async def select_starter() -> list[cl.Starter]:
    """
    Returns a random set of starter prompts to enhance user engagement.

    Prompts are selected from four predefined categories: 
    Wikipedia topics, URLs for scraping, search queries, and image generation requests. 

    Returns:
        list: A list of starter objects, each containing.
    """
    wikipedia_options = [
        "Wikipedia: vietnam war",
        "Wikipedia: openai",
        "Wikipedia: boston celtics",
        "Wikipedia: israeli war",
        "Wikipedia: artificial intelligence",
        "Wikipedia: solar energy",
        "Wikipedia: renaissance art",
        "Wikipedia: world war II",
        "Wikipedia: quantum computing",
        "Wikipedia: climate change"
    ]

    scraper_options = [
        "https://www.fox.com",
        "https://www.cbc.ca",
        "https://www.mtv.com",
        "https://www.espn.com",
        "https://www.npr.org",
        "https://www.abc.com",
        "https://www.tbs.com",
        "https://www.bet.com",
        "https://www.tlc.com",
        "https://www.vice.com"
    ]

    search_options = [
    "Find the latest updates on the global energy crisis.",
    "Search for news about the US presidential elections.",
    "Look for news on the volcanic eruption in Hawaii.",
    "Find out the most important news of the day.",
    "Look for news on the discovery of new animal species.",
    "Find news about the latest G7 summit.",
    "Look for updates on Hollywood's film industry.",
    "Find information on social protests in France.",
    "Search for news on advancements in nuclear fusion.",
    "Find the latest news on the stock market.",
    ]

    generate_image_options = [
    "An immagine of a tranquil forest clearing with sunlight streaming through the tall pine trees, casting soft shadows on a bed of wildflowers.",
    "An immagine of a futuristic cityscape at night, with towering skyscrapers covered in neon lights and flying cars zooming between them.",
    "An immagine of a majestic dragon perched on a mountain peak, with its wings spread wide against a bright orange sunset.",
    "An immagine of a cozy village in winter, with snow-covered roofs, smoke rising from chimneys, and people in warm clothes walking around.",
    "An immagine of an underwater scene with colorful coral reefs, schools of fish, and a diver exploring the area with a flashlight.",
    "An immagine of a medieval knight in full armor, standing at the edge of a cliff, looking out over a vast green valley.",
    "An immagine of an enchanted library with floating books, glowing lanterns, and an old wizard reading in a large armchair.",
    "An immagine of a bustling marketplace in an ancient Middle Eastern city, with vibrant stalls, merchants selling spices, and people in traditional clothing.",
    "An immagine of a serene Japanese garden at dusk, with a red wooden bridge, a koi pond, and cherry blossoms falling from the trees.",
    "An immagine of a whimsical steampunk airship floating above the clouds, with brass gears, large sails, and a crew of adventurers on deck."
    ]
    
    random_starters = []

    for options, icon in zip(
        [wikipedia_options, scraper_options, search_options, generate_image_options],
        ["/public/starters/search-wikipedia.svg", 
         "/public/starters/scrape-links.svg", 
         "/public/starters/duckduckgo.svg", 
         "/public/starters/generate-img.svg"]
    ):
        user_choice = random.choice(options)  
        random_starters.append(cl.Starter(
            label=user_choice,
            message=user_choice,
            icon=icon,
        ))

    return random_starters
