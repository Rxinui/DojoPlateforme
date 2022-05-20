USE dojo_auth;

INSERT INTO User (userId,username,email,hashPassword)
VALUES 
    (-1,'t.api_vbox.scope_1','t.api_vbox.scope_1@dojo.dev', "$2a$12$jnip425vz.6tsRj1zPPk9OZXScxM2bJqbYsQL4QskTO8.VkpbAPKC"),
    (-2,'t.api_vbox.scope_2','t.api_vbox.scope_2@dojo.dev', "$2a$12$jnip425vz.6tsRj1zPPk9OZXScxM2bJqbYsQL4QskTO8.VkpbAPKC"),
    (-3,'t.api_vbox.scope_3','t.api_vbox.scope_3@dojo.dev', "$2a$12$jnip425vz.6tsRj1zPPk9OZXScxM2bJqbYsQL4QskTO8.VkpbAPKC");

INSERT INTO ScopeAssignedToUser(userId, apiName, scopeValue)
VALUES
    (-1,"api_vbox","read"),
    (-2,"api_vbox", "create"),
    (-3,"api_vbox", "control");

INSERT INTO RoleOwnedByUser(userId, roleName)
VALUES
    (-1,"deshi"),
    (-2,"deshi"),
    (-3,"deshi");