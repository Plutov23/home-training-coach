import os,pathlib,json,time,threading,gc
ROOT=pathlib.Path(__file__).resolve().parent
os.environ['NO_PROXY']=os.environ.get('NO_PROXY','')+',localhost,127.0.0.1,::1'
for name,folder in [('HF_HOME','cache/huggingface'),('TORCH_HOME','cache/torch'),('XDG_CACHE_HOME','cache'),('NUMBA_CACHE_DIR','cache/numba'),('GRADIO_TEMP_DIR','tmp/gradio'),('TEMP','tmp'),('TMP','tmp')]:os.environ[name]=str(ROOT/folder)
for folder in ('results','tmp/gradio','cache'):(ROOT/folder).mkdir(parents=True,exist_ok=True)
os.environ['HF_HUB_OFFLINE']='1';os.environ['TRANSFORMERS_OFFLINE']='1';os.environ['GRADIO_ANALYTICS_ENABLED']='False'
import torch,soundfile as sf,gradio as gr
from qwen_tts import Qwen3TTSModel
meta=json.loads((ROOT/'reference'/'两种陪练音色设计.json').read_text(encoding='utf-8-sig'))
model=None;prompts={};mutex=threading.Lock();torch.set_num_threads(4)
def generate(text,voice_name):
 global model
 text=text.strip()
 if not text:raise gr.Error('请先输入需要朗读的文字。')
 if len(text)>240:raise gr.Error('每次最多240字，请把长文分段生成。')
 voice=next(v for v in meta['voices'] if v['name']==voice_name)
 with mutex:
  start=time.perf_counter()
  if model is None:
   if not torch.cuda.is_available():raise gr.Error('没有检测到可用的CUDA显卡。')
   model=Qwen3TTSModel.from_pretrained(str(ROOT/'models'/'Qwen3-TTS-12Hz-0.6B-Base'),device_map='cuda:0',dtype=torch.bfloat16,attn_implementation='sdpa',local_files_only=True)
  if voice_name not in prompts:prompts[voice_name]=model.create_voice_clone_prompt(ref_audio=str(ROOT/'reference'/voice['file']),ref_text=meta['text'],x_vector_only_mode=False)
  torch.cuda.reset_peak_memory_stats()
  with torch.inference_mode():wavs,sr=model.generate_voice_clone(text=text,language='Chinese',voice_clone_prompt=prompts[voice_name],max_new_tokens=1200,temperature=.75,top_p=.9,repetition_penalty=1.05)
  torch.cuda.synchronize()
  name=time.strftime('%Y%m%d-%H%M%S')+'-'+voice_name+'.wav';out=ROOT/'results'/name
  sf.write(str(out),wavs[0],sr,subtype='PCM_16')
  elapsed=time.perf_counter()-start
  record={'text':text,'voice':voice_name,'file':str(out),'generation_seconds':round(elapsed,2),'audio_seconds':round(len(wavs[0])/sr,2),'peak_reserved_GB':round(torch.cuda.max_memory_reserved()/1024**3,2),'offline':True}
  out.with_suffix('.json').write_text(json.dumps(record,ensure_ascii=False,indent=2),encoding='utf-8')
  return str(out),f'完成：音频 {record["audio_seconds"]} 秒，用时 {record["generation_seconds"]} 秒；文件已保存到项目 results 文件夹。'
def release():
 global model
 with mutex:
  model=None;prompts.clear();gc.collect();torch.cuda.empty_cache()
 return '模型已卸载，显存已释放。下次生成会重新加载。'
with gr.Blocks(title='在家动 · 本地声音工作台',analytics_enabled=False) as app:
 gr.Markdown('# 在家动 · 本地声音工作台\n选择陪练声音，输入文字，在本机生成 WAV。首次生成需要加载模型。')
 with gr.Accordion('已经生成的本地试听',open=True):
  for v in meta['voices']:
   sample=ROOT/'results'/('3分钟跟练-'+v['name']+'.wav')
   if sample.exists():gr.Audio(value=str(sample),label='3分钟跟练 · '+v['name'],type='filepath',interactive=False)
   short=ROOT/'results'/('本地-'+v['name']+'.wav')
   if short.exists():gr.Audio(value=str(short),label='短句试听 · '+v['name'],type='filepath',interactive=False)
 voice=gr.Radio([v['name'] for v in meta['voices']],value=meta['voices'][0]['name'],label='陪练声音')
 text=gr.Textbox(value='肩膀放松，保持自然呼吸。手肘向后拉，再慢慢还原。很好，按照自己的节奏来。',label='训练提示文字',lines=5,max_lines=8)
 button=gr.Button('生成本地语音',variant='primary')
 audio=gr.Audio(label='试听与下载',type='filepath')
 status=gr.Textbox(label='生成结果',interactive=False)
 button.click(generate,inputs=[text,voice],outputs=[audio,status],concurrency_limit=1)
 release_button=gr.Button('释放显存')
 release_button.click(release,outputs=status)
 gr.Markdown('所有模型、临时文件和生成结果均保存在当前项目目录。训练计时由训练播放器安排，本页只生成语音素材。')
if __name__=='__main__':
 app.queue(default_concurrency_limit=1).launch(server_name='127.0.0.1',server_port=7861,inbrowser=False,share=False,allowed_paths=[str(ROOT/'results')])



