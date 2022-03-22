module.exports = {
  ok: (msg, options) => Object.assign({ message: msg }, options),
  ko: (err, options) => Object.assign({ error: err.toString() }, options),
};
