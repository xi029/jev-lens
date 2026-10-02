param([string]$Repository = 'xi029/jev-lens')
$ErrorActionPreference = 'Stop'

if (-not (Get-Command gh -ErrorAction SilentlyContinue)) {
    throw 'Install GitHub CLI from https://cli.github.com, then run gh auth login and this script again.'
}
gh auth status
if ($LASTEXITCODE -ne 0) { throw 'Run gh auth login first.' }
$taskAccount = gh api user --jq .login
if ($LASTEXITCODE -ne 0 -or $taskAccount -ne 'xi029') { throw 'Sign in to the xi029 GitHub account first.' }
$taskDirty = git status --porcelain
if ($taskDirty) { throw 'Commit your intended files before publishing.' }

gh repo view $Repository --json name --jq .name 2>$null
if ($LASTEXITCODE -eq 0) {
    throw "Repository $Repository already exists. Review its contents before pushing; this script will not overwrite it."
}
gh repo create $Repository --public --source . --remote origin --push --description 'Decide before you generate. Local evidence gates, threshold replay and inspectable RAG traces for Laya, Jev and Ollama.'
if ($LASTEXITCODE -ne 0) { throw 'Repository creation or push failed. Inspect GitHub before retrying.' }
gh api -X PUT "repos/$Repository/topics" -f 'names[]=jev' -f 'names[]=laya' -f 'names[]=rag' -f 'names[]=ollama' -f 'names[]=local-ai' -f 'names[]=decision-models' -f 'names[]=python' -f 'names[]=fastapi'
if ($LASTEXITCODE -ne 0) { Write-Warning 'Repository published, but topics were not updated.' }
Write-Output "Published https://github.com/$Repository"
