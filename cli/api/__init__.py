"""
cli/api/
--------
One module per backend resource. Each module exports pure async functions
that wrap a single endpoint — no UI, no Typer, no business logic.

Names of resources match the FastAPI router prefixes:
    /api/v1/agent          -> cli.api.agent
    /api/v1/assets         -> cli.api.assets
    /api/v1/audit          -> cli.api.audit
    /api/v1/auth           -> cli.api.auth
    /api/v1/compliance     -> cli.api.compliance
    /api/v1/events         -> cli.api.events
    /api/v1/organizations  -> cli.api.organizations
    /api/v1/transactions   -> cli.api.transactions
    /api/v1/tribunal       -> cli.api.tribunal
    /api/v1/zkp            -> cli.api.zkp
"""
