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
  is_published: boolean;
  visibility: 'public' | 'private';
  author_id: number;
  author?: {
    id: number;
    username: string;
  };
  origin_recipe_id?: number;
  origin_author?: {
    id: number;
    username: string;
  };
  fork_count?: number;
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
  is_published: boolean;
  visibility: 'public' | 'private';
}

export interface UpdateRecipeRequest {
  title?: string;
  description?: string;
  ingredients?: string[];
  steps?: string[];
  tags?: string[];
  time_minutes?: number;
  difficulty?: 'easy' | 'medium' | 'hard';
  image_url?: string;
  is_published?: boolean;
  visibility?: 'public' | 'private';
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

export interface CommentReactionSummary {
  emoji: string;
  count: number;
  reacted_by_me: boolean;
}

export interface RecipeComment {
  id: number;
  recipe_id: number;
  user_id: number;
  parent_id?: number | null;
  content: string;
  created_at: string;
  user?: {
    id: number;
    username: string;
  };
  reactions: CommentReactionSummary[];
}

export interface AddCommentRequest {
  content: string;
  parent_id?: number | null;
}

export interface Conversation {
  id: number;
  user_one_id: number;
  user_two_id: number;
  user_one?: {
    id: number;
    username: string;
  };
  user_two?: {
    id: number;
    username: string;
  };
  created_at: string;
  updated_at?: string;
}

export interface StartConversationRequest {
  recipient_user_id: number;
  initial_message?: string;
}

export interface Message {
  id: number;
  conversation_id: number;
  sender_id: number;
  content: string;
  created_at: string;
  sender?: {
    id: number;
    username: string;
  };
}

export interface SendMessageRequest {
  content: string;
}
