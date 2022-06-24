USE dojo_auth;

INSERT INTO Role(roleId)
VALUES
    ("kumite"); -- [Test only] api_vbox tester role

INSERT INTO ScopeAssignedToRole(roleId, apiName, scopeValue)
VALUES
    ("kumite","api_vbox","all"); -- enable to run blackbox tests of api_vbox/

INSERT INTO User (userId,username,email,hashPassword,roleId)
VALUES 
    (-1,'test.user.deshi','test.user.deshi@dojo.dev', "$2a$12$jnip425vz.6tsRj1zPPk9OZXScxM2bJqbYsQL4QskTO8.VkpbAPKC", "deshi"),
    (-2,'test.api_vbox.kumite','test.api_vbox.kumite@dojo.dev', "$2a$12$jnip425vz.6tsRj1zPPk9OZXScxM2bJqbYsQL4QskTO8.VkpbAPKC", "kumite");