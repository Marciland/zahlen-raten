const tokenIsValid = (token) => {
  if (!token) {
    return false;
  }

  let payload;
  try {
    var base64Url = token.split(".")[1];
    var base64 = base64Url.replace(/-/g, "+").replace(/_/g, "/");
    var jsonPayload = decodeURIComponent(window.atob(base64));
    payload = JSON.parse(jsonPayload);
  } catch (error) {
    return false;
  }

  if (Date.now() >= payload.exp * 1000) {
    return false;
  }
  return true;
};

export { tokenIsValid };
