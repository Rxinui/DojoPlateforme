require("dotenv").config();
const express = require('express')
const routeUser = require('./routes/user')
const port = process.env.API_AUTH_PORT || 3000
const host = process.env.API_AUTH_HOST || "localhost"
const app = express()

app.use('/user/', routeUser)

app.get("/", async (request, reply) => {
    reply.send("Hello on api_auth!")
})

app.listen(port, () => {
    console.log(`> Go to the dojo http://${host}:${port}`)
})