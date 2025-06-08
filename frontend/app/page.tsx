import React from 'react'

export default function DashboardPage() {
  return (
    <main className="flex min-h-screen flex-col">
      <div className="flex-1 p-8">
        <h1 className="text-3xl font-bold mb-8">Dashboard</h1>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {/* Dashboard cards will go here */}
          <div className="bg-white p-6 rounded-lg shadow">
            <h2 className="text-xl font-semibold mb-4">Recent Contacts</h2>
            <p className="text-gray-600">No recent contacts</p>
          </div>
          <div className="bg-white p-6 rounded-lg shadow">
            <h2 className="text-xl font-semibold mb-4">Upcoming Events</h2>
            <p className="text-gray-600">No upcoming events</p>
          </div>
          <div className="bg-white p-6 rounded-lg shadow">
            <h2 className="text-xl font-semibold mb-4">Quick Actions</h2>
            <div className="space-y-2">
              <button className="w-full bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600">
                Add Contact
              </button>
              <button className="w-full bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600">
                Schedule Event
              </button>
            </div>
          </div>
        </div>
      </div>
    </main>
  )
} 