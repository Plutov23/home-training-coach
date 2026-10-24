import pathlib,json,base64,wave,subprocess,zipfile,os,hashlib,shutil
import numpy as np
ROOT=pathlib.Path(__file__).resolve().parent;WEB=ROOT/'trainer';RATE=24000
for folder in ('results','tmp'):(ROOT/folder).mkdir(exist_ok=True)
phrases=json.loads((WEB/'phrases.json').read_text(encoding='utf-8'))
manifest=json.loads((WEB/'voice-manifest.json').read_text(encoding='utf-8'))
bank={};meta={};samples={}
for key,text in phrases.items():
 assert key in manifest and manifest[key]['text_sha256']==hashlib.sha256(text.encode()).hexdigest(),'Missing or stale phrase '+key
 file=WEB/'audio'/(key+'.wav')
 with wave.open(str(file),'rb') as w:
  assert w.getframerate()==RATE and w.getnchannels()==1 and w.getsampwidth()==2
  pcm=np.frombuffer(w.readframes(w.getnframes()),dtype='<i2');duration=len(pcm)/RATE
 assert duration>0 and np.max(np.abs(pcm.astype(np.int32)))>100
 samples[key]=pcm;meta[key]=duration;bank[key]={'data':base64.b64encode(file.read_bytes()).decode(),'duration':duration}
(WEB/'audio-meta.json').write_text(json.dumps(meta,indent=2),encoding='utf-8')
(WEB/'audio-meta.js').write_text('window.TRAINER_AUDIO_META='+json.dumps(meta)+';',encoding='utf-8')
(WEB/'audio-bank.js').write_text('window.TRAINER_AUDIO='+json.dumps(bank,separators=(',',':'))+';',encoding='utf-8')
subprocess.run(['node',str(WEB/'tools'/'test-core.cjs')],check=True)
plan=json.loads(subprocess.check_output(['node','-e',"const c=require('./core.js'),m=require('./audio-meta.json');console.log(JSON.stringify(c.build(c.defaults,m)))"],cwd=WEB))
(WEB/'preset-plan.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2),encoding='utf-8')
track=np.zeros(round(plan['duration']*RATE),dtype='<i2')
for e in plan['events']:
 pcm=samples[e['key']];pos=round(e['time']*RATE);track[pos:pos+len(pcm)]=pcm
wav=ROOT/'results'/'完整跟练-甜美鼓励型.wav'
with wave.open(str(wav),'wb') as w:w.setnchannels(1);w.setsampwidth(2);w.setframerate(RATE);w.writeframes(track.tobytes())
import imageio_ffmpeg
ffmpeg=imageio_ffmpeg.get_ffmpeg_exe();mp3=ROOT/'results'/'完整跟练-甜美鼓励型.mp3'
subprocess.run([ffmpeg,'-y','-hide_banner','-loglevel','error','-i',str(wav),'-codec:a','libmp3lame','-q:a','4','-ar',str(RATE),str(mp3)],check=True)
check=ROOT/'tmp'/'mp3-roundtrip.wav'
subprocess.run([ffmpeg,'-y','-hide_banner','-loglevel','error','-i',str(mp3),'-acodec','pcm_s16le','-ar',str(RATE),str(check)],check=True)
with wave.open(str(check),'rb') as w:assert abs(w.getnframes()/RATE-plan['duration'])<.2
check.unlink()
for source,name in [(wav,'full-sweet.wav'),(mp3,'full-sweet.mp3')]:
 dest=WEB/name
 if dest.exists():dest.unlink()
 try:os.link(source,dest)
 except OSError:shutil.copy2(source,dest)
html=(WEB/'index.html').read_text(encoding='utf-8')
html=html.replace('<link rel="stylesheet" href="style.css">','<style>'+(WEB/'style.css').read_text(encoding='utf-8')+'</style>')
for name in ['audio-meta.js','core.js','audio-bank.js','app.js']:html=html.replace('<script src="'+name+'"></script>','<script>'+(WEB/name).read_text(encoding='utf-8').replace('</script','<\\/script')+'</script>')
html=html.replace('<link rel="manifest" href="manifest.webmanifest">','').replace('<link rel="icon" href="icon.svg" type="image/svg+xml">','')
(WEB/'offline.html').write_text(html,encoding='utf-8')
archive=ROOT/'results'/'在家动-甜美完整跟练版.zip'
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for f in WEB.rglob('*'):
  if f.is_file() and f.suffix!='.zip':z.write(f,pathlib.Path('在家动-甜美版')/f.relative_to(WEB))
shutil.copy2(archive,WEB/'offline-package.zip')
report={'voice':'甜美鼓励型','duration_seconds':plan['duration'],'duration':f"{plan['duration']//60}:{plan['duration']%60:02d}",'clips':len(bank),'wav':str(wav),'mp3':str(mp3),'mp3_MB':round(mp3.stat().st_size/1024**2,2),'zip':str(archive),'offline':True}
(ROOT/'results'/'甜美完整训练-制作报告.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report,ensure_ascii=False),flush=True)

