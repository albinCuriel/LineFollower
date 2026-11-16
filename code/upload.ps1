# upload.ps1 - compileert en uploadt een sketch naar de ESP32-S3 (Windows PowerShell).
#
#   .\upload.ps1 finaal            finale linefollower-code
#   .\upload.ps1 basis             basisprogramma
#   .\upload.ps1 blink | sensor | hbridge | interrupt | wifi     proof of concepts
#   .\upload.ps1 finaal COM7       met een vaste COM-poort
#   .\upload.ps1 finaal -Monitor   na het uploaden meteen de seriele monitor openen
#
# Sluit de devkit aan op de USB-C-poort met opdruk "COM" (UART). Zet SW1 UIT (nooit USB en batterij tegelijk).
param(
  [Parameter(Mandatory = $true)][string]$Sketch,
  [string]$Poort = "",
  [switch]$Monitor,
  [switch]$EnkelCompileren
)
$ErrorActionPreference = "Stop"
$hier = Split-Path -Parent $MyInvocation.MyCommand.Path
$mappen = @{
  finaal    = "finaal\linefollower"
  basis     = "basis\basis"
  blink     = "proof of concepts\blink\poc_blink"
  sensor    = "proof of concepts\sensor\poc_sensor"
  hbridge   = "proof of concepts\hbridge\poc_hbridge"
  interrupt = "proof of concepts\interrupt\poc_interrupt"
  wifi      = "proof of concepts\wireless communication\poc_wifi"
}
if (-not $mappen.ContainsKey($Sketch)) { Write-Host "Kies uit: $($mappen.Keys -join ', ')"; exit 1 }
$map = Join-Path $hier $mappen[$Sketch]
$fqbn = "esp32:esp32:esp32s3"
$libs = @("--library", (Join-Path $hier "lib\lf_core"), "--library", (Join-Path $hier "lib\lf_esp32"))

Write-Host "== compileren: $($mappen[$Sketch])"
arduino-cli compile --fqbn $fqbn @libs $map
if ($LASTEXITCODE -ne 0) { Write-Host "COMPILEREN MISLUKT"; exit 1 }
if ($EnkelCompileren) { exit 0 }

if ($Poort -eq "") {
  $lijst = arduino-cli board list --format json | ConvertFrom-Json
  $poorten = @($lijst.detected_ports | Where-Object { $_.port.protocol -eq "serial" } | ForEach-Object { $_.port.address })
  if ($poorten.Count -eq 0) { Write-Host "Geen COM-poort gevonden. Kabel in de poort 'COM'? Datakabel (geen laadkabel)?"; exit 1 }
  $Poort = $poorten[-1]
  if ($poorten.Count -gt 1) { Write-Host "Meerdere poorten ($($poorten -join ', ')): ik neem $Poort. Andere poort: .\upload.ps1 $Sketch COMx" }
}
Write-Host "== uploaden naar $Poort"
arduino-cli upload --fqbn $fqbn -p $Poort $map
if ($LASTEXITCODE -ne 0) {
  Write-Host "UPLOADEN MISLUKT. Probeer: BOOT ingedrukt houden, kort op RST drukken, BOOT loslaten, en opnieuw."
  exit 1
}
Write-Host "== klaar"
if ($Monitor) { arduino-cli monitor -p $Poort --config baudrate=115200 }
