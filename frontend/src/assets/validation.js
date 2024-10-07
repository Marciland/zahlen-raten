const getPayload = (token) => {
  let payload;
  try {
    var base64Url = token.split(".")[1];
    var base64 = base64Url.replace(/-/g, "+").replace(/_/g, "/");
    var jsonPayload = decodeURIComponent(window.atob(base64));
    payload = JSON.parse(jsonPayload);
  } catch (error) {
    payload = {};
  }
  return payload;
};

const tokenIsValid = async (token) => {
  if (!token) {
    return false;
  }

  try {
    let payload = getPayload(token);
    if (Date.now() >= payload.exp * 1000) {
      return false;
    }

    let response = await fetch(`http://localhost:5000/validate?token=${token}`);
    let json = await response.json();
    return json.valid;
  } catch (error) {
    return false;
  }
};

export { tokenIsValid, getPayload };
