"""
Database seeding script for UC Cookbook

This script populates the database with sample data including:
- Demo user account
- Sample recipes with various difficulty levels
"""

import sys
import os
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app.db.session import SessionLocal, engine
from app.db.models import User, Recipe, CookbookSave
from app.core.security import get_password_hash


def seed_database():
    """Seed the database with initial data"""
    db = SessionLocal()
    
    try:
        print("🌱 Seeding database...")
        
        # Create demo user
        print("Creating demo user...")
        demo_user = User(
            email="demo@mail.uc.edu",
            username="demo_user",
            password_hash=get_password_hash("demo123")
        )
        db.add(demo_user)
        db.commit()
        db.refresh(demo_user)
        print(f"✓ Created user: {demo_user.email}")
        
        # Create additional users
        user2 = User(
            email="john@mail.uc.edu",
            username="john_chef",
            password_hash=get_password_hash("password123")
        )
        db.add(user2)
        db.commit()
        db.refresh(user2)
        print(f"✓ Created user: {user2.email}")
        
        # Sample recipes
        recipes_data = [
            {
                "title": "Classic Mac and Cheese",
                "description": "Creamy, cheesy comfort food perfect for college students. Quick to make and satisfying!",
                "ingredients": [
                    "1 lb elbow macaroni",
                    "4 cups shredded cheddar cheese",
                    "3 cups milk",
                    "1/4 cup butter",
                    "1/4 cup flour",
                    "Salt and pepper to taste"
                ],
                "steps": [
                    "Cook macaroni according to package directions",
                    "In a saucepan, melt butter and whisk in flour",
                    "Gradually add milk, stirring constantly",
                    "Add cheese and stir until melted",
                    "Combine sauce with cooked pasta",
                    "Season with salt and pepper"
                ],
                "tags": ["pasta", "comfort-food", "easy", "vegetarian"],
                "time_minutes": 25,
                "difficulty": "easy",
                "image_url": "https://images.unsplash.com/photo-1543339308-43e59d6b73a6",
                "author_id": demo_user.id
            },
            {
                "title": "UC Bearcat Burrito Bowl",
                "description": "Build your own burrito bowl inspired by campus favorites. Customizable and nutritious!",
                "ingredients": [
                    "2 cups cooked rice",
                    "1 can black beans, drained",
                    "1 lb chicken breast, grilled",
                    "1 cup corn",
                    "1 cup salsa",
                    "1 avocado, sliced",
                    "Sour cream",
                    "Shredded cheese",
                    "Lime wedges"
                ],
                "steps": [
                    "Cook rice according to package",
                    "Season and grill chicken, then slice",
                    "Heat black beans and corn",
                    "Assemble bowls with rice as base",
                    "Add beans, corn, and chicken",
                    "Top with salsa, avocado, cheese, and sour cream",
                    "Serve with lime wedges"
                ],
                "tags": ["mexican", "healthy", "protein", "meal-prep"],
                "time_minutes": 35,
                "difficulty": "medium",
                "image_url": "https://images.unsplash.com/photo-1546793665-c74683f339c1",
                "author_id": user2.id
            },
            {
                "title": "Dorm Room Ramen Upgrade",
                "description": "Transform instant ramen into a gourmet meal with simple additions. Budget-friendly!",
                "ingredients": [
                    "1 package instant ramen",
                    "1 egg",
                    "Green onions, chopped",
                    "Sriracha sauce",
                    "Sesame oil",
                    "Optional: vegetables, protein"
                ],
                "steps": [
                    "Cook ramen according to package, reserve some water",
                    "Soft boil an egg (6 minutes)",
                    "Drain most of the ramen water, leaving a little",
                    "Add sesame oil and mix",
                    "Top with sliced egg, green onions",
                    "Add sriracha to taste"
                ],
                "tags": ["quick", "budget", "asian", "easy"],
                "time_minutes": 10,
                "difficulty": "easy",
                "image_url": "https://images.unsplash.com/photo-1569718212165-3a8278d5f624",
                "author_id": demo_user.id
            },
            {
                "title": "Study Fuel Energy Balls",
                "description": "No-bake energy bites perfect for late-night study sessions. Packed with protein!",
                "ingredients": [
                    "1 cup rolled oats",
                    "1/2 cup peanut butter",
                    "1/3 cup honey",
                    "1/2 cup chocolate chips",
                    "1/4 cup ground flaxseed",
                    "1 tsp vanilla extract"
                ],
                "steps": [
                    "Mix all ingredients in a bowl",
                    "Refrigerate for 30 minutes",
                    "Roll into 1-inch balls",
                    "Store in refrigerator"
                ],
                "tags": ["snack", "healthy", "no-bake", "vegetarian"],
                "time_minutes": 40,
                "difficulty": "easy",
                "image_url": "https://images.unsplash.com/photo-1548848089-d0b86b0b7c42",
                "author_id": user2.id
            },
            {
                "title": "Cincinnati Chili Spaghetti",
                "description": "A Cincinnati classic! Unique chili served over spaghetti. Go Bearcats!",
                "ingredients": [
                    "1 lb ground beef",
                    "1 can tomato sauce",
                    "2 cups water",
                    "2 tbsp chili powder",
                    "1 tsp cinnamon",
                    "1/2 tsp allspice",
                    "1 lb spaghetti",
                    "Shredded cheddar cheese",
                    "Diced onions"
                ],
                "steps": [
                    "Brown ground beef in large pot",
                    "Add tomato sauce, water, and spices",
                    "Simmer for 2 hours",
                    "Cook spaghetti according to package",
                    "Serve chili over spaghetti",
                    "Top with cheese and onions"
                ],
                "tags": ["cincinnati", "local", "comfort-food", "traditional"],
                "time_minutes": 150,
                "difficulty": "medium",
                "image_url": "https://images.unsplash.com/photo-1621996346565-e3dbc646d9a9",
                "author_id": demo_user.id
            },
            {
                "title": "Sheet Pan Chicken Fajitas",
                "description": "Easy one-pan meal perfect for meal prep. Minimal cleanup required!",
                "ingredients": [
                    "2 lbs chicken breast, sliced",
                    "3 bell peppers, sliced",
                    "1 large onion, sliced",
                    "3 tbsp olive oil",
                    "2 tbsp fajita seasoning",
                    "Tortillas",
                    "Optional toppings: sour cream, cheese, guacamole"
                ],
                "steps": [
                    "Preheat oven to 400°F",
                    "Toss chicken and vegetables with oil and seasoning",
                    "Spread on sheet pan in single layer",
                    "Bake for 25-30 minutes",
                    "Serve in warm tortillas with toppings"
                ],
                "tags": ["mexican", "meal-prep", "easy", "protein"],
                "time_minutes": 35,
                "difficulty": "easy",
                "image_url": "https://images.unsplash.com/photo-1565299585323-38d6b0865b47",
                "author_id": user2.id
            },
            {
                "title": "Lazy Lasagna",
                "description": "All the flavor of traditional lasagna with half the effort. Great for feeding a crowd!",
                "ingredients": [
                    "1 lb ground beef or turkey",
                    "1 jar marinara sauce",
                    "15 oz ricotta cheese",
                    "2 cups shredded mozzarella",
                    "1/2 cup parmesan",
                    "9 lasagna noodles",
                    "Italian seasoning"
                ],
                "steps": [
                    "Preheat oven to 375°F",
                    "Brown meat and mix with marinara",
                    "Mix ricotta with 1 cup mozzarella",
                    "Layer: sauce, uncooked noodles, cheese mixture",
                    "Repeat layers, end with sauce and remaining mozzarella",
                    "Cover and bake 45 minutes",
                    "Uncover and bake 15 more minutes"
                ],
                "tags": ["italian", "pasta", "comfort-food", "crowd-pleaser"],
                "time_minutes": 75,
                "difficulty": "medium",
                "image_url": "https://images.unsplash.com/photo-1574894709920-11b28e7367e3",
                "author_id": demo_user.id
            },
            {
                "title": "Banana Protein Pancakes",
                "description": "Healthy breakfast pancakes made with just 3 ingredients. Perfect post-workout meal!",
                "ingredients": [
                    "2 ripe bananas",
                    "4 eggs",
                    "1 scoop protein powder (optional)",
                    "Cooking spray",
                    "Maple syrup for serving"
                ],
                "steps": [
                    "Mash bananas in a bowl",
                    "Beat in eggs until combined",
                    "Add protein powder if using",
                    "Heat griddle over medium heat",
                    "Pour small circles of batter",
                    "Flip when bubbles form",
                    "Cook until golden on both sides"
                ],
                "tags": ["breakfast", "healthy", "protein", "quick"],
                "time_minutes": 15,
                "difficulty": "easy",
                "image_url": "https://images.unsplash.com/photo-1528207776546-365bb710ee93",
                "author_id": user2.id
            },
            {
                "title": "Garlic Parmesan Roasted Vegetables",
                "description": "Easy side dish that makes vegetables actually taste good. Great for meal prep!",
                "ingredients": [
                    "2 cups broccoli florets",
                    "2 cups cauliflower florets",
                    "1 cup baby carrots",
                    "3 tbsp olive oil",
                    "4 cloves garlic, minced",
                    "1/2 cup grated parmesan",
                    "Salt and pepper"
                ],
                "steps": [
                    "Preheat oven to 425°F",
                    "Toss vegetables with olive oil and garlic",
                    "Season with salt and pepper",
                    "Spread on baking sheet",
                    "Roast for 20-25 minutes",
                    "Sprinkle with parmesan last 5 minutes"
                ],
                "tags": ["vegetarian", "healthy", "side-dish", "meal-prep"],
                "time_minutes": 30,
                "difficulty": "easy",
                "image_url": "https://images.unsplash.com/photo-1512621776951-a57141f2eefd",
                "author_id": demo_user.id
            },
            {
                "title": "Slow Cooker Pulled Pork",
                "description": "Set it and forget it! Perfect for game day or meal prep Sunday.",
                "ingredients": [
                    "3-4 lb pork shoulder",
                    "1 cup BBQ sauce",
                    "1/2 cup chicken broth",
                    "2 tbsp brown sugar",
                    "1 tbsp paprika",
                    "1 tsp garlic powder",
                    "Salt and pepper",
                    "Hamburger buns"
                ],
                "steps": [
                    "Season pork with spices",
                    "Place in slow cooker",
                    "Mix BBQ sauce, broth, and brown sugar",
                    "Pour over pork",
                    "Cook on low 8 hours or high 4 hours",
                    "Shred with forks",
                    "Serve on buns"
                ],
                "tags": ["slow-cooker", "protein", "meal-prep", "crowd-pleaser"],
                "time_minutes": 480,
                "difficulty": "easy",
                "image_url": "https://images.unsplash.com/photo-1529006557810-274b9b2fc783",
                "author_id": user2.id
            }
        ]
        
        print("Creating sample recipes...")
        created_recipes = []
        for recipe_data in recipes_data:
            recipe = Recipe(**recipe_data)
            db.add(recipe)
            created_recipes.append(recipe)
        
        db.commit()
        print(f"✓ Created {len(created_recipes)} recipes")
        
        # Add some cookbook saves for demo user
        print("Adding cookbook saves for demo user...")
        for recipe in created_recipes[:3]:  # Save first 3 recipes
            save = CookbookSave(
                user_id=demo_user.id,
                recipe_id=recipe.id
            )
            db.add(save)
        
        db.commit()
        print("✓ Added cookbook saves")
        
        print("\n✅ Database seeding completed successfully!")
        print("\n📊 Summary:")
        print(f"   Users: 2")
        print(f"   Recipes: {len(created_recipes)}")
        print(f"   Cookbook Saves: 3")
        print("\n👤 Demo User Credentials:")
        print(f"   Email: demo@mail.uc.edu")
        print(f"   Password: demo123")
        
    except Exception as e:
        print(f"\n❌ Error seeding database: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
