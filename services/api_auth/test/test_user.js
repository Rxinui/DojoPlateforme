require("dotenv").config();
const mariadb = require("mariadb")
const got = require('got');
const statusCode = require('http-status-codes').StatusCodes
const { CookieJar } = require('tough-cookie');
const expect = require('expect.js')

const api = got.extend({
    prefixUrl: `http://${process.env.API_AUTH_HOST}:${process.env.API_AUTH_PORT}/user/`,
    timeout: 2000,
    responsType: 'json'
})
const EXPLICIT_FAILURE = "EXPLICIT_FAILURE"

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
            conn.query("DELETE FROM User WHERE email LIKE :email", { email: "%@dojotest.dev" })
        } catch (err) {
            console.error(err)
        }
        finally {
            if (conn) conn.end()
        }
    });

    describe('API /user/new', function () {

        let endpoint = "new/"

        it('POST register new user', async function () {
            let response = await api.post(endpoint, { json: userTest })
            expect(response.statusCode).to.be(statusCode.OK)
        });

        it('POST register registered user (fail)', async function () {
            try {
                await api.post(endpoint, { json: userTest })
                expect().fail(EXPLICIT_FAILURE)
            } catch (err) {
                expect(err.response.statusCode).to.be(statusCode.INTERNAL_SERVER_ERROR)
            }
        });

    })

    describe('API /user/login', function () {

        let endpoint = "login"

        it('POST login test user', async function () {
            let response = await api.post(endpoint, { json: userTest })
            expect(response.statusCode).to.be(statusCode.OK)
        });

        it('POST login incorrect test user (fail)', async function () {
            try {
                let response = await api.post(endpoint, {
                    json: {
                        username: "testDojoUnexistentUser",
                        email: "test.unexistent.user@dojotest.dev",
                        password: "testDojoFakePasswd"
                    }
                })
            } catch (err) {
                expect(err.response.statusCode).to.be(statusCode.INTERNAL_SERVER_ERROR)
            }
        });

    })

    describe('API /user/logout', function () {

        let endpoint = "logout"

        it('POST logout non-connected user (fail)', async function () {
            try {
                let response = await api.post(endpoint)
            } catch (err) {
                expect(err.response.statusCode).to.be(statusCode.UNAUTHORIZED)
            }
        });

    })

    describe('API Session test', function () {

        const jsonData = {
            username: "testDojoSessionUser",
            email: "test.session.user@dojotest.dev",
            password: "testDojoSessionUserPasswd"
        }

        it('create, login, logout account.', async function () {
            let cookieJar = new CookieJar();
            let response = await api.post("new", { json: jsonData })
            expect(response.statusCode).to.be(statusCode.OK)
            response = await api.post("login", { json: jsonData, cookieJar: cookieJar })
            expect(response.statusCode).to.be(statusCode.OK)
            response = await api.get("profile", { cookieJar: cookieJar })
            expect(response.statusCode).to.be(statusCode.ACCEPTED)
            response = await api.post("logout", { cookieJar: cookieJar })
            expect(response.statusCode).to.be(statusCode.ACCEPTED)
        })

        it('no access to protected /profile when not connected.', async function () {
            try {
                let response = await api.get("profile")
            } catch (err) {
                expect(err.response.statusCode).to.be(statusCode.UNAUTHORIZED)
            }
        })

        it('no access to protected /profile after logout.', async function () {
            let cookieJar = new CookieJar();
            let response = await api.post("login", { json: jsonData, cookieJar: cookieJar })
            response = await api.post("logout", { cookieJar: cookieJar })
            try {
                response = await api.get("profile")
            } catch (err) {
                expect(err.response.statusCode).to.be(statusCode.UNAUTHORIZED)
            }
        })

    })

});

