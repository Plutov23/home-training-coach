import os,pathlib,json
ROOT=pathlib.Path(__file__).resolve().parent
os.environ['NO_PROXY']=os.environ.get('NO_PROXY','')+',localhost,127.0.0.1,::1'
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import gradio as gr,uvicorn
from local_studio import app as studio
api=FastAPI(title='在家动 · 甜美陪练')
@api.get('/api/status')
def status():
 plan=json.loads((ROOT/'trainer'/'preset-plan.json').read_text(encoding='utf-8'))
 return {'app':'home-trainer-sweet','voice':'甜美鼓励型','seconds':plan['duration'],'ready':True,'root':str(ROOT)}
studio.queue(default_concurrency_limit=1)
api=gr.mount_gradio_app(api,studio,path='/voice',allowed_paths=[str(ROOT/'results')])
api.mount('/',StaticFiles(directory=str(ROOT/'trainer'),html=True),name='trainer')
if __name__=='__main__':
 (ROOT/'trainer.pid').write_text(str(os.getpid()))
 uvicorn.run(api,host='127.0.0.1',port=4173,log_level='warning')
