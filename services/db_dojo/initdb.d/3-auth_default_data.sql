USE dojo_auth;

INSERT INTO User (username,email,hashPassword,roleId)
VALUES
    ('shihan','shihan@dojo.dev', "$2a$12$a6ZxrbUqp1Z05.ygwqr50OTl5TAL60q29.Uyn0lIgtNVHCKjpF0Oe", "shihan");

INSERT INTO Role(roleId)
VALUES
    ("shihan"), -- admin role
    ("deshi"); -- regular user role

INSERT INTO Scope(apiName,scopeValue,summary)
VALUES
    -- must keep it updated
    ("api_vbox", "all", "allows to use all directives. Only for admin."),
    ("api_vbox", "create", "allows to create a new VM instance by using 'import' directive."),
    ("api_vbox", "read", "allows to use all directives that read information."),
    ("api_vbox", "control", "allows to use all control directives (ie. pausevm, startvm...) except unregistervm."),
    ("api_vbox", "delete", "allows to delete vm and related files.");

INSERT INTO ScopeAssignedToRole(roleId, apiName, scopeValue)
VALUES
    ("shihan","api_vbox","all"),
    ("deshi","api_vbox", "create"), -- enable to create a new VM instance
    ("deshi","api_vbox", "control"); -- enable to start a VM instance