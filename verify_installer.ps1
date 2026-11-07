$ErrorActionPreference = 'Stop'
$root = Join-Path $PSScriptRoot 'installer-test\中文游戏 [测试]'
$game = 'C:\Program Files (x86)\Steam\steamapps\common\HereSphere'
$relativeExe = 'HereSphere\Binaries\Win64\HereSphere-Win64-Shipping.exe'
$relativePak = 'HereSphere\Content\Paks\HereSphere_Chinese_P.pak'
$relativeBase = 'HereSphere\Content\Paks\HereSphere-WindowsNoEditor.pak'
$exe = Join-Path $root $relativeExe
$pak = Join-Path $root $relativePak
$basePak = Join-Path $root $relativeBase
$manifest = Get-Content (Join-Path $PSScriptRoot 'release\native-patch.json') -Raw | ConvertFrom-Json
New-Item -ItemType Directory -Path (Split-Path $exe),(Split-Path $pak) -Force | Out-Null
Copy-Item -LiteralPath "$(Join-Path $game $relativeExe).cn-original" -Destination $exe -Force
if (-not (Test-Path -LiteralPath $basePak)) { Copy-Item -LiteralPath (Join-Path $game $relativeBase) -Destination $basePak }
# The installer targets a disposable fixture, so mock the live-process guard.
function Get-Process { param($Name,$ErrorAction) return $null }
$installer = Join-Path $PSScriptRoot 'release\Install-Chinese.ps1'
& $installer -GameDir $root
if ((Get-FileHash -LiteralPath $exe).Hash.ToLowerInvariant() -ne $manifest.patched_sha256) { throw 'Install failed' }
& $installer -GameDir $root
& $installer -GameDir $root -Uninstall
if ((Get-FileHash -LiteralPath $exe).Hash.ToLowerInvariant() -ne $manifest.original_sha256 -or (Test-Path -LiteralPath $pak)) { throw 'Uninstall failed' }
$installed = Join-Path $game $relativeExe
if ((Get-FileHash -LiteralPath $installed).Hash.ToLowerInvariant() -in $manifest.previous_patched_sha256) {
    Copy-Item -LiteralPath $installed -Destination $exe -Force
    & $installer -GameDir $root
    if ((Get-FileHash -LiteralPath $exe).Hash.ToLowerInvariant() -ne $manifest.patched_sha256) { throw 'Previous patch upgrade failed' }
    & $installer -GameDir $root -Uninstall
    if ((Get-FileHash -LiteralPath $exe).Hash.ToLowerInvariant() -ne $manifest.original_sha256) { throw 'Upgrade restore failed' }
    Write-Host 'PASS: upgrade from previous patch and restore original.'
}
$bytes = [IO.File]::ReadAllBytes($exe)
$bytes[128] = $bytes[128] -bxor 1
[IO.File]::WriteAllBytes($exe,$bytes)
$invalidHash = (Get-FileHash -LiteralPath $exe).Hash
$rejected = $false
try { & $installer -GameDir $root } catch { $rejected = $_.Exception.Message -like '*版本不受支持*' }
if (-not $rejected -or (Get-FileHash -LiteralPath $exe).Hash -ne $invalidHash -or (Test-Path -LiteralPath $pak)) { throw 'Unsupported version was not safely rejected' }
Write-Host 'PASS: install, repeated install, exact original restoration, PAK removal, unsupported version rejection.'
