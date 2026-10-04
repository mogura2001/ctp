param([ValidateSet('baseline','min20','plus20')][string]$Variant,[ValidateRange(2,8)][int]$Player,[switch]$First,[switch]$Move,[switch]$PreviousCity,[switch]$Bottom)
# Alleen voor visueel gecontroleerde opeenvolgende observaties op T60.
# Player benoemt de opname; de knop plus selecteert de VOLGENDE speler.
# Eerst juiste voorafgaande speler en schermpositie controleren; geen beurten spelen.
$ErrorActionPreference='Stop'
$dir=Join-Path $PSScriptRoot "settlerquota/reeks/$Variant/observatie-T60"
New-Item -ItemType Directory -Path $dir -Force | Out-Null
$control=Join-Path $PSScriptRoot 'Bedien-CTP.ps1'
function Control([string[]]$a) { & powershell -NoProfile -ExecutionPolicy Bypass -File $control @a; if($LASTEXITCODE -ne 0){throw 'Bediening mislukt'} }
$script:prev=$null
function Click([int]$x,[int]$y) { if($null -eq $script:prev){Control @('-Action','Click','-X',"$x",'-Y',"$y",'-ResetCursor')}else{Control @('-Action','Click','-X',"$x",'-Y',"$y",'-FromX',"$($script:prev[0])",'-FromY',"$($script:prev[1])")}; $script:prev=@($x,$y) }
function Capture([string]$name) { Control @('-Action','Capture'); Copy-Item -LiteralPath (Join-Path $PSScriptRoot 'automatisering/ctp-window.png') -Destination (Join-Path $dir "P$Player-$name.png") -Force }
if(-not $First){ if($PreviousCity){Click 1400 639}else{Click 1188 670}; Click 397 152 }
Click 108 156
Capture 'player'
Click 175 180
Click 1874 728
if($Move){Control @('-Action','Drag','-X','300','-Y','8','-ToX','1100','-ToY','300','-ResetCursor'); $script:prev=@(1100,300)}
Capture 'cities'
if($Bottom){Control @('-Action','Drag','-X','1219','-Y','380','-ToX','1219','-ToY','530','-FromX',"$($script:prev[0])",'-FromY',"$($script:prev[1])"); $script:prev=@(1219,530); Capture 'cities-bottom'}
Click 1400 639
Click 1874 748
Capture 'units'
Add-Type -AssemblyName System.Drawing
$src=[Drawing.Bitmap]::FromFile((Join-Path $dir "P$Player-cities.png"))
$playerImg=[Drawing.Bitmap]::FromFile((Join-Path $dir "P$Player-player.png"))
$unitImg=[Drawing.Bitmap]::FromFile((Join-Path $dir "P$Player-units.png"))
$sheet=New-Object Drawing.Bitmap 650,1080
$graphics=[Drawing.Graphics]::FromImage($sheet)
$graphics.Clear([Drawing.Color]::Black)
$graphics.DrawImage($playerImg,[Drawing.Rectangle]::new(0,0,450,35),[Drawing.Rectangle]::new(10,135,450,35),[Drawing.GraphicsUnit]::Pixel)
$graphics.DrawImage($src,[Drawing.Rectangle]::new(0,40,635,360),[Drawing.Rectangle]::new(800,292,635,360),[Drawing.GraphicsUnit]::Pixel)
$graphics.DrawImage($src,[Drawing.Rectangle]::new(455,0,170,35),[Drawing.Rectangle]::new(275,925,170,35),[Drawing.GraphicsUnit]::Pixel)
$graphics.DrawImage($unitImg,[Drawing.Rectangle]::new(0,410,530,290),[Drawing.Rectangle]::new(695,392,530,290),[Drawing.GraphicsUnit]::Pixel)
if(Test-Path (Join-Path $dir "P$Player-cities-bottom.png")){$bottomImg=[Drawing.Bitmap]::FromFile((Join-Path $dir "P$Player-cities-bottom.png")); $graphics.DrawImage($bottomImg,[Drawing.Rectangle]::new(0,720,635,360),[Drawing.Rectangle]::new(800,292,635,360),[Drawing.GraphicsUnit]::Pixel); $bottomImg.Dispose()}
$sheet.Save((Join-Path $dir "P$Player-overzicht.png"),[Drawing.Imaging.ImageFormat]::Png)
$graphics.Dispose();$sheet.Dispose();$src.Dispose();$playerImg.Dispose();$unitImg.Dispose()



