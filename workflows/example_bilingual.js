export const meta = {
  name: 'moral-ai-bilingual',
  description: 'Re-render 5 scenes in EN+IT (review+fix), find Italian-language sources per case, fact-check both',
  phases: [
    { title: 'Render', detail: 'each scene rendered EN+IT, frame-reviewed, fixed' },
    { title: 'ItSources', detail: 'find a reputable Italian-language article per case' },
    { title: 'FactCheck', detail: 'verify EN+IT literals, reduced verbatim, IT sources' },
  ],
}

const DIR = '/mnt/d/visualization_manim'
const MM = '~/manim-env/bin/manim -qm --disable_caching'

const SCENES = [
  { file: 'scenes/scene_01_framing.py', cls: 'Framing', stem: 'scene_01_framing',
    spec: 'Pessimist vs optimist, then a schematic glass that is both half-empty (coral) and half-full (teal); ends on the authors’ answer = "both/entrambi". All paraphrase, no quotation marks.' },
  { file: 'scenes/scene_02_ledger.py', cls: 'DoubleEdgedLedger', stem: 'scene_02_ledger',
    spec: 'Ledger cycling all 11 domains; teal good-news headline (left) + coral bad-news headline (right) each with a ref tag; ends with "tip of the iceberg" + the 11 domain names. NOTE: Italian headlines are LONGER — watch for wrapping/overflow in the IT render.' },
  { file: 'scenes/scene_03_numbers.py', cls: 'ByTheNumbers', stem: 'scene_03_numbers',
    spec: 'Seven fact cards (one per D.NUMBERS) with big value + label + context + ref tag; a note that units are not a ranking. Cards must not overlap or clip in either language.' },
  { file: 'scenes/scene_04_values.py', cls: 'SixValues', stem: 'scene_04_values',
    spec: 'Six value cards (3x2) name + one-line illustration + accent bar; ends with the "not exhaustive" caveat. Italian illustrations are longer — check they fit the cards.' },
  { file: 'scenes/scene_05_thesis.py', cls: 'BabyAndBathwater', stem: 'scene_05_thesis',
    spec: 'A balance that settles level, then the paraphrased thesis (keep the baby / lose the bathwater), then an end card with book title/authors/section. Watch IT line lengths.' },
]

const CASES = [
  { id: 'transportation_good', t: 'Steve Mahan, blind, rides a Google self-driving car', q: 'Steve Mahan auto a guida autonoma Google cieco' },
  { id: 'transportation_bad',  t: 'Joshua Brown killed in 2016 Tesla Autopilot crash', q: 'incidente mortale Tesla Autopilot 2016 Joshua Brown' },
  { id: 'military_good',       t: 'AI bomb-disposal / EOD robot saves lives', q: 'robot artificiere intelligenza artificiale disinnesco bombe' },
  { id: 'military_bad',        t: 'Oerlikon anti-aircraft gun killed 9, wounded 14 (South Africa, 2007)', q: 'cannone Oerlikon Sudafrica morti 2007 robot' },
  { id: 'politics_good',       t: 'AI draws fairer congressional districts (anti-gerrymandering)', q: 'algoritmi contro il gerrymandering distretti elettorali equi' },
  { id: 'politics_bad',        t: 'Cambridge Analytica used 87M Facebook users’ data in 2016 election', q: 'Cambridge Analytica 87 milioni dati Facebook elezioni 2016' },
  { id: 'law_good',            t: 'ThoughtRiver AI reviews legal contracts cheaply', q: 'intelligenza artificiale revisione contratti legali' },
  { id: 'law_bad',             t: 'Eric Loomis sentenced 6 years partly via opaque AI risk score (COMPAS)', q: 'Eric Loomis COMPAS algoritmo rischio condanna' },
  { id: 'medicine_good',       t: 'IBM Watson diagnosed a rare leukaemia in 2015 (Tokyo)', q: 'IBM Watson leucemia rara diagnosi Tokyo' },
  { id: 'medicine_bad',        t: 'Health algorithm favoured White over Black patients (Obermeyer 2019)', q: 'algoritmo sanitario bias razziale pazienti neri Obermeyer' },
  { id: 'investment_good',     t: 'Robo-advisers widen access to financial advice', q: 'robo-advisor consulenza finanziaria automatica' },
  { id: 'investment_bad',      t: 'The 2010 Flash Crash: Dow fell 998.5 points in minutes', q: 'Flash Crash 6 maggio 2010 Dow Jones crollo' },
  { id: 'marketing_good',      t: 'AI raised HIV testing among homeless youth by 25%', q: 'intelligenza artificiale prevenzione HIV giovani senza dimora' },
  { id: 'marketing_bad',       t: 'Target predicted a teen’s pregnancy from purchases (2012)', q: 'Target previsione gravidanza adolescente dati acquisti' },
  { id: 'art_good',            t: 'Spotify/Pandora AI recommends new music', q: 'Spotify intelligenza artificiale raccomandazione musica' },
  { id: 'art_bad',             t: 'AI artwork Edmond de Belamy sold for $432,500 at Christie’s', q: 'Edmond de Belamy ritratto intelligenza artificiale Christie’s asta' },
  { id: 'media_good',          t: 'LA Times Quakebot reports earthquakes faster', q: 'Quakebot algoritmo terremoti Los Angeles Times' },
  { id: 'media_bad',           t: 'Deepfakes in 2023 Turkish election (İnce withdrew)', q: 'deepfake elezioni Turchia 2023 video falso candidato' },
  { id: 'surveillance_good',   t: 'AI helps rangers catch poachers (PAWS)', q: 'intelligenza artificiale anti-bracconaggio ranger' },
  { id: 'surveillance_bad',    t: 'China uses facial recognition to track Uighurs (500k scans/month)', q: 'Cina riconoscimento facciale uiguri sorveglianza' },
  { id: 'environment_good',    t: 'Blue River see-and-spray targets only weeds', q: 'agricoltura di precisione intelligenza artificiale diserbo mirato' },
  { id: 'environment_bad',     t: 'Training one AI model can emit as much CO2 as five cars’ lifetimes', q: 'addestramento modello IA emissioni CO2 cinque automobili' },
]

const RENDER_SCHEMA = {
  type: 'object', additionalProperties: false,
  required: ['scene', 'cls', 'en_ok', 'it_ok', 'en_dur', 'it_dur', 'literals_ok', 'iterations', 'issues_found', 'fixes_applied'],
  properties: {
    scene: { type: 'string' }, cls: { type: 'string' },
    en_ok: { type: 'boolean' }, it_ok: { type: 'boolean' },
    en_dur: { type: 'number' }, it_dur: { type: 'number' },
    literals_ok: { type: 'boolean' },
    iterations: { type: 'integer' },
    issues_found: { type: 'array', items: { type: 'string' } },
    fixes_applied: { type: 'array', items: { type: 'string' } },
  },
}

const ITSRC_SCHEMA = {
  type: 'object', additionalProperties: false,
  required: ['case', 'found', 'note'],
  properties: {
    case: { type: 'string' },
    found: { type: 'boolean' },
    pub: { type: 'string' }, title: { type: 'string' },
    url: { type: 'string' }, date: { type: 'string' },
    note: { type: 'string' },
  },
}

const FACT_SCHEMA = {
  type: 'object', additionalProperties: false,
  required: ['ok', 'verbatim_quotes_found', 'mismatches', 'it_sources_found', 'notes'],
  properties: {
    ok: { type: 'boolean' },
    verbatim_quotes_found: { type: 'array', items: { type: 'string' } },
    mismatches: { type: 'array', items: {
      type: 'object', additionalProperties: false,
      required: ['where', 'detail'],
      properties: { where: { type: 'string' }, detail: { type: 'string' } } } },
    it_sources_found: { type: 'integer' },
    notes: { type: 'string' },
  },
}

function renderPrompt(s) {
  return `Polish ONE bilingual Manim scene for the "Moral AI" Introduction companion.

cd ${DIR}. Scene file: ${s.file}  Class: ${s.cls}
This scene renders in TWO languages via an env var; the SAME file is used for both.
Render commands (env not on PATH; use these EXACTLY):
  English:  MORALAI_LANG=en ${MM} --media_dir media_en ${s.file} ${s.cls}
  Italian:  MORALAI_LANG=it ${MM} --media_dir media_it ${s.file} ${s.cls}
Outputs:
  media_en/videos/${s.stem}/720p30/${s.cls}.mp4
  media_it/videos/${s.stem}/720p30/${s.cls}.mp4

First Read scenes/intro_data.py (EN source of truth), scenes/intro_data_it.py (IT), scenes/style.py (helpers), and ${s.file}.

Loop, MAX 3 iterations:
  1. Render BOTH languages with the commands above. Fix any traceback in ${s.file} ONLY and re-render.
  2. For EACH language: ffprobe the duration, then  mkdir -p /tmp/rev ; extract ~5 frames (≈15%,35%,55%,75%,95%) + the last (-sseof -0.5):
       ffmpeg -y -loglevel error -ss <t> -i <mp4> -frames:v 1 /tmp/rev/${s.cls}_<lang>_<t>.png
  3. READ every frame (EN and IT) and adversarially review for:
       - text/shape CLIPPED at an edge or outside x∈[-7,7], y∈[-4,4]
       - OVERLAPPING / colliding text (footer, title, neighbours)
       - too-small or wrong-colour text
       - on-screen literals disagreeing with the matching data module (EN vs intro_data, IT vs intro_data_it)
     Italian strings are usually LONGER than English — overflow/wrapping problems often appear only in the IT frames. Fix them.
  4. Fix issues in ${s.file} ONLY (NEVER edit style.py or the data modules — a fix to the shared file must keep BOTH languages clean). Re-render both and re-check.

House style: bg #11141a; bold white title at top; teal #5ac8a8 = good, coral #e0736b = bad; ~18-32s; import every manim name used.
Scene intent: ${s.spec}

You MUST Read the final frames of BOTH languages before declaring clean. Report en_ok/it_ok, durations, whether literals matched, issues found and fixes applied.`
}

function itSourcePrompt(c) {
  return `Find ONE reputable ITALIAN-LANGUAGE article about this case, for the Italian edition of the page.

cd ${DIR}.
Case id: ${c.id}
Topic (English): ${c.t}
Suggested Italian search: "${c.q}"

Use web tools (load via ToolSearch if needed: the jina MCP "search_web" and "read_url", or WebSearch + WebFetch).
1. Search for an article IN ITALIAN from a reputable outlet (e.g. Il Post, Corriere della Sera, la Repubblica, Wired Italia, ANSA, Il Sole 24 Ore, Internazionale, Agenda Digitale, Sky TG24, Rai News, Focus, Le Scienze). Avoid forums, social posts, machine-translated mirrors, and paywalled-only pages where possible.
2. ACTUALLY FETCH the candidate URL (read_url / WebFetch) and confirm: it returns real content, it is in Italian, and it is on-topic for this case. Do NOT return a URL you have not successfully fetched. Never invent a URL.
3. If you find and verify a good one, write the file site_media/it_sources/${c.id}.json (use the Write tool) with exactly:
   {"case":"${c.id}","found":true,"pub":"<outlet name>","title":"<article title>","url":"<url>","date":"<year or date if known, else empty>","note":"<why it fits>"}
   If after a few tries you cannot verify an Italian source, write the same file with {"case":"${c.id}","found":false,"note":"<what you tried>"} (the page will fall back to the original source).
Then return the same info as your structured result.`
}

function factPrompt() {
  return `Verify the bilingual companion. cd ${DIR}.
1. Read scenes/intro_data.py and scenes/intro_data_it.py.
2. VERBATIM CHECK: the brief was to AVOID reproducing the book word-for-word. Scan FRAMING, THESIS, VALUES_CAVEAT, NOT_CLAIM, ATTRIBUTION and the DOMAIN details in BOTH modules. List any string that still reads as a long word-for-word quotation of the book (a short idiom or the book's title/section name is fine). Report them in verbatim_quotes_found (ideally empty).
3. LITERALS: confirm numbers/names/dates are consistent between EN and IT modules (e.g. 87 million / 87 milioni; 998.5 / 998,5; $432,500 / 432.500 $; 9/14; 6 years / 6 anni; 2015; 500,000). Report any inconsistency as a mismatch {where, detail}.
4. IT SOURCES: run  ls site_media/it_sources/*.json 2>/dev/null  and Read them; count how many have "found": true and a non-empty "url". Report as it_sources_found. Spot-check 3 of the URLs look like real Italian outlets (not obviously fabricated).
5. Confirm both pages exist: index.html and it/index.html (ls).
Return the structured report. ok=true only if mismatches is empty.`
}

log('Render lane (5 scenes × EN+IT) + Italian-source lane (22 cases) in parallel')
const [renders, itsources] = await parallel([
  () => pipeline(SCENES, s =>
    agent(renderPrompt(s), { label: `render:${s.cls}`, phase: 'Render', agentType: 'general-purpose', schema: RENDER_SCHEMA })),
  () => pipeline(CASES, c =>
    agent(itSourcePrompt(c), { label: `it-src:${c.id}`, phase: 'ItSources', agentType: 'general-purpose', schema: ITSRC_SCHEMA })),
])

log('Lanes done -> fact-check')
phase('FactCheck')
const factcheck = await agent(factPrompt(), { label: 'fact-check', agentType: 'general-purpose', schema: FACT_SCHEMA })

const renClean = renders.filter(Boolean).filter(r => r.en_ok && r.it_ok).length
const itFound = itsources.filter(Boolean).filter(s => s.found).length
log(`Done: ${renClean}/${SCENES.length} scenes clean (EN+IT), ${itFound}/${CASES.length} Italian sources found`)
return { renders: renders.filter(Boolean), itsources: itsources.filter(Boolean), factcheck }
