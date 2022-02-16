const dbconnector = require("../plugins/dbconnector")
const statusCode = require('http-status-codes').StatusCodes
const bcrypt = require('bcrypt');
const saltRounds = 12;
const _ = require('lodash');

const success = (object) => Object.assign({ statusCode: statusCode.OK }, object)

async function routes(fastify, options) {

    // use to define reply scheme. Can be use to filter returned object.
    const customOptions = {
        schema: {
            response: {
                200: {
                    type: 'object',
                    properties: {
                        username: { type: 'string' },
                        email: { type: 'string' },
                    }
                }
            }
        }
    }

    fastify.post('/user/login', options, async (request, reply) => {
        try {
            let fetchedUser = await dbconnector.getUserByEmail(request.body.email)
            fetchedUser = fetchedUser[0]
            console.log(fetchedUser)
            bcrypt.compare(request.body.password, fetchedUser.hashPassword).then(result => {
                if (result) {
                    reply.send(success({ message: "Authentication succesful" }))
                } else {
                    reply.send(Error("Authentication failed"))
                }
            })
        } catch (err) {
            reply.send(err)
        }
    })

    fastify.post('/user/new', options, async (request, reply) => {
        try {
            let hasUser = await dbconnector.hasUserByEmail(request.body.email)
            if (hasUser.response) {
                reply.send(Error("email already used by a user"))
            } else {
                bcrypt.hash(request.body.password, saltRounds).then(hash => {
                    dbconnector.addNewUser(request.body.username, request.body.email, hash)
                    reply.send(success({ message: `User '${request.body.username}' signed up successfully` }))
                })
            }
        } catch (err) {
            reply.send(err)
        }
    })

    fastify.post('/user/logout', options, (request, reply) => {
        reply.send(success({ message: "Logout successfully" }))
    })

}

module.exports = routes