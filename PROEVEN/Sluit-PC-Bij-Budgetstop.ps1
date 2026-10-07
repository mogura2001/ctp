# Alleen gebruiken na een nieuwe, expliciete afsluitopdracht van de gebruiker.
# Budgetbewaking of automatische doelopvolging mag dit script niet aanroepen.
# Aanroepen nadat de coordinator alle agents heeft onderbroken en hervat vastgelegd.
# Dit script installeert geen timer en sluit apps niet geforceerd.
[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [long]$ExpectedResetUnix,
    [switch]$UserRequestedShutdown
)
$ErrorActionPreference = 'Stop'
if (-not $UserRequestedShutdown) {
    throw 'Afsluiten vereist een nieuwe expliciete gebruikersopdracht; budgetstop alleen geeft geen toestemming.'
}
$budgetPython = 'C:/Users/Stephan/AppData/Local/Programs/Python/Python312/python.exe'
$budgetHelper = Join-Path $PSScriptRoot 'Controleer-Weekbudget.py'
$budgetOutput = & $budgetPython $budgetHelper --thread '01a0f7b4-4751-7513-b510-3835ce43f47d'
$budgetExit = $LASTEXITCODE
if ($budgetExit -notin @(0, 5, 10, 25)) {
    throw 'Geen bruikbare verse budgetmeting; pc wordt niet afgesloten.'
}
$budgetState = ($budgetOutput -join "`n") | ConvertFrom-Json
if ($null -eq $budgetState.five_hour_remaining_percent -or
    $null -eq $budgetState.age_seconds -or $budgetState.age_seconds -gt 120 -or
    $budgetState.state -eq 'unknown') {
    throw 'Vijfuurstand ontbreekt of is verouderd; pc wordt niet afgesloten.'
}
if ($budgetState.five_hour_remaining_percent -gt 5) {
    throw 'De afgesproken vijfuurgrens is nog niet bereikt; pc wordt niet afgesloten.'
}
$observedReset = $budgetState.windows.five_hour.reset_at_unix
if ($null -eq $observedReset -or [Math]::Abs([long]$observedReset - $ExpectedResetUnix) -gt 60) {
    throw 'Dit is niet meer het door de gebruiker bedoelde vijfuurvenster.'
}
$shutdownRecordPath = Join-Path $PSScriptRoot "budget-shutdown-window-$ExpectedResetUnix.json"
if (Test-Path -LiteralPath $shutdownRecordPath) {
    $priorShutdown = Get-Content -LiteralPath $shutdownRecordPath -Raw | ConvertFrom-Json
    if ($priorShutdown.command_accepted -eq $true) {
        throw 'Afsluitcommando voor deze eenmalige opdracht is al geaccepteerd.'
    }
}
$shutdownRecord = [ordered]@{
    requested_at_utc = (Get-Date).ToUniversalTime().ToString('o')
    budget = $budgetState
    command = 'shutdown.exe /s /t 0'
    force_apps = $false
    command_accepted = $false
    limitation = 'Acceptatie van het commando bewijst geen fysieke uitschakeling; apps kunnen afsluiten blokkeren.'
}
$shutdownRecord | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $shutdownRecordPath -Encoding UTF8
& (Join-Path $env:SystemRoot 'System32/shutdown.exe') /s /t 0
$shutdownExit = $LASTEXITCODE
$shutdownRecord['exit_code'] = $shutdownExit
$shutdownRecord['command_accepted'] = ($shutdownExit -eq 0)
$shutdownRecord | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $shutdownRecordPath -Encoding UTF8
if ($shutdownExit -ne 0) {
    throw "Windows weigerde afsluiten, exitcode $shutdownExit."
}
Write-Output 'Windows heeft het afsluitcommando geaccepteerd.'
