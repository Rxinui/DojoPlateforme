const express = require('express')
const session = require('express-session')
const statusCode = require('http-status-codes').StatusCodes
const { v4: uuidv4 } = require('uuid')
const bcrypt = require('bcrypt');
const dbconnector = require("../plugins/dbconnector")
const router = express.Router()
const MySQLStore = require('express-mysql-session')(session);
const saltRounds = 12;

const success = (msg, options) => Object.assign({ message: msg, statusCode: statusCode.OK }, options)
const error = (err, options) => Object.assign({ message: err.toString(), statusCode: statusCode.INTERNAL_SERVER_ERROR }, options)
const toMillis = (s) => s * 1000;
const IN_PROD = process.env.NODE_ENV === 'production'
const SESSION_COOKIE_NAME = "cookie-name-dev"

let sessionStore = new MySQLStore({
    host: process.env.API_DB_HOST,
    user: process.env.API_DB_USER,
    password: process.env.API_DB_PASSWORD,
    database: process.env.API_DB_DATABASE,
    connectionLimit: process.env.API_DB_CONNECTION_LIMIT,
    endConnectionOnClose: true,
    clearExpired: true,
    checkExpirationInterval: toMillis(180),
    expiration: toMillis(60),
    createDatabaseTable: false,
    schema: {
        tableName: "Session",
        columnNames: {
            session_id: "sessionId",
            data: "data",
            expires: "expires"
        }
    }
})

router.use(express.json())
router.use(session({
    key: SESSION_COOKIE_NAME,
    secret: 'session_cookie_secret',
    store: sessionStore,
    resave: false,
    saveUninitialized: false,
    secure: IN_PROD,
    cookie: {
        maxAge: toMillis(60),
        originalMaxAge: toMillis(60),
        path: "/"
    }
}))


const onRequestProtected = function (request, reply, next) {
    if (request.session) {
        console.log("onRequestProtected: access granted.", request.session)
        return next();
    } else {
        console.error("onRequestProtected: access unauthorized, session missing.", request.session.userId)
        return reply.status(statusCode.UNAUTHORIZED).send(error("No session found for user."));
    }
}

const onAuthentication = function (request, reply, next) {
    if (!request.session.userId) {
        console.log("onAuthentication: NO userId in session.", request.session.userId)
        return next();
    } else {
        console.error("onAuthentication: userId in session.", request.session.userId)
        return reply.status(statusCode.UNAUTHORIZED).send(error("Already authenticated: user id " + request.session.userId));
    }
}

router.post('/login', onAuthentication, async (request, reply) => {
    try {
        let fetchedUser = await dbconnector.getUserByEmail(request.body.email)
        fetchedUser = fetchedUser[0]
        if (fetchedUser === undefined)
            throw Error("Authentication failed: unexistent user.")
        let result = await bcrypt.compare(request.body.password, fetchedUser.hashPassword)
        if (result) {
            request.session.userId = fetchedUser.userId
            console.log("DEBUG:Session:ok:", request.session)
            reply.send(success("Authentication succesful"))
        } else {
            throw Error("Authentication failed: wrong password.")
        }

    } catch (err) {
        console.error("DEBUG:Session:err:", request.session)
        reply.status(statusCode.INTERNAL_SERVER_ERROR).send(error(err))
    }
})


router.get("/profile", onRequestProtected, async (request, reply) => {
    console.log("I can see that because I'm authenticated.")
    reply.status(statusCode.ACCEPTED).send(success("profile access granted."))
})

router.post('/new', async (request, reply) => {
    try {
        let hasUser = await dbconnector.hasUserByEmail(request.body.email)
        if (hasUser.response) {
            throw Error("email already used by a user")
        } else {
            let hash = await bcrypt.hash(request.body.password, saltRounds)
            dbconnector.addNewUser(request.body.username, request.body.email, hash)
            reply.send(success(`User '${request.body.username}' signed up successfully`))
        }
    } catch (err) {
        reply.status(statusCode.INTERNAL_SERVER_ERROR).send(error(err))
    }
})

router.post('/logout', (request, reply) => {
    request.session.destroy(err => {
        if (err)
            reply.status(statusCode.INTERNAL_SERVER_ERROR).send(error(err))
        reply.clearCookie(SESSION_COOKIE_NAME)
        reply.send(success({ message: "Logout successfully" }))
    })
})

module.exports = router