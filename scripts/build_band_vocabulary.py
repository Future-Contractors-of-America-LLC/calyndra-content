#!/usr/bin/env python3

"""Build age-band vocabulary JSON with growing word counts and phrase lists."""



from __future__ import annotations



import json

from copy import deepcopy

from pathlib import Path



ROOT = Path(__file__).resolve().parents[1]

APP_CONTENT = ROOT.parent / "calyndra-app" / "content"

VOCAB = ROOT / "vocabulary"



BAND_DIR = {

    "baby": "seed",

    "toddler": "sprout",

    "child": "bud",

    "tween": "sprig",

    "teen": "vine",

    "adult": "bloom",

    "caregiver": "canopy",

}



WORD_TARGETS = {

    "baby": 45,

    "toddler": 78,

    "child": 110,

    "tween": 172,

    "teen": 215,

    "adult": 215,

    "caregiver": 48,

}



PHRASE_TARGETS = {

    "baby": 12,

    "toddler": 20,

    "child": 22,

    "tween": 18,

    "teen": 18,

    "adult": 14,

    "caregiver": 14,

}



# Symbols not yet in source JSON - minimal stubs for vocabulary growth.

EXTRA_SYMBOLS: dict[str, dict[str, str]] = {

    "hungry": {"label": "hungry", "category": "routine"},

    "thirsty": {"label": "thirsty", "category": "routine"},

    "bye": {"label": "bye", "category": "social"},

    "hi": {"label": "hi", "category": "social"},

    "night": {"label": "night", "category": "routine"},

    "gentle": {"label": "gentle", "category": "social"},

    "pacifier": {"label": "pacifier", "category": "routine"},

    "diaper": {"label": "diaper", "category": "routine"},

    "bottle": {"label": "bottle", "category": "routine"},

    "brush-teeth": {"label": "brush teeth", "category": "routine"},

    "teeth": {"label": "teeth", "category": "routine"},

    "sock": {"label": "sock", "category": "routine"},

    "shirt": {"label": "shirt", "category": "routine"},

    "pants": {"label": "pants", "category": "routine"},

    "favorite": {"label": "favorite", "category": "preferences"},

    "weather": {"label": "weather", "category": "core"},

    "storm": {"label": "storm", "category": "sensory"},

    "library": {"label": "library", "category": "places"},

    "homework": {"label": "homework", "category": "school"},

    "insurance": {"label": "insurance", "category": "functional"},

    "pharmacy": {"label": "pharmacy", "category": "health"},

    "therapist": {"label": "therapist", "category": "health"},

    "counselor": {"label": "counselor", "category": "health"},

    "wifi": {"label": "wifi", "category": "functional"},

    "password": {"label": "password", "category": "functional"},

    "bank": {"label": "bank", "category": "functional"},

    "rent": {"label": "rent", "category": "functional"},

    "invoice": {"label": "invoice", "category": "functional"},

    "extension": {"label": "extension", "category": "work"},

    "rattle": {"label": "rattle", "category": "nursery"},

    "bib": {"label": "bib", "category": "nursery"},

    "stroller": {"label": "stroller", "category": "nursery"},

    "spoon": {"label": "spoon", "category": "routine"},

    "banana": {"label": "banana", "category": "food"},

    "duck": {"label": "duck", "category": "animals"},

    "star": {"label": "star", "category": "nursery"},

    "moon": {"label": "moon", "category": "nursery"},

    "sun": {"label": "sun", "category": "nursery"},

    "bear": {"label": "bear", "category": "animals"},

    "bunny": {"label": "bunny", "category": "animals"},

    "tickle": {"label": "tickle", "category": "social"},

    "snack": {"label": "snack", "category": "food"},

    "playground": {"label": "playground", "category": "places"},

    "crayon": {"label": "crayon", "category": "activities"},

    "swing": {"label": "swing", "category": "activities"},

    "slide": {"label": "slide", "category": "activities"},

    "rain": {"label": "rain", "category": "weather"},

    "snow": {"label": "snow", "category": "weather"},

    "hat": {"label": "hat", "category": "routine"},

    "coat": {"label": "coat", "category": "routine"},

    "pencil": {"label": "pencil", "category": "school"},

    "backpack": {"label": "backpack", "category": "school"},

    "lunchbox": {"label": "lunchbox", "category": "school"},

    "recess": {"label": "recess", "category": "school"},

    "cousin": {"label": "cousin", "category": "family"},

    "aunt": {"label": "aunt", "category": "family"},

    "uncle": {"label": "uncle", "category": "family"},

    "neighbor": {"label": "neighbor", "category": "social"},

    "locker": {"label": "locker", "category": "school"},

    "cafeteria": {"label": "cafeteria", "category": "school"},

    "project": {"label": "project", "category": "school"},

    "club": {"label": "club", "category": "activities"},

    "practice": {"label": "practice", "category": "activities"},

    "resume": {"label": "resume", "category": "work"},

    "interview": {"label": "interview", "category": "work"},

    "paycheck": {"label": "paycheck", "category": "functional"},

    "prescription": {"label": "prescription", "category": "health"},

    "refill": {"label": "refill", "category": "health"},

    "landlord": {"label": "landlord", "category": "functional"},

    "lease": {"label": "lease", "category": "functional"},

    "utility": {"label": "utility bill", "category": "functional"},

    "deadline": {"label": "deadline", "category": "work"},

    "feedback": {"label": "feedback", "category": "work"},

    "coworker": {"label": "coworker", "category": "work"},

    "supervisor": {"label": "supervisor", "category": "work"},

}



PHRASES = {

    "baby": [

        {"id": "peek-a-boo", "label": "peek-a-boo", "category": "nursery", "speakText": "Peek-a-boo!"},

        {"id": "night-night", "label": "night night", "category": "nursery", "speakText": "Night night."},

        {"id": "up-up", "label": "up up", "category": "nursery", "speakText": "Up up!"},

        {"id": "all-gone", "label": "all gone", "category": "nursery", "speakText": "All gone!"},

        {"id": "more-milk", "label": "more milk", "category": "nursery", "speakText": "More milk!"},

        {"id": "love-you-baby", "label": "love you", "category": "nursery", "speakText": "Love you!"},

        {"id": "bye-bye", "label": "bye bye", "category": "nursery", "speakText": "Bye bye!"},

        {"id": "gentle-hands", "label": "gentle hands", "category": "nursery", "speakText": "Gentle hands."},

        {"id": "all-better", "label": "all better", "category": "nursery", "speakText": "All better!"},

        {"id": "my-turn-baby", "label": "my turn", "category": "nursery", "speakText": "My turn!"},

        {"id": "so-big", "label": "so big", "category": "nursery", "speakText": "So big!"},

        {"id": "nice-song", "label": "nice song", "category": "nursery", "speakText": "Nice song!"},

    ],

    "toddler": [

        {"id": "more-please", "label": "more please", "category": "core", "speakText": "More please!"},

        {"id": "all-done", "label": "all done", "category": "core", "speakText": "All done!"},

        {"id": "help-me", "label": "help me", "category": "core", "speakText": "Help me!"},

        {"id": "my-turn", "label": "my turn", "category": "social", "speakText": "My turn!"},

        {"id": "go-play", "label": "go play", "category": "activities", "speakText": "Go play!"},

        {"id": "want-that", "label": "I want that", "category": "core", "speakText": "I want that!"},

        {"id": "need-help", "label": "I need help", "category": "core", "speakText": "I need help!"},

        {"id": "look-at", "label": "look at this", "category": "core", "speakText": "Look at this!"},

        {"id": "come-here", "label": "come here", "category": "social", "speakText": "Come here!"},

        {"id": "love-you", "label": "love you", "category": "social", "speakText": "Love you!"},

        {"id": "yucky", "label": "no thank you", "category": "core", "speakText": "No thank you."},

        {"id": "bathroom-please", "label": "bathroom please", "category": "routine", "speakText": "Bathroom please!"},

        {"id": "want-water", "label": "want water", "category": "routine", "speakText": "Want water!"},

        {"id": "not-yet", "label": "not yet", "category": "core", "speakText": "Not yet."},

        {"id": "go-potty", "label": "go potty", "category": "routine", "speakText": "Go potty!"},

        {"id": "hungry-now", "label": "I am hungry", "category": "routine", "speakText": "I am hungry!"},

        {"id": "sing-song", "label": "sing a song", "category": "activities", "speakText": "Sing a song!"},

        {"id": "read-please", "label": "read please", "category": "activities", "speakText": "Read please!"},

        {"id": "my-snack", "label": "my snack", "category": "routine", "speakText": "My snack please!"},

        {"id": "go-outside", "label": "go outside", "category": "activities", "speakText": "Go outside!"},

    ],

    "child": [

        {"id": "can-i-have", "label": "Can I have more?", "category": "core", "speakText": "Can I have more?"},

        {"id": "need-break", "label": "I need a break", "category": "regulation", "speakText": "I need a break."},

        {"id": "thank-you", "label": "Thank you", "category": "social", "speakText": "Thank you!"},

        {"id": "please-help", "label": "Please help me", "category": "core", "speakText": "Please help me."},

        {"id": "where-is", "label": "Where is it?", "category": "questions", "speakText": "Where is it?"},

        {"id": "dont-like", "label": "I don't like that", "category": "preferences", "speakText": "I don't like that."},

        {"id": "my-turn-phrase", "label": "It's my turn", "category": "social", "speakText": "It's my turn!"},

        {"id": "share-please", "label": "Can we share?", "category": "social", "speakText": "Can we share?"},

        {"id": "feel-happy", "label": "I feel happy", "category": "feelings", "speakText": "I feel happy!"},

        {"id": "feel-sad", "label": "I feel sad", "category": "feelings", "speakText": "I feel sad."},

        {"id": "too-loud", "label": "It's too loud", "category": "regulation", "speakText": "It's too loud."},

        {"id": "wait-please", "label": "Wait please", "category": "core", "speakText": "Wait please."},

        {"id": "lets-play", "label": "Let's play", "category": "activities", "speakText": "Let's play!"},

        {"id": "read-book", "label": "Read a book", "category": "activities", "speakText": "Read a book!"},

        {"id": "go-home", "label": "I want to go home", "category": "places", "speakText": "I want to go home."},

        {"id": "can-we-go", "label": "Can we go?", "category": "places", "speakText": "Can we go?"},

        {"id": "i-feel-mad", "label": "I feel mad", "category": "feelings", "speakText": "I feel mad."},

        {"id": "need-quiet", "label": "I need quiet", "category": "regulation", "speakText": "I need quiet."},

        {"id": "good-job", "label": "Good job!", "category": "social", "speakText": "Good job!"},

        {"id": "whats-that", "label": "What's that?", "category": "questions", "speakText": "What's that?"},

        {"id": "can-i-try", "label": "Can I try?", "category": "social", "speakText": "Can I try?"},

        {"id": "i-am-done", "label": "I am done", "category": "core", "speakText": "I am done."},

    ],

    "tween": [

        {"id": "dont-understand", "label": "I don't understand", "category": "core", "speakText": "I don't understand."},

        {"id": "say-again", "label": "Can you say that again?", "category": "core", "speakText": "Can you say that again?"},

        {"id": "need-space", "label": "I need space", "category": "regulation", "speakText": "I need space."},

        {"id": "not-ready", "label": "I'm not ready yet", "category": "core", "speakText": "I'm not ready yet."},

        {"id": "pick-different", "label": "Can we pick something else?", "category": "preferences", "speakText": "Can we pick something else?"},

        {"id": "feel-overwhelmed", "label": "I feel overwhelmed", "category": "feelings", "speakText": "I feel overwhelmed."},

        {"id": "can-we-talk", "label": "Can we talk about it?", "category": "social", "speakText": "Can we talk about it?"},

        {"id": "homework-help", "label": "I need help with homework", "category": "school", "speakText": "I need help with homework."},

        {"id": "join-game", "label": "Can I join the game?", "category": "social", "speakText": "Can I join the game?"},

        {"id": "pass-turn", "label": "I'll pass this turn", "category": "social", "speakText": "I'll pass this turn."},

        {"id": "schedule-change", "label": "The schedule changed", "category": "routine", "speakText": "The schedule changed."},

        {"id": "need-quiet", "label": "I need a quiet place", "category": "regulation", "speakText": "I need a quiet place."},

        {"id": "feel-stressed", "label": "I feel stressed", "category": "feelings", "speakText": "I feel stressed."},

        {"id": "can-i-leave", "label": "Can I leave?", "category": "boundaries", "speakText": "Can I leave?"},

        {"id": "tell-me-more", "label": "Can you tell me more?", "category": "core", "speakText": "Can you tell me more?"},

        {"id": "group-project", "label": "I need help with a group project", "category": "school", "speakText": "I need help with a group project."},

        {"id": "too-much", "label": "This is too much for me", "category": "regulation", "speakText": "This is too much for me."},

        {"id": "need-break-tween", "label": "I need a short break", "category": "regulation", "speakText": "I need a short break."},

    ],

    "teen": [

        {"id": "moment-respond", "label": "I need a moment to respond", "category": "core", "speakText": "I need a moment to respond."},

        {"id": "not-comfortable", "label": "I'm not comfortable with that", "category": "boundaries", "speakText": "I'm not comfortable with that."},

        {"id": "repeat-slower", "label": "Can you repeat that slower?", "category": "core", "speakText": "Can you repeat that slower?"},

        {"id": "clarify", "label": "Can you clarify?", "category": "core", "speakText": "Can you clarify?"},

        {"id": "privacy", "label": "I need privacy", "category": "boundaries", "speakText": "I need privacy."},

        {"id": "consent-no", "label": "I don't consent to that", "category": "boundaries", "speakText": "I don't consent to that."},

        {"id": "running-late", "label": "I'm running late", "category": "functional", "speakText": "I'm running late."},

        {"id": "cancel-plans", "label": "I need to cancel", "category": "functional", "speakText": "I need to cancel."},

        {"id": "feel-anxious", "label": "I feel anxious", "category": "feelings", "speakText": "I feel anxious."},

        {"id": "talk-later", "label": "Can we talk later?", "category": "social", "speakText": "Can we talk later?"},

        {"id": "need-doctor", "label": "I need to see a doctor", "category": "health", "speakText": "I need to see a doctor."},

        {"id": "order-food", "label": "I'd like to order food", "category": "functional", "speakText": "I'd like to order food."},

        {"id": "need-ride", "label": "I need a ride", "category": "functional", "speakText": "I need a ride."},

        {"id": "can-you-text", "label": "Can you text me?", "category": "functional", "speakText": "Can you text me?"},

        {"id": "respect-my-no", "label": "Please respect my no", "category": "boundaries", "speakText": "Please respect my no."},

        {"id": "need-break-teen", "label": "I need a break from this", "category": "regulation", "speakText": "I need a break from this."},

        {"id": "pick-me-up", "label": "Can you pick me up?", "category": "functional", "speakText": "Can you pick me up?"},

        {"id": "running-errands", "label": "I am running errands", "category": "functional", "speakText": "I am running errands."},

    ],

    "adult": [

        {"id": "schedule-meeting", "label": "I'd like to schedule a meeting", "category": "work", "speakText": "I'd like to schedule a meeting."},

        {"id": "need-clarification", "label": "I need clarification", "category": "work", "speakText": "I need clarification."},

        {"id": "follow-up", "label": "I will follow up by email", "category": "work", "speakText": "I will follow up by email."},

        {"id": "running-late-adult", "label": "I'm running late for work", "category": "work", "speakText": "I'm running late for work."},

        {"id": "need-accommodation", "label": "I need an accommodation", "category": "work", "speakText": "I need an accommodation."},

        {"id": "pay-bill", "label": "I need to pay a bill", "category": "functional", "speakText": "I need to pay a bill."},

        {"id": "make-appointment", "label": "I need to make an appointment", "category": "health", "speakText": "I need to make an appointment."},

        {"id": "transport-help", "label": "I need help with transport", "category": "functional", "speakText": "I need help with transport."},

        {"id": "allergy", "label": "I have a food allergy", "category": "health", "speakText": "I have a food allergy."},

        {"id": "repeat-email", "label": "Please repeat that in writing", "category": "core", "speakText": "Please repeat that in writing."},

        {"id": "need-extension", "label": "I need an extension", "category": "work", "speakText": "I need an extension."},

        {"id": "send-invoice", "label": "Please send the invoice", "category": "work", "speakText": "Please send the invoice."},

        {"id": "work-from-home", "label": "I need to work from home", "category": "work", "speakText": "I need to work from home."},

        {"id": "refill-rx", "label": "I need a prescription refill", "category": "health", "speakText": "I need a prescription refill."},

    ],

    "caregiver": [

        {"id": "model-word", "label": "Let's model this word", "category": "coaching", "speakText": "Let's model this word together."},

        {"id": "take-time", "label": "Take your time", "category": "coaching", "speakText": "Take your time. I'm listening."},

        {"id": "good-try", "label": "Good try!", "category": "coaching", "speakText": "Good try! That counts."},

        {"id": "your-choice", "label": "Your choice matters", "category": "coaching", "speakText": "Your choice matters."},

        {"id": "we-can-wait", "label": "We can wait", "category": "coaching", "speakText": "We can wait. No rush."},

        {"id": "want-break", "label": "Do you want a break?", "category": "coaching", "speakText": "Do you want a break?"},

        {"id": "show-me", "label": "Show me how you feel", "category": "coaching", "speakText": "Show me how you feel."},

        {"id": "i-see-you", "label": "I see you trying", "category": "coaching", "speakText": "I see you trying."},

        {"id": "not-emergency", "label": "This is support, not emergency care", "category": "boundary", "speakText": "This is support, not emergency care."},

        {"id": "assent-first", "label": "We follow assent first", "category": "coaching", "speakText": "We follow assent first."},

        {"id": "lets-practice", "label": "Let's practice together", "category": "coaching", "speakText": "Let's practice together."},

        {"id": "you-are-safe", "label": "You are safe with me", "category": "coaching", "speakText": "You are safe with me."},

        {"id": "one-more-try", "label": "One more try?", "category": "coaching", "speakText": "One more try? No pressure."},

        {"id": "celebrate-effort", "label": "I celebrate your effort", "category": "coaching", "speakText": "I celebrate your effort."},

    ],

}



BABY_LABEL_OVERRIDES = {"mommy": "mama", "daddy": "dada"}



BABY_IDS = [

    "help", "more", "stop", "yes", "no", "eat", "drink", "milk", "water", "mommy",

    "daddy", "hug", "sleep", "up", "down", "happy", "sad", "hurt", "love", "please",

    "wait", "go", "home", "play", "look", "listen", "ball", "book", "dog", "cat",

    "toy", "blanket", "all-done", "wet", "hungry", "bye", "hi", "night", "gentle", "pacifier",

    "rattle", "bib", "stroller", "spoon", "banana", "duck", "star", "moon", "sun", "bear",

]



TODDLER_EXTRA_IDS = [

    "hungry", "mad", "need", "scared", "tired", "want", "thirsty", "bye", "hi",

    "brush-teeth", "teeth", "sock", "shirt", "pants", "night", "gentle", "diaper", "bottle",

    "snack", "playground", "crayon", "swing", "slide", "rain", "snow", "hat", "coat", "bunny",

]



CHILD_EXTRA_IDS = [

    "sick", "school", "read", "draw", "music", "outside", "family", "share", "turn",

    "thank-you", "sorry", "break", "quiet", "loud", "like", "dont-like", "where", "what",

    "soft", "hard", "pet", "brother", "sister", "grandma", "grandpa", "teacher", "park",

    "finished", "alone", "together",

    "pencil", "backpack", "lunchbox", "recess", "cousin", "aunt", "uncle", "neighbor", "tickle",

]



TWEEN_EXTRA_IDS = [

    "who", "when", "why", "different", "same", "computer", "phone", "walk", "run",

    "swim", "dance", "sing", "write", "think", "try", "team", "fast", "slow", "morning",

    "today", "tomorrow", "yesterday", "first", "last", "forget", "remember", "win", "lose",

    "alarm", "photo", "video", "email", "store", "doctor", "nurse", "money", "pay", "buy",

    "job", "meeting", "schedule", "calendar", "message", "call", "map", "directions", "left",

    "right", "forward", "backward", "sell", "favorite", "weather", "storm", "library", "homework",

    "baby", "transport", "appointment", "grocery", "restaurant",

    "locker", "cafeteria", "project", "club", "practice", "schedule-change", "work",

]



TEEN_EXTRA_IDS = [

    "not-now", "later", "overwhelmed", "pain", "medication", "text", "repeat", "privacy",

    "consent", "uncomfortable", "anxious", "excited", "frustrated", "explain", "choice",

    "support", "accommodation", "emergency", "repeat-slower", "clarify", "topic-change",

    "leave", "stay", "space", "high-five", "introduce", "running-late", "cancel", "order",

    "allergy", "nausea", "rest", "insurance", "pharmacy", "therapist", "counselor", "wifi",

    "password", "bank", "rent",

    "resume", "interview", "paycheck", "prescription", "refill", "coworker", "supervisor",

    "deadline", "feedback", "restaurant",

]



ADULT_EXTRA_IDS = [

    "invoice", "extension", "work", "email", "meeting", "schedule", "calendar", "money",

    "pay", "buy", "job", "store", "doctor", "nurse", "message", "call", "video", "map",

    "sell", "tomorrow", "yesterday", "directions", "left", "right", "forward", "backward",

    "grocery", "restaurant", "order", "allergy", "grandma", "grandpa", "insurance",

    "pharmacy", "therapist", "counselor", "wifi", "password", "bank", "rent",

    "resume", "interview", "paycheck", "prescription", "refill", "landlord", "lease",

    "utility", "deadline", "feedback", "coworker", "supervisor", "restaurant",

]



CAREGIVER_IDS = [

    "help", "more", "stop", "yes", "no", "wait", "please", "thank-you", "share", "listen",

    "quiet", "break", "love", "happy", "sad", "hurt", "eat", "drink", "bathroom", "sleep",

    "play", "go", "home", "look", "hug", "all-done", "try", "together", "support", "family",

    "choice", "gentle", "schedule", "need", "want", "open", "close", "again", "friend", "wash",

    "tickle", "snack", "practice", "project", "feedback", "neighbor", "cousin", "aunt", "uncle",

]



BAND_META = {

    "baby": {

        "id": "baby-vocab",

        "title": "Baby Nursery (0-23 mo)",

        "nickname": "Seed",

        "ageBand": "baby",

    },

    "toddler": {

        "id": "toddler-core",

        "title": "Toddler Core (2-4)",

        "nickname": "Sprout",

        "ageBand": "toddler",

    },

    "child": {

        "id": "child-vocab",

        "title": "Child Vocabulary (5-8)",

        "nickname": "Bud",

        "ageBand": "child",

    },

    "tween": {

        "id": "tween-vocab",

        "title": "Tween Vocabulary (9-12)",

        "nickname": "Sprig",

        "ageBand": "tween",

    },

    "teen": {

        "id": "teen-vocab",

        "title": "Teen Vocabulary (13-17)",

        "nickname": "Vine",

        "ageBand": "teen",

    },

    "adult": {

        "id": "adult-vocab",

        "title": "Adult Vocabulary (18+)",

        "nickname": "Bloom",

        "ageBand": "adult",

    },

    "caregiver": {

        "id": "caregiver-vocab",

        "title": "Caregiver Modeling",

        "nickname": "Canopy",

        "ageBand": "caregiver",

    },

}



COMBINED_FILE_MAP = {

    "baby": "baby-vocab.json",

    "toddler": "toddler-core.json",

    "child": "child-vocab.json",

    "tween": "tween-vocab.json",

    "teen": "teen-vocab.json",

    "adult": "adult-vocab.json",

    "caregiver": "caregiver-vocab.json",

}





def load_json(name: str) -> dict:

    path = APP_CONTENT / name

    if not path.exists():

        path = VOCAB / name

    return json.loads(path.read_text(encoding="utf-8"))





def sym_map(symbols: list) -> dict[str, dict]:

    return {s["id"]: deepcopy(s) for s in symbols}





def merge_unique(*id_lists: list[str]) -> list[str]:

    seen: set[str] = set()

    out: list[str] = []

    for lst in id_lists:

        for i in lst:

            if i not in seen:

                seen.add(i)

                out.append(i)

    return out





def cap_ids(ids: list[str], source: dict[str, dict], target: int) -> list[str]:

    out: list[str] = []

    for i in ids:

        if i in source and i not in out:

            out.append(i)

        if len(out) >= target:

            break

    return out





def build_extra_map() -> dict[str, dict]:

    out: dict[str, dict] = {}

    for sym_id, meta in EXTRA_SYMBOLS.items():

        out[sym_id] = {

            "id": sym_id,

            "label": meta["label"],

            "category": meta["category"],

            "description": f"Functional AAC symbol: {meta['label']}.",

        }

    return out





def band_asset(sym: dict, band: str) -> dict:

    s = deepcopy(sym)

    d = BAND_DIR[band]

    s["imageAsset"] = f"assets/symbols/{d}/{s['id']}.png"

    return s





def pick_symbols(source: dict[str, dict], ids: list[str], band: str) -> list[dict]:

    out = []

    for i in ids:

        if i in source:

            s = band_asset(source[i], band)

            if band == "baby" and i in BABY_LABEL_OVERRIDES:

                s["label"] = BABY_LABEL_OVERRIDES[i]

            out.append(s)

    return out





def phrase_list(band: str) -> list[dict]:

    return PHRASES[band][: PHRASE_TARGETS[band]]





def build_sets() -> dict[str, dict]:

    toddler_data = load_json("toddler-core.json")

    child_data = load_json("child-expanded.json")

    teen_data = load_json("teen-adult-functional.json")



    toddler_map = sym_map(toddler_data["symbols"])

    child_map = sym_map(child_data["symbols"])

    teen_map = sym_map(teen_data["symbols"])

    all_source = {**toddler_map, **child_map, **teen_map, **build_extra_map()}



    toddler_base = [s["id"] for s in toddler_data["symbols"]]

    toddler_ids = cap_ids(

        merge_unique(toddler_base, TODDLER_EXTRA_IDS),

        all_source,

        WORD_TARGETS["toddler"],

    )

    baby_ids = cap_ids(BABY_IDS, all_source, WORD_TARGETS["baby"])

    child_ids = cap_ids(

        merge_unique(toddler_ids, CHILD_EXTRA_IDS),

        all_source,

        WORD_TARGETS["child"],

    )

    tween_ids = cap_ids(

        merge_unique(child_ids, TWEEN_EXTRA_IDS),

        all_source,

        WORD_TARGETS["tween"],

    )

    teen_ids = cap_ids(

        merge_unique(tween_ids, TEEN_EXTRA_IDS, [s["id"] for s in teen_data["symbols"]]),

        all_source,

        WORD_TARGETS["teen"],

    )

    adult_ids = cap_ids(

        merge_unique(teen_ids, ADULT_EXTRA_IDS),

        all_source,

        WORD_TARGETS["adult"],

    )

    caregiver_ids = cap_ids(CAREGIVER_IDS, all_source, WORD_TARGETS["caregiver"])



    band_word_ids = {

        "baby": baby_ids,

        "toddler": toddler_ids,

        "child": child_ids,

        "tween": tween_ids,

        "teen": teen_ids,

        "adult": adult_ids,

        "caregiver": caregiver_ids,

    }



    sets: dict[str, dict] = {}

    for band, ids in band_word_ids.items():

        meta = BAND_META[band]

        phrases = phrase_list(band)

        word_count = len(ids)

        phrase_count = len(phrases)

        sets[band] = {

            **meta,

            "description": (

                f"{word_count} words + {phrase_count} phrases for Caly {meta['nickname']}."

            ),

            "symbols": pick_symbols(all_source, ids, band),

            "phrases": phrases,

        }

    return sets





def write_json(path: Path, data: dict) -> None:

    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")





def write_outputs(sets: dict[str, dict]) -> None:

    for band, data in sets.items():

        combined_name = COMBINED_FILE_MAP[band]

        words_name = f"{band}-words.json"

        phrases_name = f"{band}-phrases.json"



        combined = {k: v for k, v in data.items()}

        words_doc = {

            "id": f"{band}-words",

            "title": data["title"] + "  - Words",

            "description": f"{len(data['symbols'])} basic vocabulary symbols for Caly {data['nickname']}.",

            "ageBand": data["ageBand"],

            "nickname": data["nickname"],

            "symbols": data["symbols"],

        }

        phrases_doc = {

            "id": f"{band}-phrases",

            "title": data["title"] + "  - Phrases",

            "description": f"{len(data['phrases'])} phrases for Caly {data['nickname']}.",

            "ageBand": data["ageBand"],

            "nickname": data["nickname"],

            "phrases": data["phrases"],

        }



        for base in (VOCAB, APP_CONTENT):

            write_json(base / combined_name, combined)

            write_json(base / words_name, words_doc)

            write_json(base / phrases_name, phrases_doc)



        print(

            f"{band}: {len(data['symbols'])} words, {len(data['phrases'])} phrases "

            f"-> {combined_name}, {words_name}, {phrases_name}"

        )





def main() -> None:

    sets = build_sets()

    write_outputs(sets)





if __name__ == "__main__":

    main()

