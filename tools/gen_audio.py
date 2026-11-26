"""Génère un MP3 par espèce (voix OpenAI tts-1-hd « nova ») à partir du texte parlé de la page.
Usage : python3 -I tools/gen_audio.py   (depuis la racine du dépôt ; ne régénère que les textes modifiés)
La clé est injectée par le proxy de l'environnement (en-tête Authorization), aucune variable à définir."""
import json, hashlib, os, subprocess, sys, urllib.request, time
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AUD = os.path.join(ROOT, "audio"); IDX = os.path.join(AUD, "index.json")
js = r"""
const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage();
await p.route(/wiki|github|jsdelivr/,r=>r.abort());await p.goto('file://'+process.argv[1]);await p.waitForTimeout(600);
const r=await p.evaluate(()=>{const o={};for(const s of S){o[slugSci(s.sci)]=sayText(s)}return o});
console.log(JSON.stringify(r));await b.close()})()"""
texts = json.loads(subprocess.check_output(["node", "-e", js, os.path.join(ROOT, "index.html")]))
idx = json.load(open(IDX)) if os.path.exists(IDX) else {}
todo = [k for k, t in texts.items() if idx.get(k) != hashlib.sha1(t.encode()).hexdigest()[:12] or not os.path.exists(f"{AUD}/{k}.mp3")]
print(len(texts), "espèces,", len(todo), "à générer", flush=True)
for k in todo:
    t = texts[k]
    body = {"model": "tts-1-hd", "voice": "nova", "input": t, "response_format": "mp3"}
    for attempt in range(4):
        try:
            req = urllib.request.Request("https://api.openai.com/v1/audio/speech", data=json.dumps(body).encode(),
                headers={"Content-Type": "application/json", "Authorization": "Bearer proxy-injected"})
            raw = urllib.request.urlopen(req, timeout=180).read(); break
        except Exception as e:
            print("  nouvel essai", k, e, flush=True); time.sleep(10 * (attempt + 1))
    else:
        print("ÉCHEC", k, flush=True); continue
    tmp = f"{AUD}/{k}.src.mp3"; open(tmp, "wb").write(raw)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", tmp, "-ac", "1", "-b:a", "56k", f"{AUD}/{k}.mp3"], check=True)
    os.remove(tmp)
    idx[k] = hashlib.sha1(t.encode()).hexdigest()[:12]
    json.dump(idx, open(IDX, "w"), indent=0, sort_keys=True)
    print("ok", k, flush=True)
for k in list(idx):
    if k not in texts:
        idx.pop(k); os.path.exists(f"{AUD}/{k}.mp3") and os.remove(f"{AUD}/{k}.mp3")
json.dump(idx, open(IDX, "w"), indent=0, sort_keys=True)
print("terminé", flush=True)
