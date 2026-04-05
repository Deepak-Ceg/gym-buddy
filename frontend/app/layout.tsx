import "./globals.css";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Gym Buddy",
  description: "Accountability, leaderboards, workouts, and Tamil vegetarian fitness coaching."
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
