const statusCode = require('http-status-codes').StatusCodes
const mariadb = require("mariadb")
const axios = require('axios')
let expect = require('expect.js')
require("dotenv").config();

axios.defaults.withCredentials = true
axios.defaults.baseURL = `http://${process.env.API_AUTH_HOST}:${process.env.API_AUTH_PORT}`
axios.defaults.headers.post['Content-Type'] - "application/json"
axios.defaults.timeout = 1000


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

        const apiOptions = {
            url: "/user/new",
            method: "post",
            responseType: "json",
            data: userTest
        }

        it('POST register new user', async function () {
            let response = await axios(apiOptions)
            expect(response.status).to.be(statusCode.OK)
        });

        it('POST register registered user (fail)', async function () {
            try {
                await axios(apiOptions)
                expect().fail(EXPLICIT_FAILURE)
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
            let response = await axios(apiOptions)
            expect(response.status).to.be(statusCode.OK)
        });

        it('POST login incorrect test user (fail)', async function () {
            try {
                apiOptions.data = {
                    username: "testDojoUnexistentUser",
                    email: "test.unexistent.user@dojotest.dev",
                    password: "testDojoFakePasswd"
                }
                let res = await axios(apiOptions)
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
            let response = await axios(apiOptions)
            expect(response.status).to.be(statusCode.OK)
        });

    })

    describe('API Session test', function () {

        const apiOptions = {
            url: null,
            method: null,
            responseType: "json",
            data: null,
            withCredentials: true
        }

        it(' after creating a new account.', async function () {
            apiOptions.url = "/user/new"
            apiOptions.method = "post"
            apiOptions.data = {
                username: "testDojoSessionUser",
                email: "test.session.user@dojotest.dev",
                password: "testDojoSessionUserPasswd"
            }
            let response = await axios(apiOptions)
            expect(response.status).to.be(statusCode.OK)
            apiOptions.url = "/user/login"
            response = await axios(apiOptions)
            expect(response.status).to.be(statusCode.OK)
            response = await axios.get("/user/profile",{
                headers: {
                    'set-cookie': response.headers['set-cookie']
                }
            })
            console.log(response)

            // apiOptions.headers = {'set-cookie': response.headers['set-cookie']}
            // expect(response.status).to.be(statusCode.ACCEPTED)
        })

        // it(' after logged in to an account.')
        // it(' session destroyed after logged out.')

    })

});

