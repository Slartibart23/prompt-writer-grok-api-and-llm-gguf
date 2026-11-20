// Texts of the Prompt Writer nodes for their language switch (English / Deutsch).
// English widget labels and tooltips come from the node definition (Python);
// this file holds the German ones plus every text of the buttons, dialogs and
// notifications in both languages. Display only: widget names, saved values,
// preset names and the prompts sent to the model never change with the language.

export const LANGUAGES = { en: "English", de: "Deutsch" };

const plural = (n, one, many) => `${n} ${n === 1 ? one : many}`;

const IMAGE_DE = (n) =>
  `Optionales Referenzbild ${n} von 4. Das Modell sieht es als 'Image ${n}'. Ein einzelnes Bild ` +
  "anschließen, keinen Batch (von einem Batch wird nur das erste Bild genutzt).\n" +
  "So nutzen die Auswahlen die Bilder:\n" +
  "- Caption > Describe image: image_1 ist das zu beschreibende Bild.\n" +
  "- Qwen-Image-Edit: image_1..3 sind die Eingangsbilder des Edits, in derselben " +
  "Reihenfolge wie im Edit-Workflow (Qwen nimmt höchstens 3).\n" +
  "- Seedream Edit: image_1..4 sind die Eingangsbilder des Edits (Image 1..4), in derselben " +
  "Reihenfolge wie im Seedream-Node.\n" +
  "- MiniMax H3 FL2VA: image_1 = Startbild, image_2 = Endbild.\n" +
  "- MiniMax H3 REF2VA: image_1..4 = Referenzbilder (Personen, Orte, Objekte, Stil).\n" +
  "- Seedance Reference: image_1..4 = Referenzbilder (Image 1..4), in derselben Reihenfolge " +
  "wie im Seedance-Node.\n" +
  "- Kling Omni und Grok Imagine Referenz-zu-Video: image_1..4 = @Image1..4, in derselben " +
  "Reihenfolge wie im Video-Node.\n" +
  "- Bild-zu-Video (Wan, Seedance, Kling, Veo, Grok Imagine): image_1 = Startbild (image_2 = " +
  "Endbild bei Start-/Endbild-Video).\n" +
  "- GPT Image, Nano Banana, Grok Imagine Image, Flux 3: image_1..4 = Eingangsbilder zum " +
  "Bearbeiten oder als Referenz.\n" +
  "- Alle anderen Auswahlen: optionaler visueller Kontext, aus dem das Modell Details übernimmt.\n" +
  `- Mit gesetzter person_${n} und 'Bild N = Person N' an: image_${n} ist ein Foto dieser Person.\n` +
  "Bilder kosten zusätzliche Tokens; max. Bildseite steuert die Upload-Größe.";

const PERSON_DE = (n) =>
  `Person ${n} aus deiner Bibliothek (Button '👤 Personen & Stile...'), gewählt über ihre ` +
  "Bezeichnung. Name im Prompt (nicht die Bezeichnung), Geschlecht, LoRA-Trigger, " +
  "Beschreibung und Stimme kommen in den Prompt und sind verbindlich; der Name erscheint " +
  "immer, damit jede Pose und Handlung eindeutig dieser Person zugeordnet ist. Im Text " +
  `sprichst du die Person mit Namen oder als 'Person ${n}' an. (none) = keine Person. ` +
  "Ein Eintrag, dessen Beschreibung mit 'A group of' beginnt, ist eine Gruppe benannter " +
  "Personen in einem Slot.";
const LOCK_DE = " Gesperrt, solange der Eingang 'Personen' angeschlossen ist.";
const NOIMG_DE = (n) =>
  ` Es gibt nur vier Bild-Eingänge: person_${n} hat kein eigenes Bild, 'Bild N = Person N' gilt ` +
  "für sie nicht.";
const SYSLOCK_DE =
  " Gesperrt, solange eine System Prompt Library im Modus 'replace' am Eingang 'Systemprompt' " +
  "hängt: dieser Node legt dann den Systemprompt fest.";

const STYLE_DE = (n) =>
  `Stil-Baustein ${n} aus deiner Bibliothek (Button '👤 Personen & Stile...'): ein ` +
  "gespeicherter Text wie ein Kameralook, eine Lichtstimmung oder eine Verbotsliste. Er wird " +
  "auf jedes Ergebnis angewendet und ist verbindlich. (none) = aus.";

const WORDS_DE =
  "Optionale Länge des erzeugten Prompts in Wörtern: min. Wörter / max. Wörter. 0 = aus " +
  "(dann gilt die Längenvorgabe der Auswahl). Gesetzt ist die Spanne für jede Auswahl " +
  "verbindlich, auch für eigene Systemprompts. In Tag-Listen zählt jeder Tag als ein Wort; " +
  "mehrteilige Formate (MiniMax H3) wenden sie auf die Hauptbeschreibung an.";

// German label and tooltip per widget, input socket and output of the node.
export const NODE_TEXT_DE = {
  preset: { label: "Aufgabe", tooltip:
    "Die Aufgabe. Eine Auswahl füllt Systemprompt, Negativprompt, Temperatur, top_p und " +
    "max. Tokens mit passenden Werten. Ändere sie frei und speichere sie mit 'Auswahl " +
    "speichern als...' unter eigenem Namen.\n" +
    "Generation > ...: eine kurze Idee oder Stichworte zu einem vollständigen Prompt für " +
    "dieses Modell ausbauen.\n" +
    "Caption > ...: eine vorhandene Caption treu (ohne neue Inhalte) in den Prompt-Stil " +
    "dieses Modells umschreiben.\n" +
    "Die Eingabe darf in jeder Sprache sein; die Ausgabe ist immer Englisch." },
  text: { label: "Eingabe", tooltip:
    "Deine Eingabe, in jeder Sprache: eine kurze Idee, eine vorhandene Caption oder ein " +
    "Bearbeitungswunsch. Du kannst auch einen Text-Ausgang (z. B. JoyCaption oder den Text " +
    "File Loader) an dieses Feld anschließen." },
  system_prompt: { label: "Systemprompt", tooltip:
    "Anweisungen, die festlegen, was das Modell tut. Wird von der Auswahl gefüllt; frei " +
    "bearbeitbar. Wird ignoriert, wenn custom_system_prompt angeschlossen ist." + SYSLOCK_DE },
  negative_prompt: { label: "Negativprompt", tooltip:
    "Standard-Negativprompt des Zielmodells; geht direkt an den Ausgang negative_prompt " +
    "(wird nicht an das Modell geschickt). Leer bei Modellen, die Negativprompts bei CFG 1 " +
    "ignorieren (FLUX, Krea 2, Z-Image Turbo, Qwen mit Lightning-LoRAs ...)." },
  model: { label: "Modell", tooltip:
    "xAI-Grok-Modell. Standard: grok-4.20-0309-reasoning - es akzeptiert Temperatur und " +
    "top_p. 'Modell-Liste aktualisieren' lädt die aktuelle Liste aus dem API." },
  temperature: { label: "Temperatur", tooltip:
    "Kreativitätsregler. Niedrig (0,2-0,4) = treu und wiederholbar - für Caption-" +
    "Umschreibungen und Edit-Anweisungen. Hoch (0,8-1,0) = abwechslungsreich - zum " +
    "Ausbauen von Ideen. Über ~1,3 zerfällt die Grammatik." },
  top_p: { label: "top_p", tooltip:
    "Abschneidefilter: verwirft vor der Wortwahl die unwahrscheinlichsten Wörter. 1,0 = aus " +
    "(wird nicht gesendet). Hoch lassen (0,9-1,0) und mit der Temperatur steuern." },
  max_tokens: { label: "max. Tokens", tooltip:
    "Obergrenze für die Antwort EINSCHLIESSLICH des versteckten Nachdenkens des Modells. " +
    "Reasoning-Modelle verbrauchen zuerst einige hundert bis einige tausend Tokens zum " +
    "Nachdenken - zu niedrig ergibt leere oder abgeschnittene Antworten." },
  seed: { label: "Seed", tooltip:
    "Cache-Brecher, wird NICHT an das API geschickt. 'randomize' = bei jedem Lauf ein " +
    "frischer Prompt. 'fixed' = gleiche Eingabe nutzt das zwischengespeicherte Ergebnis " +
    "(spart Geld beim Umschreiben von Captions)." },
  control_after_generate: { label: "Seed nach dem Lauf", tooltip:
    "Was nach jedem Lauf mit dem Seed passiert: fixed = bleibt gleich, increment = +1, " +
    "decrement = -1, randomize = zufällig (für jeden Lauf ein frischer Prompt)." },
  custom_system_prompt: { label: "eigener Systemprompt", tooltip:
    "Einen Text hier anschließen, um ihn STATT des Feldes Systemprompt zu verwenden - er " +
    "hat immer Vorrang vor der Auswahl. Nicht angeschlossen (oder leer) = Auswahl gilt." },
  image_1: { label: "Bild 1", tooltip: IMAGE_DE(1) },
  image_2: { label: "Bild 2", tooltip: IMAGE_DE(2) },
  image_3: { label: "Bild 3", tooltip: IMAGE_DE(3) },
  image_4: { label: "Bild 4", tooltip: IMAGE_DE(4) },
  persons: { label: "Personen", tooltip:
    "Optional: 'Prompt Writer · Persons' anschließen, um die Personen außerhalb dieses Nodes " +
    "zu wählen - z. B. eine Besetzung für mehrere Writer-Nodes. Solange er angeschlossen ist, " +
    "sind person_1..person_6 an diesem Node gesperrt und werden ignoriert; es zählen die " +
    "Slotnummern des Persons-Nodes (Person 3 dort = Person 3 hier, auch für 'Bild N = " +
    "Person N')." },
  system: { label: "Systemprompt", tooltip:
    "Optional: 'Prompt Writer · System Prompt Library' anschließen, um den Systemprompt dort zu " +
    "wählen - aus den mitgelieferten Auswahlen, deinen eigenen Auswahlen oder deinen gespeicherten " +
    "Systemprompts. Modus 'replace' nimmt ihn statt des Feldes Systemprompt (das dann gesperrt " +
    "ist), Modus 'append' hängt ihn als zusätzliche verbindliche Anweisungen an." },
  light: { label: "Licht / Stimmung", tooltip:
    "Erzwingt ein Licht oder eine Stimmung, sofern dein Text nichts anderes sagt (dein Text hat " +
    "immer Vorrang).\n" +
    "free (Standard): keine Regel; Auswahl, Stil-Baustein oder dein Text bestimmen.\n" +
    "daylight: klares, weißes, natürliches Tageslicht mit weichen Schatten und echten Farben - " +
    "keine dramatische Beleuchtung, keine goldene Stunde, kein Neon, kein Color Grading. Ohne " +
    "Stil und ohne Medium in deinem Text wird es ein natürliches Foto.\n" +
    "night: tiefe Nacht; die Szene ist sehr dunkel und nur von einer einzigen schwachen " +
    "Lichtquelle beleuchtet (Mondlicht, oder eine Kerze, ein Handydisplay ..., wenn dein Text " +
    "eine nennt).\n" +
    "redlight: sinnliches, erotisches Rotlicht - drinnen ein Raum im Schein roter Lampen auf " +
    "Haut, Satin und Samt; draußen eine Rotlichtstraße bei Nacht mit roten Fenstern und Neon.\n" +
    "rundown: ein heruntergekommener, verwahrloster Ort in trübem, schmutzigem Licht - drinnen " +
    "abblätternde Wände und eine nackte Glühbirne; draußen bröckelnde Fassaden, Graffiti und " +
    "bedeckter Himmel.\n" +
    "threatening: eine angespannte, bedrohliche Szene - drinnen tiefe Schatten und ein hartes " +
    "Licht; draußen ein leerer Ort in der Dämmerung oder Nacht mit Nebel und grellem " +
    "Straßenlicht.\n" +
    "Drinnen oder draußen richtet sich nach dem Ort in deinem Text. Das legt nur Licht und " +
    "Stimmung fest, nicht das Medium: mit einem Stil wie Cartoon bleibt das Bild ein Cartoon." },
  safe: { label: "safe", tooltip:
    "Aus (Standard): Sexuelles und Nacktheit werden explizit und präzise beschrieben - Posen, " +
    "Handlungen, wer wen wo berührt, Kleidungszustand und Körperflüssigkeiten.\n" +
    "An: Sexuelles wird nur angedeutet - Nacktheit ohne explizite Details, keine expliziten " +
    "Handlungen, keine Körperflüssigkeiten. Für API-Modelle mit Inhaltsfilter (Seedream, " +
    "Seedance, GPT Image, Nano Banana, Grok Imagine, Flux 3, Kling, Veo) oder wenn das " +
    "Ergebnis jugendfrei bleiben muss.\n" +
    "Auswahlen mit '· SFW' oder '· NSFW' bringen eigene Inhaltsregeln für ihr Modell mit; " +
    "'safe' an hat auch vor einer '· NSFW'-Auswahl Vorrang." },
  person_5: { label: "Person 5", tooltip: PERSON_DE(5) + LOCK_DE + NOIMG_DE(5) },
  person_6: { label: "Person 6", tooltip: PERSON_DE(6) + LOCK_DE + NOIMG_DE(6) },
  variation: { label: "Variation", tooltip:
    "An (Standard): Mit dem Seed des Laufs wählt der Node eine Pose, eine Interaktion, einen " +
    "Kamerawinkel, einen Bildausschnitt, einen Ort und (bei Video) eine Kamerabewegung; der " +
    "Writer nimmt sie überall dort, wo dein Text, die Personen und die Bilder etwas offen " +
    "lassen. Ein Sprachmodell allein wählt jedes Mal dieselbe 'zufällige' Pose; so gibt ein " +
    "neuer Seed eine neue Szene und derselbe Seed dieselbe. SFW-Listen als Standard, " +
    "NSFW-Listen mit einer '· NSFW'-Auswahl (und 'safe' aus). Nicht bei 'Caption >'-, Edit- " +
    "und Recast-Auswahlen.\n" +
    "Aus: keine Variation, wie vor 1.7.0." },
  trigger_word: { label: "Trigger-Wort", tooltip:
    "Nur für 'Caption > LoRA training caption': der Trigger des LoRAs für das Hauptmotiv " +
    "(ersetzt {trigger} im Systemprompt). Leer lassen für Captions ohne Trigger." },
  max_side: { label: "max. Bildseite", tooltip:
    "Verkleinert die längste Bildseite vor dem Upload (spart Tokens; Prompts und Captions " +
    "brauchen keine volle Auflösung)." },
  api_key: { label: "API-Key", tooltip:
    "Dein xAI-API-Key. Möglichst LEER lassen - hier eingetragene Keys landen in " +
    "exportierten Workflows! Besser die Umgebungsvariable XAI_API_KEY oder die Key-Datei " +
    "unten verwenden." },
  api_key_file: { label: "API-Key-Datei", tooltip:
    "Pfad zu einer Textdatei, die nur deinen xAI-API-Key enthält. Relative Pfade werden im " +
    "ComfyUI-Hauptordner, im Portable-Hauptordner und im Ordner dieses Node-Pakets gesucht." },
  base_url: { label: "API-Adresse", tooltip:
    "API-Endpunkt. Nur ändern, wenn Anfragen über einen Proxy oder einen anderen " +
    "OpenAI-kompatiblen Server laufen sollen." },
  fallback_to_input: { label: "bei Fehler Eingabe durchreichen", tooltip:
    "Schlägt der API-Aufruf fehl (kein Key, Netzwerkfehler, Ablehnung ...), wird die " +
    "Eingabe unverändert durchgereicht, statt die Warteschlange anzuhalten. Hält lange " +
    "Batch-Läufe am Laufen." },
  timeout_seconds: { label: "Timeout (Sek.)", tooltip:
    "Wie lange auf das API gewartet wird, bevor neu versucht wird (insgesamt 3 Versuche). " +
    "Reasoning-Modelle denken vor der Antwort nach - großzügig einstellen." },
  min_words: { label: "min. Wörter", tooltip: WORDS_DE },
  max_words: { label: "max. Wörter", tooltip: WORDS_DE },
  person_1: { label: "Person 1", tooltip: PERSON_DE(1) + LOCK_DE },
  person_2: { label: "Person 2", tooltip: PERSON_DE(2) + LOCK_DE },
  person_3: { label: "Person 3", tooltip: PERSON_DE(3) + LOCK_DE },
  person_4: { label: "Person 4", tooltip: PERSON_DE(4) + LOCK_DE },
  image_n_is_person_n: { label: "Bild N = Person N", tooltip:
    "Koppelt jede Person mit dem Bild-Eingang derselben Nummer: person_1 = image_1, " +
    "person_2 = image_2, person_3 = image_3, person_4 = image_4. person_5 und person_6 haben " +
    "kein eigenes Bild.\n" +
    "An: Lädst du ein Foto der Person in den passenden Bild-Eingang, erfährt das Modell 'dieses " +
    "Bild zeigt diese Person' und übernimmt das Aussehen aus dem Foto. Bei Qwen-Image-Edit, " +
    "MiniMax H3 REF2VA, Wan 2.7/3.0, Seedream, Seedance, Kling, Grok Imagine, GPT Image, Nano " +
    "Banana und FLUX verweist der Prompt auf das Bild (z. B. <image1>, Image 1, @Image1), statt " +
    "das Gesicht zu beschreiben.\n" +
    "Aus: Bilder und Personen haben nichts miteinander zu tun - z. B. wenn die Bilder " +
    "Start- und Endbild für MiniMax H3 FL2VA sind." },
  style_1: { label: "Stil 1", tooltip: STYLE_DE(1) },
  style_2: { label: "Stil 2", tooltip: STYLE_DE(2) },
  archive: { label: "archivieren", tooltip:
    "An: jedes Ergebnis wird mit Eingabe, Auswahl, Personen und Einstellungen an " +
    "ComfyUI/user/grok_prompt_forge/archive.jsonl angehängt. '📜 Aus Archiv laden...' holt " +
    "einen archivierten Prompt zurück ins Eingabefeld, z. B. um ihn mit einer anderen " +
    "Person neu zu besetzen ('Recast ▸ Swap persons')." },
  // outputs
  "output:prompt": { label: "Prompt" },
  "output:negative_prompt": { label: "Negativprompt" },
};

// German texts of the fields that only Prompt Writer · LLM GGUF has; all other
// fields use NODE_TEXT_DE.
export const LOCAL_TEXT_DE = {
  model: { label: "Modell", tooltip:
    "Lokales, unzensiertes Qwen3.8-27B (GGUF) mit Bildverständnis. ✓ = schon heruntergeladen. " +
    "Sonst werden Modell und Bildmodul (mmproj, 0,9 GB) beim ersten Lauf nach " +
    "ComfyUI/models/LLM_gguf/ geladen. Größere Quantisierung = bessere Qualität, mehr VRAM. " +
    "Faustregel mit Standard-Kontext: 12 GB VRAM -> IQ2, 16 GB -> Q3 / IQ4_XS, 24 GB -> Q4, " +
    "32 GB -> Q4 / Q5. huihui = abliterated; HauhauCS = 'Aggressive' entzensiertes Fine-Tune. " +
    "Braucht llama-cpp-python mit CUDA - siehe docs/LOCAL_GGUF.md." },
  thinking: { label: "nachdenken", tooltip:
    "An: das Modell denkt vor der Antwort nach (bessere Prompts, langsamer - meist 10-40 s auf " +
    "einer schnellen Karte). Aus: antwortet direkt. Das Nachdenken landet nie im Ergebnis." },
  unload_after_run: { label: "nach dem Lauf entladen", tooltip:
    "An: das Modell verlässt nach jedem Lauf den VRAM, damit dein Bild- oder Videomodell wieder " +
    "Platz hat (der nächste Lauf lädt es neu, ~5-20 s von einer SSD). Aus: es bleibt geladen " +
    "und der nächste Lauf startet sofort - nur wenn dein VRAM für beides reicht." },
  context_length: { label: "Kontextlänge", tooltip:
    "Arbeitsspeicher in Tokens: Systemprompt + Bilder + Nachdenken + Antwort. Mehr kostet VRAM. " +
    "32768 reicht für alle Auswahlen; bei 12-16 GB VRAM 8192-16384 nehmen und max. Tokens " +
    "passend senken." },
  gpu_layers: { label: "GPU-Schichten", tooltip:
    "-1 = automatisch: llama.cpp legt so viele Schichten auf die GPU, wie passen (empfohlen). " +
    "0 = nur CPU (sehr langsam). Eine Zahl = so viele Schichten auf der GPU, der Rest im RAM - " +
    "für Karten, die für das ganze Modell zu klein sind." },
  top_k: { label: "top_k", tooltip:
    "Berücksichtigt nur die k wahrscheinlichsten nächsten Wörter. Qwen empfiehlt 20; 0 = aus." },
};

// German texts of the Prompt Writer · System Prompt Library node.
export const SYSTEM_TEXT_DE = {
  label: { label: "Bezeichnung", tooltip:
    "Name dieses Systemprompts. Eine Wahl aus der Bibliothek trägt ihn ein; '💾 Speichern als...' " +
    "fragt nach einem eigenen Namen (mitgelieferte Auswahlen werden nie überschrieben)." },
  text: { label: "Text", tooltip:
    "Der Systemprompt (Modus replace) oder die zusätzlichen Anweisungen (Modus append). " +
    "'📝 Editor öffnen...' bearbeitet ihn in einem großen Fenster mit Wort- und Zeichenzählung. " +
    "Leer = dieser Node tut nichts." },
  mode: { label: "Modus", tooltip:
    "replace (Standard): wird statt des Feldes Systemprompt am Writer verwendet; das Feld ist " +
    "gesperrt, solange dieser Node angeschlossen ist.\n" +
    "append: wird an den Systemprompt des Writers angehängt, als zusätzliche verbindliche " +
    "Anweisungen (z. B. eigene Regeln zusätzlich zu einem Modell-Leitfaden)." },
  save: { label: "speichern", tooltip:
    "An: der Text wird bei jedem Lauf unter der Bezeichnung in deiner Bibliothek gespeichert " +
    "(ComfyUI/user/grok_prompt_forge/system_prompts.json).\n" +
    "Aus (Standard): ein Lauf speichert nichts - '💾 Speichern als...' speichert bei Bedarf " +
    "unter einem Namen deiner Wahl. Mitgelieferte Auswahlen werden nie überschrieben." },
  "output:system": { label: "Systemprompt" },
};

// German texts of the Prompt Writer · Persons node.
export const PERSONS_TEXT_DE = {
  person_1: { label: "Person 1", tooltip: PERSON_DE(1) },
  person_2: { label: "Person 2", tooltip: PERSON_DE(2) },
  person_3: { label: "Person 3", tooltip: PERSON_DE(3) },
  person_4: { label: "Person 4", tooltip: PERSON_DE(4) },
  person_5: { label: "Person 5", tooltip: PERSON_DE(5) + NOIMG_DE(5) },
  person_6: { label: "Person 6", tooltip: PERSON_DE(6) + NOIMG_DE(6) },
  "output:persons": { label: "Personen" },
};

// German texts of the Prompt Writer · Show Prompt node (separate: "text" means something else there).
export const SHOW_TEXT_DE = {
  text: { label: "Text", tooltip:
    "Beliebiger Text, z. B. der Prompt-Ausgang eines Prompt-Writer-Nodes. Er wird am Node " +
    "angezeigt und unverändert weitergegeben - das Zählen ändert ihn nie und startet nie " +
    "einen neuen Lauf." },
  "output:text": { label: "Text" },
};

export const STRINGS = {
  en: {
    language: "🌐 Language / Sprache",
    btnSavePreset: "💾 Save preset as...",
    btnDeletePreset: "🗑 Delete preset",
    btnRefreshModels: "🔄 Refresh model list",
    btnLibrary: "👤 Persons & styles...",
    btnArchive: "📜 Load from archive...",
    filterType: "Filter: type",
    filterTypeTip: "Shows only presets of this type in the preset list: image models, edit models, video models, captions & tools, or your own presets. Display only: it never changes the selected preset and never starts a new run.",
    filterTask: "Filter: task",
    filterTaskTip: "Shows only 'Generation ▸' presets (expand a short idea into a full prompt) or 'Caption ▸' presets (rewrite an existing caption). Display only: it never changes the selected preset and never starts a new run.",
    opt_all: "All",
    opt_image: "Image",
    opt_edit: "Edit",
    opt_video: "Video",
    opt_tools: "Captions & tools",
    opt_own: "My presets",
    opt_generation: "Generation",
    opt_caption: "Caption",
    filterContent: "Filter: content",
    filterContentTip: "Shows only '· SFW' or '· NSFW' presets: their system prompt has its own content rules for that model. SFW: everyone is dressed, poses and interactions are described step by step. NSFW: explicit, adults only, sexual interactions described step by step ('safe' on still keeps the result safe for work). Display only: it never changes the selected preset and never starts a new run.",
    opt_sfw: "SFW",
    opt_nsfw: "NSFW",
    recommended: (name, words) => `Recommended for "${name}": ${words}.`,
    noLength: "This preset has no recommended length.",
    length: "Length",
    savePresetTitle: "Save preset as...",
    presetName: "Name of the preset:",
    overwriteBuiltin: (n) => `"${n}" is a built-in preset. Save your values in its place? (Delete brings the built-in values back.)`,
    overwriteOwn: (n) => `Overwrite your preset "${n}"?`,
    presetNotSaved: "Preset not saved",
    presetSaved: "Preset saved",
    builtinPreset: "Built-in preset",
    builtinCannotDelete: (n) => `"${n}" ships with the node pack and cannot be deleted.`,
    discardOverride: (n) => `Discard your saved values for "${n}" and go back to the built-in values?`,
    deleteOwnPreset: (n) => `Delete your preset "${n}"?`,
    presetNotDeleted: "Preset not deleted",
    builtinRestored: "Built-in values restored",
    presetDeleted: "Preset deleted",
    modelsNotRefreshed: "Model list not refreshed",
    modelsRefreshed: "Model list refreshed",
    nModels: (n) => `${n} models`,
    libTitle: "Prompt Writer · persons & style blocks",
    tabPersons: "👤 Persons",
    tabStyles: "🎨 Style blocks",
    newEntry: "＋ New",
    nothingSaved: "Nothing saved yet.",
    name: "Label",
    namePlaceholderPerson: "e.g. Peter with glasses",
    namePlaceholderStyle: "Label shown in the selection box",
    nameHintPerson: "Only for your overview: shown in the list and the selection boxes, never in the prompt. Several entries may share one name, e.g. 'Peter with glasses' and 'Peter with beard'.",
    nameHintStyle: "Only a label for the selection box - it is never written into the prompt.",
    promptNameLabel: "Name in the prompt",
    groupHover: "Group - every member appears under their own name",
    promptNameHint: "Written into every prompt exactly like this, e.g. 'P3ter' - with a digit for a letter it works as a trigger. Use it in the description too. Empty = the label is used.",
    genderLabel: "Gender",
    genderHint: "Shown on hover and passed to the prompt, so pronouns and gendered details fit.",
    gender_none: "-",
    gender_m: "male",
    gender_f: "female",
    triggerLabel: "Trigger",
    triggerHint: "Optional, for special cases: an extra LoRA trigger, written right after the name when it differs from it. Usually the name already works as the trigger.",
    descriptionLabel: "Description",
    descriptionHint: "Appearance and fixed traits (face, hair, body, age, typical look). Binding in every prompt; tag models get it as tags. For a group, start with 'A group of' and give every member a name of their own.",
    voiceLabel: "Voice",
    voiceHint: "Timbre, pitch, pace, accent, e.g. 'deep raspy male voice, slow, northern German accent'. Used only by models with audio: MiniMax H3 FL2VA / REF2VA, Wan 2.7, Wan 3.0, Seedance 1.5 / 2.0 / 2.5, Kling 3.0 / 2.6, Veo 3.1, Grok Imagine Video. Ignored by Wan 2.2 and all image models.",
    textLabel: "Text",
    textHint: "Applied to every result while selected, e.g. a camera look ('shot on 35mm film, grain, muted colours'), a lighting mood or a ban list ('never: golden hour, neon lights').",
    save: "💾 Save",
    delete: "🗑 Delete",
    saved: "Saved",
    notSaved: "Not saved",
    confirmDeleteEntry: (n) => `Delete "${n}" from your library?`,
    deleted: "Deleted",
    notDeleted: "Not deleted",
    importClash: (count, names) => `${count} name(s) already exist in your library (${names}). Replace them with the imported ones? Cancel keeps yours and imports only the new names.`,
    imported: "Imported",
    importResult: (a, r, s) => `${a} added, ${r} replaced, ${s} skipped`,
    importFailed: "Import failed",
    exportLibrary: "⬇ Export library",
    exportTitle: "Download all persons and style blocks as one JSON file, e.g. to move them to another ComfyUI install.",
    addTemplates: "📥 Add templates",
    templatesTitle: "Adds 10 template persons, 6 groups (Group of men I … V, Group of women I) and 17 style blocks (Natural daylight, Cartoon, Oil painting, Manga, Van Gogh, Pixar ...) to your library. Labels you already have are never changed; Group_of_men / Group_of_women from older versions are renamed to Group of men I / Group of women I, with your edits.",
    templatesAdded: "Templates added",
    templatesResult: (a, s, u) => `${a} added, ${u} updated, ${s} already in your library`,
    templatesFailed: "Templates not added",
    btnSystemEditor: "📝 Open editor...",
    btnSystemSave: "💾 Save as...",
    btnSystemDelete: "🗑 Delete my prompt",
    sysLibrary: "System prompt",
    sysLibraryTip: "The whole library: the system prompts of the built-in presets, of your own presets and your saved system prompts (★). Choosing one puts its label and text into the node - edit them freely; the library itself only changes with '💾 Save as...' or '🗑 Delete my prompt'. The filters above narrow the list. Display only: choosing never starts a run by itself.",
    sysChoose: "(choose from the library)",
    sysFilterContentTip: "Shows only system prompts with their own SFW or NSFW content section (the '· SFW' / '· NSFW' presets, and your saved prompts that contain such a section). Display only.",
    sysFilterTypeTip: "Shows only system prompts of this type: of image, edit or video presets, of captions & tools, of your own presets, or your saved system prompts (★). Display only.",
    sysFilterTaskTip: "Shows only the system prompts of 'Generation ▸' or 'Caption ▸' presets. Your saved system prompts (★) are always shown. Display only.",
    opt_saved: "★ My system prompts",
    sysEditorTitle: "Prompt Writer · edit system prompt",
    sysEditorHint: "Edit freely. '✔ Apply' puts label and text into the node (nothing is saved); '💾 Save as...' also saves it in your library under a name of your own.",
    sysApply: "✔ Apply",
    sysCancel: "Cancel",
    sysCount: (w, c, l) => [plural(w, "word", "words"), plural(c, "character", "characters"),
      plural(l, "line", "lines")].join(" · "),
    sysSaveTitle: "Save system prompt as...",
    sysSaveName: "Name in your library:",
    sysBuiltinName: (n) => `"${n}" is a built-in preset - built-ins stay unchanged. Choose a name of your own.`,
    sysEmptyText: "The text is empty.",
    sysBuiltinNoDelete: (n) => `"${n}" is a preset, not one of your saved system prompts: nothing to delete here.`,
    sysLocked: "Locked: the connected System Prompt Library (mode 'replace') sets the system prompt.",
    systemSaved: "System prompt saved",
    systemNotSaved: "System prompt not saved",
    systemOverwrite: (l) => `Replace the saved system prompt "${l}" with this text?`,
    systemNotInLibrary: "Not in your library",
    systemConfirmDelete: (l) => `Delete the system prompt "${l}" from your library?`,
    personsLocked: "Locked: the connected 'Prompt Writer · Persons' node chooses the persons.",
    importLibrary: "⬆ Import...",
    importTitle: "Add persons and style blocks from an exported JSON file.",
    storedIn: "Stored in ComfyUI/user/grok_prompt_forge/library.json",
    archiveTitle: "Prompt Writer · load from archive",
    archiveSearch: "Search prompts, inputs, presets, persons...",
    archiveHint: "'Use as text' puts the prompt into the text field. 'Recast' also selects the preset 'Recast ▸ Swap persons' (· SFW while the node is on an SFW preset, otherwise · NSFW, which keeps every explicit detail) and the archived negative prompt - then choose person_1..6 and add an instruction such as 'replace the man with Person 1'.",
    persons: "persons",
    useAsText: "Use as text",
    recast: "Recast",
    readyToRecast: "Ready to recast",
    recastHint: "Choose person_1..6 and say whom to replace in the text.",
    loadedIntoText: "Loaded into text",
    nothingFound: "Nothing found.",
    archiveEmpty: "The archive is empty. Results are archived while 'archive' is on.",
    showCounts: "show counts",
    showCountsTip: "Shows the number of words, tags (comma-separated parts), sentences and characters below the text. Display only: switching it never starts a new run.",
    shownText: "Shown text",
    notRunYet: "Not run yet - the text appears here after the next run.",
    stats: (w, tg, s, c) => [plural(w, "word", "words"), plural(tg, "tag", "tags"),
      plural(s, "sentence", "sentences"), plural(c, "character", "characters")].join(" · "),
  },
  de: {
    language: "🌐 Language / Sprache",
    btnSavePreset: "💾 Auswahl speichern als...",
    btnDeletePreset: "🗑 Auswahl löschen",
    btnRefreshModels: "🔄 Modell-Liste aktualisieren",
    btnLibrary: "👤 Personen & Stile...",
    btnArchive: "📜 Aus Archiv laden...",
    filterType: "Filter: Typ",
    filterTypeTip: "Zeigt in der Auswahlliste nur Auswahlen dieses Typs: Bildmodelle, Edit-Modelle, Videomodelle, Captions & Werkzeuge oder deine eigenen Auswahlen. Nur Anzeige: ändert nie die gewählte Auswahl und startet nie einen neuen Lauf.",
    filterTask: "Filter: Aufgabe",
    filterTaskTip: "Zeigt nur 'Generation ▸'-Auswahlen (eine kurze Idee zum vollständigen Prompt ausbauen) oder 'Caption ▸'-Auswahlen (eine vorhandene Caption umschreiben). Nur Anzeige: ändert nie die gewählte Auswahl und startet nie einen neuen Lauf.",
    opt_all: "Alle",
    opt_image: "Bild",
    opt_edit: "Bearbeiten",
    opt_video: "Video",
    opt_tools: "Captions & Werkzeuge",
    opt_own: "Eigene",
    opt_generation: "Generation",
    opt_caption: "Caption",
    filterContent: "Filter: Inhalt",
    filterContentTip: "Zeigt nur '· SFW'- oder '· NSFW'-Auswahlen: Ihr Systemprompt bringt eigene Inhaltsregeln für dieses Modell mit. SFW: alle sind bekleidet, Posen und Interaktionen werden Schritt für Schritt beschrieben. NSFW: explizit, nur Erwachsene, sexuelle Interaktionen Schritt für Schritt beschrieben ('safe' an hält das Ergebnis trotzdem jugendfrei). Nur Anzeige: ändert nie die gewählte Auswahl und startet nie einen neuen Lauf.",
    opt_sfw: "SFW",
    opt_nsfw: "NSFW",
    recommended: (name, words) => `Empfohlen für "${name}": ${words}.`,
    noLength: "Für diese Auswahl gibt es keine Längenempfehlung.",
    length: "Länge",
    savePresetTitle: "Auswahl speichern als...",
    presetName: "Name der Auswahl:",
    overwriteBuiltin: (n) => `"${n}" ist eine mitgelieferte Auswahl. Deine Werte an ihrer Stelle speichern? (Löschen holt die mitgelieferten Werte zurück.)`,
    overwriteOwn: (n) => `Deine Auswahl "${n}" überschreiben?`,
    presetNotSaved: "Auswahl nicht gespeichert",
    presetSaved: "Auswahl gespeichert",
    builtinPreset: "Mitgelieferte Auswahl",
    builtinCannotDelete: (n) => `"${n}" gehört zum Node-Paket und kann nicht gelöscht werden.`,
    discardOverride: (n) => `Deine gespeicherten Werte für "${n}" verwerfen und zu den mitgelieferten Werten zurückkehren?`,
    deleteOwnPreset: (n) => `Deine Auswahl "${n}" löschen?`,
    presetNotDeleted: "Auswahl nicht gelöscht",
    builtinRestored: "Mitgelieferte Werte wiederhergestellt",
    presetDeleted: "Auswahl gelöscht",
    modelsNotRefreshed: "Modell-Liste nicht aktualisiert",
    modelsRefreshed: "Modell-Liste aktualisiert",
    nModels: (n) => `${n} Modelle`,
    libTitle: "Prompt Writer · Personen & Stil-Bausteine",
    tabPersons: "👤 Personen",
    tabStyles: "🎨 Stil-Bausteine",
    newEntry: "＋ Neu",
    nothingSaved: "Noch nichts gespeichert.",
    name: "Bezeichnung",
    namePlaceholderPerson: "z. B. Peter mit Brille",
    namePlaceholderStyle: "Bezeichnung in der Auswahlbox",
    nameHintPerson: "Nur für deinen Überblick: erscheint in der Liste und den Auswahlboxen, nie im Prompt. Mehrere Einträge dürfen denselben Namen haben, z. B. 'Peter mit Brille' und 'Peter mit Bart'.",
    nameHintStyle: "Nur eine Bezeichnung für die Auswahlbox - wird nie in den Prompt geschrieben.",
    promptNameLabel: "Name im Prompt",
    groupHover: "Gruppe - jedes Mitglied erscheint unter eigenem Namen",
    promptNameHint: "Steht genau so in jedem Prompt, z. B. 'P3ter' - mit einer Ziffer statt eines Buchstabens wirkt er als Trigger. Auch in der Beschreibung verwenden. Leer = die Bezeichnung wird verwendet.",
    genderLabel: "Geschlecht",
    genderHint: "Erscheint beim Überfahren und geht in den Prompt, damit Pronomen und Details passen.",
    gender_none: "-",
    gender_m: "männlich",
    gender_f: "weiblich",
    triggerLabel: "Trigger",
    triggerHint: "Optional, für Sonderfälle: ein zusätzlicher LoRA-Trigger, direkt nach dem Namen geschrieben, wenn er sich von ihm unterscheidet. Meist wirkt schon der Name als Trigger.",
    descriptionLabel: "Beschreibung",
    descriptionHint: "Aussehen und feste Merkmale (Gesicht, Haare, Körper, Alter, typischer Look). In jedem Prompt verbindlich; Tag-Modelle bekommen sie als Tags. Für eine Gruppe mit 'A group of' beginnen und jedem Mitglied einen eigenen Namen geben.",
    voiceLabel: "Stimme",
    voiceHint: "Klangfarbe, Tonhöhe, Tempo, Akzent, z. B. 'tiefe, raue Männerstimme, langsam, norddeutscher Akzent'. Nur für Modelle mit Ton: MiniMax H3 FL2VA / REF2VA, Wan 2.7, Wan 3.0, Seedance 1.5 / 2.0 / 2.5, Kling 3.0 / 2.6, Veo 3.1, Grok Imagine Video. Wan 2.2 und alle Bildmodelle ignorieren sie.",
    textLabel: "Text",
    textHint: "Wird auf jedes Ergebnis angewendet, solange gewählt, z. B. ein Kameralook ('shot on 35mm film, grain, muted colours'), eine Lichtstimmung oder eine Verbotsliste ('never: golden hour, neon lights').",
    save: "💾 Speichern",
    delete: "🗑 Löschen",
    saved: "Gespeichert",
    notSaved: "Nicht gespeichert",
    confirmDeleteEntry: (n) => `"${n}" aus deiner Bibliothek löschen?`,
    deleted: "Gelöscht",
    notDeleted: "Nicht gelöscht",
    importClash: (count, names) => `${count} Name(n) gibt es schon in deiner Bibliothek (${names}). Durch die importierten ersetzen? Abbrechen behält deine und importiert nur die neuen Namen.`,
    imported: "Importiert",
    importResult: (a, r, s) => `${a} hinzugefügt, ${r} ersetzt, ${s} übersprungen`,
    importFailed: "Import fehlgeschlagen",
    exportLibrary: "⬇ Bibliothek exportieren",
    exportTitle: "Alle Personen und Stil-Bausteine als eine JSON-Datei herunterladen, z. B. für eine andere ComfyUI-Installation.",
    addTemplates: "📥 Vorlagen hinzufügen",
    templatesTitle: "Fügt deiner Bibliothek 10 Vorlage-Personen, 6 Gruppen (Group of men I … V, Group of women I) und 17 Stil-Bausteine (Natural daylight, Cartoon, Oil painting, Manga, Van Gogh, Pixar ...) hinzu. Bezeichnungen, die du schon hast, bleiben unverändert; Group_of_men / Group_of_women aus älteren Versionen heißen danach Group of men I / Group of women I, mit deinen Änderungen.",
    templatesAdded: "Vorlagen hinzugefügt",
    templatesResult: (a, s, u) => `${a} hinzugefügt, ${u} aktualisiert, ${s} schon in deiner Bibliothek`,
    templatesFailed: "Vorlagen nicht hinzugefügt",
    btnSystemEditor: "📝 Editor öffnen...",
    btnSystemSave: "💾 Speichern als...",
    btnSystemDelete: "🗑 Eigenen Prompt löschen",
    sysLibrary: "Systemprompt",
    sysLibraryTip: "Die ganze Bibliothek: die Systemprompts der mitgelieferten Auswahlen, deiner eigenen Auswahlen und deine gespeicherten Systemprompts (★). Eine Wahl setzt Bezeichnung und Text in den Node - frei bearbeitbar; die Bibliothek selbst ändert sich nur mit '💾 Speichern als...' oder '🗑 Eigenen Prompt löschen'. Die Filter darüber grenzen die Liste ein. Nur Anzeige: eine Wahl startet nie selbst einen Lauf.",
    sysChoose: "(aus der Bibliothek wählen)",
    sysFilterContentTip: "Zeigt nur Systemprompts mit eigenem SFW- oder NSFW-Inhaltsabschnitt (die '· SFW'-/'· NSFW'-Auswahlen und deine gespeicherten Prompts mit einem solchen Abschnitt). Nur Anzeige.",
    sysFilterTypeTip: "Zeigt nur Systemprompts dieses Typs: von Bild-, Edit- oder Video-Auswahlen, von Captions & Werkzeugen, von deinen eigenen Auswahlen oder deine gespeicherten Systemprompts (★). Nur Anzeige.",
    sysFilterTaskTip: "Zeigt nur die Systemprompts von 'Generation ▸'- oder 'Caption ▸'-Auswahlen. Deine gespeicherten Systemprompts (★) erscheinen immer. Nur Anzeige.",
    opt_saved: "★ Eigene Systemprompts",
    sysEditorTitle: "Prompt Writer · Systemprompt bearbeiten",
    sysEditorHint: "Frei bearbeiten. '✔ Übernehmen' setzt Bezeichnung und Text in den Node (nichts wird gespeichert); '💾 Speichern als...' speichert ihn zusätzlich unter eigenem Namen in deiner Bibliothek.",
    sysApply: "✔ Übernehmen",
    sysCancel: "Abbrechen",
    sysCount: (w, c, l) => [plural(w, "Wort", "Wörter"), plural(c, "Zeichen", "Zeichen"),
      plural(l, "Zeile", "Zeilen")].join(" · "),
    sysSaveTitle: "Systemprompt speichern als...",
    sysSaveName: "Name in deiner Bibliothek:",
    sysBuiltinName: (n) => `"${n}" ist eine mitgelieferte Auswahl - sie bleibt unverändert. Bitte einen eigenen Namen wählen.`,
    sysEmptyText: "Der Text ist leer.",
    sysBuiltinNoDelete: (n) => `"${n}" ist eine Auswahl, kein gespeicherter Systemprompt: hier gibt es nichts zu löschen.`,
    sysLocked: "Gesperrt: die angeschlossene System Prompt Library (Modus 'replace') legt den Systemprompt fest.",
    systemSaved: "Systemprompt gespeichert",
    systemNotSaved: "Systemprompt nicht gespeichert",
    systemOverwrite: (l) => `Den gespeicherten Systemprompt "${l}" durch diesen Text ersetzen?`,
    systemNotInLibrary: "Nicht in deiner Bibliothek",
    systemConfirmDelete: (l) => `Den Systemprompt "${l}" aus deiner Bibliothek löschen?`,
    personsLocked: "Gesperrt: der angeschlossene Node 'Prompt Writer · Persons' wählt die Personen.",
    importLibrary: "⬆ Importieren...",
    importTitle: "Personen und Stil-Bausteine aus einer exportierten JSON-Datei hinzufügen.",
    storedIn: "Gespeichert in ComfyUI/user/grok_prompt_forge/library.json",
    archiveTitle: "Prompt Writer · aus Archiv laden",
    archiveSearch: "Prompts, Eingaben, Auswahlen, Personen durchsuchen...",
    archiveHint: "'Als Eingabe' setzt den Prompt ins Eingabefeld. 'Recast' wählt zusätzlich die Auswahl 'Recast ▸ Swap persons' (· SFW, wenn der Node auf einer SFW-Auswahl steht, sonst · NSFW, das jedes explizite Detail behält) und den archivierten Negativprompt - dann person_1..6 wählen und eine Anweisung ergänzen wie 'ersetze den Mann durch Person 1'.",
    persons: "Personen",
    useAsText: "Als Eingabe",
    recast: "Recast",
    readyToRecast: "Bereit zum Neubesetzen",
    recastHint: "person_1..6 wählen und im Text sagen, wer ersetzt wird.",
    loadedIntoText: "In die Eingabe geladen",
    nothingFound: "Nichts gefunden.",
    archiveEmpty: "Das Archiv ist leer. Ergebnisse werden archiviert, solange 'archivieren' an ist.",
    showCounts: "Zählung anzeigen",
    showCountsTip: "Zeigt unter dem Text die Anzahl der Wörter, Tags (durch Kommas getrennte Teile), Sätze und Zeichen. Nur Anzeige: das Umschalten startet nie einen neuen Lauf.",
    shownText: "Angezeigter Text",
    notRunYet: "Noch nicht gelaufen - der Text erscheint hier nach dem nächsten Lauf.",
    stats: (w, tg, s, c) => [plural(w, "Wort", "Wörter"), plural(tg, "Tag", "Tags"),
      plural(s, "Satz", "Sätze"), plural(c, "Zeichen", "Zeichen")].join(" · "),
  },
};
