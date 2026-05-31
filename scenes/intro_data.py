# -*- coding: utf-8 -*-
"""
SINGLE SOURCE OF TRUTH for the "Moral AI" Introduction visual companion.

Every on-screen number, name, date and quotation used by the Manim scenes and
by the website is transcribed from:

    Jana Schaich Borg, Walter Sinnott-Armstrong & Vincent Conitzer,
    "Moral AI and How We Get There", Pelican Books (Penguin Random House), 2024.
    ISBN 978-0-241-45474-9.
    Introduction: "What's the Problem?", pp. xiii-xx.
    Reference notes 1-23 transcribed from the book's "References" section, pp. 237-238.

HONESTY DISCIPLINE
------------------
* No scene invents a number. Scenes import from this module.
* `detail` fields are FAITHFUL PARAPHRASES of the book's prose.
* Text inside `quote(...)` / the FRAMING/THESIS verbatim fields is WORD-FOR-WORD
  from the book and is always shown in quotation marks with author credit.
* The book *reports* these cases (citing the sources below); this companion does
  not independently verify them. Any drawn glass/scale/icon is schematic, not data.
* `image_query` is a hint for finding a FREELY-LICENSED, representative image
  (Wikimedia Commons / public domain / CC). Representative images are labelled as
  such on the page and credited; they are not claimed to depict the exact event.
"""

BOOK = {
    "title": "Moral AI",
    "subtitle": "and How We Get There",
    "authors": [
        "Jana Schaich Borg",
        "Walter Sinnott-Armstrong",
        "Vincent Conitzer",
    ],
    "publisher": "Pelican Books (Penguin Random House)",
    "year": 2024,
    "isbn": "978-0-241-45474-9",
    "section": "Introduction: What's the Problem?",
    "pages": "xiii-xx",
}

# ---------------------------------------------------------------------------
# FRAMING  (Introduction, pp. xiii-xiv)
# ---------------------------------------------------------------------------
FRAMING = {
    # verbatim, shown in quotation marks
    "alarm": "The robots are coming! The robots are coming!",
    # faithful paraphrases of the two camps
    "pessimist_label": "The pessimist",
    "pessimist_points": [
        "AI could control everything (the Matrix fear)",
        "Robs us of privacy",
        "We can't tell a real email or photo from a fake",
        "Manipulates how we vote and what we buy",
        "Conclusion: stop — or slow down — AI before it's too late",
    ],
    "optimist_label": "The optimist",
    "optimist_points": [
        "Fears drunk human drivers, not self-driving cars",
        "Wants AI to end the atrocities human soldiers commit",
        "Expects rapid progress in science and medicine",
        "Some look forward to humans merging with AI",
        "Conclusion: don't slow down AI progress",
    ],
    # concise on-screen condensations (faithful) for the animation columns
    "pessimist_short": ["Loss of privacy", "Real photo or fake?",
                        "Manipulated votes & purchases", "→ Slow AI down"],
    "optimist_short": ["Safer than drunk drivers", "Fewer wartime atrocities",
                       "Faster science & medicine", "→ Don't slow down"],
    # verbatim, shown in quotation marks
    "verdict_question": "Is the glass half empty or half full?",
    "verdict": "Our answer is: both.",
    "verdict_gloss": (
        "There is bad news that gives us reason to worry about some uses of AI, "
        "and good news that gives us reason to advocate for others — sometimes "
        "for the very same AI technique."
    ),
}

# ---------------------------------------------------------------------------
# THE ELEVEN DOMAINS  (Introduction, pp. xiv-xviii)
# Each carries a good-news case and a bad-news case, the book's footnote number,
# and the actual source the authors cite (notes 1-23, pp. 237-238).
# ---------------------------------------------------------------------------
DOMAINS = [
    {
        "key": "transportation",
        "title": "Transportation",
        "good": {
            "head": "A blind driver gains independence",
            "detail": "Steve Mahan, who is blind, rides his autonomous car around "
                      "Santa Clara, California — sometimes alone, by himself.",
            "fn": 1,
            "source": {"title": "Steve Mahan's first ride (Google Self-Driving Car)",
                       "pub": "YouTube", "date": "",
                       "url": "https://www.youtube.com/watch?v=x_d3MCkivg8"},
            "image_query": "Waymo Google self-driving car",
        },
        "bad": {
            "head": "First fatal Autopilot crash",
            "detail": "Joshua Brown was killed in May 2016 when his Tesla Model S on "
                      "Autopilot drove into a white truck it could not distinguish "
                      "from the bright sky.",
            "fn": 2,
            "source": {"title": "Tesla driver dies in first autonomous car crash in US",
                       "pub": "New Scientist (Alice Klein)", "date": "1 July 2016",
                       "url": "https://www.newscientist.com/article/2095740-tesla-driver-dies-in-first-autonomous-car-crash-in-us/"},
            "image_query": "Tesla Model S car",
        },
    },
    {
        "key": "military",
        "title": "Military",
        "good": {
            "head": "Robots defuse bombs, not people",
            "detail": "An AI-augmented bomb-disposal robot reaches tight spots and "
                      "defuses or detonates deadly devices without humans risking "
                      "their lives.",
            "fn": 3,
            "source": {"title": "What does a bomb-disposal robot actually do?",
                       "pub": "BBC Future", "date": "14 July 2016",
                       "url": "http://www.bbc.com/future/story/20160714-what-does-a-bomb-disposal-robot-actually-do"},
            "image_query": "bomb disposal EOD robot military",
        },
        "bad": {
            "head": "Robot cannon kills 9, wounds 14",
            "detail": "In Lohatlha, South Africa, an Oerlikon GDF-005 anti-aircraft "
                      "gun directed by AI went out of control and sprayed cannon "
                      "shells, killing nine and wounding 14.",
            "fn": 4,
            "source": {"title": "Robot Cannon Kills 9, Wounds 14",
                       "pub": "Wired (Noah Shachtman)", "date": "18 October 2007",
                       "url": "https://www.wired.com/2007/10/robot-cannon-ki/"},
            "image_query": "Oerlikon 35mm anti-aircraft gun GDF",
        },
    },
    {
        "key": "politics",
        "title": "Politics",
        "good": {
            "head": "Fairer electoral maps",
            "detail": "AI can draw congressional districts in North Carolina that are "
                      "fair to both political parties and to various interest groups.",
            "fn": 5,
            "source": {"title": "Quantifying Gerrymandering",
                       "pub": "Duke University", "date": "",
                       "url": "https://sites.duke.edu/quantifyinggerrymandering/"},
            "image_query": "North Carolina congressional districts map",
        },
        "bad": {
            "head": "Cambridge Analytica",
            "detail": "Cambridge Analytica used AI trained on the personal data of up "
                      "to 87 million Facebook users — without their knowledge — to try "
                      "to influence the 2016 US presidential election.",
            "fn": 6,
            "number": "87 million",
            "source": {"title": "Facebook and Cambridge Analytica: What happened?",
                       "pub": "Fortune; Hu, 'Cambridge Analytica's black box', Big Data & Society (2020)",
                       "date": "10 April 2018",
                       "url": "https://fortune.com/2018/04/10/facebook-cambridge-analytica-what-happened/"},
            "image_query": "Facebook headquarters sign",
        },
    },
    {
        "key": "law",
        "title": "Law",
        "good": {
            "head": "Cheaper contract review",
            "detail": "ThoughtRiver built an AI that reads legal contracts, answers "
                      "key questions and suggests next steps — for a far smaller fee "
                      "than human lawyers charge.",
            "fn": 7,
            "source": {"title": "ThoughtRiver",
                       "pub": "thoughtriver.com", "date": "",
                       "url": "https://www.thoughtriver.com"},
            "image_query": "legal contract signing document",
        },
        "bad": {
            "head": "A six-year sentence from a black box",
            "detail": "Eric Loomis was sentenced to six years partly because a "
                      "proprietary AI risk assessment labelled him a 'high risk to the "
                      "community'. No one could see how it decided; critics argue it is "
                      "biased by race and gender.",
            "fn": 8,
            "number": "6 years",
            "source": {"title": "Loomis v. Wisconsin, 881 N.W.2d 749 (Wis. 2016)",
                       "pub": "cert. denied, 137 S.Ct. 2290 (2017)", "date": "2016",
                       "url": "https://en.wikipedia.org/wiki/State_v._Loomis"},
            "image_query": "courtroom judge gavel",
        },
    },
    {
        "key": "medicine",
        "title": "Medicine",
        "good": {
            "head": "Watson catches a rare leukaemia",
            "detail": "In 2015 IBM's Watson diagnosed a rare leukaemia that human "
                      "doctors couldn't pinpoint at first. Doctors said Watson's speed "
                      "was crucial for a fast-progressing disease.",
            "fn": 9,
            "number": "2015",
            "source": {"title": "IBM Watson detects rare leukaemia (University of Tokyo)",
                       "pub": "Asian Scientist", "date": "2016",
                       "url": "https://www.asianscientist.com/2016/08/topnews/ibm-watson-rare-leukemia-university-tokyo-artificial-intelligence/"},
            "image_query": "IBM Watson computer",
        },
        "bad": {
            "head": "An algorithm that favoured White patients",
            "detail": "Bias in training data led a widely used 'high-risk care' "
                      "algorithm to prioritize White patients over Black patients who "
                      "were equally ill.",
            "fn": 10,
            "source": {"title": "Dissecting racial bias in an algorithm used to manage "
                                "the health of populations",
                       "pub": "Obermeyer et al., Science 366(6464)", "date": "2019",
                       "url": "https://www.science.org/doi/10.1126/science.aax2342"},
            "image_query": "hospital corridor healthcare",
        },
    },
    {
        "key": "investment",
        "title": "Investment",
        "good": {
            "head": "Advice for the rest of us",
            "detail": "Robo-advisers such as Betterment, Wealthfront and Wealthsimple "
                      "claim to be at least as accurate as human advisers, with low "
                      "minimums that open financial advice to lower-income investors.",
            "fn": 11,
            "source": {"title": "Robo-advisers (example credited to Coleman Kraemer)",
                       "pub": "Moral AI, Introduction note 11", "date": "",
                       "url": "https://www.betterment.com"},
            "image_query": "stock market trading chart screen",
        },
        "bad": {
            "head": "The Flash Crash",
            "detail": "On 6 May 2010 at 2:45 pm the Dow Jones Industrial Average dropped "
                      "998.5 points in minutes as AI-driven trading systems spiralled "
                      "into high-speed automated selling.",
            "fn": 12,
            "number": "998.5 pts",
            "source": {"title": "2010 Flash Crash",
                       "pub": "Wikipedia", "date": "6 May 2010",
                       "url": "https://en.wikipedia.org/wiki/2010_flash_crash"},
            "image_query": "stock market crash falling chart",
        },
    },
    {
        "key": "marketing",
        "title": "Marketing",
        "good": {
            "head": "Reaching youth who need testing",
            "detail": "The 'Have You Heard?' (HYH) project used AI to raise HIV testing "
                      "among homeless youth by 25%, by finding the young people most "
                      "influential in their social networks.",
            "fn": 13,
            "number": "+25%",
            "source": {"title": "HIV Prevention Among Homeless Youth",
                       "pub": "USC Center for AI in Society (CAIS)", "date": "",
                       "url": "https://www.cais.usc.edu/projects/hiv-prevention-homeless-youth/"},
            "image_query": "red ribbon HIV awareness",
        },
        "bad": {
            "head": "Target knew before her father did",
            "detail": "In 2012 a Target store mailed baby coupons to a 16-year-old "
                      "because its AI predicted, from her buying patterns, that she was "
                      "pregnant — before she had told her father.",
            "fn": 14,
            "source": {"title": "How Target Figured Out A Teen Girl Was Pregnant Before "
                                "Her Father Did",
                       "pub": "Forbes (Kashmir Hill)", "date": "16 February 2012",
                       "url": "https://www.forbes.com/sites/kashmirhill/2012/02/16/how-target-figured-out-a-teen-girl-was-pregnant-before-her-father-did/"},
            "image_query": "Target store retail",
        },
    },
    {
        "key": "art",
        "title": "Art",
        "good": {
            "head": "Music you'd never have found",
            "detail": "Pandora and Spotify use AI analyses of musical taste to "
                      "recommend new songs and artists listeners enjoy and might never "
                      "have discovered otherwise.",
            "fn": 15,
            "source": {"title": "A Spotify AI bot will judge your taste in music",
                       "pub": "CNN", "date": "24 December 2020",
                       "url": "https://www.cnn.com/2020/12/24/entertainment/spotify-ai-bot-judges-your-taste-in-music-trnd/index.html"},
            "image_query": "music streaming headphones",
        },
        "bad": {
            "head": "Art that sold for $432,500",
            "detail": "AI-made art has sold for as much as $432,500 — but the AI could "
                      "do it only by training on human artists' images, used without "
                      "permission, credit or pay, and hard to make it 'forget'.",
            "fn": 16,
            "number": "$432,500",
            "source": {"title": "Is artificial intelligence set to take over the art "
                                "world? (Edmond de Belamy, Obvious collective)",
                       "pub": "Christie's", "date": "2018",
                       "url": "https://www.christies.com/features/a-collaboration-between-two-artists-one-human-one-a-machine-9332-1.aspx"},
            "image_query": "ornate empty gold picture frame",
        },
    },
    {
        "key": "media",
        "title": "Media",
        "good": {
            "head": "Quakebot warns faster",
            "detail": "The Los Angeles Times uses an algorithm called Quakebot to warn "
                      "readers about California earthquakes more quickly and accurately "
                      "than traditional reporting.",
            "fn": 17,
            "source": {"title": "What is Quakebot? (LA Times FAQ)",
                       "pub": "Los Angeles Times", "date": "17 May 2019",
                       "url": "https://www.latimes.com/la-me-quakebot-faq-20190517-story.html"},
            "image_query": "seismograph earthquake recording",
        },
        "bad": {
            "head": "Deepfakes hit an election",
            "detail": "In 2023 Turkish presidential candidate Muharrem İnce withdrew "
                      "after a sex video he called a 'deepfake' spread on Facebook; a "
                      "fake video also tied a rival, Kemal Kılıçdaroğlu, to a "
                      "terrorist group.",
            "fn": 18,
            "source": {"title": "Deepfakes, Cheapfakes and Twitter Censorship Mar "
                                "Turkey's Elections",
                       "pub": "Wired", "date": "2023",
                       "url": "https://www.wired.com/story/deepfakes-cheapfakes-and-twitter-censorship-mar-turkeys-elections/"},
            "image_query": "deepfake digital face manipulation",
        },
    },
    {
        "key": "surveillance",
        "title": "Surveillance",
        "good": {
            "head": "Catching poachers before they strike",
            "detail": "AI helps locate poachers in India and Africa — even predicting "
                      "poaching before it happens — and game-theoretic AI optimizes "
                      "ranger patrol routes to intercept snares.",
            "fn": 19,
            "source": {"title": "The technology fighting poachers (PAWS)",
                       "pub": "BBC Earth (Zoe Cormier)", "date": "",
                       "url": "https://www.bbcearth.com"},
            "image_query": "wildlife ranger anti-poaching patrol",
        },
        "bad": {
            "head": "Tracking a minority by face",
            "detail": "China is reported to use a vast facial-recognition system to "
                      "track and control the Uighurs, a largely Muslim minority — "
                      "500,000 face scans in a single month.",
            "fn": 20,
            "number": "500,000 scans/mo",
            "source": {"title": "One Month, 500,000 Face Scans: How China Is Using A.I. "
                                "to Profile a Minority",
                       "pub": "The New York Times (Paul Mozur)", "date": "14 April 2019",
                       "url": "https://www.nytimes.com/2019/04/14/technology/china-surveillance-artificial-intelligence-racial-profiling.html"},
            "image_query": "facial recognition surveillance camera",
        },
    },
    {
        "key": "environment",
        "title": "Environment",
        "good": {
            "head": "Spray only the weeds",
            "detail": "Blue River Technology uses AI camera vision to tell crops from "
                      "weeds and deliver herbicide only to the weeds — helping avoid "
                      "resistance and saving cotton growers money.",
            "fn": 22,
            "source": {"title": "How self-driving tractors, AI, and precision "
                                "agriculture will save us from the food crisis",
                       "pub": "TechRepublic (Natalie Gagliardi)", "date": "December 2018",
                       "url": "https://www.techrepublic.com/article/how-self-driving-tractors-ai-and-precision-agriculture-will-save-us-from-the-impending-food-crisis/"},
            "image_query": "agricultural tractor spraying crop field",
        },
        "bad": {
            "head": "A model's carbon shadow",
            "detail": "Training many high-performing AI models takes enormous compute. "
                      "One estimate: training a single AI model can emit as much carbon "
                      "as five cars do across their entire lifetimes.",
            "fn": 23,
            "number": "≈5 cars",
            "source": {"title": "Training a single AI model can emit as much carbon as "
                                "five cars in their lifetimes",
                       "pub": "MIT Technology Review (Karen Hao)", "date": "6 June 2019",
                       "url": "https://www.technologyreview.com/2019/06/06/239031/training-a-single-ai-model-can-emit-as-much-carbon-as-five-cars-in-their-lifetimes/"},
            "image_query": "data center server room",
        },
    },
]

# ---------------------------------------------------------------------------
# BY THE NUMBERS  (curated literals, each verbatim from the Introduction)
# These units are DELIBERATELY incommensurable - shown for scale of stakes,
# never as a single ranked axis.
# ---------------------------------------------------------------------------
NUMBERS = [
    {"value": "87 million", "label": "Facebook users' data",
     "context": "used by Cambridge Analytica without consent to try to sway the 2016 US election",
     "fn": 6, "domain": "politics", "tone": "bad"},
    {"value": "998.5", "unit": "points", "label": "Dow drop in minutes",
     "context": "the 6 May 2010 'Flash Crash' driven by AI high-speed selling",
     "fn": 12, "domain": "investment", "tone": "bad"},
    {"value": "$432,500", "label": "price of an AI artwork",
     "context": "sold at auction; the model trained on artists' work without consent",
     "fn": 16, "domain": "art", "tone": "bad"},
    {"value": "+25%", "label": "more youth tested for HIV",
     "context": "the 'Have You Heard?' project found socially influential young people",
     "fn": 13, "domain": "marketing", "tone": "good"},
    {"value": "9 / 14", "label": "killed / wounded",
     "context": "an AI-directed Oerlikon GDF-005 anti-aircraft gun, Lohatlha, South Africa",
     "fn": 4, "domain": "military", "tone": "bad"},
    {"value": "6 years", "label": "prison, partly from a black box",
     "context": "Eric Loomis, scored 'high risk' by a proprietary algorithm",
     "fn": 8, "domain": "law", "tone": "bad"},
    {"value": "≈5 cars", "label": "lifetime carbon, in one model",
     "context": "an estimate of the emissions of training a single large AI model",
     "fn": 23, "domain": "environment", "tone": "bad"},
]

# ---------------------------------------------------------------------------
# SIX MORAL VALUES  (Introduction, pp. xix-xx)
# The book stresses this list "is not meant to be exhaustive."
# ---------------------------------------------------------------------------
VALUES = [
    {"name": "Safety",
     "illustration": "autonomous cars and weapons, deepfakes, social media, robot "
                     "surgeons, and future AI that could make us lose control."},
    {"name": "Equality",
     "illustration": "risk scores keyed to race, wealth and gender; bias in "
                     "healthcare; robo-advisers; inequality from AI job losses."},
    {"name": "Privacy",
     "illustration": "Cambridge Analytica; Target's pregnancy-prediction coupons; "
                     "Chinese surveillance of the Uighurs."},
    {"name": "Freedom",
     "illustration": "aiding blind people like Steve Mahan; impeding movement or "
                     "religious practice through targeted surveillance."},
    {"name": "Transparency",
     "illustration": "Eric Loomis; AI that grades job performance, résumés, loan "
                     "creditworthiness and student papers."},
    {"name": "Deception",
     "illustration": "deepfakes and AI-generated fake news used to interfere in "
                     "elections."},
]

VALUES_CAVEAT = "Some AI uses implicate more than one value, and this list is not meant to be exhaustive."

# ---------------------------------------------------------------------------
# THESIS  (Introduction, p. xx) - verbatim fragments shown in quotation marks
# ---------------------------------------------------------------------------
THESIS = {
    "tip_of_iceberg": "These examples are just the tip of the iceberg.",
    "not_underestimate": "The dangers of AI should not be underestimated,",
    "not_overestimate": "but they also should not be overestimated.",
    "balance": "Typically, AI can be built and used safely and ethically as long as "
               "these moral issues are addressed thoughtfully.",
    "baby_bathwater": "To keep the AI baby without its bathwater, we will try to "
                      "illuminate the moral issues at stake — and show why we all need "
                      "to pay more attention to AI ethics.",
}

# Honest "what we do NOT claim" box for the website.
NOT_CLAIM = [
    "We do not claim these cases are exhaustive or representative of all AI — the "
    "book calls them 'the tip of the iceberg.'",
    "We do not independently verify the events; we report them as the book does, and "
    "link the source the authors cite.",
    "The numbers use different units and are not comparable on a single scale — they "
    "show the scale of the stakes, not a ranking.",
    "Photographs are freely-licensed, representative images (credited below); unless "
    "noted, they do not depict the exact event described.",
    "Diagrams such as the glass and the balance are schematic illustrations, not data.",
]
