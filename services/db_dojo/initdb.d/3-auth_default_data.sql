USE dojo_auth;

INSERT INTO User (username,email,hashPassword)
VALUES 
    ('admin','admin@dojo.dev', "$2a$12$HIpKNQIPL16scuo5.OO1bOIV5uogmMsrEvWYqH/bgLNmCAr6cTbNa"),
    ('shihan','shihan@dojo.dev', "$2a$12$a6ZxrbUqp1Z05.ygwqr50OTl5TAL60q29.Uyn0lIgtNVHCKjpF0Oe");

INSERT INTO Role(roleName)
VALUES
    ("sensei"), -- teacher role
    ("deshi"); -- student role

INSERT INTO Scope(apiName,scopeValue,summary)
VALUES
    -- must keep it updated
    ("api_vbox", "all", "allows to use all directives. Only for admin."),
    ("api_vbox", "create", "allows to create a new VM instance by using 'import' directive."),
    ("api_vbox", "read", "allows to use all directives that read information."),
    ("api_vbox", "control", "allows to use all directives that read information.");

INSERT INTO ScopeAssignedToUser(userId, apiName, scopeValue)
VALUES
    (1,"api_vbox","all"),
    (2,"api_vbox", "create"),
    (2,"api_vbox", "read"),
    (2,"api_vbox", "control");

INSERT INTO RoleOwnedByUser(userId, roleName)
VALUES
    (1,"sensei"),
    (1,"deshi"),
    (2,"sensei");