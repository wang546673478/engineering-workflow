# Copy this file to a project hook/CI step and set ENGINEERING_WORKFLOW_SKILL_DIR.
$ErrorActionPreference = "Stop"
$projectRoot = if ($env:ENGINEERING_PROJECT_ROOT) { $env:ENGINEERING_PROJECT_ROOT } else { (git rev-parse --show-toplevel).Trim() }
$manifest = if ($env:ENGINEERING_MANIFEST) { $env:ENGINEERING_MANIFEST } else { "engineering-manifest.json" }
$skillDir = $env:ENGINEERING_WORKFLOW_SKILL_DIR
if (-not $skillDir) { throw "Set ENGINEERING_WORKFLOW_SKILL_DIR to the engineering-workflow skill directory" }
$pythonBin = if ($env:PYTHON) { $env:PYTHON } else { "python" }
$arguments = @("$skillDir/scripts/check_project.py", "--root", $projectRoot, "--manifest", $manifest, "--mode", "commit", "--run-checks")
if ($env:ENGINEERING_TASK_ID) { $arguments += @("--task", $env:ENGINEERING_TASK_ID) }
& $pythonBin @arguments
exit $LASTEXITCODE
