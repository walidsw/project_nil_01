#!/bin/bash

echo "🚀 Starting DeepMed Application..."

# Function to check if a command is running
is_running() {
    pgrep -f "$1" > /dev/null
}

# Start backend if not running
if ! is_running "manage.py runserver"; then
    echo "📡 Starting Backend Server..."
    cd backend
    source venv/bin/activate
    python manage.py runserver &
    BACKEND_PID=$!
    echo "Backend started with PID: $BACKEND_PID"
    cd ..
    sleep 3
else
    echo "✅ Backend already running"
fi

# Start Flutter app if not running
if ! is_running "flutter run"; then
    echo "📱 Starting Flutter App..."
    flutter run -d "18B959A1-9BFC-43C1-9D4B-797A93086957" &
    FLUTTER_PID=$!
    echo "Flutter app started with PID: $FLUTTER_PID"
else
    echo "✅ Flutter app already running"
fi

echo ""
echo "🎉 DeepMed Application Started!"
echo ""
echo "📱 Flutter App: Running on iPhone Simulator"
echo "📡 Backend API: http://localhost:8000/api/v1/"
echo "🔧 Admin Panel: http://localhost:8000/admin (admin/admin123)"
echo ""
echo "Press Ctrl+C to stop all services"

# Wait for user to stop
trap 'echo "Stopping services..."; kill $BACKEND_PID $FLUTTER_PID 2>/dev/null; exit' INT
wait
