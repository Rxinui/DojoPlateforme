require("dotenv").config();
const express = require('express')
const routeUser = require('./routes/user')
const port = 3000
const app = express()

app.use('/user/',routeUser)

app.listen(port, () => {
    console.log(`> Go to the dojo http://localhost:${port}`)
})