import pathlib,os,psutil
root=pathlib.Path(__file__).resolve().parent
target=os.path.normcase(str(root/'training_server.py'))
count=0
for proc in psutil.process_iter(['pid','exe','cmdline']):
 try:
  exe=proc.info['exe'];args=proc.info['cmdline'] or []
  if not exe or not pathlib.Path(exe).resolve().is_relative_to(root):continue
  if not any(os.path.normcase(os.path.abspath(arg))==target for arg in args[1:]):continue
  proc.terminate();count+=1
 except (psutil.NoSuchProcess,psutil.AccessDenied):continue
print('已停止训练助手。' if count else '当前没有运行中的训练助手。')

