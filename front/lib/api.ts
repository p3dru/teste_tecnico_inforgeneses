/**
 * API Client for Wildfire Detection Backend
 */

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export interface LoginRequest {
    username: string;
    password: string;
}

export interface TokenResponse {
    access_token: string;
    token_type: string;
}

export interface Report {
    id: string;
    user_id: number;
    file_path: string;
    status: 'PROCESSING' | 'DONE' | 'ERROR';
    created_at: string;
    latitude?: number;
    longitude?: number;
}

export interface BoundingBox {
    x1: number;
    y1: number;
    x2: number;
    y2: number;
    confidence: number;
    class_name: string;
}

export interface ReportDetail extends Report {
    detections: BoundingBox[];
    model_version?: string;
    processing_time_ms?: number;
}

class ApiClient {
    private baseUrl: string;
    private token: string | null = null;

    constructor(baseUrl: string) {
        this.baseUrl = baseUrl;

        // Load token from localStorage if available
        if (typeof window !== 'undefined') {
            this.token = localStorage.getItem('access_token');
        }
    }

    private async request<T>(
        endpoint: string,
        options: RequestInit = {}
    ): Promise<T> {
        const headers: Record<string, string> = {
            'Content-Type': 'application/json',
            ...(options.headers as Record<string, string>),
        };

        if (this.token) {
            headers['Authorization'] = `Bearer ${this.token}`;
        }

        const response = await fetch(`${this.baseUrl}${endpoint}`, {
            ...options,
            headers,
        });

        if (!response.ok) {
            const error = await response.json().catch(() => ({ detail: 'Unknown error' }));
            throw new Error(error.detail || `HTTP ${response.status}`);
        }

        return response.json();
    }

    // Authentication
    async login(username: string, password: string): Promise<TokenResponse> {
        const formData = new URLSearchParams();
        formData.append('username', username);
        formData.append('password', password);

        const response = await fetch(`${this.baseUrl}/auth/token`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: formData,
        });

        if (!response.ok) {
            throw new Error('Invalid credentials');
        }

        const data: TokenResponse = await response.json();
        this.token = data.access_token;

        if (typeof window !== 'undefined') {
            localStorage.setItem('access_token', data.access_token);
        }

        return data;
    }

    async signup(username: string, password: string): Promise<void> {
        await this.request('/auth/users', {
            method: 'POST',
            body: JSON.stringify({ username, password }),
        });
    }

    logout(): void {
        this.token = null;
        if (typeof window !== 'undefined') {
            localStorage.removeItem('access_token');
        }
    }

    // File Upload
    async uploadImage(
        file: File,
        latitude?: number,
        longitude?: number
    ): Promise<Report> {
        const formData = new FormData();
        formData.append('file', file);
        if (latitude !== undefined) formData.append('latitude', latitude.toString());
        if (longitude !== undefined) formData.append('longitude', longitude.toString());

        const headers: HeadersInit = {};
        if (this.token) {
            headers['Authorization'] = `Bearer ${this.token}`;
        }

        const response = await fetch(`${this.baseUrl}/files/upload`, {
            method: 'POST',
            headers,
            body: formData,
        });

        if (!response.ok) {
            throw new Error('Upload failed');
        }

        return response.json();
    }

    // Reports
    async getReports(skip = 0, limit = 10): Promise<Report[]> {
        return this.request(`/reports?skip=${skip}&limit=${limit}`);
    }

    async getReport(id: string): Promise<ReportDetail> {
        return this.request(`/reports/${id}`);
    }

    // Health Check
    async healthCheck(): Promise<{ status: string; service: string }> {
        const response = await fetch(`${this.baseUrl}/`);
        return response.json();
    }

    isAuthenticated(): boolean {
        return this.token !== null;
    }
}

export const apiClient = new ApiClient(API_URL);
