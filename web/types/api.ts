export interface ApiResponse<T> {
  status: number;
  error: {
    code: number;
    message: string;
    field?: any;
  } | null;
  data: T;
}

export interface NewsItem {
  news_id: number;
  title: string;
  url: string;
  source: string;
  image_url?: string;
  content?: string;
  category: string;
  created_at: number;
}

export interface NewsPage {
  content: NewsItem[];
  pageNumber: number;
  pageSize: number;
  totalElements: number;
  totalPages: number;
  last: boolean;
}

export interface MemeResponse {
  meme_url: string;
  top_text: string;
  bottom_text: string;
}

export interface ChatRequest {
  model: string;
  system_prompt: string;
  input: string;
}

export interface ChatResponse {
  model: string;
  response: string;
}
