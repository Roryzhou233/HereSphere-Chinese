function Test-HereSphereDirectory([string]$Path) {
    if ([string]::IsNullOrWhiteSpace($Path)) { return $false }
    return (Test-Path -LiteralPath (Join-Path $Path 'HereSphere\Binaries\Win64\HereSphere-Win64-Shipping.exe') -PathType Leaf) -and
           (Test-Path -LiteralPath (Join-Path $Path 'HereSphere\Content\Paks\HereSphere-WindowsNoEditor.pak') -PathType Leaf)
}

function Find-HereSphereDirectories([string[]]$SteamRoots, [string[]]$LocalPaths) {
    $libraries = @($SteamRoots)
    foreach ($steam in $SteamRoots) {
        $vdf = Join-Path $steam 'steamapps\libraryfolders.vdf'
        if (Test-Path -LiteralPath $vdf -PathType Leaf) {
            $content = Get-Content -LiteralPath $vdf -Raw -Encoding UTF8
            # Steam's current "path" entries and the older numeric entries.
            foreach ($match in [regex]::Matches($content, '(?m)^\s*"(?:path|\d+)"\s+"((?:\\.|[^"\\])*)"')) {
                $libraries += $match.Groups[1].Value.Replace('\\', '\').Replace('\"', '"')
            }
        }
    }
    $candidates = @($LocalPaths)
    foreach ($library in ($libraries | Sort-Object -Unique)) {
        $candidates += Join-Path $library 'steamapps\common\HereSphere'
        $acf = Join-Path $library 'steamapps\appmanifest_1234730.acf'
        if (Test-Path -LiteralPath $acf -PathType Leaf) {
            $match = [regex]::Match((Get-Content -LiteralPath $acf -Raw -Encoding UTF8), '"installdir"\s+"([^"]+)"')
            if ($match.Success) { $candidates += Join-Path (Join-Path $library 'steamapps\common') $match.Groups[1].Value }
        }
    }
    $candidates | Where-Object { Test-HereSphereDirectory $_ } |
        ForEach-Object { (Get-Item -LiteralPath $_).FullName } | Sort-Object -Unique
}

function Resolve-HereSphereDirectory([string]$Requested) {
    if (-not [string]::IsNullOrWhiteSpace($Requested)) {
        $path = $Requested.Trim().Trim('"')
        if ((Split-Path $path -Leaf) -eq 'HereSphere.exe') { $path = Split-Path $path -Parent }
        if (-not (Test-HereSphereDirectory $path)) { throw "未找到 HereSphere 游戏文件：$path。请选择包含 HereSphere.exe 的游戏根目录。" }
        return (Get-Item -LiteralPath $path).FullName
    }
    $roots = @()
    foreach ($key in @('HKCU:\Software\Valve\Steam', 'HKLM:\SOFTWARE\WOW6432Node\Valve\Steam', 'HKLM:\SOFTWARE\Valve\Steam')) {
        $entry = Get-ItemProperty -LiteralPath $key -ErrorAction SilentlyContinue
        if ($entry.SteamPath) { $roots += $entry.SteamPath }
        if ($entry.InstallPath) { $roots += $entry.InstallPath }
    }
    foreach ($programs in @(${env:ProgramFiles(x86)}, $env:ProgramFiles)) {
        if ($programs) { $roots += Join-Path $programs 'Steam' }
    }
    $found = @(Find-HereSphereDirectories ($roots | Sort-Object -Unique) @($PSScriptRoot, (Split-Path $PSScriptRoot -Parent), (Get-Location).Path))
    if ($found.Count -eq 1) { return $found[0] }
    if ($found.Count -gt 1) {
        Write-Host '找到多个 HereSphere 安装目录：'
        for ($i = 0; $i -lt $found.Count; $i++) { Write-Host ("[{0}] {1}" -f ($i + 1), $found[$i]) }
    } else { Write-Host '未自动找到 HereSphere。可在 Steam 中右键游戏，选择“管理 → 浏览本地文件”查看安装位置。' }
    while ($true) {
        $answer = Read-Host '输入游戏根目录（可拖入文件夹；多个目录可输入编号；直接回车取消）'
        if ([string]::IsNullOrWhiteSpace($answer)) { throw '已取消，未修改游戏文件。' }
        $number = 0
        if ([int]::TryParse($answer, [ref]$number) -and $number -ge 1 -and $number -le $found.Count) { return $found[$number - 1] }
        $path = $answer.Trim().Trim('"')
        if ((Split-Path $path -Leaf) -eq 'HereSphere.exe') { $path = Split-Path $path -Parent }
        if (Test-HereSphereDirectory $path) { return (Get-Item -LiteralPath $path).FullName }
        Write-Host '此目录中没有找到完整游戏文件，请重新输入包含 HereSphere.exe 的根目录。' -ForegroundColor Yellow
    }
}
