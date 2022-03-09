const statusCode = require('http-status-codes').StatusCodes
const mariadb = require("mariadb");
var expect = require('expect.js')
require("dotenv").config();

const api = require('axios').create({
    baseURL: `http://${process.env.API_AUTH_HOST}:${process.env.API_AUTH_PORT}`,
    timeout: 1000,
    headers: { "Content-Type": "application/json" }
})

describe('API /user/', function () {

    const userTest = {
        username: "testDojoUser0",
        email: "test@dojotest.dev",
        password: "testDojoUserPassword"
    }

    after(async function () {
        // runs once after the last test in this block
        let conn;
        try {
            conn = await mariadb.createConnection(
                {
                    host: process.env.API_DB_HOST,
                    user: process.env.API_DB_USER,
                    password: process.env.API_DB_PASSWORD,
                    database: process.env.API_DB_DATABASE,
                    connectionLimit: process.env.API_DB_CONNECTION_LIMIT,
                    namedPlaceholders: true
                }
            )
            conn.query("DELETE FROM User WHERE email=:email", { email: userTest.email })
        } catch (err) {
            console.error(err)
        }
        finally {
            if (conn) conn.end()
        }
    });

    describe('API /user/new', function () {

        const apiOptions = {
            url: "/user/new",
            method: "post",
            responseType: "json",
            data: userTest
        }

        it('POST register new user', async function () {
            let response = await api(apiOptions)
            expect(response.status).to.be(statusCode.OK)
        });

        it('POST register registered user (fail)', async function () {
            try {
                await api(apiOptions)
            } catch (err) {
                expect(err.response.status).to.be(statusCode.INTERNAL_SERVER_ERROR)
            }
        });

    })

    describe('API /user/login', function () {

        const apiOptions = {
            url: "/user/login",
            method: "post",
            responseType: "json",
            data: userTest
        }

        it('POST login test user', async function () {
            let response = await api(apiOptions)
            expect(response.status).to.be(statusCode.OK)
        });

        it('POST login incorrect test user (fail)', async function () {
            try {
                await api(apiOptions)
            } catch (err) {
                expect(err.response.status).to.be(statusCode.INTERNAL_SERVER_ERROR)
            }
        });

    })

    describe('API /user/logout', function () {

        const apiOptions = {
            url: "/user/logout",
            method: "post",
            responseType: "json",
            data: userTest
        }

        it('POST logout test user', async function () {
            let response = await api(apiOptions)
            expect(response.data.statusCode).to.be(statusCode.OK)
        });

    })
});

