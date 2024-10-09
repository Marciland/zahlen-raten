import { request } from "@/assets/request.js";
describe("request", () => {
  const mockFetch = (
    status,
    body,
    headers = { "content-type": "application/json" }
  ) =>
    vi
      .spyOn(global, "fetch")
      .mockResolvedValue(mockResponse(status, body, headers));

  const mockResponse = (status, body, headers = {}) => {
    return {
      ok: status >= 200 && status < 300,
      status,
      json: () => Promise.resolve(body),
      headers: {
        get: (header) => headers[header] || null,
      },
    };
  };

  beforeEach(() => {
    sessionStorage.clear();
    vi.clearAllMocks();
  });
  /*
  it("should make a GET request with auth header", async () => {
    sessionStorage.setItem("token", "mockToken");

    mockFetch(200, { success: true }, { "content-type": "application/json" });

    const response = await request(
      "http://localhost:5000/some-endpoint",
      "GET"
    );

    expect(fetch).toHaveBeenCalledWith("http://localhost:5000/some-endpoint", {
      method: "GET",
      headers: {
        Authorization: "Bearer mockToken",
      },
    });

    expect(response).toEqual({ success: true });
  });

  it("should handle a 204 response without JSON body", async () => {
    mockFetch(204, null);

    const response = await request("http://localhost:5000/no-content", "GET");
    expect(response).toBeUndefined();
  });

  it("should handle a 401 error by removing token and redirecting", async () => {
    sessionStorage.setItem("token", "mockToken");
    const mockRouterPush = vi.fn();
    global.router = { push: mockRouterPush };
    mockFetch(401, null);

    await expect(
      request("http://localhost:5000/protected", "GET")
    ).rejects.toMatchObject({
      statusCode: 401,
      message: "Ungültige Sitzung. Bitte erneut anmelden!",
    });

    expect(sessionStorage.getItem("token")).toBeNull();
    expect(mockRouterPush).toHaveBeenCalledWith("/");
  });
*/
  it("should set Content-Type header when body is present", async () => {
    sessionStorage.setItem("token", "mockToken");

    mockFetch(200, { success: true }, { "content-type": "application/json" });

    const response = await request("http://localhost:5000/with-body", "POST", {
      data: "test",
    });

    expect(fetch).toHaveBeenCalledWith("http://localhost:5000/with-body", {
      method: "POST",
      headers: {
        Authorization: "Bearer mockToken",
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ data: "test" }),
    });

    expect(response).toEqual({ success: true });
  });

  it("should handle a 422 error with a validation message", async () => {
    sessionStorage.setItem("token", "mockToken");
    const mockRouterPush = vi.fn();
    global.router = { push: mockRouterPush };
    mockFetch(422, null);

    await expect(
      request("http://localhost:5000/validation-endpoint", "POST")
    ).rejects.toMatchObject({
      statusCode: 422,
      message: "Es ist ein Validierungs Fehler aufgetreten!",
    });

    expect(mockRouterPush).not.toHaveBeenCalled();
  });

  it("should handle a 403 error and redirect", async () => {
    sessionStorage.setItem("token", "mockToken");
    const mockRouterPush = vi.fn();
    global.router = { push: mockRouterPush };
    mockFetch(403, null);

    await expect(
      request("http://localhost:5000/protected", "GET")
    ).rejects.toMatchObject({
      statusCode: 403,
      message: "Kein Zugriff",
    });

    expect(mockRouterPush).toHaveBeenCalledWith("/");
  });

  describe("Error Handling in request function", () => {
    const errorStatusCodes = [400, 404, 409, 500, 504];

    errorStatusCodes.forEach((status) => {
      it(`should handle ${status} error and return a generic error message`, async () => {
        sessionStorage.setItem("token", "mockToken");
        const mockRouterPush = vi.fn();
        global.router = { push: mockRouterPush };
        mockFetch(status, null);

        await expect(
          request("http://localhost:5000/protected", "GET")
        ).rejects.toMatchObject({
          statusCode: status,
          message: "Es ist ein Fehler aufgetreten!",
        });

        expect(mockRouterPush).not.toHaveBeenCalled();
      });
    });
  });

  it("should return null when response is not JSON", async () => {
    sessionStorage.setItem("token", "mockToken");
    mockFetch(200, "plain text response", { "content-type": "text/plain" });

    const response = await request(
      "http://localhost:5000/some-endpoint",
      "GET"
    );

    expect(fetch).toHaveBeenCalledWith("http://localhost:5000/some-endpoint", {
      method: "GET",
      headers: {
        Authorization: "Bearer mockToken",
      },
    });

    expect(response).toBeNull();
  });
});
