import { createContext, useState, type ReactNode } from 'react';

export interface User {
  id: number;
  username: string;
  token?: string;
}

interface UserContextType {
  user: User | null;
  setUser: (user: User | null) => void;
}

// eslint-disable-next-line react-refresh/only-export-components
export const UserContext = createContext<UserContextType | undefined>(undefined);

export function UserProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  return (
    <UserContext.Provider value={{ user, setUser }}>
      {children}
    </UserContext.Provider>
  );
}

