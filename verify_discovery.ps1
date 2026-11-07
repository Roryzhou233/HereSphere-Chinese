$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot 'release\Find-HereSphere.ps1')
$testRoot = Join-Path $PSScriptRoot 'installer-test\目录识别 [测试]'
$steam = Join-Path $testRoot 'Steam 根目录'
$library = Join-Path $testRoot '另一个磁盘的游戏库'
$game = Join-Path $library 'steamapps\common\HereSphere 自定义名称'
New-Item -ItemType Directory -Path (Join-Path $steam 'steamapps'),(Join-Path $game 'HereSphere\Binaries\Win64'),(Join-Path $game 'HereSphere\Content\Paks') -Force | Out-Null
[IO.File]::WriteAllBytes((Join-Path $game 'HereSphere\Binaries\Win64\HereSphere-Win64-Shipping.exe'),[byte[]]@())
[IO.File]::WriteAllBytes((Join-Path $game 'HereSphere\Content\Paks\HereSphere-WindowsNoEditor.pak'),[byte[]]@())
$vdf = Join-Path $steam 'steamapps\libraryfolders.vdf'
$acf = Join-Path $library 'steamapps\appmanifest_1234730.acf'
[IO.File]::WriteAllText($acf,'"AppState" { "installdir" "HereSphere 自定义名称" }',[Text.Encoding]::UTF8)
foreach ($content in @(
    ('"libraryfolders"' + "`r`n{`r`n" + ' "1"' + "`r`n {`r`n" + ' "path" "' + $library.Replace('\','\\') + '"' + "`r`n }`r`n}"),
    ('"LibraryFolders"' + "`r`n{`r`n" + ' "1" "' + $library.Replace('\','\\') + '"' + "`r`n}")
)) {
    [IO.File]::WriteAllText($vdf,$content,[Text.Encoding]::UTF8)
    $found = @(Find-HereSphereDirectories @($steam) @())
    if ($found.Count -ne 1 -or $found[0] -ne $game) { throw 'Steam library discovery failed' }
}
if ((Resolve-HereSphereDirectory ('"' + $game + '"')) -ne $game) { throw 'Quoted Chinese path resolution failed' }
if ((Resolve-HereSphereDirectory (Join-Path $game 'HereSphere.exe')) -ne $game) { throw 'Launcher path resolution failed' }
$found = @(Find-HereSphereDirectories @() @($game,$game))
if ($found.Count -ne 1) { throw 'Local directory deduplication failed' }
if (Test-HereSphereDirectory (Join-Path $testRoot '不存在的目录')) { throw 'Invalid directory accepted' }
# Exercise the actual prompt branches without touching the real game.
function Get-ItemProperty { param($LiteralPath,$ErrorAction) return $null }
function Find-HereSphereDirectories { return @() }
function Read-Host { param($Prompt) return ('"' + $game + '"') }
if ((Resolve-HereSphereDirectory '') -ne $game) { throw 'Manual path prompt failed' }
function Find-HereSphereDirectories { return @($game,(Join-Path $testRoot '第二个安装')) }
function Read-Host { param($Prompt) return '1' }
if ((Resolve-HereSphereDirectory '') -ne $game) { throw 'Multiple installation selection failed' }
function Find-HereSphereDirectories { return @() }
function Read-Host { param($Prompt) return '' }
$cancelled = $false
try { Resolve-HereSphereDirectory '' | Out-Null } catch { $cancelled = $true }
if (-not $cancelled) { throw 'Blank input did not cancel' }
Write-Host 'PASS: modern/legacy Steam libraries, manifest install directory, Chinese/spaced/bracketed paths, manual selection, multiple installs, cancellation.'
