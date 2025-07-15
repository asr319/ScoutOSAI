import { useUser } from "../hooks/useUser";

export default function LogoutButton() {
  const { setUser } = useUser();
  return (
    <button
      onClick={() => setUser(null)}
      className="text-sm text-red-600 underline"
    >
      Logout
    </button>
  );
}
