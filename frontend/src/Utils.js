export function nullToX(object, x) {
  return Object.fromEntries(
    Object.entries(object).map(([key, val]) => [key, val ? val : x]),
  );
}

export function getAuthorization(user) {
  return typeof user !== "undefined" ? "Token " + user.token : "";
}

Number.prototype.mod = function (n) {
  return ((this % n) + n) % n;
};
