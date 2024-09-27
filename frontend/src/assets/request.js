const request = async (url, method, body) => {
  const requestOptions = {
    method,
    headers: authHeader(url),
  };

  if (body) {
    requestOptions.headers["Content-Type"] = "application/json";
    requestOptions.body = JSON.stringify(body);
  }

  return await fetch(url, requestOptions).then(handleResponse);
};

function authHeader(url) {
  const token = sessionStorage.getItem("token");
  const isLoggedIn = !!token; // not not existing...
  const apiUrl = `http://localhost:5000`; // 5000 is API
  const isApiUrl = url.startsWith(apiUrl);
  if (isLoggedIn && isApiUrl) {
    return { Authorization: `Bearer ${token}` };
  } else {
    return {};
  }
}

async function handleResponse(response) {
  if (response.status === 204) {
    // 204 No Content will fail parsing json
    return;
  }

  const isJson = response.headers
    ?.get("content-type")
    ?.includes("application/json");
  const data = isJson ? await response.json() : null;

  if (!response.ok) {
    const token = sessionStorage.getItem("token");
    let error = "Unbekannter Fehler!";

    if (response.status === 401 && token) {
      sessionStorage.removeItem("token");
      sessionStorage.removeItem("gameId");
      router.push("/");
      error = "Ungültige Sitzung. Bitte erneut anmelden!";
    }
    if (response.status === 403 && token) {
      router.push("/");
      error = "Kein Zugriff";
    }
    if (response.status === 422) {
      error = "Es ist ein Validierungs Fehler aufgetreten!";
    }
    if ([400, 404, 409, 500, 504].includes(response.status)) {
      error = "Es ist ein Fehler aufgetreten!";
    }
    return Promise.reject({
      statusCode: response.status,
      message: error,
    });
  }

  return data;
}

export { request };
