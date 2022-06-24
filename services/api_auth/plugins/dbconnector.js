const mariadb = require("mariadb");

const pool = mariadb.createPool({
  host: process.env.API_DB_HOST,
  user: process.env.API_DB_USER,
  password: process.env.API_DB_PASSWORD,
  database: process.env.API_DB_DATABASE,
  connectionLimit: process.env.API_DB_CONNECTION_LIMIT,
});

const __hasUserBy = async (byCallback, args) => {
  let user = await byCallback(args);
  return { response: user.length > 0, items: user };
};

const __queryDb = async (query, rowsAsArray, args) => {
  let conn;
  try {
    conn = await pool.getConnection();
    console.log(`POOL_ID#${conn.threadId}`, args);
    return conn.query({ sql: query, rowsAsArray: rowsAsArray }, args);
  } catch (err) {
    console.error(err);
    throw err;
  } finally {
    if (conn) conn.release();
  }
};

module.exports = {
  getRoleScopes: async function (roleId) {
    return __queryDb(
      "SELECT apiName, scopeValue FROM ScopeAssignedToRole WHERE roleId=?;",
      true,
      roleId
    );
  },
  getUserById: async function (userId) {
    return __queryDb("SELECT * FROM User WHERE userId=?;",false, userId);
  },
  getUserByEmail: async function (email) {
    return __queryDb("SELECT * FROM User WHERE email=?;",false, email);
  },
  getUserByUsername: async function (username) {
    return __queryDb("SELECT * FROM User WHERE username=?;",false, username);
  },
  addNewUser: async function (username, email, hash) {
    return __queryDb(
      "INSERT INTO User (username,email,hashPassword) VALUES (?,?,?);",
      false,
      [username, email, hash]
    );
  },
};
