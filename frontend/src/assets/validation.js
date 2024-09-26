const tokenIsValid = async (token) => {
  if (!token) {
    return false;
  }

  let payload;
  try {
    var base64Url = token.split(".")[1];
    var base64 = base64Url.replace(/-/g, "+").replace(/_/g, "/");
    var jsonPayload = decodeURIComponent(window.atob(base64));
    payload = JSON.parse(jsonPayload);
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

export { tokenIsValid };
