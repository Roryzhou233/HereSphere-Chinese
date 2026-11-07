param([string]$GameDir, [switch]$Uninstall)
$ErrorActionPreference = 'Stop'
$utf8 = New-Object System.Text.UTF8Encoding($false)
[Console]::InputEncoding = $utf8
[Console]::OutputEncoding = $utf8
$OutputEncoding = $utf8
. (Join-Path $PSScriptRoot 'Find-HereSphere.ps1')
$GameDir = Resolve-HereSphereDirectory $GameDir
Write-Host "游戏目录：$GameDir"
$exePath = Join-Path $GameDir 'HereSphere\Binaries\Win64\HereSphere-Win64-Shipping.exe'
$pakPath = Join-Path $GameDir 'HereSphere\Content\Paks\HereSphere_Chinese_P.pak'
$basePak = Join-Path $GameDir 'HereSphere\Content\Paks\HereSphere-WindowsNoEditor.pak'
$backup = "$exePath.cn-original"
$manifest = Get-Content -LiteralPath (Join-Path $PSScriptRoot 'native-patch.json') -Raw | ConvertFrom-Json
$build = Get-Content -LiteralPath (Join-Path $PSScriptRoot 'build-report.json') -Raw | ConvertFrom-Json
function Hash([string]$Path) { (Get-FileHash -LiteralPath $Path -Algorithm SHA256).Hash.ToLowerInvariant() }
function FromHex([string]$Value) {
    $bytes = New-Object byte[] ($Value.Length / 2)
    for ($i = 0; $i -lt $bytes.Length; $i++) { $bytes[$i] = [Convert]::ToByte($Value.Substring($i * 2, 2), 16) }
    return ,$bytes
}
if (-not (Test-Path -LiteralPath $exePath)) { throw "HereSphere not found: $exePath" }
if (Get-Process -Name 'HereSphere','HereSphere-Win64-Shipping' -ErrorAction SilentlyContinue) { throw '请先完全退出 HereSphere，再安装或卸载补丁。' }
$current = Hash $exePath
$knownPatches = @($manifest.patched_sha256) + @($manifest.previous_patched_sha256)
if ($Uninstall) {
    if ($current -in $knownPatches) {
        if (-not (Test-Path -LiteralPath $backup)) { throw '找不到原程序备份，无法自动恢复。' }
        if ((Hash $backup) -ne $manifest.original_sha256) { throw '原程序备份校验失败，已停止恢复。' }
        Copy-Item -LiteralPath $backup -Destination $exePath -Force
    } elseif ($current -ne $manifest.original_sha256) {
        Write-Host '游戏程序已更新或发生变化，将保留当前程序。'
    }
    if (Test-Path -LiteralPath $pakPath) {
        if ((Hash $pakPath) -ne $build.patch_sha256) { throw '当前中文 PAK 与本版不一致，已保留该文件。' }
        Remove-Item -LiteralPath $pakPath
    }
    Write-Host '汉化补丁已卸载，原程序备份已保留。'
    exit 0
}
if ($current -ne $manifest.original_sha256 -and $current -notin $knownPatches) { throw '游戏程序版本不受支持，未修改任何文件。' }
if ((Hash $basePak) -ne $build.base_pak_sha256) { throw '原始 PAK 版本不受支持，未修改任何文件。' }
$packagePak = Join-Path $PSScriptRoot 'HereSphere_Chinese_P.pak'
if ((Hash $packagePak) -ne $build.patch_sha256) { throw '补丁资源包校验失败，请重新解压完整补丁。' }
if ($current -ne $manifest.patched_sha256) {
    $previousExe = [IO.File]::ReadAllBytes($exePath)
    if ($current -eq $manifest.original_sha256) {
        $original = $previousExe
    } else {
        if (-not (Test-Path -LiteralPath $backup) -or (Hash $backup) -ne $manifest.original_sha256) { throw '旧版汉化缺少有效的原程序备份，无法升级。' }
        $original = [IO.File]::ReadAllBytes($backup)
    }
    $section = [IO.File]::ReadAllBytes((Join-Path $PSScriptRoot 'native-section.bin'))
    $patched = New-Object byte[] ($manifest.append_offset + $section.Length)
    [Array]::Copy($original, $patched, $original.Length)
    foreach ($edit in $manifest.edits) {
        $before = FromHex $edit.before
        $after = FromHex $edit.after
        for ($i = 0; $i -lt $before.Length; $i++) {
            if ($original[$edit.offset + $i] -ne $before[$i]) { throw '程序补丁位置校验失败，已停止安装。' }
        }
        [Array]::Copy($after, 0, $patched, [int]$edit.offset, $after.Length)
    }
    [Array]::Copy($section, 0, $patched, [int]$manifest.append_offset, $section.Length)
    $sha = [Security.Cryptography.SHA256]::Create()
    try { $result = ([BitConverter]::ToString($sha.ComputeHash($patched))).Replace('-', '').ToLowerInvariant() } finally { $sha.Dispose() }
    if ($result -ne $manifest.patched_sha256) { throw '汉化程序校验失败，已停止安装。' }
    if (Test-Path -LiteralPath $backup) {
        if ((Hash $backup) -ne $manifest.original_sha256) { throw '已有备份与原程序不一致，未修改任何文件。' }
    } else { Copy-Item -LiteralPath $exePath -Destination $backup }
    [IO.File]::WriteAllBytes("$exePath.cn-new", $patched)
    Move-Item -LiteralPath "$exePath.cn-new" -Destination $exePath -Force
}
try { Copy-Item -LiteralPath $packagePak -Destination $pakPath -Force } catch {
    if ($previousExe) { [IO.File]::WriteAllBytes($exePath, $previousExe) }
    throw
}
if ((Hash $exePath) -ne $manifest.patched_sha256 -or (Hash $pakPath) -ne $build.patch_sha256) { throw '安装后文件校验失败。' }
Write-Host '汉化补丁安装完成，文件校验通过。现在可以从 Steam 正常启动 HereSphere。'
