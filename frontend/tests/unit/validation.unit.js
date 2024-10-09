import { tokenIsValid, getPayload } from "@/assets/validation";

describe("getPayload", () => {
  it("should return a valid payload from a valid token", () => {
    const token = "header.payload.signature";
    const expectedPayload = { exp: Math.floor(Date.now() / 1000) + 1000 };
    const base64Payload = btoa(JSON.stringify(expectedPayload))
      .replace(/=/g, "")
      .replace(/\+/g, "-")
      .replace(/\//g, "_");
    const validToken = `header.${base64Payload}.signature`;

    const result = getPayload(validToken);
    expect(result).toEqual(expectedPayload);
  });

  it("should return an empty object for an invalid token", () => {
    const invalidToken = "invalid.token";
    const result = getPayload(invalidToken);
    expect(result).toEqual({});
  });

  it("should handle malformed token gracefully", () => {
    const malformedToken = "header.payload";
    const result = getPayload(malformedToken);
    expect(result).toEqual({});
  });
});

describe("tokenIsValid", () => {
  beforeEach(() => {
    global.fetch = vi.fn();
  });

  it("should return false for an empty token", async () => {
    const result = await tokenIsValid("");
    expect(result).toBe(false);
  });

  it("should return false if token is expired", async () => {
    const expiredToken =
      "header." +
      btoa(JSON.stringify({ exp: Math.floor(Date.now() / 1000) - 1000 }))
        .replace(/=/g, "")
        .replace(/\+/g, "-")
        .replace(/\//g, "_") +
      ".signature";

    const result = await tokenIsValid(expiredToken);
    expect(result).toBe(false);
  });

  it("should return false if fetch fails", async () => {
    const validToken =
      "header." +
      btoa(JSON.stringify({ exp: Math.floor(Date.now() / 1000) + 1000 }))
        .replace(/=/g, "")
        .replace(/\+/g, "-")
        .replace(/\//g, "_") +
      ".signature";

    fetch.mockImplementationOnce(() =>
      Promise.reject(new Error("Fetch error"))
    );

    const result = await tokenIsValid(validToken);
    expect(result).toBe(false);
  });

  it("should return the validity of the token from the server", async () => {
    const validToken =
      "header." +
      btoa(JSON.stringify({ exp: Math.floor(Date.now() / 1000) + 1000 }))
        .replace(/=/g, "")
        .replace(/\+/g, "-")
        .replace(/\//g, "_") +
      ".signature";

    fetch.mockResolvedValueOnce({
      json: () => Promise.resolve({ valid: true }),
    });

    const result = await tokenIsValid(validToken);
    expect(result).toBe(true);
  });

  it("should return false if the server says the token is invalid", async () => {
    const validToken =
      "header." +
      btoa(JSON.stringify({ exp: Math.floor(Date.now() / 1000) + 1000 }))
        .replace(/=/g, "")
        .replace(/\+/g, "-")
        .replace(/\//g, "_") +
      ".signature";

    fetch.mockResolvedValueOnce({
      json: () => Promise.resolve({ valid: false }),
    });

    const result = await tokenIsValid(validToken);
    expect(result).toBe(false);
  });
});
