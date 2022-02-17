const express = require('express')
const router = express.Router()
const dbconnector = require("../plugins/dbconnector")
const statusCode = require('http-status-codes').StatusCodes
const bcrypt = require('bcrypt');
const saltRounds = 12;

const success = (msg, options) => Object.assign({ message: msg, statusCode: statusCode.OK }, options)
const error = (err, options) => Object.assign({ message: err.toString(), statusCode: statusCode.INTERNAL_SERVER_ERROR }, options)

router.use(express.json())

router.post('/login', async (request, reply) => {
    try {
        let fetchedUser = await dbconnector.getUserByEmail(request.body.email)
        fetchedUser = fetchedUser[0]
        console.log(fetchedUser)
        let result = await bcrypt.compare(request.body.password, fetchedUser.hashPassword)
        if (result) {
            reply.send(success("Authentication succesful"))
        } else {
            throw Error("Authentication failed")
        }
    } catch (err) {
        reply.status(statusCode.INTERNAL_SERVER_ERROR).send(error(err))
    }
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
    reply.send(success({ message: "Logout successfully" }))
})

module.exports = router