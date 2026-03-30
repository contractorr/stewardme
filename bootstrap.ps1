param(
    [switch]$WithWeb,
    [switch]$WithAllProviders,
    [switch]$DryRun
)

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

function Invoke-External {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Description,
        [Parameter(Mandatory = $true)]
        [string]$FilePath,
        [string[]]$Arguments = @()
    )

    $display = (@($FilePath) + $Arguments) -join " "
    Write-Host "==> $Description"
    Write-Host "    $display"

    if ($DryRun) {
        return
    }

    & $FilePath @Arguments
    if ($LASTEXITCODE -ne 0) {
        throw "Command failed: $display"
    }
}

function Get-PythonCommand {
    $python = Get-Command python -ErrorAction SilentlyContinue
    if ($python) {
        return @{
            FilePath = $python.Source
            Arguments = @()
        }
    }

    $py = Get-Command py -ErrorAction SilentlyContinue
    if ($py) {
        return @{
            FilePath = $py.Source
            Arguments = @("-3")
        }
    }

    throw "Python 3.11+ is required but neither 'python' nor 'py' was found on PATH."
}

$repoRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Push-Location $repoRoot

try {
    $pythonCmd = Get-PythonCommand

    $uvCommand = Get-Command uv -ErrorAction SilentlyContinue
    if (-not $uvCommand) {
        Invoke-External `
            -Description "Installing uv via pip" `
            -FilePath $pythonCmd.FilePath `
            -Arguments ($pythonCmd.Arguments + @("-m", "pip", "install", "uv"))

        $uvFilePath = $pythonCmd.FilePath
        $uvArgumentsPrefix = $pythonCmd.Arguments + @("-m", "uv")
    }
    else {
        $uvFilePath = $uvCommand.Source
        $uvArgumentsPrefix = @()
    }

    $extras = @("--extra", "dev")
    if ($WithWeb) {
        $extras += @("--extra", "web")
    }
    if ($WithAllProviders) {
        $extras += @("--extra", "all-providers")
    }

    Invoke-External `
        -Description "Creating local virtual environment" `
        -FilePath $uvFilePath `
        -Arguments ($uvArgumentsPrefix + @("venv", ".venv"))
    Invoke-External `
        -Description "Syncing Python dependencies" `
        -FilePath $uvFilePath `
        -Arguments ($uvArgumentsPrefix + @("sync", "--frozen") + $extras)

    if ($WithWeb) {
        if (-not (Get-Command npm -ErrorAction SilentlyContinue)) {
            throw "npm is required for frontend setup. Install Node.js 18+ and rerun with -WithWeb."
        }
        Invoke-External -Description "Installing frontend dependencies" -FilePath "npm" -Arguments @("ci", "--prefix", "web")
    }

    Write-Host ""
    Write-Host "Bootstrap complete."
    Write-Host "Recommended next commands:"
    Write-Host "  uv run pytest -m `"not slow and not web and not integration`" --durations=20"
    Write-Host "  uv run ruff check src tests"
    if ($WithWeb) {
        Write-Host "  npm --prefix web run lint"
    }
}
finally {
    Pop-Location
}
