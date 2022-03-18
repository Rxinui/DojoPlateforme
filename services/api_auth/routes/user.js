const express = require("express");
const statusCode = require("http-status-codes").StatusCodes;
const bcrypt = require("bcrypt");
const dbconnector = require("../plugins/dbconnector");
const passport = require("passport");
const jwt = require("jsonwebtoken");
const router = express.Router();
const saltRounds = 12;
const success = (msg, options) => Object.assign({ message: msg }, options);
const error = (err, options) =>
  Object.assign({ error: err.toString() }, options);
const JWT_EXPIRATION_TIME = "10m"; // 10 minute
const SEP_JWT_MULTIVALUES = " ";
router.use(express.json());

router.get(
  "/profile",
  passport.authenticate("jwtVerification", { session: false }),
  async (request, reply) => {
    console.log("I can see that because I'm authenticated.");
    // console.log(request.user);
    reply.status(statusCode.ACCEPTED).send(success("profile access granted."));
  }
);

router.post("/login", async (request, reply, next) => {
  passport.authenticate("login", async (err, user, info) => {
    try {
      if (err) throw err;
      console.log("/login debug:",info);
      request.login(user, { session: false }, async (err) => {
        if (err) return next(err);
        let roles = await dbconnector.getUserRoles(user.userId);
        let scope = await dbconnector.getUserScopes(user.userId);
        const options = {
          issuer: "api_auth",
          subject: user.userId.toString(),
          expiresIn: JWT_EXPIRATION_TIME,
        };
        const payload = {
          user: { name: user.username, userId: user.userId },
          roles: [...roles].flat(1).join(SEP_JWT_MULTIVALUES),
          scope: scope.map((arr) => arr.join(":")).join(SEP_JWT_MULTIVALUES),
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
      reply.status(statusCode.INTERNAL_SERVER_ERROR).send(error(err));
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
    reply.send(
      success(`User '${request.body.username}' signed up successfully`)
    );
  } catch (err) {
    console.error("/new failed:", err.text);
    reply.status(statusCode.INTERNAL_SERVER_ERROR).send(error(err.text));
  }
});

router.post("/logout", (request, reply) => {});

module.exports = router;
