require("dotenv").config();
const express = require('express')
const cors = require('cors')
const routeUser = require('./routes/user')
const routeToken = require('./routes/token')
const port = process.env.API_AUTH_PORT || 3000
const host = process.env.API_AUTH_HOST || "localhost"
const app = express()

require('./plugins/auth');

app.use(cors({
    origin: [`http://${host}:${port}`],
    methods: ["GET", "POST", "PUT", "DELETE"],
    credentials: true
}))

app.use('/token/', routeToken)
app.use('/user/', routeUser)

app.get("/", async (request, reply) => {
    reply.send("Hello on api_auth!")
})

app.listen(port, () => {
    console.log(`> Go to the dojo http://${host}:${port}`)
})