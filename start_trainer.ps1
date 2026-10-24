param([switch]$NoBrowser)
$ErrorActionPreference='Stop'
$ttsRoot=$PSScriptRoot
. (Join-Path $ttsRoot 'env.ps1')
$ttsAddress='http://127.0.0.1:4173'
function Get-TrainerStatus {
 $ttsRequest=[System.Net.HttpWebRequest]::Create($ttsAddress+'/api/status')
 $ttsRequest.Proxy=$null
 $ttsRequest.Timeout=2000
 $ttsResponse=$ttsRequest.GetResponse()
 try { $ttsReader=New-Object System.IO.StreamReader($ttsResponse.GetResponseStream()); try { return ($ttsReader.ReadToEnd() | ConvertFrom-Json) } finally { $ttsReader.Dispose() } } finally { $ttsResponse.Dispose() }
}
$ttsReady=$false
try { $ttsReady=((Get-TrainerStatus).app -eq 'home-trainer-sweet') } catch {}
if (-not $ttsReady) {
 New-Item -ItemType Directory -Force -Path (Join-Path $ttsRoot 'logs') | Out-Null
 $ttsProcess=Start-Process -FilePath (Join-Path $ttsRoot 'venv\Scripts\python.exe') -ArgumentList @((Join-Path $ttsRoot 'training_server.py')) -WorkingDirectory $ttsRoot -WindowStyle Hidden -RedirectStandardOutput (Join-Path $ttsRoot 'logs\trainer-out.log') -RedirectStandardError (Join-Path $ttsRoot 'logs\trainer-error.log') -PassThru
 for ($ttsAttempt=0;$ttsAttempt -lt 60;$ttsAttempt++) {
  Start-Sleep -Milliseconds 500
  try { if ((Get-TrainerStatus).app -eq 'home-trainer-sweet') { $ttsReady=$true;break } } catch {}
  if ($ttsProcess.HasExited) { throw '启动失败，请查看 logs/trainer-error.log' }
 }
}
if (-not $ttsReady) { throw '启动超时，请查看 logs/trainer-error.log' }
Write-Output ('在家动已启动：'+$ttsAddress)
if (-not $NoBrowser) { Start-Process $ttsAddress }

if ($ttsProcess) { Write-Output '保持此窗口开启。结束使用可运行 停止训练助手.cmd'; $ttsProcess.WaitForExit() }

