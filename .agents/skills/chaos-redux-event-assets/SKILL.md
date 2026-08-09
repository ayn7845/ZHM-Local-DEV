---
name: the event asset skill
description: Use when creating, sourcing, processing, converting, organizing, wiring, or documenting visual assets for HOI4.
---

# HOI4 Event Assets

Use this skill when a HOI4 task requires final visual assets.

This includes event assets, UI assets, focus tree assets, country assets, achievement assets, generated icons, sourced event art, generated icon art, animated sprites, animated portraits, sprite sheets, GIF previews, and any asset package that must be wired into the mod.

## 1. Core purpose

The goal is to turn asset needs from an event spec into real HOI4-ready files.

The asset workflow must produce:

- source artwork
- processed PNG previews
- final DDS files
- correct file placement
- sprite handoff notes for the main agent
- documentation of what was created

Do not leave assets as loose generated or downloaded images.

If an asset is used by the event, it must be processed, placed, documented, and handed off so the main agent can wire it cleanly.

## 2. When to use this skill

Use this skill for:

- event pictures
- report event pictures
- news event pictures
- super-event images
- decision icons
- decision category icons
- idea icons
- national spirit icons
- officer corps spirit icons
- focus icons
- achievement icons
- flags
- leader portraits
- faction emblems
- UI panels
- progression-state variants
- animated sprites
- animated UI pieces
- animated leader portraits
- sprite sheets and GIF previews for review
- any other static or animated visual asset required by a HOI4 event or mechanic

Use this skill when the user asks the agent to create, source, process, or wire final visual assets.

Use this skill when the implementation task includes generated, sourced, or user-provided PNG files that must be turned into HOI4-ready assets.

Use `the frame animation skill` together with this skill when an asset needs animation. Animated final assets must come from planned source frames, not from moving, scaling, rotating, warping, blurring, recoloring, or filtering one still image.


## 2.1 Custom subagent split

When actual files must be created, route the work through narrow project subagents instead of one broad asset worker.

The main agent decides which subagent to spawn, gives it a bounded asset prompt, reviews the output, and performs final wiring.

Use:

- `chaosx_asset_source_researcher` for real or archival image sourcing, real leader portraits, historical flags, historically attested symbols, user-provided source photos, and report/news/super-event images that must depict a real photographed person, place, object, or historical document
- `chaosx_generated_event_art` for generated non-icon event art, including fictional or alternate-history report images, news images, super-event images, fictional portraits, fictional flags, faction emblems, UI panels, dossier art, and progression-state base art
- `chaosx_icon_artist` for focus icons, idea icons, national spirit icons, officer corps spirit icons, decision icons, decision category icons, achievement icons, and tech icons

For animated work, route by asset type first. Then require the chosen asset subagent to follow `the frame animation skill` for frame plans, per-frame source art, normalization, contact sheets, preview GIFs, frame sheets, static fallbacks, and animation handoffs.

Asset subagents may create:

- source files
- processed PNG previews
- final DDS files
- contact sheets
- manifests
- `docs/assets/<event_id>_<event_slug>/gfx_handoff.md`

Asset subagents must not edit `.gfx`, localisation, GUI, event, focus, idea, decision, scripted effect, scripted trigger, on_action, history, country, or spreadsheet files unless the parent explicitly grants that scope.

The main agent owns final `.gfx` sprite definitions, gameplay references, docs alignment, spreadsheet alignment, and validation.

A good parent prompt to an asset subagent includes the event id, asset list, asset type, target size, source mode, final DDS folder, sprite name if already registered, reference folder, visual direction, source constraints, and anything the subagent must mark blocked instead of substituting.


## 2.2 Final asset placement and naming

Event-owned final assets should be grouped under an event-scoped folder whenever the engine surface uses explicit sprite or texture paths.

Use this folder form:


Place the event folder directly under the asset category folder, for example `gfx/event_pictures/014_cannibalism/` or `gfx/interface/ideas/014_cannibalism/`. Do not insert a project namespace layer such as `gfx/event_pictures/hoi4/014_cannibalism/`; the mod root already provides the project namespace.

Do not leave new event assets loose in category roots such as `gfx/event_pictures/`, `gfx/super_events/`, `gfx/interface/ideas/`, `gfx/interface/goals/`, `gfx/interface/decisions/`, or `gfx/leaders/` unless that root placement is an engine-facing lookup requirement.

Root-only and engine-convention exceptions:

- `gfx/achievements/` must keep achievement DDS files directly in the root. Do not create `gfx/achievements/<event_id>_<event_slug>/` subfolders unless a new engine behavior has been verified locally. Achievement filenames must match the full achievement ids from `common/achievements/`, so event-owned achievement ids and triplet filenames should use `<event_id>_<event_slug>_<achievement_name>{,_grey,_not_eligible}.dds` or the exact established id if it includes an ordinal.
- `gfx/flags/`, `gfx/flags/medium/`, and `gfx/flags/small/` must keep HOI4 tag/ideology filenames. Do not put flags into event folders; use cosmetic tags or route-specific tag filenames when an event needs transformed flags.

Shared or non-event systems may use a clear shared/system folder. Do not force shared assets into an event folder just to avoid a root directory.

When moving or adding an asset, update every `.gfx`, `.gui`, event, idea, decision, focus, localisation, and documentation reference that names the old path or sprite. Keep sprite names stable unless the engine-facing identifier itself has to change, as with achievement ids.

Super-event audio follows the `the super-events skill` convention. Final music belongs under `music/<event_id>_<event_slug>/super_event_<super_event_id>_<super_event_name>.ogg`, and matching sound-channel files belong under `sound/<event_id>_<event_slug>/super_event_<super_event_id>_<super_event_name>.wav`. Do not create persistent `music/source/` or `music/super_events/` folders; preserve source downloads under docs/assets source-audio paths instead.

## 3. Asset source rules

Choose the source mode based on asset type.

### Scene-first and mood-first selection rule

Do not default event art to maps, cartographic overlays, arrows, staff tables, conference rooms, or generic war-room compositions unless that is the strongest visual for the specific asset.

For HOI4, many event visuals should focus on the actor, force, symbol, ritual, creature, crowd, machine, government, army, leader, or strange condition behind the event. The image should usually make the event feel active and dangerous, not merely show that territory changed.

Prefer visuals that show:

- a country, movement, army, cult, council, machine, plague, or supernatural force as the subject
- people, banners, ruins, storms, fires, shadows, masks, relics, halls, crowds, weapons, monuments, or rituals
- obsession, wrath, zeal, panic, corruption, transformation, prophecy, dread, awe, or other event-specific mood
- fantasy, surreal, mythic, occult, symbolic, or unexplained elements when the event concept supports them
- a clear subject and strong atmosphere over neutral geography

Avoid making the main visual read like:

- a map has changed
- borders have shifted
- officers are discussing an expansion route
- the art is mainly a strategic diagram with decoration
- the scene is a generic command table without a strong event identity

Maps may still appear as secondary props when useful, but they should rarely be the main visual idea for fictional, alternate-history, high-chaos, supernatural, symbolic, or strange event assets.

### Use `$imagegen` for generated symbolic or fictional assets

Use Codex's official `$imagegen` skill by default for:

- idea icons
- focus icons
- decision icons
- decision category icons
- achievement icons
- fictional flags
- faction emblems
- fictional leader portraits
- UI panels
- progression-state base art
- other symbolic or fictional static assets

When creating generated assets, follow the `$imagegen` skill workflow. Do not define a separate image generation route in this skill.

For transparent icons, ask `$imagegen` for the required transparent output and follow the `$imagegen` skill's transparent image workflow. The final PNG must have real transparency, no fake checkerboard, no white halo, no white outline, and no opaque square background unless the asset type explicitly uses a painted backdrop.

If `$imagegen` is unavailable, report that clearly and stop before using an alternate route.

For generated animated assets, use `$imagegen` through `the frame animation skill`. Each animation frame must be generated or edited as its own source frame according to a frame plan. Do not use local filters, transforms, glow pulses, or offsets as the source of final motion.

### Choose source mode for event photo assets

Report images, news images, and super-event images may be either internet-sourced or generated.

Use internet-sourced imagery when the asset must show a real photographed person, specific real battle, real place, real object, real newspaper, real poster, real map, real archive item, or other verifiable historical material.

Use `$imagegen` when the event is fictional, alternate-history, symbolic, supernatural, high-chaos, or when a unique scene is more important than matching an existing archive image. Generated event-photo assets should be prompted as period-authentic documentary material, not modern cinematic concept art.

For generated World War II-era report/news/super-event images:

- prompt for 1936-1945 photographic technology, period composition, period clothing, period vehicles, period architecture, and documentary realism
- avoid modern streets, uniforms, props, weapons, vehicles, signage, UI overlays, cinematic color grading, and readable generated text
- keep the source PNG, processed preview, final DDS, prompt, and manifest entry
- record the source mode as generated and explain why generation fit better than sourcing
- never use generated images for real leader portraits or to fabricate a real person's likeness

Follow the repository web research rules from `AGENTS.md` when searching for source images.

For internet-sourced event photo assets that are meant to represent the World War II era, search for period-matching source imagery from roughly 1936 to 1945 unless the event spec gives a narrower date range. Prefer contemporary photographs, war correspondents' photographs, press agency images, propaganda posters, maps, newspapers, official records, government or military archive images, museum scans, library scans, and period illustrations. Do not use modern photographs, reenactment images, film stills, AI-looking reconstructions, postwar uniforms, streets, weapons, vehicles, buildings, colorized tourist photos, reenactments, or modern props when they do not fit the era. If no suitable period source can be found, either generate a period-authentic fictional/documentary image when the asset does not require a real source, or mark the asset as blocked or `needs_user_review`.

Record the image source, source link, author or archive if available, license or public domain status if available, estimated date or date range, why the image fits the World War II era, and any uncertainty in the manifest.

### Real leader portraits

Do not generate a leader portrait for a real person.

For real people, use a real source image from the internet or a user-provided image, then crop, resize, process, convert, and document it. Use the repository web research tools when a source image is needed, and prefer public domain, archival, official, or clearly licensed images. If the person belongs to the World War II setting, prefer contemporary portraits, wartime photographs, news photographs, official portraits, military archive images, passport or identity photos, or archival illustrations. Do not use modern actors, reenactors, statues, cosplay, later fictional depictions, postwar images, or modern images that do not fit the era unless the user explicitly approves them as placeholders.

Real leader portraits should be processed toward the HOI4 portrait style rather than left as raw photos: bust or upper-torso crop, face readable, subdued contrast, mild painterly or period texture, HOI4-like color grading, no modern UI artifacts, no hard white cutout halo, and no over-smoothed face. Do not change the person's identity or generate missing facial features.

Record the source link, author or archive if available, license or public domain status if available, source image path, processed PNG path, final DDS path, and sprite name

For generated or sourced one-person leader portraits, the asset handoff must identify the portrait's gender presentation and any matching leader-name pool requirement. Female-presenting portraits must not be paired with male names and should require `female = yes` where a country leader is created directly. Male-presenting portraits must not be paired with female names or `female = yes`. Council, board, office, crowd, and symbolic-institution portraits should keep institutional leader names instead of personal random-name pools.


### Fictional leader portraits

Fictional leaders, invented councils, collective bodies, supernatural leaders, and symbolic regime portraits must use `$imagegen`.

Generated leader portraits should follow HOI4 leader portrait conventions: 156x210 final DDS unless an existing sprite uses another size, bust or upper-torso framing, strong face or governing-body focal point, subdued painterly finish, period-appropriate uniform or civilian clothing, transparent or HOI4-compatible portrait background as required by the existing asset pattern, and no text, labels, watermarks, modern UI, or meme-like exaggeration.

For generated one-person leader portraits, record the portrait's apparent gender presentation in the manifest and handoff. Female-presenting portraits require female leader-name pools and female leader metadata where the implementation surface supports it. Male-presenting portraits require male leader-name pools and must not be paired with female metadata. Never hand off a portrait in a way that lets implementation randomly assign names from the opposite gender pool. Council, committee, junta, crowd, office, or symbolic-body portraits should be marked as institutional leaders and use institutional names instead of personal random-name pools.

For council or collective leaders, use one clear symbolic council portrait rather than a cluttered crowd. Keep the subject readable at leader portrait size and document that the leader is fictional or collective.

### User-provided assets

If the user provides an image, treat it as a source asset.

Record that the image was user-provided in the manifest.

Still crop, resize, convert, place, wire, and document it like any other source asset.

## 4. Reference asset examples

This skill includes reference images that show how different HOI4 asset types should look.

Before generating, sourcing, processing, or wiring an asset, inspect the relevant reference folder for that asset type. Use the examples to match style, framing, contrast, readability, scale, texture, and HOI4 presentation.


Vanilla inspection should stay grounded in the installed HOI4 tree under `D:\SteamLibrary\steamapps\common\Hearts of Iron IV`.

Inspect the closest relevant `gfx`, `interface`, `common`, and `documentation` folders there before generating, sourcing, cropping, processing, or wiring new artwork. Use those live HOI4 examples for compatibility and style, not placeholder skill paths that were copied into the wrong workspace context.

If the needed asset type has no matching project-local reference folder, inspect the closest relevant folder and existing HOI4 or vanilla assets before choosing a style.
## 5. Generated artwork rules

Do not create core artwork from simple shapes, placeholders, contact sheets, layout-only mockups, empty UI boxes, or generated charts. Final art must be real generated, sourced, or user-provided artwork, not circles, rectangles, lines, gradients, geometric diagrams, or other primitive-shape stand-ins.

For super-event images, this rule is strict: final art must be a real scene, archival image, painted illustration, or generated documentary-style image. Do not use symbolic diagrams, flat icons, abstract geometry, title cards, or UI-like compositions as the final super-event image unless the user explicitly requests that exact visual approach and the exception is documented.

Use `$imagegen` for generated artwork and follow the `$imagegen` skill workflow for the source image.

Generated artwork must be real source art that can be processed into the final game asset. Final assets must be clean: must not have sticking artifacts, an icon is centered in the image, etc. Do not use contact sheets, review boards, or layout drafts as final source art.

## 5.1 Icon creation rules

Small gameplay icons must be readable at their final in-game size.

- Use transparent backgrounds for asset types that are transparent in vanilla, especially idea and decision icons and small symbolic interface icons.
- Keep unused pixels fully transparent. Do not leave a square opaque fill behind icons unless the asset type explicitly uses a painted frame or backdrop.
- Give the icon silhouette a dark or black outline and a subtle drop shadow when the icon is displayed over variable UI backgrounds. Do not leave some chroma green outline on the icon.
- Avoid tiny interior detail that disappears at 45x45 or 64x64. Favor one clear subject, strong value contrast, and a centered silhouette.
- Avoid fake checkerboard pixels, white halos, white outlines, oversized medallion fills, and square opaque backdrops.

For every generated icon, follow the `$imagegen` skill's transparent image workflow. Preserve the original generated image, create a processed PNG preview, convert to DDS, and validate the final appearance over a checker background before treating the icon as complete.

The final icon should have transparent unused canvas, no fake checker or matte pixels, no transparent holes inside the painted subject, a slight black outline, a subtle drop shadow, and a centered subject that remains readable at final size.

Generated icon packages must keep visible `$imagegen` source evidence: save the source atlas or source PNGs, record the prompt and source mode in the manifest, process to real transparent backgrounds, and include a contact sheet that shows final alignment, dimensions, transparency, and absence of white matte or opaque square backgrounds. Do not mark a generated icon complete if the final art is a primitive local drawing, a resized unrelated icon, or a locally assembled shape substitute instead of imagegen or sourced artwork.

## 5.2 Icon type separation rules

Focus icons, idea icons, national spirit icons, officer corps spirit icons, decision icons, decision category icons, achievement icons, and tech icons are separate asset types.

Never treat focus, idea, and decision icons as interchangeable.

Do not create focus icons first and then satisfy idea icons or decision icons by resizing, cropping, shrinking, recoloring, padding, or lightly editing the focus icon. This is not a valid asset workflow.

Each icon type must have its own asset-type-specific brief, reference inspection, source artwork, prompt or source choice, crop, target size, filename prefix, manifest entry, and final DDS output.

Shared visual themes are allowed only when every icon is still designed for its own in-game use:

- focus icons should read as full HOI4 focus art at 94x86 with focus-tree style detail and composition
- idea and national spirit icons should read as compact 64x64 symbolic spirit art without borrowing the full focus icon frame
- decision icons should read clearly at 32x32 with simpler shapes, stronger silhouettes, and less interior detail
- decision category icons should be designed for the category button or scripted GUI surface, not derived from a focus icon
- officer corps spirit icons should follow the vanilla officer corps spirit look and 45x45 transparent style
- achievement icons should follow achievement presentation rules and variant rules

If a mechanic needs matching focus, idea, and decision visuals, build them as a coordinated icon family. A coordinated family can share subject matter, symbols, colors, and lore cues, but each member still needs separate source art or a separate generated output designed for its target size and UI role.

The manifest must record the exact asset type for every icon and should note when icons are part of a coordinated family. Do not mark an icon complete if it only exists as a resized version of another icon type.

## 6. Required asset workflow

For every asset package:

1. Read the event spec, asset prompt, or implementation task.
2. Identify every required visual asset.
3. Group assets by usage type.
4. Split focus icons, idea icons, national spirit icons, officer corps spirit icons, decision icons, decision category icons, achievement icons, and tech icons into separate asset-type work items. Never satisfy one icon type by resizing or lightly editing another icon type.
5. Assign each asset a stable filename.
6. Assign each asset a sprite name if it needs one.
7. Identify the target size.
8. Identify the intended in-game use.
9. Inspect the matching reference folder from section 4 before generating, sourcing, processing, or wiring the asset.
10. Decide the source mode for each asset:
   - `$imagegen`
   - internet source image
   - user-provided source image
11. If the asset is animated, follow `the frame animation skill` before ordinary static processing. Write the animation brief and frame plan, create or approve the static fallback, generate or source every frame, then normalize the frame sequence.
12. For `$imagegen` assets, write a specific image generation prompt and create the base artwork by following the official `$imagegen` skill.
13. For internet-sourced assets, find a suitable source image and record its source link, author or archive if available, and license or public domain status if available.
14. For user-provided assets, record that the image was provided by the user.
15. Save the original generated, sourced, or provided image as a source PNG.
16. Crop and resize the image to the target size.
17. Save a processed PNG preview.
18. Convert the processed PNG to DDS 32 bit unsigned BGRB 8.8.8.8.
19. Move the DDS into the correct mod folder.
20. Create or update the asset manifest.
21. Create or update `gfx_handoff.md` for any asset that needs a sprite definition.
22. Update event docs or asset docs when the parent prompt grants that documentation scope.
23. Report all created files, proposed sprite names, final paths, blocked assets, and any handoff uncertainty.

Do not mark assets complete until the DDS files exist, the manifest is written, and the main agent has enough handoff information to wire every sprite without guessing.

## Asset depth from improvement addenda

When an improvement addendum asks for richer presentation, the asset handoff should name the visual states instead of asking for generic polish. A good asset request says what the player sees before activation, while active, when locked, when dangerous, when complete, and when the route has failed.

For scripted GUI, plan asset families. A panel usually needs a background, header, button states, value icons, warning indicators, progress frames, locked overlays, selected overlays, hover states, and any animated glow, particle, float, or pulse layers. The main agent owns `.gui` and `.gfx` wiring, but the asset package must provide clear sprite names, sizes, frame counts, static fallbacks, and contact sheets.

## 7. Asset package structure

When creating a new asset package, use a stable working folder.

Recommended working structure:


Final DDS files must be moved into the correct gameplay asset folders.

Do not keep final assets under `docs/assets/`.

## 8. Manifest requirements

Every asset package must include a markdown manifest.

Recommended path:


The manifest must list every asset.

Each asset entry should include:

- asset name
- related event id
- related event slug
- asset type
- intended in-game use
- source mode: `$imagegen`, internet source image, or user-provided source image
- image generation prompt if generated with `$imagegen`
- source link if internet-sourced
- source author, archive, or collection if available
- source date or estimated date range if internet-sourced
- license or public domain status if available
- era-fit note for World War II-era assets
- source PNG path
- processed PNG path
- final DDS path
- target size
- sprite name
- `.gfx` file
- localisation key if relevant
- related focus, idea, event, decision, UI element, or super-event if relevant
- notes
- asset status
- frame count, frame timing, loop behavior, and anchor point for animated assets
- static fallback path and animated sheet or frame-sequence path for animated assets
- source mode and source note for every animation frame when animated

Use `not_needed`, `planned`, `sourced`, `generated`, `processed`, `converted`, `handed_off`, `wired`, `complete`, `needs_user_review`, or `blocked` as asset statuses.

## 9. Standard HOI4 asset sizes

Use these sizes unless the event spec or an existing repo pattern gives a better project-specific requirement.

- report event images: 210x176
- news event images: 397x153, black and white
- leader portraits: 156x210
- flags small: 10x7
- flags medium: 41x26
- flags normal: 82x52
- tech icons small: 64x64
- tech icons medium: 132x52
- achievements: 64x64
- super-event images: 457x328
- decision icons: 32x32
- idea and national spirit icons: 64x64
- focus icons: 94x86

Use other sizes when the event's UI or asset type requires it.

When unsure, inspect the existing HOI4 pattern and vanilla HOI4 assets before choosing.

## 10. Naming rules

Use lowercase snake_case.

Keep names stable once they are wired into `.gfx`.

Recommended filename prefixes:

- idea icons: `idea_`
- focus icons: `goal_`
- decision icons: `decision_`
- decision category icons: `decision_category_`
- report event images: `report_event_`
- news event images: `news_event_`
- super-event images: `super_event_`
- achievement icons: `achievement_`
- leader portraits: `leader_`

For event-specific assets, include the event id or slug where useful. For example, all idea assets related to an event should go into one folder of that event.

## 11. Image generation prompt rules

Every `$imagegen` prompt should be specific enough to produce usable game art.

A good prompt should include:

- asset type
- target in-game use
- subject
- visual style
- readability requirements
- what must be avoided
- whether the result must be readable at small size

Do not ask for vague "cool icon" style outputs.

Do not rely on text inside generated images. Generated text is unreliable.

Prefer strong symbols, clear silhouettes, and readable composition.

For transparent icon prompts, explicitly request a transparent canvas, no fake checkerboard, no white rim, no white/colored outline, no glow, no sticker border, no opaque square background, and a clean silhouette suitable for HOI4 UI.

## 12. Internet source image rules

When using internet source images:

1. Search for images that fit the event tone, target use, and intended era.
2. For World War II-era event assets, search for source images from roughly 1936 to 1945 unless the event spec gives a narrower date range.
3. Prefer contemporary or near-contemporary public domain, archival, official, museum, library, newspaper, map, press photograph, propaganda poster, government record, military record, period illustration, or clearly licensed sources.
4. Reject modern photographs, reenactments, film stills, postwar streets, uniforms, props, weapons, vehicles, buildings, AI-looking reconstructions, and later stylized images when they do not fit the era.
5. Record source links, source date or estimated date range, and license or public domain status when available.
6. If licensing, date, or era fit is unclear, mark it as uncertain in the manifest.
7. Process the image into the correct HOI4 size and style.
8. Preserve the source image path and processed preview path.

For public-facing or uncertain assets, keep the manifest honest about the source status, date uncertainty, and World War II-era fit uncertainty.

## 13. Report event images

Report event images may use internet-sourced imagery or generated period-documentary imagery. Prefer generated report images when the event needs a unique fictional or alternate-history scene, staged document, invented location, or more specific visual than archive search can reliably provide. Use real sources when the image must depict a real person, real historical scene, or real archival document.

Report event images should look like documentary-style photographs, field documentation, or period documentary material.

For World War II-era subjects, prefer contemporary photographs, war correspondents' photographs, press agency images, propaganda posters, newspapers, maps, official records, military archive images, museum or library scans, or period illustrations. Do not use modern reenactment photos or modern documentary photos that visually belong to a later era.

Use:

- realistic or period-authentic source imagery
- black-and-white treatment with sepia applied
- World War II-era visual fit when the event belongs to that era
- period-appropriate framing where possible
- strong subject clarity
- natural composition
- no modern UI overlays
- no modern clothing, streets, weapons, vehicles, buildings, or props unless they are intentionally part of the event
- no generated text

Target size:


Report event images must be black and white with sepia applied. Do not leave report event images in full colour unless the user explicitly requests a colour exception, and record that exception in the manifest.

### Report-event card treatment

Report-event images use a finished `210x176` RGBA canvas. The source photograph is processed as a slightly tilted documentary card with transparent edge space and a soft drop shadow. The transparent corners are part of the style.

Do not ask `$imagegen` to create the tilted card. Generate or source the documentary photograph first, then apply the card treatment locally. This keeps the tilt, shadow, and margins consistent.

```bash
python tools/process_report_event_image.py source.png processed_report_event.png
python tools/process_report_event_image.py source_folder processed_folder
```

The script performs cover crop, black-and-white conversion, sepia application, grain, paper border, deterministic tilt, transparent canvas margin, and soft shadow. It writes RGBA PNG output. Convert the processed PNG to DDS through the normal repo workflow.

Validation:

- processed PNG is exactly `210x176`
- final DDS is exactly `210x176`
- corner pixels are transparent
- no hard photo pixels are clipped
- tilt is visible but subtle
- shadow is soft and not a thick border
- edge space is transparent, not black padding
- source remains readable after crop, tilt, shadow, and DDS conversion

Generated report images must still receive this local report-card treatment.

## 14. News event images

News event images may use internet-sourced imagery or generated period-news imagery. Prefer generated news images when the event needs a unique fictional or alternate-history scene, invented crisis, or scene that is unlikely to exist in archives. Use real sources when the image must depict a real person, real historical scene, or real archival item.

News images should look like black-and-white documentary photographs or period news illustrations.

For World War II-era subjects, prefer contemporary newspapers, news photographs, war correspondents' photographs, press agency images, propaganda posters, maps, official visual records, military archive images, museum or library scans, or period illustrations. Do not use modern reenactment photos, modern news photos, film stills, or later images that do not fit the era.

Use:

- old news photograph or period press illustration style
- World War II-era visual fit when the event belongs to that era
- clear central subject
- strong contrast
- period-appropriate composition
- no modern UI overlays
- no modern clothing, streets, weapons, vehicles, buildings, or props unless they are intentionally part of the event
- no generated text

Target size:


News images must be black and white.

Generated news images must be converted to black and white during processing, with period press contrast/grain and no modern color remnants. Record the source link and license or public domain status for internet-sourced images, or the generation prompt and source-mode rationale for generated images.

## 15. Super-event images

Super-event images may use internet-sourced imagery or generated art. Prefer generated super-event images for fictional, alternate-history, symbolic, supernatural, high-chaos, or emotionally specific moments where a unique composed image better fits the super-event role. Use internet sources when the image must depict a real historical person, real photographed event, or real archival artifact.

Super-event images should have:

- strong central composition
- clear dramatic theme
- readable subject
- enough contrast for HOI4 UI
- World War II-era visual fit when the event belongs to that era
- no generated text
- no modern clothing, streets, weapons, vehicles, buildings, props, film stills, or reenactment imagery when they do not fit the era
- no cluttered small details that disappear at final size

Target size:


If a super-event needs music, use `the super-events skill` and research suitable public domain or clearly licensed music. Final audio should use the event-scoped `music/<event_id>_<event_slug>/` and `sound/<event_id>_<event_slug>/` layout from that skill. Never create event or super-event audio from generated test tones, primitive waveforms, beeps, noise beds, or local oscillator output; that includes sine, square, triangle, and sawtooth waveforms.

For each track, document:

- title
- composer
- performer or recording source if relevant
- public domain status or license status
- source link
- why it fits
- suggested in-game use
- editing notes

Do not claim public domain status without checking.

If the license is unclear, mark it as uncertain or unsuitable.

## 16. Idea and national spirit icons

Idea and national spirit icons should look like compact HOI4-style icon art.

They should have:

- strong central symbol
- clear silhouette
- aged texture
- strong contrast
- readable meaning at 64x64
- no generated text

Target size:


Use `idea_` filename prefix.

These icons usually do not need the full focus icon frame.

Do not derive idea or national spirit icons from focus icons. They must be designed as 64x64 spirit-style icons from their own prompt or source art, even when they share a theme with a focus.

Use `$imagegen` for the base artwork unless the user provides or requests a specific source image.

Follow the `$imagegen` skill's transparent image workflow when the icon should have a transparent background.

