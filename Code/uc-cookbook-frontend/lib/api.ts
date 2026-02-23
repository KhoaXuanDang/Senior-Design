// API Client for UC Cookbook Backend

import type {
  AuthResponse,
  LoginRequest,
  RegisterRequest,
  Recipe,
  RecipesResponse,
  CreateRecipeRequest,
  CookbookRecipe,
  ErrorResponse,
} from './types';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';

class APIError extends Error {
  constructor(public status: number, message: string) {
    super(message);
    this.name = 'APIError';
  }
}

async function handleResponse<T>(response: Response): Promise<T> {
  if (!response.ok) {
    let errorMessage = `HTTP ${response.status}: ${response.statusText}`;
    
    try {
      const errorData: ErrorResponse = await response.json();
      errorMessage = errorData.detail || errorData.message || errorMessage;
    } catch {
      // If parsing fails, use default error message
    }
    
    throw new APIError(response.status, errorMessage);
  }
  
  // Handle 204 No Content
  if (response.status === 204) {
    return {} as T;
  }
  
  return response.json();
}

// Health check
export async function checkHealth(): Promise<{ status: string }> {
  const response = await fetch(`${API_BASE_URL}/health`);
  return handleResponse(response);
}

// Auth endpoints
export async function register(data: RegisterRequest): Promise<AuthResponse> {
  const response = await fetch(`${API_BASE_URL}/auth/register`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    credentials: 'include',
    body: JSON.stringify(data),
  });
  return handleResponse(response);
}

export async function login(data: LoginRequest): Promise<AuthResponse> {
  const response = await fetch(`${API_BASE_URL}/auth/login`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    credentials: 'include',
    body: JSON.stringify(data),
  });
  return handleResponse(response);
}

export async function logout(): Promise<{ message: string }> {
  const response = await fetch(`${API_BASE_URL}/auth/logout`, {
    method: 'POST',
    credentials: 'include',
  });
  return handleResponse(response);
}

// Recipe endpoints
export async function getRecipes(params?: {
  search?: string;
  tag?: string;
  difficulty?: string;
  limit?: number;
  offset?: number;
}): Promise<RecipesResponse> {
  const queryParams = new URLSearchParams();
  
  if (params?.search) queryParams.append('search', params.search);
  if (params?.tag) queryParams.append('tag', params.tag);
  if (params?.difficulty) queryParams.append('difficulty', params.difficulty);
  if (params?.limit) queryParams.append('limit', params.limit.toString());
  if (params?.offset) queryParams.append('offset', params.offset.toString());
  
  const url = `${API_BASE_URL}/recipes${queryParams.toString() ? `?${queryParams.toString()}` : ''}`;
  const response = await fetch(url, {
    credentials: 'include',
  });
  return handleResponse(response);
}

export async function getRecipeById(id: number): Promise<Recipe> {
  const response = await fetch(`${API_BASE_URL}/recipes/${id}`, {
    credentials: 'include',
  });
  return handleResponse(response);
}

export async function createRecipe(data: CreateRecipeRequest): Promise<Recipe> {
  const response = await fetch(`${API_BASE_URL}/recipes`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    credentials: 'include',
    body: JSON.stringify(data),
  });
  return handleResponse(response);
}

// Cookbook endpoints
export async function getCookbook(): Promise<CookbookRecipe[]> {
  const response = await fetch(`${API_BASE_URL}/cookbook`, {
    credentials: 'include',
  });
  return handleResponse(response);
}

export async function saveRecipeToCookbook(recipeId: number): Promise<{ message: string }> {
  const response = await fetch(`${API_BASE_URL}/cookbook/${recipeId}`, {
    method: 'POST',
    credentials: 'include',
  });
  return handleResponse(response);
}

export async function removeRecipeFromCookbook(recipeId: number): Promise<{ message: string }> {
  const response = await fetch(`${API_BASE_URL}/cookbook/${recipeId}`, {
    method: 'DELETE',
    credentials: 'include',
  });
  return handleResponse(response);
}

export { APIError };
