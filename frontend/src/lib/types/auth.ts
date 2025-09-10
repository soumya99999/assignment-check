export interface RegisterForm {
  username: string;
  email: string;
  first_name: string;
  last_name: string;
  role: string;
  password: string;
  password2: string;
  regdno: string;
}

export interface LoginForm {
  username: string;
  password: string;
}

export interface AuthResponse {
  access: string;
  refresh: string;
}

export interface User {
  id: number;
  username: string;
  first_name: string;
  last_name: string;
  role: string;
  regdno?: string;
}
