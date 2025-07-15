const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";
const USE_MOCK = import.meta.env.VITE_USE_MOCK === "true";

const mockData: Record<string, unknown> = {
  "/ai/chat": { response: "Mocked chat reply" },
  "/ai/tags": { tags: ["mock"] },
  "/ai/merge": { verdict: "Local merge advice" },
  "/memory/list": [],
};

export async function apiFetch(path: string, options?: RequestInit) {
  if (USE_MOCK) {
    const data = mockData[path] ?? { message: "mocked" };
    return {
      ok: true,
      json: async () => data,
    } as Response;
  }
  const res = await fetch(`${API_URL}${path}`, options);
  return res;
}
