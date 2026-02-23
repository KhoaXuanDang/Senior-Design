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
  User,
} from './types';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';
const TOKEN_KEY = 'access_token';
const USER_KEY = 'user';

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

function getToken(): string | null {
  try {
    return localStorage.getItem(TOKEN_KEY);
  } catch {
    return null;
  }
}

function setToken(token: string) {
  try {
    localStorage.setItem(TOKEN_KEY, token);
  } catch {}
}

function clearAuthStorage() {
  try {
    localStorage.removeItem(TOKEN_KEY);
    localStorage.removeItem(USER_KEY);
  } catch {}
}

function setUserLocal(user: any) {
  try {
    localStorage.setItem(USER_KEY, JSON.stringify(user));
  } catch {}
}

function getUserLocal(): any | null {
  try {
    const raw = localStorage.getItem(USER_KEY);
    return raw ? JSON.parse(raw) : null;
  } catch {
    return null;
  }
}

async function makeRequest(input: RequestInfo, init: RequestInit = {}) {
  const token = getToken();
  // Debug: show whether token is available for this request
  try {
    // eslint-disable-next-line no-console
    console.debug('[api] makeRequest', input, 'hasToken=', !!token);
  } catch {}

  const headers = new Headers(init.headers || {});
  if (token) headers.set('Authorization', `Bearer ${token}`);
  const merged: RequestInit = { ...init, headers };
  const resp = await fetch(input, merged);
  // Debug: log 401 responses to help trace unexpected logouts
  if (resp.status === 401) {
    try {
      console.warn('[api] request returned 401 Unauthorized for', input);
    } catch {}
  }
  return resp;
}

// Health check
export async function checkHealth(): Promise<{ status: string }> {
  const response = await fetch(`${API_BASE_URL}/health`);
  return handleResponse(response);
}

// Auth endpoints
export async function register(data: RegisterRequest): Promise<AuthResponse> {
  const response = await makeRequest(`${API_BASE_URL}/auth/register`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });

  const payload = await handleResponse<AuthResponse>(response);
  if (payload?.access_token) setToken(payload.access_token);
  if (payload?.user) setUserLocal(payload.user);
  return payload;
}

export async function login(data: LoginRequest): Promise<AuthResponse> {
  const response = await makeRequest(`${API_BASE_URL}/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });

  const payload = await handleResponse<AuthResponse>(response);
  if (payload?.access_token) setToken(payload.access_token);
  if (payload?.user) setUserLocal(payload.user);
  return payload;
}

export async function getCurrentUser(): Promise<User> {
  const local = getUserLocal();
  if (local) return local;
  throw new APIError(401, 'No authenticated user');
}

export async function logout(): Promise<{ message: string }> {
  // Call backend logout (best-effort) and clear local auth state
  try {
    await makeRequest(`${API_BASE_URL}/auth/logout`, { method: 'POST' });
  } catch (e) {
    // ignore backend failures
  }
  clearAuthStorage();
  return { message: 'Logout successful' } as { message: string };
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
  const response = await makeRequest(url);
  return handleResponse(response);
}

export async function getRecipeById(id: number): Promise<Recipe> {
  const response = await makeRequest(`${API_BASE_URL}/recipes/${id}`);
  return handleResponse(response);
}

export async function createRecipe(data: CreateRecipeRequest): Promise<Recipe> {
  const response = await makeRequest(`${API_BASE_URL}/recipes`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });
  return handleResponse(response);
}

// Cookbook endpoints
export async function getCookbook(): Promise<CookbookRecipe[]> {
  const response = await makeRequest(`${API_BASE_URL}/cookbook`);
  return handleResponse(response);
}

export async function saveRecipeToCookbook(recipeId: number): Promise<{ message: string }> {
  const response = await makeRequest(`${API_BASE_URL}/cookbook/${recipeId}`, { method: 'POST' });
  return handleResponse(response);
}

export async function removeRecipeFromCookbook(recipeId: number): Promise<{ message: string }> {
  const response = await makeRequest(`${API_BASE_URL}/cookbook/${recipeId}`, { method: 'DELETE' });
  return handleResponse(response);
}

export { APIError };
export { getUserLocal as getStoredUser, setToken, clearAuthStorage, getToken as getStoredToken };
