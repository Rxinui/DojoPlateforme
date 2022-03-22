const dbconnector = require("../plugins/dbconnector");
const passport = require("passport");
const localStrategy = require("passport-local").Strategy;
const JWTstrategy = require("passport-jwt").Strategy;
const ExtractJWT = require("passport-jwt").ExtractJwt;
const bcrypt = require("bcrypt");

passport.use(
  "login",
  new localStrategy(
    {
      usernameField: "email",
      passwordField: "password",
    },
    async (email, password, done) => {
      try {
        let fetchedUser = await dbconnector.getUserByEmail(email);
        fetchedUser = fetchedUser[0];
        if (!fetchedUser)
          throw Error("Authentication failed: unexistent user.");
        let result = await bcrypt.compare(password, fetchedUser.hashPassword);
        if (!result) {
          throw Error("Authentication failed: wrong password.");
        }
        console.log("DEBUG:Login:ok:");
        return done(null, fetchedUser, "Authentication succesful");
      } catch (err) {
        done(err);
      }
    }
  )
);

passport.use(
  "jwtVerification",
  new JWTstrategy(
    {
      secretOrKey: process.env.API_AUTH_JWT_SECRET,
      jwtFromRequest: ExtractJWT.fromAuthHeaderAsBearerToken(),
      issuer: "api_auth"
    },
    async (token, done) => {
      try {
        let userId = await dbconnector.getUserById(token.sub)
        if (!userId[0]) throw Error(`User with id=${userId} is not registered in the db.`)
        done(null, token);
      } catch (err) {
        console.error(err)
        done(err,false);
      }
    }
  )
);
