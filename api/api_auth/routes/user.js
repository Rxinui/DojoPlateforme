const dbconnector = require('../plugins/dbconnector.mock')
const statusCode = require('http-status-codes').StatusCodes
const bcrypt = require('bcrypt');
const saltRounds = 12;

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

    fastify.post('/user/login', options, (request, reply) => {
        try {
            let fetchedUser = dbconnector.getUserByEmail(request.body.email)
            bcrypt.compare(request.body.password, fetchedUser.password).then(result => {
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

    fastify.post('/user/new', options, (request, reply) => {
        let hasUser = dbconnector.hasUserByEmail(request.body.email)
        if (hasUser.response) {
            reply.send(Error("email already used by a user"))
        }
        bcrypt.hash(request.body.password, saltRounds).then(hash => {
            dbconnector.addNewUser(request.body.username, request.body.email, hash)
            reply.send(success({ message: `User '${request.body.username}' signed up successfully` }))
        })
    })

    fastify.post('/user/logout', options, (request, reply) => {
        reply.send(success({message: "Logout successfully"}))
    })

}

module.exports = routes