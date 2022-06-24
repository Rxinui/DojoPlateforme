const express = require("express");
const statusCode = require("http-status-codes").StatusCodes;
const bcrypt = require("bcrypt");
const dbconnector = require("../plugins/dbconnector");
const { ok, ko } = require("../plugins/utils");
const passport = require("passport");
const jwt = require("jsonwebtoken");
const router = express.Router();
const saltRounds = 12;
const JWT_EXPIRATION_TIME = "60m"; // 10 minute
const SEP_JWT_MULTIVALUES = " ";
// const DOJO_USER_ROLE = "deshi";
router.use(express.json());

router.get(
  "/profile",
  passport.authenticate("jwtVerification", { session: false }),
  async (request, reply) => {
    // console.log(request.user);
    reply.status(statusCode.ACCEPTED).send(ok("profile access granted."));
  }
);

router.post("/login", async (request, reply, next) => {
  passport.authenticate("login", async (err, user, info) => {
    try {
      if (err) throw err;
      console.log("/login debug:", info, user);
      request.login(user, { session: false }, async (err) => {
        if (err) return next(err);
        let role = user.roleId;
        let scope = await dbconnector.getRoleScopes(user.roleId);
        const options = {
          issuer: "api_auth",
          subject: user.userId.toString(),
          expiresIn: JWT_EXPIRATION_TIME,
        };
        const payload = { 
          user: user.username,
          roles: role,
          scope: scope.map((arr) => arr.join(":")).join(SEP_JWT_MULTIVALUES)
        };
        const token = jwt.sign(
          payload,
          process.env.API_AUTH_JWT_SECRET,
          options
        );
        return reply.send({ token });
      });
    } catch (err) {
      console.error("DEBUG:login:error", err);
      reply.status(statusCode.INTERNAL_SERVER_ERROR).send(ko(err));
    }
  })(request, reply, next);
});

router.post("/new", async (request, reply) => {
  try {
    let hash = await bcrypt.hash(request.body.password, saltRounds);
    await dbconnector.addNewUser(
      request.body.username,
      request.body.email,
      hash
    );
    reply.send(ok(`User '${request.body.username}' signed up successfully`));
  } catch (err) {
    console.error("/new failed:", err.text);
    reply.status(statusCode.INTERNAL_SERVER_ERROR).send(ko(err.text));
  }
});

router.post("/logout", (request, reply) => {});

module.exports = router;
