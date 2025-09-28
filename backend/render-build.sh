#!/bin/bash
# Render build script for backend

echo "🔧 Building Khel Bhoomi Backend..."

# Install dependencies
pip install -r requirements.txt

echo "✅ Backend dependencies installed"

# Optional: Run any database migrations or setup
if [ "$ENVIRONMENT" = "production" ]; then
    echo "🏃‍♂️ Running production setup..."
    # Add any production-specific setup here
fi

echo "🎉 Backend build complete!"