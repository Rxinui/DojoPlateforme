const dbconnector = require('../plugins/dbconnector.mock')
const statusCode = require('http-status-codes').StatusCodes

const success = (object) => Object.assign({ statusCode: statusCode.OK }, object)

async function routes(fastify, options) {

}

module.exports = routes