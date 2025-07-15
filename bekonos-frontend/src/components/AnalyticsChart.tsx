import { useEffect, useState } from "react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
} from "recharts";
import { useUser } from "../hooks/useUser";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

interface SummaryData {
  name: string;
  count: number;
}

export default function AnalyticsChart() {
  const { user } = useUser();
  const [data, setData] = useState<SummaryData[]>([]);

  useEffect(() => {
    if (!user) return;
    fetch(`${API_URL}/analytics/summary`, {
      headers: user.token ? { Authorization: `Bearer ${user.token}` } : {},
    })
      .then((r) => r.json())
      .then((d) => {
        const arr = Object.entries<number>(d).map(([name, count]) => ({
          name,
          count,
        }));
        setData(arr);
      });
  }, [user]);

  return (
    <div className="w-full h-64">
      <ResponsiveContainer>
        <BarChart data={data}>
          <XAxis dataKey="name" />
          <YAxis allowDecimals={false} />
          <Tooltip />
          <Bar dataKey="count" fill="#8884d8" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
