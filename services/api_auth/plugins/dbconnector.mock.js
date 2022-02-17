const crypto = require('crypto')

const generateRandomId = () => crypto.randomBytes(6).toString('hex')

module.exports = {
    db: {
        user: {
            '4e57417ff33b': {
                username: "Rxinui",
                email: "rxinui@dojoplateforme.com",
                password: "$2b$12$YBRW19Nt2.huhHUZoBrNQeDiP1EiYJeHHtZP278zz1KXNpM8UQWRy"
            }
        }
    },
    getCurrentUser: function () {
        return { current: true }
    },
    getUserByEmail: function (email) {
        let user = Object.values(this.db.user).filter(u => u.email === email).pop()
        if (user === undefined) throw Error("Inexistent user.")
        return user
    },
    getUserByUsername: function (username) {
        let user = Object.values(this.db.user).filter(u => u.username === username).pop()
        if (user === undefined) throw Error("Inexistent user.")
        return user
    },
    hasUserByEmail: function (email) {
        try {
            const user = this.getUserByEmail(email)
            return { response: true, items: user }
        } catch (err) {
            return { response: false, items: null }
        }
    },
    hasUserByUsername: function (username) {
        try {
            const user = this.getUserByUsername(username)
            return { response: true, items: user }
        } catch (err) {
            return { response: false, items: null }
        }
    },
    addNewUser: function (username, email, hash) {
        let userId = generateRandomId()
        while (userId in this.db.user); {
            userId = generateRandomId()
        }
        this.db.user[userId] = {username: username, email: email, password: hash}
    }
}