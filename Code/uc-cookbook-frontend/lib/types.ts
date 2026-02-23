// Type definitions for UC Cookbook API

export interface User {
  id: number;
  email: string;
  username: string;
  created_at: string;
}

export interface Recipe {
  id: number;
  title: string;
  description: string;
  ingredients: string[];
  steps: string[];
  tags: string[];
  time_minutes: number;
  difficulty: 'easy' | 'medium' | 'hard';
  image_url?: string;
  author_id: number;
  author?: {
    id: number;
    username: string;
  };
  created_at: string;
  updated_at?: string;
}

export interface AuthResponse {
  access_token?: string;
  token?: string;
  user: User;
  message?: string;
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface RegisterRequest {
  email: string;
  username: string;
  password: string;
}

export interface CreateRecipeRequest {
  title: string;
  description: string;
  ingredients: string[];
  steps: string[];
  tags: string[];
  time_minutes: number;
  difficulty: 'easy' | 'medium' | 'hard';
  image_url?: string;
}

export interface RecipesResponse {
  recipes: Recipe[];
  total: number;
  limit: number;
  offset: number;
}

export interface CookbookRecipe {
  id: number;
  user_id: number;
  recipe_id: number;
  recipe: Recipe;
  saved_at: string;
}

export interface ErrorResponse {
  detail: string;
  message?: string;
}
