import os,pathlib,json,hashlib,time,shutil,argparse
ROOT=pathlib.Path(__file__).resolve().parent
for name,folder in [('TEMP','tmp'),('TMP','tmp'),('GRADIO_TEMP_DIR','tmp/gradio'),('HF_HOME','cache/huggingface')]:os.environ[name]=str(ROOT/folder)
os.environ['NO_PROXY']=os.environ.get('NO_PROXY','')+',localhost,127.0.0.1,::1';os.environ['GRADIO_ANALYTICS_ENABLED']='False'
import numpy as np,soundfile as sf
from gradio_client import Client
web=ROOT/'trainer';audio=web/'audio';audio.mkdir(exist_ok=True)
phrases=json.loads((web/'phrases.json').read_text(encoding='utf-8'))
manifest_path=web/'voice-manifest.json';manifest=json.loads(manifest_path.read_text()) if manifest_path.exists() else {}
parser=argparse.ArgumentParser(description='Generate missing or changed sweet voice cues using the running local studio')
parser.add_argument('--studio-url',default='http://127.0.0.1:4173/voice')
args=parser.parse_args()
client=Client(args.studio_url,verbose=False,download_files=False)
started=time.perf_counter()
for i,(key,text) in enumerate(phrases.items(),1):
 out=audio/(key+'.wav');digest=hashlib.sha256(text.encode()).hexdigest()
 if out.exists() and manifest.get(key,{}).get('text_sha256')==digest:print('Cached',i,key,flush=True);continue
 cached=ROOT/'results'/'three-minute'/'甜美鼓励型'/(key+'.wav')
 if key in ['n'+str(n) for n in range(1,9)] and cached.exists():
  shutil.copy2(cached,out);pcm,sr=sf.read(out,dtype='float32');elapsed=0
 else:
  t=time.perf_counter();print('Generating',i,'/',len(phrases),key,text,flush=True)
  result=client.predict(text=text,voice_name='甜美鼓励型',api_name='/generate')
  item=result[0];source=pathlib.Path(item['path'] if isinstance(item,dict) else item)
  assert source.resolve().is_relative_to(ROOT),'Unexpected generated file location'
  pcm,sr=sf.read(source,dtype='float32');assert sr==24000
  if pcm.ndim>1:pcm=pcm.mean(axis=1)
  active=np.flatnonzero(abs(pcm)>.008)
  if len(active):pcm=pcm[max(0,int(active[0]-.03*sr)):min(len(pcm),int(active[-1]+.12*sr))]
  peak=max(abs(pcm)) if len(pcm) else 0
  assert peak>.01,'Silent speech clip'
  pcm*=.85/peak
  sf.write(out,pcm,sr,subtype='PCM_16');elapsed=time.perf_counter()-t
 manifest[key]={'text':text,'text_sha256':digest,'duration':round(len(pcm)/sr,5),'sample_rate':sr,'voice':'甜美鼓励型','generation_seconds':round(elapsed,2)}
 manifest_path.write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
 print('Saved',key,round(len(pcm)/sr,2),'s;',round(elapsed,2),'s generation',flush=True)
print(client.predict(api_name='/release'),flush=True)
print('SWEET_AUDIO_BANK_COMPLETE',len(manifest),'clips;',round(time.perf_counter()-started,1),'seconds',flush=True)
