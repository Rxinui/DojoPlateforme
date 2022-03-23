const express = require("express");
const statusCode = require("http-status-codes").StatusCodes;
const passport = require("passport");
const { ok, ko } = require("../plugins/utils");
const router = express.Router();
router.use(express.json());

// TODO: make this route internal
// only accessible by other internal API. Configure network and API gateway
router.get(
  "/internal/verify",
  passport.authenticate("jwtVerification", { session: false }),
  async (request, reply) => {
    reply.status(statusCode.ACCEPTED).send(ok("token is legitimate.",request.user));
  }
);

module.exports = router;
