# -*- coding: utf-8 -*-
"""
Versione ITALIANA della fonte di verità per il companion visivo all'Introduzione
di "Moral AI and How We Get There" (Schaich Borg, Sinnott-Armstrong & Conitzer,
Pelican Books, 2024).

Stessa struttura di intro_data.py: ogni testo a schermo è una PARAFRASI nostra,
non una citazione letterale. I numeri, i nomi e le date sono ripresi dal libro.
Le fonti riportate qui sono quelle citate dagli autori (fallback); l'edizione
italiana del sito sovrascrive, dove disponibile, con un articolo in lingua
italiana (vedi site_media/it_sources/<case>.json).
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
    "section": "Introduzione: «Qual è il problema?»",
    "pages": "xiii-xx",
}

FRAMING = {
    "alarm": "L'allarme si diffonde: arrivano i robot.",
    "pessimist_label": "Il pessimista",
    "pessimist_short": ["Perdita di privacy", "Foto vera o falsa?",
                        "Voti e acquisti manipolati", "→ Rallentare l'IA"],
    "optimist_label": "L'ottimista",
    "optimist_short": ["Più sicura degli ubriachi al volante",
                       "Meno atrocità in guerra", "Scienza e medicina più rapide",
                       "→ Non rallentare"],
    "verdict_question": "Mezzo vuoto o mezzo pieno?",
    "verdict_pre": "La risposta degli autori:",
    "verdict": "entrambi.",
    "verdict_gloss": (
        "Il libro sostiene che ci sono cattive notizie che dovrebbero preoccuparci "
        "per alcuni usi dell'IA, e buone notizie per cui vale la pena battersi in "
        "altri — a volte per la stessa identica tecnica."
    ),
}

DOMAINS = [
    {
        "key": "transportation",
        "title": "Trasporti",
        "good": {
            "head": "Un automobilista cieco riconquista l'autonomia",
            "detail": "Steve Mahan, cieco, gira per Santa Clara, in California, sulla "
                      "sua auto a guida autonoma — a volte da solo.",
            "fn": 1,
            "source": {"title": "Il primo viaggio di Steve Mahan (Google Self-Driving Car)",
                       "pub": "YouTube", "date": "",
                       "url": "https://www.youtube.com/watch?v=x_d3MCkivg8"},
            "image_query": "Waymo Google self-driving car",
        },
        "bad": {
            "head": "Primo incidente mortale in Autopilot",
            "detail": "Joshua Brown è morto nel maggio 2016 quando la sua Tesla Model S "
                      "in Autopilot si è schiantata contro un camion bianco che non "
                      "riusciva a distinguere dal cielo luminoso.",
            "fn": 2,
            "source": {"title": "Tesla driver dies in first autonomous car crash in US",
                       "pub": "New Scientist (Alice Klein)", "date": "1 luglio 2016",
                       "url": "https://www.newscientist.com/article/2095740-tesla-driver-dies-in-first-autonomous-car-crash-in-us/"},
            "image_query": "Tesla Model S car",
        },
    },
    {
        "key": "military",
        "title": "Militare",
        "good": {
            "head": "I robot disinnescano le bombe, non le persone",
            "detail": "Un robot artificiere potenziato dall'IA raggiunge punti angusti "
                      "e disinnesca o fa brillare ordigni mortali senza che gli esseri "
                      "umani rischino la vita.",
            "fn": 3,
            "source": {"title": "What does a bomb-disposal robot actually do?",
                       "pub": "BBC Future", "date": "14 luglio 2016",
                       "url": "http://www.bbc.com/future/story/20160714-what-does-a-bomb-disposal-robot-actually-do"},
            "image_query": "bomb disposal EOD robot military",
        },
        "bad": {
            "head": "Un cannone robot uccide 9 persone e ne ferisce 14",
            "detail": "A Lohatlha, in Sudafrica, un cannone antiaereo Oerlikon GDF-005 "
                      "guidato dall'IA è andato fuori controllo sparando raffiche di "
                      "colpi, uccidendo nove persone e ferendone 14.",
            "fn": 4,
            "source": {"title": "Robot Cannon Kills 9, Wounds 14",
                       "pub": "Wired (Noah Shachtman)", "date": "18 ottobre 2007",
                       "url": "https://www.wired.com/2007/10/robot-cannon-ki/"},
            "image_query": "Oerlikon 35mm anti-aircraft gun GDF",
        },
    },
    {
        "key": "politics",
        "title": "Politica",
        "good": {
            "head": "Mappe elettorali più eque",
            "detail": "L'IA può tracciare i distretti del Congresso in North Carolina in "
                      "modo equo per entrambi i partiti e per i diversi gruppi d'interesse.",
            "fn": 5,
            "source": {"title": "Quantifying Gerrymandering",
                       "pub": "Duke University", "date": "",
                       "url": "https://sites.duke.edu/quantifyinggerrymandering/"},
            "image_query": "North Carolina congressional districts map",
        },
        "bad": {
            "head": "Cambridge Analytica",
            "detail": "Cambridge Analytica ha usato un'IA addestrata sui dati personali "
                      "di un massimo di 87 milioni di utenti Facebook — a loro insaputa "
                      "— per cercare di influenzare le elezioni presidenziali USA del 2016.",
            "fn": 6,
            "number": "87 milioni",
            "source": {"title": "Facebook and Cambridge Analytica: What happened?",
                       "pub": "Fortune; Hu, 'Cambridge Analytica's black box', Big Data & Society (2020)",
                       "date": "10 aprile 2018",
                       "url": "https://fortune.com/2018/04/10/facebook-cambridge-analytica-what-happened/"},
            "image_query": "Facebook headquarters sign",
        },
    },
    {
        "key": "law",
        "title": "Diritto",
        "good": {
            "head": "Revisione dei contratti a basso costo",
            "detail": "ThoughtRiver ha creato un'IA che legge i contratti legali, "
                      "risponde alle domande chiave e suggerisce i passi successivi, a "
                      "una frazione del costo di un avvocato.",
            "fn": 7,
            "source": {"title": "ThoughtRiver",
                       "pub": "thoughtriver.com", "date": "",
                       "url": "https://www.thoughtriver.com"},
            "image_query": "legal contract signing document",
        },
        "bad": {
            "head": "Sei anni di carcere decisi da una scatola nera",
            "detail": "Eric Loomis è stato condannato a sei anni anche perché una "
                      "valutazione del rischio basata su un'IA proprietaria lo ha "
                      "etichettato come 'ad alto rischio'. Nessuno poteva vedere come "
                      "decidesse; secondo i critici è influenzata da razza e genere.",
            "fn": 8,
            "number": "6 anni",
            "source": {"title": "Loomis v. Wisconsin, 881 N.W.2d 749 (Wis. 2016)",
                       "pub": "cert. denied, 137 S.Ct. 2290 (2017)", "date": "2016",
                       "url": "https://en.wikipedia.org/wiki/State_v._Loomis"},
            "image_query": "courtroom judge gavel",
        },
    },
    {
        "key": "medicine",
        "title": "Medicina",
        "good": {
            "head": "Watson individua una leucemia rara",
            "detail": "Nel 2015 Watson di IBM ha diagnosticato una leucemia rara che i "
                      "medici non riuscivano a identificare; secondo loro la velocità di "
                      "Watson è stata cruciale per una malattia che progredisce in fretta.",
            "fn": 9,
            "number": "2015",
            "source": {"title": "IBM Watson detects rare leukaemia (University of Tokyo)",
                       "pub": "Asian Scientist", "date": "2016",
                       "url": "https://www.asianscientist.com/2016/08/topnews/ibm-watson-rare-leukemia-university-tokyo-artificial-intelligence/"},
            "image_query": "IBM Watson computer",
        },
        "bad": {
            "head": "Un algoritmo che favoriva i pazienti bianchi",
            "detail": "Un bias nei dati di addestramento ha portato un diffuso algoritmo "
                      "per le 'cure ad alto rischio' a dare priorità ai pazienti bianchi "
                      "rispetto a quelli neri a parità di gravità.",
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
        "title": "Investimenti",
        "good": {
            "head": "Consulenza anche per chi non è ricco",
            "detail": "I robo-advisor come Betterment, Wealthfront e Wealthsimple "
                      "dichiarano di essere accurati quanto i consulenti umani, con "
                      "soglie minime basse che aprono la consulenza ai piccoli investitori.",
            "fn": 11,
            "source": {"title": "Robo-advisor (esempio attribuito a Coleman Kraemer)",
                       "pub": "Moral AI, Introduzione nota 11", "date": "",
                       "url": "https://www.betterment.com"},
            "image_query": "stock market trading chart screen",
        },
        "bad": {
            "head": "Il Flash Crash",
            "detail": "Il 6 maggio 2010, alle 14:45, il Dow Jones è crollato di 998,5 "
                      "punti in pochi minuti, mentre i sistemi di trading guidati "
                      "dall'IA precipitavano in una spirale di vendite automatiche.",
            "fn": 12,
            "number": "998,5 pt",
            "source": {"title": "2010 Flash Crash",
                       "pub": "Wikipedia", "date": "6 maggio 2010",
                       "url": "https://it.wikipedia.org/wiki/Flash_crash"},
            "image_query": "stock market crash falling chart",
        },
    },
    {
        "key": "marketing",
        "title": "Marketing",
        "good": {
            "head": "Raggiungere i giovani che hanno bisogno del test",
            "detail": "Il progetto 'Have You Heard?' (HYH) ha usato l'IA per aumentare "
                      "del 25% i test HIV tra i giovani senza dimora, individuando i "
                      "ragazzi più influenti nelle loro reti sociali.",
            "fn": 13,
            "number": "+25%",
            "source": {"title": "HIV Prevention Among Homeless Youth",
                       "pub": "USC Center for AI in Society (CAIS)", "date": "",
                       "url": "https://www.cais.usc.edu/projects/hiv-prevention-homeless-youth/"},
            "image_query": "red ribbon HIV awareness",
        },
        "bad": {
            "head": "Target lo sapeva prima del padre",
            "detail": "Nel 2012 un punto vendita Target ha inviato coupon per neonati a "
                      "una sedicenne perché la sua IA, dai suoi acquisti, aveva previsto "
                      "che fosse incinta — prima che lei lo dicesse al padre.",
            "fn": 14,
            "source": {"title": "How Target Figured Out A Teen Girl Was Pregnant Before "
                                "Her Father Did",
                       "pub": "Forbes (Kashmir Hill)", "date": "16 febbraio 2012",
                       "url": "https://www.forbes.com/sites/kashmirhill/2012/02/16/how-target-figured-out-a-teen-girl-was-pregnant-before-her-father-did/"},
            "image_query": "Target store retail",
        },
    },
    {
        "key": "art",
        "title": "Arte",
        "good": {
            "head": "Musica che non avresti mai scoperto",
            "detail": "Pandora e Spotify usano analisi dei gusti musicali basate sull'IA "
                      "per consigliare brani e artisti nuovi che gli ascoltatori amano e "
                      "che forse non avrebbero mai trovato.",
            "fn": 15,
            "source": {"title": "A Spotify AI bot will judge your taste in music",
                       "pub": "CNN", "date": "24 dicembre 2020",
                       "url": "https://www.cnn.com/2020/12/24/entertainment/spotify-ai-bot-judges-your-taste-in-music-trnd/index.html"},
            "image_query": "music streaming headphones",
        },
        "bad": {
            "head": "Un'opera venduta per 432.500 dollari",
            "detail": "Un'opera realizzata con l'IA è stata venduta per 432.500 dollari "
                      "— ma l'IA c'è riuscita solo addestrandosi su immagini di artisti "
                      "umani, usate senza permesso, credito o compenso, e difficili da "
                      "farle 'dimenticare'.",
            "fn": 16,
            "number": "432.500 $",
            "source": {"title": "Edmond de Belamy, opera d'arte generata dall'IA (Obvious)",
                       "pub": "Christie's", "date": "2018",
                       "url": "https://www.christies.com/features/a-collaboration-between-two-artists-one-human-one-a-machine-9332-1.aspx"},
            "image_query": "ornate empty gold picture frame",
        },
    },
    {
        "key": "media",
        "title": "Media",
        "good": {
            "head": "Quakebot avvisa più in fretta",
            "detail": "Il Los Angeles Times usa un algoritmo chiamato Quakebot per "
                      "avvisare i lettori dei terremoti in California più rapidamente e "
                      "accuratamente del giornalismo tradizionale.",
            "fn": 17,
            "source": {"title": "What is Quakebot? (LA Times FAQ)",
                       "pub": "Los Angeles Times", "date": "17 maggio 2019",
                       "url": "https://www.latimes.com/la-me-quakebot-faq-20190517-story.html"},
            "image_query": "seismograph earthquake recording",
        },
        "bad": {
            "head": "I deepfake colpiscono un'elezione",
            "detail": "Nel 2023 il candidato presidenziale turco Muharrem İnce si è "
                      "ritirato dopo che un video sessuale, che lui ha definito un "
                      "'deepfake', si è diffuso su Facebook; un altro video falso legava "
                      "il rivale Kemal Kılıçdaroğlu a un gruppo terroristico.",
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
        "title": "Sorveglianza",
        "good": {
            "head": "Fermare i bracconieri prima che colpiscano",
            "detail": "L'IA aiuta a localizzare i bracconieri in India e Africa — "
                      "prevedendo persino il bracconaggio prima che avvenga — e ottimizza "
                      "con la teoria dei giochi le rotte di pattuglia dei ranger.",
            "fn": 19,
            "source": {"title": "The technology fighting poachers (PAWS)",
                       "pub": "BBC Earth (Zoe Cormier)", "date": "",
                       "url": "https://www.bbcearth.com"},
            "image_query": "wildlife ranger anti-poaching patrol",
        },
        "bad": {
            "head": "Tracciare una minoranza dal volto",
            "detail": "La Cina userebbe un vasto sistema di riconoscimento facciale per "
                      "tracciare e controllare gli uiguri, una minoranza in gran parte "
                      "musulmana — 500.000 scansioni di volti in un solo mese.",
            "fn": 20,
            "number": "500.000 scans/mese",
            "source": {"title": "One Month, 500,000 Face Scans: How China Is Using A.I. "
                                "to Profile a Minority",
                       "pub": "The New York Times (Paul Mozur)", "date": "14 aprile 2019",
                       "url": "https://www.nytimes.com/2019/04/14/technology/china-surveillance-artificial-intelligence-racial-profiling.html"},
            "image_query": "facial recognition surveillance camera",
        },
    },
    {
        "key": "environment",
        "title": "Ambiente",
        "good": {
            "head": "Diserbare solo le erbacce",
            "detail": "Blue River Technology usa la visione artificiale per distinguere "
                      "le colture dalle erbacce e somministrare l'erbicida solo a queste "
                      "ultime — riducendo le resistenze e facendo risparmiare i coltivatori.",
            "fn": 22,
            "source": {"title": "How self-driving tractors, AI, and precision "
                                "agriculture will save us from the food crisis",
                       "pub": "TechRepublic (Natalie Gagliardi)", "date": "dicembre 2018",
                       "url": "https://www.techrepublic.com/article/how-self-driving-tractors-ai-and-precision-agriculture-will-save-us-from-the-impending-food-crisis/"},
            "image_query": "agricultural tractor spraying crop field",
        },
        "bad": {
            "head": "L'impronta di carbonio di un modello",
            "detail": "Addestrare molti modelli di IA ad alte prestazioni richiede "
                      "enormi risorse di calcolo. Secondo una stima, addestrare un solo "
                      "modello può emettere tanta CO₂ quanto cinque automobili nell'intero "
                      "ciclo di vita.",
            "fn": 23,
            "number": "≈5 auto",
            "source": {"title": "Training a single AI model can emit as much carbon as "
                                "five cars in their lifetimes",
                       "pub": "MIT Technology Review (Karen Hao)", "date": "6 giugno 2019",
                       "url": "https://www.technologyreview.com/2019/06/06/239031/training-a-single-ai-model-can-emit-as-much-carbon-as-five-cars-in-their-lifetimes/"},
            "image_query": "data center server room",
        },
    },
]

NUMBERS = [
    {"value": "87 milioni", "label": "dati di utenti Facebook",
     "context": "usati da Cambridge Analytica senza consenso per influenzare le elezioni USA del 2016",
     "fn": 6, "domain": "politics", "tone": "bad"},
    {"value": "998,5", "unit": "punti", "label": "crollo del Dow in pochi minuti",
     "context": "il 'Flash Crash' del 6 maggio 2010, dovuto a vendite IA ad alta velocità",
     "fn": 12, "domain": "investment", "tone": "bad"},
    {"value": "432.500 $", "label": "prezzo di un'opera d'IA",
     "context": "venduta all'asta; il modello si è addestrato sul lavoro di artisti senza consenso",
     "fn": 16, "domain": "art", "tone": "bad"},
    {"value": "+25%", "label": "più giovani testati per l'HIV",
     "context": "il progetto 'Have You Heard?' ha individuato i giovani più influenti",
     "fn": 13, "domain": "marketing", "tone": "good"},
    {"value": "9 / 14", "label": "morti / feriti",
     "context": "un cannone antiaereo Oerlikon GDF-005 guidato dall'IA, Lohatlha, Sudafrica",
     "fn": 4, "domain": "military", "tone": "bad"},
    {"value": "6 anni", "label": "di carcere, in parte da una scatola nera",
     "context": "Eric Loomis, classificato 'ad alto rischio' da un algoritmo proprietario",
     "fn": 8, "domain": "law", "tone": "bad"},
    {"value": "≈5 auto", "label": "CO₂ di una vita, in un solo modello",
     "context": "stima delle emissioni per addestrare un grande modello di IA",
     "fn": 23, "domain": "environment", "tone": "bad"},
]

VALUES = [
    {"name": "Sicurezza",
     "illustration": "auto e armi autonome, deepfake, social media, robot chirurghi e "
                     "una futura IA che potrebbe farci perdere il controllo."},
    {"name": "Uguaglianza",
     "illustration": "punteggi di rischio basati su razza, reddito e genere; bias nella "
                     "sanità; robo-advisor; disuguaglianza dovuta alla perdita di lavoro."},
    {"name": "Privacy",
     "illustration": "Cambridge Analytica; i coupon di Target sulla previsione di "
                     "gravidanza; la sorveglianza cinese degli uiguri."},
    {"name": "Libertà",
     "illustration": "aiutare persone cieche come Steve Mahan; ostacolare i movimenti o "
                     "la pratica religiosa tramite sorveglianza mirata."},
    {"name": "Trasparenza",
     "illustration": "Eric Loomis; IA che valuta prestazioni lavorative, curriculum, "
                     "merito creditizio e compiti degli studenti."},
    {"name": "Inganno",
     "illustration": "deepfake e fake news generate dall'IA usate per interferire "
                     "nelle elezioni."},
]

VALUES_CAVEAT = "Gli autori sottolineano che l'elenco non è esaustivo — e molti casi toccano più di un valore."

THESIS = {
    "tip_of_iceberg": "Questi casi sono solo un piccolo campione.",
    "not_underestimate": "I pericoli dell'IA non vanno sottovalutati —",
    "not_overestimate": "ma non vanno nemmeno sopravvalutati.",
    "balance": "La tesi del libro: di solito l'IA può essere costruita e usata in "
               "sicurezza, purché questi problemi morali siano presi sul serio.",
    "baby_bathwater": "Tenere i benefici dell'IA senza i suoi danni — non buttare il "
                      "bambino con l'acqua sporca — e dare all'etica dell'IA "
                      "l'attenzione che merita.",
}

NOT_CLAIM = [
    "Questo è un companion non ufficiale, non il libro. Parafrasiamo gli autori con "
    "parole nostre; leggete il libro per la loro argomentazione completa.",
    "Le undici storie sono quelle scelte dagli autori per l'Introduzione — un piccolo "
    "campione che definiscono 'la punta dell'iceberg', non una rassegna di tutta l'IA.",
    "Non verifichiamo gli eventi in modo indipendente; li riportiamo come fa il libro e "
    "colleghiamo la fonte citata dagli autori (e, in questa edizione, una fonte italiana).",
    "Le cifre usano unità diverse e non sono confrontabili su un'unica scala — mostrano "
    "la portata della posta in gioco, non una classifica.",
    "Le fotografie sono immagini rappresentative con licenza libera (accreditate sotto); "
    "salvo indicazione contraria non ritraggono l'evento esatto. Bicchiere e bilancia "
    "sono schematici.",
]

ATTRIBUTION = {
    "kicker": "Un companion visivo non ufficiale al libro",
    "selection": "Le undici storie di buone/cattive notizie qui sotto sono gli esempi "
                 "scelti dagli autori per l'Introduzione del libro («Qual è il problema?»).",
    "method": "Le parafrasiamo con parole nostre e colleghiamo le fonti citate dagli "
              "autori — questo companion non sostituisce la lettura del libro.",
    "not_affiliated": "Non affiliato né approvato dagli autori o da Pelican Books.",
    "read_the_book": "Leggi il libro",
}

LANG = "it"
LANG_NAME = "Italiano"
OTHER_LANG_LABEL = "English"
OTHER_LANG_HREF = "../"

UI = {
    "good_news": "Buone notizie",
    "bad_news": "Cattive notizie",
    "ref": "rif.",
    "source": "Fonte",
    "from_book": "dall'Introduzione del libro",
    "companion": "Un companion visivo · parafrasato, con le fonti del libro",
}

SCENE_TITLES = {
    "framing": {"eyebrow": "Moral AI · l'Introduzione del libro",
                "title": "Qual è il problema?", "foot": "premessa"},
    "ledger":  {"eyebrow": "Undici ambiti · dall'Introduzione",
                "title": "La stessa tecnologia, due volti", "foot": "il registro"},
    "numbers": {"eyebrow": "Cifre riportate nel libro",
                "title": "In cifre", "foot": "in cifre"},
    "values":  {"eyebrow": "Ciò che esplora il resto del libro",
                "title": "Sei valori morali in gioco", "foot": "i valori"},
    "thesis":  {"eyebrow": "La tesi del libro",
                "title": "Non buttare via il bambino", "foot": "la tesi"},
}

STRINGS = {
    "alarm_sub": "L'allarme si diffonde in fretta.",
    "glass_empty": "mezzo vuoto",
    "glass_full": "mezzo pieno",
    "numbers_note": "unità diverse — mostrate per dare la scala, non una classifica",
    "under": "sottovalutare\ni pericoli",
    "over": "sopravvalutare\ni pericoli",
    "balanced": "affrontati con serietà",
    "section_label": "Introduzione · Qual è il problema?",
    "endcard_tagline": "un companion visivo · parafrasato, con le fonti del libro",
}

# ---------------------------------------------------------------------------
# PAGE chrome — stringhe usate solo dal sito (build_site.py).
# ---------------------------------------------------------------------------
PAGE = {
    "blurbs": {
        "framing": "I pessimisti temono il peggio; gli ottimisti non vedono l'ora. La "
                   "risposta del libro a «mezzo vuoto o mezzo pieno?» è: entrambi.",
        "ledger":  "Undici ambiti quotidiani, ciascuno con una buona e una cattiva "
                   "notizia — a volte dalla stessa identica tecnica.",
        "numbers": "Le cifre dell'Introduzione, ciascuna nel suo contesto. Unità diverse "
                   "— mostrate per dare la scala, mai come una classifica.",
        "values":  "Sei valori morali attorno a cui ruota il resto del libro — e il "
                   "monito degli autori che l'elenco non è esaustivo.",
        "thesis":  "Non sottovalutare i pericoli dell'IA; ma non sopravvalutarli "
                   "nemmeno. Tenere il bambino, buttare l'acqua sporca.",
    },
    "references_eyebrow": "Provenienza",
    "references_h": "Riferimenti",
    "references_lead": "Le fonti citate dagli autori nell'Introduzione del libro (note "
                       "1–23). Dove possibile aggiungiamo una fonte in italiano.",
    "credits_eyebrow": "Crediti immagini",
    "credits_h": "Immagini rappresentative",
    "credits_lead": "Fotografie con licenza libera (in prevalenza Wikimedia Commons). "
                    "Salvo indicazione contraria, illustrano l'ambito e non l'evento esatto.",
    "notclaim_pre": "Cosa ", "notclaim_em": "non", "notclaim_post": " sosteniamo",
    "good_label_short": "buona", "bad_label_short": "cattiva",
    "footer_companion": "Un companion visivo non ufficiale all'Introduzione («Qual è il "
                        "problema?») del libro di",
    "footer_method": "Cifre, nomi e date sono ripresi dal libro; la prosa è una nostra "
                     "parafrasi. Animazioni realizzate a mano in Manim CE.",
    "footer_staging": "Versione di staging · non ufficiale · non affiliata né approvata "
                      "dagli autori o da Pelican Books.",
    "lang_switch": "English",
}
