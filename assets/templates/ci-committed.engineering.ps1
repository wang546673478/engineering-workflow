# CI should check out each target commit before invoking this template.
$ErrorActionPreference = "Stop"
if (-not $env:ENGINEERING_COMMIT_SHA) { throw "Set ENGINEERING_COMMIT_SHA to the checked-out commit" }
if (-not $env:ENGINEERING_TASK_ID) { throw "Set ENGINEERING_TASK_ID for the checked-out commit" }
if (-not $env:ENGINEERING_WORKFLOW_SKILL_DIR) { throw "Set ENGINEERING_WORKFLOW_SKILL_DIR" }

$projectRoot = if ($env:ENGINEERING_PROJECT_ROOT) { $env:ENGINEERING_PROJECT_ROOT } else { (git rev-parse --show-toplevel).Trim() }
$manifest = if ($env:ENGINEERING_MANIFEST) { $env:ENGINEERING_MANIFEST } else { "engineering-manifest.json" }
$pythonBin = if ($env:PYTHON) { $env:PYTHON } else { "python" }
& $pythonBin "$env:ENGINEERING_WORKFLOW_SKILL_DIR/scripts/check_project.py" `
  --root $projectRoot --manifest $manifest --mode committed `
  --commit-ref $env:ENGINEERING_COMMIT_SHA --task $env:ENGINEERING_TASK_ID --run-checks
exit $LASTEXITCODE
