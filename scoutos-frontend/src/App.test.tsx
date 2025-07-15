import { describe, it, expect, vi } from "vitest";
import { render, fireEvent } from "@testing-library/react";
import { UserProvider, UserContext, type User } from "./context/UserContext";
import { WebSocketProvider } from "./context/WebSocketContext";
import App from "./App";

describe("App", () => {
  it("renders without crashing", () => {
    const { container } = render(
      <UserProvider>
        <App />
      </UserProvider>,
    );
    expect(container).toBeTruthy();
  });

  it("navigates to memory manager when authenticated", () => {
    const user: User = { id: 1, username: "bob", token: "t" };
    const fetchMock = vi
      .fn()
      .mockResolvedValue({ ok: true, json: () => Promise.resolve([]) });
    vi.stubGlobal("fetch", fetchMock);
    const { getByText } = render(
      <UserContext.Provider value={{ user, setUser: vi.fn() }}>
        <WebSocketProvider>
          <App />
        </WebSocketProvider>
      </UserContext.Provider>,
    );
    fireEvent.click(getByText("Memories"));
    expect(getByText("Add Memory")).toBeTruthy();
    vi.restoreAllMocks();
  });
});
