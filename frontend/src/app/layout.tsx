import type { Metadata } from "next";
import "./globals.css";
import { QueryProvider } from "@/lib/providers/QueryProvider";

export const metadata: Metadata = {
  title: "Plateforme Dropshipping Automatisée",
  description: "Plateforme automatisée pour le dropshipping",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="fr">
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link
          rel="preconnect"
          href="https://fonts.gstatic.com"
          crossOrigin="anonymous"
        />
        <link
          href="https://fonts.googleapis.com/css2?family=Inter:wght@200;300;400;500&display=swap"
          rel="stylesheet"
        />
      </head>
      <body className="relative">
        <div className="fixed inset-0 -z-10">
          {/* Background overlay for glassmorphism */}
        </div>
        <QueryProvider>{children}</QueryProvider>
      </body>
    </html>
  );
}
