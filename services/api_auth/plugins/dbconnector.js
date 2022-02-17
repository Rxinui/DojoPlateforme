const mariadb = require("mariadb");

console.log(process.env.API_DB_HOST)

const pool = mariadb.createPool({
    host: process.env.API_DB_HOST,
    user: process.env.API_DB_USER,
    password: process.env.API_DB_PASSWORD,
    database: process.env.API_DB_DATABASE,
    connectionLimit: process.env.API_DB_CONNECTION_LIMIT,
});

const __hasUserBy = async (byCallback, args) => {
    let user = await byCallback(args)
    return { response: user.length > 0, items: user }

}

const __getUserBy = async (query, ...args) => {
    let conn;
    try {
        conn = await pool.getConnection()
        console.log(`POOL_ID#${conn.threadId}`, args)
        return conn.query({sql: query}, args)
    } catch (err) {
        throw err
    } finally {
        if (conn) conn.release()
    }
}

module.exports = {
    getUserByEmail: async function (email) {
        return __getUserBy("SELECT * FROM User WHERE email=?;", email)
    },
    getUserByUsername: async function (username) {
        return __getUserBy("SELECT * FROM User WHERE username=?;", username)
    },
    hasUserByEmail: async function (email) {
        return __hasUserBy(this.getUserByEmail, email);
    },
    hasUserByUsername: async function (username) {
        return __hasUserBy(this.getUserByUsername, username);
    },
    addNewUser: async function (username, email, hash) {
        let conn;
        try {
            conn = await pool.getConnection()
            return conn.query({sql: "INSERT INTO User (username,email,hashPassword) VALUES (?,?,?);",}, [username, email, hash])
        } catch (err) {
            throw err
        } finally {
            if (conn) conn.release()
        }
    }
};
