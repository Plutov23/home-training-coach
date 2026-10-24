$ttsRoot=$PSScriptRoot
$env:TEMP=Join-Path $ttsRoot 'tmp'
$env:TMP=$env:TEMP
$env:PIP_CACHE_DIR=Join-Path $ttsRoot 'cache\pip'
$env:HF_HOME=Join-Path $ttsRoot 'cache\huggingface'
$env:TORCH_HOME=Join-Path $ttsRoot 'cache\torch'
$env:XDG_CACHE_HOME=Join-Path $ttsRoot 'cache'
$env:NUMBA_CACHE_DIR=Join-Path $ttsRoot 'cache\numba'
$env:GRADIO_TEMP_DIR=Join-Path $ttsRoot 'tmp\gradio'
$env:PYTHONPYCACHEPREFIX=Join-Path $ttsRoot 'cache\pycache'
$env:HF_HUB_DISABLE_TELEMETRY='1'
$env:DO_NOT_TRACK='1'
$env:PYTHONUTF8='1'
$env:PYTHONIOENCODING='utf-8'
$env:CUDA_VISIBLE_DEVICES='0'


$env:NO_PROXY=($env:NO_PROXY+',localhost,127.0.0.1,::1')
