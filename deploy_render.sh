# ============================================================================
# FILE 7: deploy_render.sh (Root Directory)
# Deployment helper script
# ============================================================================

#!/bin/bash

echo "=========================================="
echo "  Air Quality Predictor - Render Deploy  "
echo "=========================================="

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if render.yaml exists
if [ ! -f "render.yaml" ]; then
    echo -e "${RED}✗ render.yaml not found!${NC}"
    exit 1
fi

echo -e "${GREEN}✓ render.yaml found${NC}"

# Check if required files exist
echo ""
echo "Checking required files..."

required_files=("requirements.txt" "backend/app/main.py" "data/models/best_model_gradientboosting.pkl")

for file in "${required_files[@]}"; do
    if [ -f "$file" ]; then
        echo -e "${GREEN}✓ $file${NC}"
    else
        echo -e "${RED}✗ $file missing!${NC}"
        exit 1
    fi
done

echo ""
echo -e "${YELLOW}Next steps:${NC}"
echo "1. Create account at https://render.com"
echo "2. Connect your GitHub repository"
echo "3. Create new 'Web Service'"
echo "4. Select your repository"
echo "5. Render will auto-detect render.yaml"
echo "6. Click 'Create Web Service'"
echo ""
echo -e "${GREEN}Your API will be live at: https://your-service.onrender.com${NC}"
echo ""