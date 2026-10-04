param(
    [Parameter(Mandatory=$true)][ValidateSet('Install','Load','OpenEditor','AcceptEditor','StartUnits','Resume','Advance','Cities','MoveCities','Units','Finish')][string]$Stage,
    [Parameter(Mandatory=$true)][ValidateSet(-20,20,-10,10,-5,5)][int]$Quota,
    [int]$Turn = 0
)
$ErrorActionPreference = 'Stop'
$root = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
$sourceRoot = Join-Path $root 'CTP-og/ctp_data/default/aidata/AIPs'
$probeRoot = Join-Path $root 'CTP-proef/ctp_data/default/aidata/AIPs'
$label = if ($Quota -lt 0) { 'min'+(-$Quota) } else { 'plus'+$Quota }
$resultRoot = Join-Path $PSScriptRoot ('settlerquota/reeks/'+$label)
[IO.Directory]::CreateDirectory($resultRoot) | Out-Null
$control = Join-Path $PSScriptRoot 'Bedien-CTP.ps1'
function Invoke-Control {
    param([string[]]$ControlArgs)
    & powershell -NoProfile -ExecutionPolicy Bypass -File $control @ControlArgs
    if ($LASTEXITCODE -ne 0) { throw 'CTP-bediening mislukt; controleer scherm.' }
}
function Click-Control {
    param([int]$ClickX,[int]$ClickY,[int]$PreviousX=-1,[int]$PreviousY=-1)
    if ($PreviousX -lt 0) { Invoke-Control @('-Action','Click','-X',"$ClickX",'-Y',"$ClickY",'-ResetCursor') }
    else { Invoke-Control @('-Action','Click','-X',"$ClickX",'-Y',"$ClickY",'-FromX',"$PreviousX",'-FromY',"$PreviousY") }
}
function Capture-Result {
    Invoke-Control @('-Action','Capture')
    Copy-Item -LiteralPath (Join-Path $PSScriptRoot 'automatisering/ctp-window.png') -Destination (Join-Path $resultRoot ("T$Turn-$Stage.png")) -Force
}
if ($Stage -eq 'Install') {
    $probeExe = Join-Path $root 'CTP-proef/ctp_program/ctp/civctp.exe'
    $running = @(Get-Process civctp -ErrorAction SilentlyContinue)
    foreach ($process in $running) {
        if ($process.Path -ne $probeExe) { throw 'Andere CTP-installatie actief; niet afsluiten.' }
        $process.Kill()
        $process.WaitForExit(5000) | Out-Null
    }
    $encoding = [Text.Encoding]::GetEncoding(28591)
    $changes = @()
    foreach ($file in Get-ChildItem -LiteralPath $sourceRoot -Filter '*.aip') {
        $original = $encoding.GetString([IO.File]::ReadAllBytes($file.FullName))
        $changed = $original
        if ($file.Name -ne 'barbarian.aip') {
            $changed = [regex]::Replace($original,'(?s)(Build_List_Element\s+Land_Settler_Troops_Primary\[MAX_ELEMENTS\];.*?#DATA)(.*?)(#END_DATA)', {
                param($block)
                $block.Groups[1].Value + [regex]::Replace($block.Groups[2].Value,'("UNIT_SETTLER",\s*)-?\d+(?:\.\d+)?(\s*;)',('${1}'+$Quota+'${2}')) + $block.Groups[3].Value
            })
        }
        $target = Join-Path $probeRoot $file.Name
        [IO.File]::WriteAllBytes($target,$encoding.GetBytes($changed))
        if ($encoding.GetString([IO.File]::ReadAllBytes($target)) -cne $changed) { throw 'Variantcontrole mislukt' }
        if ($changed -cne $original) {
            [IO.File]::WriteAllBytes((Join-Path $resultRoot $file.Name),$encoding.GetBytes($changed))
            $changes += [pscustomobject]@{File=$file.Name;Quota=$Quota;Only='Land_Settler_Troops_Primary UNIT_SETTLER'}
        }
    }
    $changes | Export-Csv -LiteralPath (Join-Path $resultRoot 'wijzigingen.csv') -Encoding UTF8 -NoTypeInformation
    $save = Join-Path $PSScriptRoot 'settlerquota/vaste-start/QUOTA-START-T0.sav'
    if ((Get-FileHash -LiteralPath $save).Hash -ne '8C34364200E539870E0DEA0790C98D7441925F52267D24CF0E0ADB152141AD26') { throw 'Startsave veranderd' }
    Copy-Item -LiteralPath $save -Destination (Join-Path $root 'CTP-proef/ctp_program/ctp/save/games/Julius/QUOTA-START-T0') -Force
    Write-Output "Installed $label; $($changes.Count) bestanden uitsluitend primary-quota gewijzigd."
    Invoke-Control @('-Action','Start')
    exit
}
switch ($Stage) {
    'Load' {
        Invoke-Control @('-Action','Key','-Keys','{ESC}')
        Click-Control 1300 390
        Click-Control 1300 427 1300 390
        Click-Control 1040 437 1300 427
        Click-Control 1080 584 1040 437
        Click-Control 1243 751 1080 584
        Start-Sleep -Seconds 3
    }
    'OpenEditor' {
        Invoke-Control @('-Action','Key','-Keys','{ESC}')
        Click-Control 960 620
    }
    'AcceptEditor' {
        Click-Control 1075 627
        Click-Control 1070 667 1075 627
    }
    'StartUnits' {
        Click-Control 395 60
        Click-Control 108 156 395 60
        Click-Control 175 180 108 156
        Click-Control 1879 880 175 180
        Click-Control 1874 748 1879 880
    }
    'Resume' {
        Click-Control 1188 670
        Click-Control 397 152 1188 670
        Click-Control 84 156 397 152
        Click-Control 427 241 84 156
    }
    'Advance' {
        if ($Turn -notin @(5,10,15,20)) { throw 'Gebruik meetpunten 5/10/15/20.' }
        for ($step=0; $step -lt 5; $step++) {
            Invoke-Control @('-Action','Key','-Keys','n')
            Start-Sleep -Seconds 4
        }
    }
    'Cities' {
        Copy-Item -LiteralPath (Join-Path $root 'CTP-proef/ctp_program/ctp/save/games/Julius/AUTOSAVE-Julius') -Destination (Join-Path $resultRoot ("T$Turn.sav")) -Force
        Invoke-Control @('-Action','Key','-Keys','{ESC}')
        Click-Control 960 620
        Click-Control 108 156 960 620
        Click-Control 175 180 108 156
        Click-Control 1874 728 175 180
    }
    'MoveCities' {
        Invoke-Control @('-Action','Drag','-X','300','-Y','8','-ToX','1100','-ToY','300','-ResetCursor')
    }
    'Units' {
        Click-Control 1400 639
        Click-Control 1874 748 1400 639
    }
    'Finish' {
        foreach ($file in Get-ChildItem -LiteralPath $sourceRoot -Filter '*.aip') {
            Copy-Item -LiteralPath $file.FullName -Destination (Join-Path $probeRoot $file.Name) -Force
            if ((Get-FileHash -LiteralPath $file.FullName).Hash -ne (Get-FileHash -LiteralPath (Join-Path $probeRoot $file.Name)).Hash) { throw 'Herstel mislukt' }
        }
        Write-Output 'Originele AIPs hersteld. Lopende game gebruikt mogelijk nog variant; herstart voor verder spelen.'
        exit
    }
}
Capture-Result
