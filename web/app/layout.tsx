
import './globals.css'
import React from 'react';
import Link from 'next/link';

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" suppressHydrationWarning={true}>
      <body className="bg-gray-100 text-gray-900">
        <div className="flex min-h-screen">
          <nav className="w-64 bg-white shadow-md">
            <div className="p-4">
              <h1 className="text-2xl font-bold text-primary-600">HELIO</h1>
            </div>
            <ul className="mt-4">
              <li className="mb-2">
                <Link href="/" className="flex items-center p-2 text-gray-700 rounded-md hover:bg-gray-200">
                  <span>Home</span>
                </Link>
              </li>
              <li className="mb-2">
                <Link href="/dashboard" className="flex items-center p-2 text-gray-700 rounded-md hover:bg-gray-200">
                  <span>Dashboard</span>
                </Link>
              </li>
              <li className="mb-2">
                <Link href="/agentes" className="flex items-center p-2 text-gray-700 rounded-md hover:bg-gray-200">
                  <span>Agentes</span>
                </Link>
              </li>
              <li className="mb-2">
                <Link href="/resultados" className="flex items-center p-2 text-gray-700 rounded-md hover:bg-gray-200">
                  <span>Resultados</span>
                </Link>
              </li>
            </ul>
          </nav>
          <main className="flex-1 p-8">{children}</main>
        </div>
      </body>
    </html>
  )
}
