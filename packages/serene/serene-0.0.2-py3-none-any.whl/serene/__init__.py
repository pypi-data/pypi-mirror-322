import random

FLIRTY_MESSAGES = [
    "Your smile lights up my entire day.",
    "Is your name Google? Because you've got everything I've been searching for.",
    "Do you believe in love at first sight, or should I walk by again?",
    "Are you a magician? Because whenever I look at you, everyone else disappears.",
    "If you were a vegetable, you'd be a cute-cumber.",
    "Are you a camera? Because every time I look at you, I smile.",
    "Do you have a map? I keep getting lost in your eyes.",
    "Is your name WiFi? Because I'm really feeling a connection.",
    "You must be tired because you've been running through my mind all day.",
    "If you were a cat, you'd purr-fectly complete my life.",
    "Are you a parking ticket? Because you've got FINE written all over you.",
    "Do you like science? Because I've got my ion you.",
    "Is your name Spotify? Because you're the hottest single around.",
    "Are you French? Because Eiffel for you.",
    "If you were words on a page, you'd be fine print.",
    "Do you like math? Because you're adding joy to my life.",
    "Is this the Hogwarts Express? Because platform 9¾ isn't the only thing making me crash into walls.",
    "Are you a campfire? Because you are hot and I want s'more.",
    "If you were a fruit, you'd be a fine-apple.",
    "Do you play soccer? Because you're a keeper!"
]

def flirtysays():
    """
    Returns a random flirty message from a preset list of messages.
    
    Returns:
        str: A random flirty message
    """
    return random.choice(FLIRTY_MESSAGES)


