export const meta = {
  name: 'moral-ai-intro-build',
  description: 'Render 5 Manim scenes (review+fix) and gather licensed images for each cited case, then fact-check',
  phases: [
    { title: 'Render', detail: 'render + adversarial frame review + fix per scene' },
    { title: 'Images', detail: 'fetch + verify a free-licensed image per case' },
    { title: 'FactCheck', detail: 'verify on-screen literals vs intro_data + image credits' },
  ],
}

const DIR = '/mnt/d/visualization_manim'

const SCENES = [
  { file: 'scenes/scene_01_framing.py', cls: 'Framing',
    mp4: 'media/videos/scene_01_framing/720p30/Framing.mp4',
    spec: 'Pessimist vs optimist camps, then a schematic glass that is BOTH half empty (coral) and half full (teal); ends on "Our answer is: both." Verbatim alarm + verdict question in quotes.' },
  { file: 'scenes/scene_02_ledger.py', cls: 'DoubleEdgedLedger',
    mp4: 'media/videos/scene_02_ledger/720p30/DoubleEdgedLedger.mp4',
    spec: 'A two-column ledger cycling through ALL 11 domains; for each a teal good-news headline (left) and coral bad-news headline (right) with a "ref N" tag; 11 progress dots; ends with "tip of the iceberg" + the 11 domain names.' },
  { file: 'scenes/scene_03_numbers.py', cls: 'ByTheNumbers',
    mp4: 'media/videos/scene_03_numbers/720p30/ByTheNumbers.mp4',
    spec: 'Seven fact cards, one per D.NUMBERS entry, each big value + label + context + ref tag; a note says units are not comparable. Cards must not overlap or clip.' },
  { file: 'scenes/scene_04_values.py', cls: 'SixValues',
    mp4: 'media/videos/scene_04_values/720p30/SixValues.mp4',
    spec: 'Six value cards (3x2 grid) name + one-line illustration, each with a coloured accent bar; ends with the verbatim "not exhaustive" caveat. No clipping at edges.' },
  { file: 'scenes/scene_05_thesis.py', cls: 'BabyAndBathwater',
    mp4: 'media/videos/scene_05_thesis/720p30/BabyAndBathwater.mp4',
    spec: 'A balance that wobbles then settles LEVEL (neither under- nor over-estimate), then the verbatim thesis ("keep the AI baby without its bathwater"), then an end card with book title/authors/section.' },
]

const CASES = [
  { id: 'transportation_good', subject: 'an autonomous / self-driving car', q: ['Waymo self-driving car', 'Google self-driving car', 'autonomous car'] },
  { id: 'transportation_bad',  subject: 'a Tesla Model S car', q: ['Tesla Model S car', 'Tesla Model S'] },
  { id: 'military_good',       subject: 'a bomb-disposal / EOD robot', q: ['bomb disposal robot', 'EOD robot military', 'PackBot robot'] },
  { id: 'military_bad',        subject: 'an Oerlikon anti-aircraft autocannon', q: ['Oerlikon 35mm anti-aircraft gun', 'Oerlikon GDF autocannon', 'anti-aircraft autocannon'] },
  { id: 'politics_good',       subject: 'a US congressional districts map (redistricting)', q: ['North Carolina congressional districts map', 'congressional district map', 'redistricting map'] },
  { id: 'politics_bad',        subject: 'Facebook (Cambridge Analytica data context)', q: ['Facebook headquarters sign', 'Facebook Menlo Park headquarters', 'Facebook building'] },
  { id: 'law_good',            subject: 'a legal contract being signed', q: ['contract signing document', 'signing contract pen', 'legal document signature'] },
  { id: 'law_bad',             subject: 'a courtroom / judge gavel', q: ['courtroom', 'judge gavel court', 'court bench'] },
  { id: 'medicine_good',       subject: 'IBM Watson computer', q: ['IBM Watson computer', 'IBM Watson Jeopardy', 'IBM Watson'] },
  { id: 'medicine_bad',        subject: 'a hospital corridor / ward', q: ['hospital corridor', 'hospital ward', 'hospital interior'] },
  { id: 'investment_good',     subject: 'a financial markets / trading screen', q: ['stock market display screen', 'financial trading screen', 'stock ticker board'] },
  { id: 'investment_bad',      subject: 'a falling stock-market chart (the 2010 Flash Crash)', q: ['2010 Flash Crash chart', 'stock market crash chart', 'falling stock chart'] },
  { id: 'marketing_good',      subject: 'an HIV/AIDS red awareness ribbon', q: ['red ribbon HIV', 'AIDS red ribbon', 'red awareness ribbon'] },
  { id: 'marketing_bad',       subject: 'a Target store', q: ['Target Corporation store', 'Target store exterior', 'Target retail store'] },
  { id: 'art_good',            subject: 'music streaming / headphones', q: ['headphones music', 'music streaming smartphone', 'listening headphones'] },
  { id: 'art_bad',             subject: 'AI-generated portrait or an ornate empty gold frame', q: ['Edmond de Belamy', 'ornate empty gold picture frame', 'gilded picture frame'] },
  { id: 'media_good',          subject: 'a seismograph / earthquake recording', q: ['seismograph', 'seismogram earthquake', 'seismometer recording'] },
  { id: 'media_bad',           subject: 'a deepfake / digitally manipulated face', q: ['deepfake', 'face swap manipulation', 'digital face manipulation'] },
  { id: 'surveillance_good',   subject: 'an anti-poaching wildlife ranger', q: ['anti-poaching ranger', 'wildlife ranger patrol Africa', 'game ranger anti poaching'] },
  { id: 'surveillance_bad',    subject: 'facial-recognition surveillance', q: ['facial recognition surveillance', 'surveillance camera city', 'CCTV surveillance camera'] },
  { id: 'environment_good',    subject: 'a farm sprayer / tractor in a field (precision agriculture)', q: ['agricultural sprayer tractor field', 'precision agriculture tractor', 'crop sprayer machine'] },
  { id: 'environment_bad',     subject: 'a data center / server room (AI compute & carbon)', q: ['data center server room', 'server racks data center', 'computer server room'] },
]

const RENDER_SCHEMA = {
  type: 'object', additionalProperties: false,
  required: ['scene', 'cls', 'status', 'iterations', 'mp4_exists', 'frames_reviewed', 'literals_ok', 'issues_found', 'fixes_applied', 'duration_sec'],
  properties: {
    scene: { type: 'string' }, cls: { type: 'string' },
    status: { type: 'string', enum: ['clean', 'issues_remain', 'render_failed'] },
    iterations: { type: 'integer' },
    mp4_exists: { type: 'boolean' },
    frames_reviewed: { type: 'integer' },
    literals_ok: { type: 'boolean' },
    duration_sec: { type: 'number' },
    issues_found: { type: 'array', items: { type: 'string' } },
    fixes_applied: { type: 'array', items: { type: 'string' } },
  },
}

const IMAGE_SCHEMA = {
  type: 'object', additionalProperties: false,
  required: ['case', 'status', 'appropriate', 'note'],
  properties: {
    case: { type: 'string' },
    status: { type: 'string', enum: ['ok', 'replaced', 'none', 'error'] },
    file: { type: 'string' },
    license: { type: 'string' },
    artist: { type: 'string' },
    source_url: { type: 'string' },
    query_used: { type: 'string' },
    appropriate: { type: 'boolean' },
    note: { type: 'string' },
  },
}

const FACT_SCHEMA = {
  type: 'object', additionalProperties: false,
  required: ['ok', 'mismatches', 'completeness', 'images_with_credit', 'notes'],
  properties: {
    ok: { type: 'boolean' },
    mismatches: { type: 'array', items: {
      type: 'object', additionalProperties: false,
      required: ['scene', 'onscreen', 'expected'],
      properties: { scene: { type: 'string' }, onscreen: { type: 'string' }, expected: { type: 'string' } } } },
    completeness: { type: 'object', additionalProperties: false,
      required: ['domains', 'numbers', 'values'],
      properties: { domains: { type: 'integer' }, numbers: { type: 'integer' }, values: { type: 'integer' } } },
    images_with_credit: { type: 'integer' },
    notes: { type: 'string' },
  },
}

function renderPrompt(s) {
  return `You are polishing ONE Manim scene for a visual companion to the book "Moral AI" (its Introduction).

Working directory: ${DIR}  (cd there first).
Scene file: ${s.file}   Class: ${s.cls}
Render command (the env is NOT on PATH, use this absolute path EXACTLY):
  ~/manim-env/bin/manim -qm --disable_caching ${s.file} ${s.cls}
Resulting video: ${s.mp4}

First, Read scenes/intro_data.py (the single source of truth for every number/name/quote) and scenes/style.py (shared helpers + palette). Then Read ${s.file}.

Then run this loop, MAX 3 iterations:
  1. Render with the command above. If it errors, read the traceback, fix the bug in ${s.file} ONLY, and re-render until it renders.
  2. Get duration:  ffprobe -v error -show_entries format=duration -of csv=p=0 ${s.mp4}
  3. mkdir -p /tmp/rev ; extract ~6 frames across the timeline (at roughly 12%, 30%, 48%, 66%, 84% of duration, plus the final frame via  -sseof -0.5 ):
       ffmpeg -y -loglevel error -ss <t> -i ${s.mp4} -frames:v 1 /tmp/rev/${s.cls}_<t>.png
  4. READ every extracted PNG and adversarially review for:
       - any text or shape CLIPPED at a frame edge or spilling outside the safe area (x in [-7,7], y in [-4,4])
       - OVERLAPPING / colliding text (especially body text colliding with the footer line, the title, or the other column)
       - text too small to read, or wrong colour
       - any on-screen NUMBER, NAME, DATE or QUOTE that disagrees with scenes/intro_data.py
       - general polish: alignment, even spacing, nothing awkward
  5. If you find ANY issue, fix it in ${s.file} ONLY (NEVER edit style.py or intro_data.py — if a shared helper seems wrong, report it instead), then re-render and re-review.

House style to preserve: background #11141a; bold white title pinned to top; teal #5ac8a8 = good news, coral #e0736b = bad news; keep ~18-32s; import every manim name you use.
Intended content of THIS scene: ${s.spec}

You MUST actually Read the final frames before declaring "clean". Report duration_sec from ffprobe, how many frames you reviewed, whether on-screen literals matched intro_data.py, the issues you found, and the fixes you applied. Return the structured verdict.`
}

function imagePrompt(c) {
  const qs = c.q.map(x => `--query "${x}"`).join(' ')
  return `Find ONE freely-licensed, tasteful, representative image for a website case.

Working directory: ${DIR}  (cd there first).
Case id: ${c.id}
Subject it should depict: ${c.subject}

Step 1 - auto fetch (Wikimedia Commons, free licenses only):
  python3 tools/commons_fetch.py auto --case ${c.id} --out site_media/images ${qs}
This downloads the best candidate to site_media/images/${c.id}.jpg (or .png) and writes site_media/images/${c.id}.json with attribution, and prints a JSON line.

Step 2 - VERIFY: Read the downloaded image file (site_media/images/${c.id}.jpg or .png) and judge honestly:
  does it clearly and appropriately depict "${c.subject}"? Is it tasteful (no logo-only, no meme, nothing NSFW or offensive, not the wrong subject)?

Step 3 - if it is NOT a good fit:
  run  python3 tools/commons_fetch.py list --query "<one of the queries>" --limit 12
  to see candidates (each shows pageid, mime, size, license, title). Choose a better one and fetch it specifically:
    python3 tools/commons_fetch.py get --case ${c.id} --out site_media/images --query "<query>" --pageid <PAGEID>
  (or use --title "<substring>"). Re-Read and re-judge. You may invent a better query of your own. Try at most ~3 times.

If after your tries no FREE, appropriate image exists, return status "none" (the website will fall back to a clean typographic tile — that's acceptable, do not force a bad image).

Read the final site_media/images/${c.id}.json and report its license + artist + source_url in your structured result. Set appropriate=true only if you actually Read the image and it fits.`
}

function factPrompt() {
  return `Verify the visual companion's on-screen text against its single source of truth, and check image credits.

Working directory: ${DIR}  (cd there first).
1. Read scenes/intro_data.py (the source of truth) and all five scene files: scenes/scene_01_framing.py, scenes/scene_02_ledger.py, scenes/scene_03_numbers.py, scenes/scene_04_values.py, scenes/scene_05_thesis.py.
2. For EVERY on-screen literal in the scenes that is a NUMBER, NAME, DATE, or QUOTED phrase, confirm it is either pulled from intro_data (referenced as D.something) or matches intro_data.py exactly. Flag any invented or mismatched literal as a mismatch {scene, onscreen, expected}.
3. Completeness: confirm scene_02 iterates ALL 11 entries of D.DOMAINS, scene_03 shows ALL 7 of D.NUMBERS, scene_04 shows ALL 6 of D.VALUES. Report the counts you can verify from the code.
4. Images: list site_media/images/*.json (use:  ls site_media/images/*.json ), Read each, and count how many have a non-empty "license" AND ("artist" or "source_url"). Report that count as images_with_credit.
Return the structured report. ok=true only if there are zero mismatches.`
}

log('Launching render lane (5 scenes) + image lane (22 cases) in parallel')

const [renders, images] = await parallel([
  () => pipeline(SCENES, s =>
    agent(renderPrompt(s), { label: `render:${s.cls}`, phase: 'Render', agentType: 'general-purpose', schema: RENDER_SCHEMA })),
  () => pipeline(CASES, c =>
    agent(imagePrompt(c), { label: `img:${c.id}`, phase: 'Images', agentType: 'general-purpose', schema: IMAGE_SCHEMA })),
])

log('Lanes complete -> fact-check barrier')
phase('FactCheck')
const factcheck = await agent(factPrompt(), { label: 'fact-check', agentType: 'general-purpose', schema: FACT_SCHEMA })

const renderClean = renders.filter(Boolean).filter(r => r.status === 'clean').length
const imgOk = images.filter(Boolean).filter(i => i.status === 'ok' || i.status === 'replaced').length
log(`Done: ${renderClean}/${SCENES.length} scenes clean, ${imgOk}/${CASES.length} images sourced`)

return { renders: renders.filter(Boolean), images: images.filter(Boolean), factcheck }
